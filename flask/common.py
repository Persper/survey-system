import re

sha1_pattern = re.compile(r'[0-9a-f]{40}')


def check_sha1(digest):
    return not re.match(sha1_pattern, digest) is None


reason_pattern = re.compile(r'\[(.*)\] is more valuable than \[(.*)\]')


def check_reason(text):
    return not re.match(reason_pattern, text) is None


def parse_descriptions(reason):
    m = re.match(reason_pattern, reason)
    if m is None:
        return None, None
    return m.group(1), m.group(2)


github_project_git_pattern = re.compile(r'git@github.com:(.+)/(.+).git')
github_project_https_pattern = re.compile(
    r'http[s]?://github.com/(.+)/([^.]+)(?:\.git)?')


def github_commit_url(project_url, commit_id, short=False):
    match = re.match(github_project_git_pattern, project_url)
    if match is None:
        match = re.match(github_project_https_pattern, project_url)
    if match is None:
        raise ValueError('Repository URL not recognized')
    if short:
        commit_id = commit_id[:12]
    return 'https://github.com/%s/%s/commit/%s' % (
        match.group(1), match.group(2), commit_id)
