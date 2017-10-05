#!/usr/bin/env python3

import argparse
from pprint import pprint
import requests


def test_next_question(address):
    url = address + '/v1/projects/6f2295863057c2e7059b74a01c79ab707f8789c3/questions/next'
    print('Next question: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
    else:
        print(r.text)


def test_submit_answer(address):
    url = address + '/v1/projects/6f2295863057c2e7059b74a01c79ab707f8789c3/questions/' \
                    'a248f3aaf9c99bed17ef9ca24d131cebeaa1906f'
    print('Submit answer: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
    payload = {'selected': '915330ffc269eed821d652292993ff75b717a66b'}
    r = requests.post(url, headers=headers, json=payload)
    if r.ok:
        pprint(r.json())
    else:
        print(r.text)


def test_next_review(address):
    url = address + '/v1/projects/6f2295863057c2e7059b74a01c79ab707f8789c3/reviews/next'
    print('Next review: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
    else:
        print(r.text)


def test_submit_review(address):
    url = address + '/v1/projects/6f2295863057c2e7059b74a01c79ab707f8789c3/reviews/' \
                    'a248f3aaf9c99bed17ef9ca24d131cebeaa1906f'
    print('Submit review: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
    payload = {'reason': 'Who knows.',
               'commitLabels': [
                   {'commitID': 'b35414f93aa5caaff115791d4040271047df25b3',
                    'labelID': '506f25f62a7e5acfb4b5f866a570e78e4efd638a'}
               ]}
    r = requests.post(url, headers=headers, json=payload)
    if r.ok:
        pprint(r.json())
    else:
        print(r.text)


def test_new_label(address):
    url = address + '/v1/projects/6f2295863057c2e7059b74a01c79ab707f8789c3/labels/new'
    print('New label: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
    payload = {'labelTitle': 'tiny'}
    r = requests.post(url, headers=headers, json=payload)
    if r.ok:
        pprint(r.json())
    else:
        print(r.text)


def test_get_labels(address):
    url = address + '/v1/projects/6f2295863057c2e7059b74a01c79ab707f8789c3/labels'
    print('Get labels: ' + url)
    headers = {'X-USR-TOKEN': 'tqxe2wmETskTsWq6t_MZwaUdzm8HY3Cqvahg-R-oR38'}
    r = requests.get(url, headers=headers)
    if r.ok:
        pprint(r.json())
    else:
        print(r.text)


def main():
    parser = argparse.ArgumentParser(description='test app server')
    parser.add_argument('-a', '--address', default='http://127.0.0.1:5000',
                        help='RESTful web service address')
    args = parser.parse_args()

    test_next_question(args.address)
    test_submit_answer(args.address)
    test_next_review(args.address)
    test_submit_review(args.address)
    test_new_label(args.address)
    test_get_labels(args.address)


if __name__ == '__main__':
    main()