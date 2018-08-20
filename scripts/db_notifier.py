#!/usr/bin/env python3.6

import argparse
import os
import re

import requests
import sendgrid
from sendgrid.helpers.mail import *

import database


def parse_file(path):
    email2author = dict()
    with open(path) as f:
        lines = f.readlines()
    for l in lines:
        m = re.match(r"([\w.\-+]+@[\w.\-]+).+?'(.+?)'", l)
        if m:
            email2author[m.group(1).lower()] = m.group(2)
    return email2author


def main():
    parser = argparse.ArgumentParser(
        description='Email developers with their survey links')
    parser.add_argument('-f', '--file', required=True,
                        help='email author list file')
    parser.add_argument('-t', '--test', action='store_true',
                        help='preview emails and links')
    parser.add_argument('-s', '--send', action='store_true',
                        help='send out emails')
    args = parser.parse_args()
    if not (args.test or args.send):
        parser.error('No action specified: add --test or --send')

    email2author = parse_file(args.file)

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email('survey@persper.org', 'Persper')
    subject = 'Linux Developer Survey (with a Prize)'
    message = Content('text/html', '@ 2018 Persper Foundation')

    for r in database.list_email_project():
        link = 'http://survey.persper.org/#/entry/%s?projectId=%s' % (r['token'], r['project_id'])
        if r['email'] in email2author:
            name = email2author[r['email']]
        else:
            continue
        if args.test:
            print(r['email'], name, link, sep='\t')
        elif args.send:
            print('Sending to ' + r['email'])
            to_email = Email(r['email'])
            m = Mail(from_email, subject, to_email, message)
            m.template_id = 'b93aec41-e221-44dc-be8f-6b67a99f86c2'
            m.personalizations[0].add_substitution(Substitution('-name-', name))
            m.personalizations[0].add_substitution(Substitution('-link-', link))
            try:
                response = sg.client.mail.send.post(request_body=m.get())
                if response.status_code != requests.codes.accepted:
                    print(response.body)
                    print(response.headers)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
