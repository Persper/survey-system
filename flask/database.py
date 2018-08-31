import configparser
from hashlib import sha1
import logging
import secrets

from neo4j.v1 import basic_auth
from neo4j.v1 import GraphDatabase

import query


_driver = None


def compose_comparison_id(commit1: str, commit2: str):
    return commit1 + commit2 if commit1 < commit2 else commit2 + commit1


def parse_comparison_id(comp_id: str):
    n = len(comp_id)
    assert n % 2 == 0
    half = int(n / 2)
    return comp_id[:half], comp_id[half:]


def neo4j_credential():
    config = configparser.ConfigParser()
    config.read('survey.ini')
    section = config['neo4j']
    return section['bolt'], section['user'], section['password']


def init_driver():
    global _driver
    bolt, usr, pwd = neo4j_credential()
    _driver = GraphDatabase.driver(bolt, auth=basic_auth(usr, pwd))
    logging.info('The Neo4j driver is initialized.')


def add_project(name, github_url):
    if not _driver:
        init_driver()
    pid = sha1(name.encode('utf-8')).hexdigest()
    # noinspection PyBroadException
    try:
        project = _driver.session().write_transaction(query.create_project_node,
                                                      pid, name, github_url)
        if project is None:
            return None
        assert project['id'] == pid
        if project['github_url'] != github_url:
            logging.warning('Existing project %s with a different URL: %s => %s' %
                            (name, project['github_url'], github_url))
            return None
        return pid
    except Exception:
        logging.exception("Failed to create project: " + name)
        return None


def get_project(project_id):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        return _driver.session().read_transaction(query.get_project_node,
                                                  project_id)
    except Exception:
        logging.exception("Failed to retrieve info for project ID: " + project_id)
        return None


def add_developer(name, email):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        token = secrets.token_urlsafe()
        _driver.session().write_transaction(query.create_developer_email,
                                            name, email, token)
        return token
    except Exception:
        logging.exception("Failed to create developer: %s <%s>" % (name, email))
        return None


def get_developer_token(email):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        return _driver.session().read_transaction(query.get_developer_token,
                                                  email)
    except Exception:
        logging.exception("Failed to get developer token: " + email)
        return None


def add_reviewer(email):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        token = secrets.token_urlsafe()
        _driver.session().write_transaction(query.create_reviewer_node,
                                            email, token)
        return token
    except Exception:
        logging.exception("Failed to create reviewer: " + email)
        return None


def add_commit(*, sha1_hex, title, email, project_id):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        tx = _driver.session().begin_transaction()
        query.create_commit_node(tx, sha1_hex, title)
        query.link_commit_author(tx, sha1_hex, email)
        query.link_project_commit(tx, sha1_hex, project_id)
        tx.commit()
    except Exception:
        logging.exception("Failed to add commit: " + sha1_hex)


def add_comparison(commit1, commit2, email):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        cid = compose_comparison_id(commit1, commit2)
        _driver.session().write_transaction(query.create_comparison_node,
                                            cid, commit1, commit2, email)
        return cid
    except Exception:
        logging.exception("Failed to add comparison: %s vs. %s for %s" % (commit1, commit2, email))
        return None


def count_compared(project_id, token):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        return _driver.session().read_transaction(query.count_compared_relationships,
                                                  project_id, token)
    except Exception:
        logging.exception("Failed to count compared relationships for token: " + token)
        return -1


def next_comparison(project_id, token):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        comparison, commit1, commit2 = _driver.session().read_transaction(query.next_comparison_node,
                                                                          project_id, token)
        if comparison is None:
            return None, commit1, commit2
        return comparison['id'], commit1, commit2
    except Exception:
        logging.exception("Failed to get next comparison for token: " + token)
        return None, None, None


def next_other_comparison(project_id, token):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        commit1, commit2 = _driver.session().read_transaction(query.next_other_comparison_node,
                                                              project_id, token)
        if commit1 is None or commit2 is None:
            return None, commit1, commit2
        return '-' + compose_comparison_id(commit1['id'], commit2['id']), commit1, commit2
    except Exception:
        logging.exception("Failed to get next other comparison for token: " + token)
        return None, None, None


def next_other_compared(project_id, token, threshold):
    """
    Select the next pair of commits that is not authored by the caller but has been compared by others.
    :param project_id: the project to select commits from
    :param token: the credential of the caller
    :param threshold: the max number of other developers that have compared the pair
    :return: comparison ID, first commit object, and second commit object
    """
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        commit1, commit2 = _driver.session().read_transaction(query.next_other_compared_relationship,
                                                              project_id, token, threshold)
        if commit1 is None or commit2 is None:
            return None, commit1, commit2
        comparison_id = compose_comparison_id(commit1['id'], commit2['id'])
        return '-' + comparison_id, commit1, commit2
    except Exception:
        logging.exception("Failed to get next comparison authored by others for token: " + token)
        return None, None, None


def add_answer(*, comparison_id, valuable_commit, reason, token):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        tx = _driver.session().begin_transaction()
        if comparison_id.startswith('-'):
            comparison_id = comparison_id[1:]
            c1, c2 = parse_comparison_id(comparison_id)
        else:
            c1, c2 = query.delete_comparison_node(tx, comparison_id, token)
        if valuable_commit is None:
            tx.commit()
            return
        if c2 == valuable_commit:
            c1, c2 = c2, c1
        assert c1 == valuable_commit
        query.create_compared_relationship(tx, comparison_id, c1, c2, reason, token)
        tx.commit()
    except Exception:
        logging.exception("Failed to add answer for comparison ID: %s (token = %s)" % (comparison_id, token))


