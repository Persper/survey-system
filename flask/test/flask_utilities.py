from pprint import pprint
import requests


def test_next_question(address, token, project_id):
    url = '%s/survey/v1/projects/%s/questions/next' % (address, project_id)
    print('[ NEXT QUESTION ] ' + url)
    headers = {'X-USR-TOKEN': token}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
        if r.json()['status'] == 0:
            return r.json()['data']
        else:
            return None
    else:
        print(r.text)


def test_submit_answer(address, token, project_id, question_id, selected, reason):
    url = '%s/survey/v1/projects/%s/questions/%s' % (
        address, project_id, question_id)
    print('[ SUBMIT ANSWER ] ' + url)
    headers = {'X-USR-TOKEN': token}
    payload = {'selected': selected, 'reason': reason}
    r = requests.post(url, headers=headers, json=payload)
    if r.ok:
        pprint(r.json())
    else:
        print(r.text)


def test_next_review(address, token, project_id):
    url = '%s/survey/v1/projects/%s/reviews/next' % (address, project_id)
    print('[ NEXT REVIEW ] ' + url)
    headers = {'X-USR-TOKEN': token}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
        if r.json()['status'] == 0:
            return r.json()['data']
        else:
            return None
    else:
        print(r.text)


def test_submit_review(address, token, project_id, review_id, **kwargs):
    url = '%s/survey/v1/projects/%s/reviews/%s' % (
        address, project_id, review_id)
    print('[ SUBMIT REVIEW ] ' + url)
    headers = {'X-USR-TOKEN': token}
    payload = {}
    commit_labels = kwargs.get('commit_labels')
    if commit_labels is not None:
        payload['commitLabels'] = commit_labels
    comment = kwargs.get('comment')
    if comment is not None:
        payload['comment'] = comment
    r = requests.post(url, headers=headers, json=payload)
    if r.ok:
        pprint(r.json())
        if r.json()['status'] == 0:
            return r.json()['data']
    else:
        print(r.text)


def test_get_labels(address, token, project_id):
    url = '%s/survey/v1/projects/%s/labels' % (address, project_id)
    print('[ GET LABELS ] ' + url)
    headers = {'X-USR-TOKEN': token}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
        return r.json()['data']
    else:
        print(r.text)


def test_project_info(address, token, project_id):
    url = '%s/survey/v1/projects/%s/project-info' % (address, project_id)
    print('[ GET PROJECT INFO ] ' + url)
    headers = {'X-USR-TOKEN': token}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
    else:
        print(r.text)


def test_developer_stats(address, token, project_id):
    url = '%s/survey/v1/projects/%s/developer-stats' % (address, project_id)
    print('[ GET DEVELOPER STATS ] ' + url)
    headers = {'X-USR-TOKEN': token}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
        return r.json()['data']
    else:
        print(r.text)
