#!/usr/bin/env python3.6

import argparse
import git
import json
import os.path
import re

import database

max_ratio = 20
ratio_buckets = [0] * max_ratio


def record_ratio(a, b):
    r = int(max(a / b, b / a))
    if r > max_ratio:
        r = max_ratio
    ratio_buckets[r-1] += 1


def sum_percents():
    s = sum(ratio_buckets)
    return s, [n / s for n in ratio_buckets]


def compose_url(token, project_id):
    return 'https://survey.persper.org/#/entry/%s?projectId=%s' % (
        token, project_id)


def parse_repo_url(remote_url):
    match = re.match(r'git@github.com:(.+)/(.+).git', remote_url)
    if match is None:
        match = re.match(r'http[s]?://github.com/(.+)/([^.]+)(?:\.git)?',
                         remote_url)
    if match is None:
        raise ValueError('Repository URL not recognized')
    return match.group(1), match.group(2)


def main():
    parser = argparse.ArgumentParser(
        description='Input selected commit pairs to a database')
    parser.add_argument('-d', '--parent-dir', required=True,
                        help='parent dir of all involved repos')
    parser.add_argument('-f', '--file', required=True, help='project-email-pairs JSON file')
    parser.add_argument('-c', '--check', action='store_true',
                        help='check stats of chosen commits, without populating the database')
    args = parser.parse_args()

    with open(args.file) as f:
        selected = json.load(f)
        for project, dev in selected.items():
            repo = git.Repo(os.path.join(args.parent_dir, project))
            github_url = repo.remotes.origin.url
            user_name, repo_name = parse_repo_url(github_url)
            project_name = '%s-%s' % (user_name, repo_name)
            project_id = database.add_project(project_name, github_url) if not args.check else None

            for email, pairs in dev.items():
                if not args.check:
                    token = database.get_developer_token(email)
                    if token is None:
                        token = database.add_developer(email.split('@')[0], email)
                    print(project, email, compose_url(token, project_id))
                for pair in pairs:
                    try:
                        c1 = repo.commit(pair[0])
                        c2 = repo.commit(pair[1])
                    except Exception as e:
                        print(e)
                        print("Project: " + project)
                        continue

                    c1_email = c1.author.email.lower()
                    c2_email = c2.author.email.lower()
                    assert c1_email == c2_email

                    n1 = c1.stats.total['lines']
                    n2 = c2.stats.total['lines']
                    record_ratio(n1, n2)

                    if not args.check:
                        database.add_commit(sha1_hex=c1.hexsha, title=c1.summary,
                                            email=c1_email, project_id=project_id)
                        database.add_commit(sha1_hex=c2.hexsha, title=c2.summary,
                                            email=c2_email, project_id=project_id)
                        database.add_comparison(c1.hexsha, c2.hexsha, email)

    if args.check:
        s, d = sum_percents()
        print('Total number of commits:', s)
        for i, p in enumerate(d):
            print('%dx=%.1f%%' % (i + 1, p * 100), end=', ')
        print()


if __name__ == '__main__':
    main()
