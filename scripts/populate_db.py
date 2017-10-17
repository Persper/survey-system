#!/usr/bin/env python3

import argparse
import git
import random
import re
import sys

import database


check_commit_pool = set()
check_email2comparisons = dict()


def check_comparison_id(commit1, commit2):
    assert commit1 != commit2
    return commit1 + commit2 if commit1 < commit2 else commit2 + commit1


# A comparison structure is a list that consists of the author email,
# the first commit hash, and the second commit hash.
def check_one_author(email, comparisons, n, m):
    check_n = set()
    check_m = set()
    for comparison in comparisons:
        c1 = comparison[1]
        c2 = comparison[2]
        assert c1 in check_commit_pool and c2 in check_commit_pool
        if comparison[0] == email:
            check_n.add(check_comparison_id(c1, c2))
        else:
            check_m.add(check_comparison_id(c1, c2))
    assert len(check_n) == n and len(check_m) == m


def check(n, m):
    for email, comparisons in check_email2comparisons.items():
        check_one_author(email, comparisons, n, m)


def main():
    parser = argparse.ArgumentParser(
        description='Populate database with commits')
    parser.add_argument('-d', '--repo-dir', required=True,
                        help='dir of the repo to select commits')
    parser.add_argument('-b', '--branch', default='master',
                        help='branch of the repo to analyze')
    parser.add_argument('-e', '--emails', nargs='+', required=True,
                        help='emails of repo developers in the survey')
    parser.add_argument('-n', type=int, required=True,
                        help='number of self comparisons')
    parser.add_argument('-m', type=int, default=0,
                        help="number of comparisons of others' commits")
    args = parser.parse_args()

    if args.m > 0 and len(args.emails) < 1 or args.n < 2:
        sys.exit('ERR: Cannot meet the requirement of m.')
    if args.m > args.n and args.n % (len(args.emails) - 1) == 0:
        sys.exit('ERR: The current algorithm does not support such n and m. '
                 'Increase/decrease n by 1 or increase the number of emails.')
    if args.m > args.n * (len(args.emails) - 1):
        sys.exit('ERR: Cannot meet the requirement of m. Increase n.')

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

    for e, author in enumerate(args.emails):
        print('Populating selected commits by ' + author)
        selected = random.sample(email2commits[author], args.n)
        for i in range(-1, args.n - 1):
            c1 = selected[i]
            c2 = selected[i + 1]
            assert c1.author.email == c2.author.email

            database.add_commit(sha1_hex=c1.hexsha, title=c1.summary,
                                author=c1.author.name, email=c1.author.email,
                                project_id=project_id)
            database.add_commit(sha1_hex=c2.hexsha, title=c2.summary,
                                author=c2.author.name, email=c2.author.email,
                                project_id=project_id)
            database.add_comparison(c1.hexsha, c2.hexsha, author)

            # Below is for the check purpose.
            check_commit_pool.add(c1.hexsha)
            check_commit_pool.add(c2.hexsha)
            if author not in check_email2comparisons:
                check_email2comparisons[author] = []
            check_email2comparisons[author].append(
                [c1.author.email, c1.hexsha, c2.hexsha])
        base = e
        for i in range(-1, args.m - 1):
            if args.emails[(base + i + 2) % len(args.emails)] == author:
                base = base + 1
            email = args.emails[(base + i + 2) % len(args.emails)]
            assert email != author or len(args.emails) == 1
            c1 = selected[i % args.n]
            c2 = selected[(i + 1) % args.n]
            assert c1.author.email == c2.author.email

            database.add_comparison(c1.hexsha, c2.hexsha, email)
            # Below is for the check purpose.
            if email not in check_email2comparisons:
                check_email2comparisons[email] = []
            check_email2comparisons[email].append(
                [c1.author.email, c1.hexsha, c2.hexsha])

    check(args.n, args.m)
    url_header = 'http://survey.persper.org/berkeley-cs169/index.html?id='
    print('Survey URL: ' + url_header + project_id)


if __name__ == '__main__':
    main()
