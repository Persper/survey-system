from flask import abort
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

import common
import database

app = Flask(__name__)
CORS(app)

STATUS_REQ_JSON = {'status': 1, 'message': 'A JSON request is required!'}
STATUS_BAD_REQUEST = {'status': 2, 'message': 'Bad request format!'}
STATUS_END = {'status': 100, 'message': 'Mission accomplished! Thank you!'}


@app.route('/survey/v1', methods=['GET'])
def version():
    return 'The Persper Survey System API v1'


def assemble_descriptions(commit, answers):
    final_description = None
    for a in answers:
        d1, d2 = common.parse_descriptions(a['reason'])
        assert a['commit1'] == commit or a['commit2'] == commit
        d = d1 if a['commit1'] == commit else d2
        if d is None:
            continue
        if final_description is None:
            final_description = d
        else:
            final_description += '/' + d
    return final_description


@app.route('/survey/v1/projects/<project_id>/questions/next', methods=['GET'])
def next_question(project_id):
    token = request.headers.get('X-USR-TOKEN')
    if token is None:
        abort(403)
    project = database.get_project(project_id)
    if project is None:
        return jsonify(STATUS_BAD_REQUEST)

    n = database.count_compared(project_id, token)
    if n >= 25:
        return jsonify(STATUS_END)
    if n % 2 == 0:
        comp_id, c1, c2 = database.next_comparison(project_id, token)
        if comp_id is None:
            comp_id, c1, c2 = database.next_other_compared(project_id, token, 0)
    else:
        comp_id, c1, c2 = database.next_other_compared(project_id, token, 0)
        if comp_id is None:
            comp_id, c1, c2 = database.next_comparison(project_id, token)
    if comp_id is None:
        comp_id, c1, c2 = database.next_other_compared(project_id, token, 1)
        if comp_id is None:
            comp_id, c1, c2 = database.next_other_comparison(project_id, token)
            if comp_id is None:
                return jsonify(STATUS_END)

    answers = database.get_related_answers(c1['id'], token)
    d1 = assemble_descriptions(c1['id'], answers)
    answers = database.get_related_answers(c2['id'], token)
    d2 = assemble_descriptions(c2['id'], answers)

    commit1 = {'id': c1['id'], 'title': c1['title'],
               'url': common.github_commit_url(project['url'], c1['id'], short=True),
               'description': d1}
    commit2 = {'id': c2['id'], 'title': c2['title'],
               'url': common.github_commit_url(project['url'], c2['id'], short=True),
               'description': d2}
    question = {'id': comp_id, 'type': 'single',
                'commits': [commit1, commit2], 'answered': n}

    return jsonify({'status': 0, 'data': {'question': question}})


@app.route('/survey/v1/projects/<project_id>/questions/<question_id>', methods=['POST'])
def submit_answer(project_id, question_id):
    token = request.headers.get('X-USR-TOKEN')
    if token is None:
        abort(403)
    if not request.json:
        return jsonify(STATUS_REQ_JSON)
    if not common.check_sha1(project_id):
        return jsonify(STATUS_BAD_REQUEST)

    selected = request.json.get('selected')
    reason = request.json.get('reason')

    # If no commit is selected, the reason must be specified by
    # either human input or the option title (e.g., 'not comparable').
    if selected is None or reason is None:
        return jsonify(STATUS_BAD_REQUEST)
    if not common.check_sha1(selected):
        selected = None
    elif not common.check_reason(reason):
        return jsonify(STATUS_BAD_REQUEST)
    database.add_answer(comparison_id=question_id, valuable_commit=selected,
                        reason=reason, token=token)
    return jsonify({'status': 0})


@app.route('/survey/v1/projects/<project_id>/reviews/next', methods=['GET'])
def next_review(project_id):
    token = request.headers.get('X-USR-TOKEN')
    if token is None:
        abort(403)
    project = database.get_project(project_id)
    if project is None:
        return jsonify(STATUS_BAD_REQUEST)

    comp, c1, c2, n = database.next_review(project_id, token)
    if comp is None:
        return jsonify(STATUS_END)
    review = {'id': comp['id'], 'reason': comp['reason'],
              'type': 'single', 'selected': c1['id'], 'reviewed': n}
    if c1['id'] > c2['id']:
        c1, c2 = c2, c1
    commit1 = {'id': c1['id'], 'title': c1['title'],
               'url': common.github_commit_url(project['url'], c1['id'])}
    commit2 = {'id': c2['id'], 'title': c2['title'],
               'url': common.github_commit_url(project['url'], c2['id'])}
    review['commits'] = [commit1, commit2]

    return jsonify({'status': 0, 'data': {'review': review}})


@app.route('/survey/v1/projects/<project_id>/reviews/<review_id>', methods=['POST'])
def submit_review(project_id, review_id):
    token = request.headers.get('X-USR-TOKEN')
    if token is None:
        abort(403)
    if not request.json:
        return jsonify(STATUS_REQ_JSON)
    if not common.check_sha1(project_id):
        return jsonify(STATUS_BAD_REQUEST)

    comment = request.json.get('comment')
    commit_labels = request.json.get('commitLabels')
    if not comment and not commit_labels:
        return jsonify(STATUS_BAD_REQUEST)
    if comment:
        database.add_comment(review_id, comment, token)
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
            label_id = database.add_label(label_name, 'Customized', token)
            new_labels.append({'label': {'id': label_id, 'name': label_name}})
            commit2labels[commit_id].append(label_id)
            continue
        return jsonify(STATUS_BAD_REQUEST)
    for commit_id, label_ids in commit2labels.items():
        database.add_review(comparison_id=review_id, commit_id=commit_id,
                            label_ids=label_ids, token=token)
    return jsonify({'status': 0, 'data': new_labels})


@app.route('/survey/v1/projects/<project_id>/labels', methods=['GET'])
def labels(project_id):
    token = request.headers.get('X-USR-TOKEN')
    if token is None:
        abort(403)
    if not common.check_sha1(project_id):
        return jsonify(STATUS_BAD_REQUEST)

    builtin, customized = database.list_labels(token)

    return jsonify({'status': 0,
                    'data': {'builtin': builtin, 'customized': customized}})


@app.route('/survey/v1/projects/<project_id>/project-info', methods=['GET'])
def project_info(project_id):
    token = request.headers.get('X-USR-TOKEN')
    if token is None:
        abort(403)

    node = database.get_project(project_id)
    if node is None:
        return jsonify(STATUS_BAD_REQUEST)

    project = {'id': node['id'], 'name': node['name'],
               'githubUrl': node['github_url']}
    return jsonify({'status': 0, 'data': {'project': project}})


@app.route('/survey/v1/projects/<project_id>/developer-stats', methods=['GET'])
def developer_stats(project_id):
    token = request.headers.get('X-USR-TOKEN')
    if token is None:
        abort(403)
    if not common.check_sha1(project_id):
        return jsonify(STATUS_BAD_REQUEST)

    total, answered = database.developer_stats(project_id, token)
    return jsonify({'status': 0,
                    'data': {'total': total, 'answered': answered}})


if __name__ == '__main__':
    app.run()
