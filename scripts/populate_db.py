#!/usr/bin/env python3

import argparse
import git
import random
import re

import database


def main():
    parser = argparse.ArgumentParser(
        description='Populate database with commits')
    parser.add_argument('-d', '--repo-dir', required=True,
                        help='dir of the repo to select commits')
    parser.add_argument('-b', '--branch', default='master',
                        help='branch of the repo to analyze')
    parser.add_argument('-e', '--emails', nargs='+', required=True,
                        help='emails of repo developers in the survey')
    parser.add_argument('-n', '--num-comparisons', type=int, required=True,
                        help='number of comparisons to make')
    args = parser.parse_args()

    repo = git.Repo(args.repo_dir)

    project_url = repo.remotes.origin.url
    user_name, repo_name = re.split('[/:.]', project_url)[-3:-1]
    project_name = '%s-%s' % (user_name, repo_name)
    project_id = database.add_project(project_name, project_url)

    email2commits = dict()
    for commit in repo.iter_commits(args.branch):
        email = commit.author.email
        if email not in email2commits:
            email2commits[email] = [commit]
        else:
            email2commits[email].append(commit)

    n = args.num_comparisons
    for author in args.emails:
        print('Populating selected commits by ' + author)
        selected = random.sample(email2commits[author], n)
        for i in range(-1, n - 1):
            c1 = selected[i]
            c2 = selected[i + 1]
            database.add_commit(sha1_hex=c1.hexsha, title=c1.summary,
                                author=c1.author.name, email=c1.author.email,
                                project_id=project_id)
            database.add_commit(sha1_hex=c2.hexsha, title=c2.summary,
                                author=c2.author.name, email=c2.author.email,
                                project_id=project_id)
            for email in args.emails:
                database.add_comparison(c1.hexsha, c2.hexsha, email)

    url_header = 'http://survey.persper.org/berkeley-cs169/index.html?id='
    print('Survey URL: ' + url_header + project_id)


if __name__ == '__main__':
    main()
