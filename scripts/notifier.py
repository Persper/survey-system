#!/usr/bin/env python3.6

import argparse
import json
import os
import requests

import sendgrid
from sendgrid.helpers.mail import *


def select_name(names, email_addr):
    if len(names) == 0:
        return email_addr.split('@')[0]
    for name in names:
        if ' ' in name or ',' in name or name[0].isupper():
            return name
    return names[0]


def main():
    parser = argparse.ArgumentParser(
        description='Email developers with their survey links')
    parser.add_argument('-i', '--input', required=True,
                        help='project-email-author-link file')
    parser.add_argument('-t', '--test', action='store_true',
                        help='preview emails and links')
    parser.add_argument('-s', '--send', action='store_true',
                        help='send out emails')
    args = parser.parse_args()
    if not (args.test or args.send):
        parser.error('No action specified: add --test or --send')

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email('survey@persper.org', 'Jinglei Ren')
    subject = 'Developer survey for better open source sustainability (with a prize!)'
    message = Content('text/html', '@ 2018 Persper Foundation')

    with open(args.input, 'r') as f:
        for line in f:
            project, receiver, names, link = line.split('\t')

            names = json.loads(names)
            name = select_name(names, receiver)

            if args.test:
                print(project, receiver, name, link, sep='\t')
            elif args.send:
                print('Sending to ' + receiver)
                to_email = Email(receiver)
                m = Mail(from_email, subject, to_email, message)
                m.template_id = '985509ac-501c-4edd-9748-b22c38726c65'
                m.personalizations[0].add_substitution(Substitution('-name-', name))
                m.personalizations[0].add_substitution(Substitution('-project-', project))
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
