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
        if r.json()['status'] == 0:
            return r.json()['data']['question']
    else:
        print(r.text)


def test_submit_answer(address, token, project_id, question_id, selected, reason):
    url = '%s/survey/v1/projects/%s/questions/%s' % (
        address, project_id, question_id)
    print('[ SUBMIT ANSWER ] ' + url)
    headers = {'X-USR-TOKEN': token}
    payload = {'selected': selected, 'reason': reason}
    r = requests.post(url, headers=headers, json=payload)
    assert r.ok and r.json()['status'] == 0


def test_developer_stats(address, token, project_id):
    url = '%s/survey/v1/projects/%s/developer-stats' % (address, project_id)
    print('[ GET DEVELOPER STATS ] ' + url)
    headers = {'X-USR-TOKEN': token}
    r = requests.get(url, headers=headers)
    assert r.ok and r.json()['status'] == 0
    return r.json()['data']


def main():
    # This test fetches and answers all questions.
    # It checks whether consecutive questions share an identical commit.
    parser = argparse.ArgumentParser(
        description='test app server (NOTE: run populate_db.py first)')
    parser.add_argument('-a', '--address', default='http://127.0.0.1:5000/',
                        help='RESTful web service address')
    parser.add_argument('-p', '--project-id', required=True,
                        help='project ID '
                             '(to be manually obtained from the database)')
    parser.add_argument('-t', '--token', required=True,
                        help='access token of one developer '
                             '(to be manually obtained from the database)')
    args = parser.parse_args()

    address = args.address.strip('/')

    stats = test_developer_stats(address, args.token, args.project_id)

    last_commit = None
    new_answers = 0
    while True:
        question = test_next_question(address, args.token, args.project_id)
        if question is None:
            break

        assert last_commit is None or last_commit == question['commits'][0]['id']
        last_commit = question['commits'][1]['id']

        test_submit_answer(address, args.token, args.project_id, question['id'],
                           question['commits'][0]['id'], 'Who knows')
        new_answers += 1

    assert stats['total'] - stats['answered'] == new_answers
    print('Checks %d questions and sees no problem!' % new_answers)


if __name__ == '__main__':
    main()
