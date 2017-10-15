import re
from urllib.parse import urljoin

from flask import abort
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

import database


app = Flask(__name__)
CORS(app)

STATUS_REQ_JSON = {'status': 1, 'message': 'A JSON request is required!'}
STATUS_BAD_REQUEST = {'status': 2, 'message': 'Bad request format!'}
STATUS_END = {'status': 100, 'message': 'Good job! Mission complete!'}

sha1_pattern = re.compile(r'[0-9a-f]{40}')


def check_sha1(digest):
    return not re.match(sha1_pattern, digest) is None


@app.route('/survey/v1', methods=['GET'])
def version():
    return 'The Persper Survey System API v1'


def commit_url(project_url, commit_id):
    if 'github' in project_url.lower():
        return urljoin(project_url, '/commit/') + commit_id


@app.route('/survey/v1/projects/<project_id>/questions/next', methods=['GET'])
def next_question(project_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    project = database.get_project(project_id)
    if project is None:
        return jsonify(STATUS_BAD_REQUEST)

    comp, c1, c2, n = database.next_comparison('w@persper.org')  # TODO
    if comp is None:
        return jsonify(STATUS_END)
    commit1 = {'id': c1['id'], 'title': c1['title'],
               'url': commit_url(project['url'], c1['id'])}
    commit2 = {'id': c2['id'], 'title': c2['title'],
               'url': commit_url(project['url'], c2['id'])}
    question = {'id': comp['id'], 'type': 'single',
                'commits': [commit1, commit2], 'answered': n}

    return jsonify({'status': 0, 'data': {'question': question}})


@app.route('/survey/v1/projects/<project_id>/questions/<question_id>', methods=['POST'])
def submit_answer(project_id, question_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    if not request.json:
        return jsonify(STATUS_REQ_JSON)
    if not check_sha1(project_id):
        return jsonify(STATUS_BAD_REQUEST)

    selected = request.json.get('selected')
    reason = request.json.get('reason')
    # If no commit is selected, the reason must be specified by
    # either human input or the option title (e.g., 'not comparable').
    if selected is None or reason is None:
        return jsonify(STATUS_BAD_REQUEST)
    if not check_sha1(selected):
        selected = None
        if not reason:
            return jsonify(STATUS_BAD_REQUEST)
    database.add_answer(comparison_id=question_id, valuable_commit=selected,
                        reason=reason, email='w@persper.org')   # TODO
    return jsonify({'status': 0})


@app.route('/survey/v1/projects/<project_id>/reviews/next', methods=['GET'])
def next_review(project_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    project = database.get_project(project_id)
    if project is None:
        return jsonify(STATUS_BAD_REQUEST)

    cid, c1, c2, n = database.next_review(project_id, 'jinglei@persper.org')  # TODO
    if cid is None:
        return jsonify(STATUS_END)
    review = {'id': cid, 'type': 'single', 'selected': c1['id'], 'reviewed': n}
    if c1['id'] > c2['id']:
        c1, c2 = c2, c1
    commit1 = {'id': c1['id'], 'title': c1['title'],
               'url': commit_url(project['url'], c1['id'])}
    commit2 = {'id': c2['id'], 'title': c2['title'],
               'url': commit_url(project['url'], c2['id'])}
    review['commits'] = [commit1, commit2]

    return jsonify({'status': 0, 'data': {'review': review}})


@app.route('/survey/v1/projects/<project_id>/reviews/<review_id>', methods=['POST'])
def submit_review(project_id, review_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    if not request.json:
        return jsonify(STATUS_REQ_JSON)
    if not check_sha1(project_id):
        return jsonify(STATUS_BAD_REQUEST)

    comment = request.json.get('comment')
    commit_labels = request.json.get('commitLabels')
    if not comment and not commit_labels:
        return jsonify(STATUS_BAD_REQUEST)
    if comment:
        database.add_comment(review_id, comment, 'jinglei@persper.org')  # TODO
        return jsonify({'status': 0})
    commit2labels = dict()
    new_labels = []
    for label in commit_labels:
        commit_id = label.get('commitId')
        if not commit_id:
            return jsonify(STATUS_BAD_REQUEST)
        if commit_id not in commit2labels:
            commit2labels[commit_id] = []
        label_id = label.get('labelId')
        if label_id:
            commit2labels[commit_id].append(label_id)
            continue
        label_name = label.get('labelName')
        if label_name:
            label_id = database.add_label(label_name)
            new_labels.append({'label': {'id': label_id, 'name': label_name}})
            commit2labels[commit_id].append(label_id)
            continue
        return jsonify(STATUS_BAD_REQUEST)
    for commit_id, label_ids in commit2labels.items():
        print(label_ids)
        database.add_review(comparison_id=review_id, commit_id=commit_id,
                            label_ids=label_ids,
                            email='jinglei@persper.org')  # TODO
    return jsonify({'status': 0, 'data': new_labels})


@app.route('/survey/v1/projects/<project_id>/labels', methods=['GET'])
def labels(project_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    if not check_sha1(project_id):
        return jsonify(STATUS_BAD_REQUEST)

    builtin, customized = database.list_labels()

    return jsonify({'status': 0,
                    'data': {'builtin': builtin, 'customized': customized}})


if __name__ == '__main__':
    app.run()
