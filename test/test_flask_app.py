#!/usr/bin/env python3

import argparse
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
            return r.json()['data']['question']
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
            return r.json()['data']['review']
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


def main():
    # The test of database fills the graph store with 6 pairs of commits.
    # Also, it has answered and reviewed 2 pairs.
    parser = argparse.ArgumentParser(
        description='test app server (NOTE: run test_database.py first)')
    parser.add_argument('-a', '--address', default='http://127.0.0.1:5000/',
                        help='RESTful web service address')
    parser.add_argument('-d', '--developer-token', required=True,
                        help='access token of one developer '
                             '(to be manually obtained from the database)')
    parser.add_argument('-r', '--reviewer-token', required=True,
                        help='access token of one reviewer '
                             '(to be manually obtained from the database)')
    args = parser.parse_args()

    address = args.address.strip('/')
    dt = args.developer_token
    rt = args.reviewer_token
    project_id = 'de65f79e6f3391866ab4d68cbebeee1bcdc859f0'

    test_project_info(address, None, project_id)
    test_project_info(address, dt, project_id)

    stats = test_developer_stats(address, dt, project_id)
    assert stats['total'] == 6 and stats['answered'] == 2

    labels = test_get_labels(address, rt, project_id)

    # Makes the the 3rd answer.
    question = test_next_question(address, dt, project_id)
    test_submit_answer(address, dt, project_id, question['id'],
                       question['commits'][0]['id'], 'Who knows')
    # Makes the 4th answer.
    question = test_next_question(address, dt, project_id)
    test_submit_answer(address, dt, project_id, question['id'],
                       question['commits'][1]['id'], 'Who knows')

    # Makes the 3rd review.
    review = test_next_review(address, rt, project_id)
    label1 = {'commitId': review['commits'][0]['id'],
              'labelId': labels['builtin'][0]['id']}
    label2 = {'commitId': review['commits'][1]['id'],
              'labelName': 'whatever'}
    label3 = {'commitId': review['commits'][1]['id'],
              'labelId': labels['builtin'][1]['id']}
    new_labels = test_submit_review(address, rt, project_id, review['id'],
                                    commit_labels=[label1, label2, label3],
                                    comment='As explained by labels')
    assert len(new_labels) == 1 and new_labels[0]['label']['name'] == 'whatever'

    # Makes the 5th and 6th answer.
    while True:
        question = test_next_question(address, dt, project_id)
        if question is None:
            break
        test_submit_answer(address, dt, project_id, question['id'],
                           question['commits'][0]['id'], 'Who knows')

    stats = test_developer_stats(address, dt, project_id)
    assert stats['total'] == 6 and stats['answered'] == 6

    # Makes the 4th - 6th reviews.
    while True:
        review = test_next_review(address, rt, project_id)
        if review is None:
            break
        label1 = {'commitId': review['commits'][0]['id'],
                  'labelId': labels['builtin'][2]['id']}
        label2 = {'commitId': review['commits'][1]['id'],
                  'labelId': labels['builtin'][3]['id']}
        label3 = {'commitId': review['commits'][0]['id'],
                  'labelId': new_labels[0]['label']['id']}
        test_submit_review(address, rt, project_id, review['id'],
                           commit_labels=[label1, label2, label3])


if __name__ == '__main__':
    main()
