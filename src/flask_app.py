from flask import abort
from flask_cors import CORS
from flask import Flask
from flask import jsonify
from flask import request
from hashlib import sha1

app = Flask(__name__)
CORS(app)

STATUS_REQ_JSON = {'status': 1, 'message': 'A JSON request is required!'}
STATUS_BAD_REQUEST = {'status': 2, 'message': 'Bad request parameters!'}

@app.route('/survey/v1', methods=['GET'])
def version():
    return 'The Persper Survey System API v1'


@app.route('/survey/v1/projects/<project_id>/questions/next', methods=['GET'])
def next_question(project_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    if project_id != '6f2295863057c2e7059b74a01c79ab707f8789c3':
        return jsonify(STATUS_BAD_REQUEST)

    commit1 = dict()
    commit1['id'] = '915330ffc269eed821d652292993ff75b717a66b'
    commit1['title'] = 'new image for tweets which are retweeted by user.'
    commit1['url'] = 'https://github.com/lyricat/Hotot/commit/915330ffc2'

    commit2 = dict()
    commit2['id'] = 'b35414f93aa5caaff115791d4040271047df25b3'
    commit2['title'] = 'disable the position saving'
    commit2['url'] = 'https://github.com/lyricat/Hotot/commit/b35414f93a'

    question = dict()
    question['id'] = 'a248f3aaf9c99bed17ef9ca24d131cebeaa1906f'
    question['type'] = 'single'
    question['commits'] = [commit1, commit2]

    return jsonify({'status': 0, 'data': question})


@app.route('/survey/v1/projects/<project_id>/questions/<question_id>', methods=['POST'])
def submit_answer(project_id, question_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    if not request.json:
        return jsonify(STATUS_REQ_JSON)
    if project_id != '6f2295863057c2e7059b74a01c79ab707f8789c3':
        return jsonify(STATUS_BAD_REQUEST)

    commit_id = request.json.get('selected')
    if not commit_id:
        return jsonify(STATUS_BAD_REQUEST)
    return jsonify({'status': 0})


@app.route('/survey/v1/projects/<project_id>/reviews/next', methods=['GET'])
def next_review(project_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    if project_id != '6f2295863057c2e7059b74a01c79ab707f8789c3':
        return jsonify(STATUS_BAD_REQUEST)

    commit1 = dict()
    commit1['id'] = '915330ffc269eed821d652292993ff75b717a66b'
    commit1['title'] = 'new image for tweets which are retweeted by user.'
    commit1['url'] = 'https://github.com/lyricat/Hotot/commit/915330ffc2'

    commit2 = dict()
    commit2['id'] = 'b35414f93aa5caaff115791d4040271047df25b3'
    commit2['title'] = 'disable the position saving'
    commit2['url'] = 'https://github.com/lyricat/Hotot/commit/b35414f93a'

    review = dict()
    review['id'] = 'a248f3aaf9c99bed17ef9ca24d131cebeaa1906f'
    review['type'] = 'single'
    review['selected'] = '915330ffc269eed821d652292993ff75b717a66b'
    review['commits'] = [commit1, commit2]

    return jsonify({'status': 0, 'data': review})


@app.route('/survey/v1/projects/<project_id>/reviews/<review_id>', methods=['POST'])
def submit_review(project_id, review_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    if not request.json:
        return jsonify(STATUS_REQ_JSON)
    if project_id != '6f2295863057c2e7059b74a01c79ab707f8789c3':
        return jsonify(STATUS_BAD_REQUEST)

    reason = request.json.get('reason')
    commit_labels = request.json.get('commitLabels')
    if not reason or not commit_labels:
        return jsonify(STATUS_BAD_REQUEST)
    for label in commit_labels:
        if not label.get('commitID') or not label.get('labelID'):
            return jsonify(STATUS_BAD_REQUEST)
    return jsonify({'status': 0})


@app.route('/survey/v1/projects/<project_id>/labels/new', methods=['POST'])
def new_label(project_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    if not request.json:
        return jsonify(STATUS_REQ_JSON)
    if project_id != '6f2295863057c2e7059b74a01c79ab707f8789c3':
        return jsonify(STATUS_BAD_REQUEST)

    title = request.json.get('labelTitle')
    if not title:
        return jsonify(STATUS_BAD_REQUEST)
    sha = sha1(title.encode('utf-8')).hexdigest()

    label = dict()
    label['id'] = sha
    label['title'] = title

    return jsonify({'status': 0, 'label': label})


@app.route('/survey/v1/projects/<project_id>/labels', methods=['GET'])
def labels(project_id):
    if request.headers.get('X-USR-TOKEN') != 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38':
        abort(403)
    if project_id != '6f2295863057c2e7059b74a01c79ab707f8789c3':
        return jsonify(STATUS_BAD_REQUEST)

    label = dict()
    label['id'] = sha1(b'tiny').hexdigest()
    label['title'] = 'tiny'

    builtins = [label, label]
    customised = [label]

    return jsonify({'status': 0,
                    'data': {'builtins': builtins, 'customized': customised}})


if __name__ == '__main__':
    app.run()
