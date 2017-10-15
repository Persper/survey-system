#!/usr/bin/env python3

import argparse
from pprint import pprint
import requests


def test_next_question(address, project_id):
    url = '%s/survey/v1/projects/%s/questions/next' % (address, project_id)
    print('Next question: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
        if r.json()['status'] == 0:
            return r.json()['data']['question']
        else:
            return None
    else:
        print(r.text)


def test_submit_answer(address, project_id, question_id, selected, reason):
    url = '%s/survey/v1/projects/%s/questions/%s' % (
        address, project_id, question_id)
    print('Submit answer: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
    payload = {'selected': selected, 'reason': reason}
    r = requests.post(url, headers=headers, json=payload)
    if r.ok:
        pprint(r.json())
    else:
        print(r.text)


def test_next_review(address, project_id):
    url = '%s/survey/v1/projects/%s/reviews/next' % (address, project_id)
    print('Next review: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
        if r.json()['status'] == 0:
            return r.json()['data']['review']
        else:
            return None
    else:
        print(r.text)


def test_submit_review(address, project_id, review_id, **kwargs):
    url = '%s/survey/v1/projects/%s/reviews/%s' % (
        address, project_id, review_id)
    print('Submit review: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
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
    else:
        print(r.text)


def test_get_labels(address, project_id):
    url = '%s/survey/v1/projects/%s/labels' % (address, project_id)
    print('Get labels: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
        return r.json()['data']
    else:
        print(r.text)


def main():
    # The test of database fills the graph store with 6 pairs of commits.
    # Also, it has answered and reviewed 2 pairs.
    parser = argparse.ArgumentParser(description='test app server')
    parser.add_argument('-a', '--address', default='http://api.persper.org',
                        help='RESTful web service address')
    args = parser.parse_args()

    address = args.address
    project_id = 'de65f79e6f3391866ab4d68cbebeee1bcdc859f0'

    labels = test_get_labels(address, project_id)

    # Makes the the 3rd answer.
    question = test_next_question(address, project_id)
    test_submit_answer(address, project_id, question['id'],
                       question['commits'][0]['id'], 'Who knows')
    # Makes the 4th answer.
    question = test_next_question(address, project_id)
    test_submit_answer(address, project_id, question['id'],
                       question['commits'][1]['id'], 'Who knows')

    # Makes the 3rd review.
    review = test_next_review(address, project_id)
    label1 = {'commitId': review['commits'][0]['id'],
              'labelId': labels['builtin'][0]['id']}
    label2 = {'commitId': review['commits'][1]['id'],
              'labelName': 'whatever'}
    test_submit_review(address, project_id, review['id'], comment='Not known.')

    # Makes the 5th and 6th answer.
    while True:
        question = test_next_question(address, project_id)
        if question is None:
            break
        test_submit_answer(address, project_id, question['id'],
                           question['commits'][0]['id'], 'Who knows')

    # Makes the 4th - 6th reviews.
    while True:
        review = test_next_review(address, project_id)
        if review is None:
            break
        label1 = {'commitId': review['commits'][0]['id'],
                  'labelId': labels['builtin'][0]['id']}
        label2 = {'commitId': review['commits'][1]['id'],
                  'labelName': 'whatever'}
        test_submit_review(address, project_id, review['id'],
                           commit_labels=[label1, label2])


if __name__ == '__main__':
    main()
