#!/usr/bin/env python3.6

import argparse
import os

import requests
import sendgrid
from sendgrid.helpers.mail import *

import database


def main():
    parser = argparse.ArgumentParser(
        description='Email developers with their survey links')
    parser.add_argument('-t', '--test', action='store_true',
                        help='preview emails and links')
    parser.add_argument('-s', '--send', action='store_true',
                        help='send out emails')
    args = parser.parse_args()
    if not (args.test or args.send):
        parser.error('No action specified: add --test or --send')

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email('survey@persper.org', 'Persper Survey')
    subject = 'Berkeley CS169 Survey Link'
    content = Content('text/html', 'CS169 Persper Team')

    for r in database.list_email_project():
        link = 'http://survey.persper.org/#/entry/%s?project=%s' % (
            r['token'], r['project'])
        if args.test:
            print(r['email'], link)
        elif args.send:
            print('Sending to ' + r['email'])
            to_email = Email(r['email'])
            m = Mail(from_email, subject, to_email, content)
            m.template_id = '22d50eb9-11fb-4ede-a266-5435207cbc92'
            m.personalizations[0].add_substitution(
                Substitution('-link-', link))
            try:
                response = sg.client.mail.send.post(request_body=m.get())
                if response.status_code != requests.codes.accepted:
                    print(response.body)
                    print(response.headers)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
