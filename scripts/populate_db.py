#!/usr/bin/env python3.6

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
    assert len(check_n) <= n and len(check_m) == m
    if len(check_n) < n:
        print('WARN: %s is assigned with less self-comparisons than n '
              '(Check if this developer makes less commits than n)' % email)


def check(n, m):
    for email, comparisons in check_email2comparisons.items():
        check_one_author(email, comparisons, n, m)


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
    return 'http://survey.persper.org/#/entry/%s?projectId=%s' % (
        token, project_id)


def parse_repo_url(remote_url):
    match = re.match(r'git@github.com:(.+)/(.+).git', remote_url)
    if match is None:
        match = re.match(r'http[s]?://github.com/(.+)/([^.]+)(?:\.git)?',
                         remote_url)
    if match is None:
        raise ValueError('Repository URL not recognized')
    return match.group(1), match.group(2)


def parse_emails(file_path):
    with open(file_path) as f:
        content = f.read()
    return [email.lower() for email in re.findall(r'[\w.-]+@[\w.-]+', content)]


def main():
    parser = argparse.ArgumentParser(
        description='Populate a database with commits')
    parser.add_argument('-d', '--repo-dir', required=True,
                        help='dir of the repo to select commits')
    parser.add_argument('-b', '--branch', default='master',
                        help='branch of the repo to select commits')
    parser.add_argument('-l', '--min-count', type=int, default=0,
                        help='min number of commit to begin with')
    parser.add_argument('-u', '--max-count', type=int, default=sys.maxsize,
                        help='max number of commit to end with')
    parser.add_argument('-e', '--emails', nargs='+',
                        help='emails of repo developers in the survey')
    parser.add_argument('-f', '--file', help='email author list file')
    parser.add_argument('-n', type=int, required=True,
                        help='number of self comparisons')
    parser.add_argument('-m', type=int, default=0,
                        help="number of comparisons of others' commits")
    parser.add_argument('-s', '--stats', action='store_true',
                        help='show stats of chosen commits, '
                             'without populating the database')
    parser.add_argument('-r', '--ratio', type=int, default=sys.maxsize,
                        help='max ratio of commit sizes in a comparision')
    args = parser.parse_args()

    emails = args.emails if args.emails else []
    emails += parse_emails(args.file) if args.file else []
    if len(emails) < 1:
        sys.exit('Please specify emails by -e or -f. See help info by -h.')

    if args.m > 0 and len(emails) < 1 or args.n < 2:
        sys.exit('ERR: Cannot meet the requirement of m.')
    if args.m > args.n and args.n % (len(emails) - 1) == 0:
        sys.exit('ERR: The current algorithm does not support such n and m. '
                 'Increase/decrease n by 1 or increase the number of emails.')
    if args.m > args.n * (len(emails) - 1):
        sys.exit('ERR: Cannot meet the requirement of m. Increase n.')

    repo = git.Repo(args.repo_dir)

    github_url = repo.remotes.origin.url
    user_name, repo_name = parse_repo_url(github_url)
    project_name = '%s-%s' % (user_name, repo_name)
    if not args.stats:
        project_id = database.add_project(project_name, github_url)

    email2commits = dict()
    for commit in repo.iter_commits(args.branch, max_count=args.max_count,
                                    skip=args.min_count):
        if len(commit.parents) > 1:
            continue
        email = commit.author.email.lower()
        if email not in email2commits:
            email2commits[email] = [commit]
        else:
            email2commits[email].append(commit)

    for e, author in enumerate(emails):
        if not args.stats:
            token = database.get_developer_token(author)
            if token is None:
                token = database.add_developer(author.split('@')[0], author)
            print(author, compose_url(token, project_id))
        selected = random.sample(email2commits[author],
                                 min(args.n * 4, len(email2commits[author])))
        selected = sorted(selected, key=lambda x: x.hexsha)
        n_added = 0
        for i in range(-1, len(selected) - 1):
            c1 = selected[i]
            c2 = selected[i + 1]
            c1_email = c1.author.email.lower()
            c2_email = c2.author.email.lower()
            assert c1_email == c2_email

            n1 = c1.stats.total['lines']
            n2 = c2.stats.total['lines']
            if not n1 or not n2:
                continue
            if args.stats:
                record_ratio(n1, n2)
            elif int(max(n1 / n2, n2 / n1)) > args.ratio:
                continue
            else:
                n_added += 1
                database.add_commit(sha1_hex=c1.hexsha, title=c1.summary,
                                    author=c1.author.name, email=c1_email,
                                    project_id=project_id)
                database.add_commit(sha1_hex=c2.hexsha, title=c2.summary,
                                    author=c2.author.name, email=c2_email,
                                    project_id=project_id)
                database.add_comparison(c1.hexsha, c2.hexsha, author)

                # Below is for the check purpose.
                check_commit_pool.add(c1.hexsha)
                check_commit_pool.add(c2.hexsha)
                if author not in check_email2comparisons:
                    check_email2comparisons[author] = []
                check_email2comparisons[author].append(
                    [c1_email, c1.hexsha, c2.hexsha])

                if n_added >= args.n:
                    break

        m_added = 0
        base = e
        for i in range(-1, args.m - 1):
            if emails[(base + i + 2) % len(emails)] == author:
                base = base + 1
            email = emails[(base + i + 2) % len(emails)]
            assert email != author or len(emails) == 1
            c1 = selected[i % len(selected)]
            c2 = selected[(i + 1) % len(selected)]
            assert c1.author.email.lower() == c2.author.email.lower()

            n1 = c1.stats.total['lines']
            n2 = c2.stats.total['lines']
            if not n1 or not n2:
                continue
            if args.stats:
                record_ratio(n1, n2)
            elif int(max(n1 / n2, n2 / n1)) > args.ratio:
                continue
            else:
                m_added += 1
                database.add_comparison(c1.hexsha, c2.hexsha, email)

                # Below is for the check purpose.
                if email not in check_email2comparisons:
                    check_email2comparisons[email] = []
                check_email2comparisons[email].append(
                    [c1.author.email.lower(), c1.hexsha, c2.hexsha])

                if m_added >= args.m:
                    break

    if args.stats:
        s, d = sum_percents()
        print('Total number of commits:', s)
        for i, p in enumerate(d):
            print('%dx=%.1f%%' % (i + 1, p * 100), end=', ')
        print()
    else:
        check(args.n, args.m)

        # Add builtin labels
        reviewer = database.add_reviewer('jinglei@persper.org')
        database.add_label('tiny', 'Builtin', reviewer)
        database.add_label('small', 'Builtin', reviewer)
        database.add_label('moderate', 'Builtin', reviewer)
        database.add_label('large', 'Builtin', reviewer)
        database.add_label('huge', 'Builtin', reviewer)


if __name__ == '__main__':
    main()