def get_related_answers(commit, token):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        answers = _driver.session().read_transaction(query.get_compared_relationships,
                                                     commit, token)
        if answers is None:
            return []
        return [{'commit1': a['commit1']['id'],
                 'reason': a['outvalues']['reason'],
                 'commit2': a['commit2']['id']}
                for a in answers]
    except Exception:
        logging.exception("Failed to retrieve related answers for commit: %s (token = %s)" % (commit, token))
        return None


def get_related_answers_unsafe(commit):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        answers = _driver.session().read_transaction(query.get_compared_relationships,
                                                     commit)
        if answers is None:
            return []
        return [{'commit1': a['commit1']['id'],
                 'title1': a['commit1']['title'],
                 'reason': a['outvalues']['reason'],
                 'commit2': a['commit2']['id'],
                 'title2': a['commit2']['title']}
                for a in answers]
    except Exception:
        logging.exception("Failed to retrieve answers for commit: " + commit)
        return None


def next_review(project_id, token):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        n = _driver.session().read_transaction(query.count_reviewed_relationships,
                                               token)
        compared, commit1, commit2 = _driver.session().read_transaction(query.next_compared_relationship,
                                                                        project_id, token)
        return compared, commit1, commit2, n
    except Exception:
        logging.exception("Failed to fetch next review for project ID: %s (token = %s)" % (project_id, token))
        return None, None, None, -1


def add_label(name, genre, token):
    if not _driver:
        init_driver()
    lid = sha1(name.encode('utf-8')).hexdigest()
    # noinspection PyBroadException
    try:
        res_lid = _driver.session().write_transaction(query.create_label_node,
                                                      lid, name, genre, token)
        assert res_lid == lid
        return lid
    except Exception:
        logging.exception("Failed to add label: " + name)
        return None


def list_labels(token):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        rec_builtin, rec_custom = _driver.session().read_transaction(query.list_label_nodes,
                                                                     token)
        builtin = [{'id': r['label']['id'], 'name': r['label']['name']}
                   for r in rec_builtin] if rec_builtin is not None else []
        custom = [{'id': r['label']['id'], 'name': r['label']['name']}
                  for r in rec_custom] if rec_custom is not None else []
        return builtin, custom
    except Exception:
        logging.exception("Failed to list labels for token: " + token)
        return None, None


def add_review(*, comparison_id, commit_id, label_ids, token):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        _driver.session().write_transaction(query.create_label_relationship,
                                            comparison_id, commit_id, label_ids, token)
    except Exception:
        logging.exception("Failed to add review for comparison ID: %s (token = %s)" % (comparison_id, token))


def add_comment(comparison_id, comment, token):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        _driver.session().write_transaction(query.create_comment_property,
                                            comparison_id, comment, token)
    except Exception:
        logging.exception("Failed to add comment for comparison ID: %s (token = %s)" % (comparison_id, token))


def developer_stats(project_id, token):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        # unanswered = _driver.session().read_transaction(query.count_comparison_nodes,
        #                                                token)
        answered = _driver.session().read_transaction(query.count_compared_relationships,
                                                      project_id, token)
        return 25, answered
    except Exception:
        logging.exception("Failed to retrieve stats for token: " + token)
        return None, None


def list_email_project():
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        return _driver.session().read_transaction(query.list_email_project)
    except Exception:
        logging.exception("Failed to list emails of all projects")
        return None


def stats_compared(project_name):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        counts = _driver.session().read_transaction(query.count_project_compared_relationships,
                                                    project_name)
        return [(c['email'], c['count']) for c in counts]
    except Exception:
        logging.exception("Failed to count compared commit pairs by email for project: " + project_name)
        return None


def count_compared_by_email():
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        counts = _driver.session().read_transaction(query.count_compared_relationships_by_email)
        return [(c['email'], c['count']) for c in counts]
    except Exception:
        logging.exception("Failed to count compared commit pairs by email!")
        return None


def list_project_compared(project_name):
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        counts = _driver.session().read_transaction(query.list_project_compared_relationships,
                                                    project_name)
        if counts is None:
            return []
        return [{'commit1': c['commit1']['id'],
                 'title1': c['commit1']['title'],
                 'commit2': c['commit2']['id'],
                 'title2': c['commit2']['title'],
                 'reason': c['outvalues']['reason']} for c in counts]
    except Exception:
        logging.exception("Failed to list compared commits of project: " + project_name)
        return None


def list_compared():
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        counts = _driver.session().read_transaction(query.list_compared_relationships)
        if counts is None:
            return []
        return [{'project': c['project']['url'],
                 'author': c['author']['email'],
                 'commit1': c['commit1']['id'],
                 'title1': c['commit1']['title'],
                 'email': c['relation']['email'],
                 'commit2': c['commit2']['id'],
                 'title2': c['commit2']['title'],
                 'reason': c['relation']['reason']} for c in counts]
    except Exception:
        logging.exception("Failed to list all compared commits!")
        return None


def create_indexes():
    if not _driver:
        init_driver()
    # noinspection PyBroadException
    try:
        _driver.session().run("CREATE INDEX ON :Email(token)")
        _driver.session().run("CREATE INDEX ON :Commit(id)")
        _driver.session().run("CREATE INDEX ON :Project(id)")
        _driver.session().run("CREATE INDEX ON :Comparison(commit1, commit2)")
    except Exception:
        logging.exception("Failed to create indexes!")
