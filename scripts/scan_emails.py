#!/usr/bin/env python3.6

import git
import argparse
import subprocess
import glob


def get_immediate_subdirectories(a_dir):
    return glob.glob(a_dir + '/*/')


def is_temp_email(email):
    return 'airbears' in email or email.endswith('local')


def is_github_private_email(email):
    return email.endswith('noreply.github.com')


def main():
    parser = argparse.ArgumentParser(
        description='Populate database in batch by invoking populate_db.py')
    parser.add_argument('-d', '--repo-dir', required=True)
    parser.add_argument('--batch-mode', dest='batch_mode', action='store_true')
    parser.set_defaults(batch_mode=False)
    parser.add_argument('-s', type=int, default=6,
                        help='number of most recent emails to scan')
    parser.add_argument('-n', type=int, default=5,
                        help='number of self comparisons')
    parser.add_argument('-m', type=int, default=5,
                        help="number of comparisons of others' commits")
    args = parser.parse_args()

    if args.batch_mode:
        repos_dir = get_immediate_subdirectories(args.repo_dir)
    else:
        repos_dir = [args.repo_dir]

    num_private_emails = 0

    for repo_dir in repos_dir:
        print('---- %s ----' % repo_dir)
        repo = git.Repo(repo_dir)
        emails = set()
        for commit in repo.iter_commits():
            e = commit.author.email.lower()
            if not is_temp_email(e):
                emails.add(e)
            if is_github_private_email(e):
                num_private_emails += 1
            if len(emails) == args.s:
                break

        emails_str = ' '.join(emails)
        print('# of selected emails: %d' % len(emails))
        print('Selected emails: %s' % emails_str)

        cmd = './populate_db.py -d %s -e %s -n %d -m %d' % \
            (repo_dir, emails_str, args.n, args.m)
        subprocess.call(cmd, shell=True)
        print('\n\n')

    print('\n\n------ Summary -------')
    print('Total # of private github emails: %d' % num_private_emails)


if __name__ == '__main__':
    main()
