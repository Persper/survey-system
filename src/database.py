from hashlib import sha1
from os import environ
from os.path import isfile
from os.path import join
from os import listdir
import random
import secrets

from neo4j.v1 import basic_auth
from neo4j.v1 import GraphDatabase

import query


_driver = None


def local_credential(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    usr = random.choice(files)
    with open(join(path, usr), 'r') as f:
        pwd = f.readline()
    return usr, pwd.strip()


def init_driver():
    global _driver
    bolt = environ.get('NEO4J_BOLT', None)
    usr = environ.get('NEO4J_USER', None)
    pwd = environ.get('NEO4J_PASSWORD', None)
    if bolt is None or usr is None or pwd is None:
        raise ValueError('No bolt/user/password environmental variables '
                         'are set!')
    _driver = GraphDatabase.driver(bolt, auth=basic_auth(usr, pwd))
    print('INFO: the Neo4j driver is initialized.')


def add_project(name, github_url):
    if not _driver:
        init_driver()
    pid = sha1(name.encode('utf-8')).hexdigest()
    try:
        project = _driver.session().write_transaction(
            query.create_project_node, pid, name, github_url)
        assert project['id'] == pid
        if project['github_url'] != github_url:
            print('WARN: an existing project with a different URL {name: %s} '
                  '{url: %s} => {url: %s}' %
                  (name, project['github_url'], github_url))
            return None
        return pid
    except Exception as e:
        print(e)


def get_project(project_id):
    if not _driver:
        init_driver()
    try:
        return _driver.session().read_transaction(
            query.get_project_node, project_id)
    except Exception as e:
        print(e)


def add_developer(name, email):
    if not _driver:
        init_driver()
    try:
        token = secrets.token_urlsafe()
        _driver.session().write_transaction(
            query.create_developer_email, name, email, token)
        return token
    except Exception as e:
        print(e)


def get_developer_token(email):
    if not _driver:
        init_driver()
    try:
        return _driver.session().read_transaction(
            query.get_developer_token, email)
    except Exception as e:
        print(e)


def add_reviewer(email):
    if not _driver:
        init_driver()
    try:
        token = secrets.token_urlsafe()
        _driver.session().write_transaction(
            query.create_reviewer_node, email, token)
        return token
    except Exception as e:
        print(e)


def add_commit(*, sha1_hex, title, author, email, project_id):
    if not _driver:
        init_driver()
    try:
        tx = _driver.session().begin_transaction()
        query.create_commit_node(tx, sha1_hex, title)
        query.link_commit_author(tx, sha1_hex, email)
        query.link_project_commit(tx, sha1_hex, project_id)
        tx.commit()
    except Exception as e:
        print(e)


def add_comparison(commit1, commit2, email):
    if not _driver:
        init_driver()
    try:
        if commit1 > commit2:
            commit1, commit2 = commit2, commit1
        cid = sha1((commit1 + commit2 + email).encode('utf-8')).hexdigest()
        _driver.session().write_transaction(query.create_comparison_node,
                                            cid, commit1, commit2, email)
        return cid
    except Exception as e:
        print(e)


def next_comparison(token):
    if not _driver:
        init_driver()
    n = -1
    try:
        n = _driver.session().read_transaction(
            query.count_compared_relationships, token)
        comparison, commit1, commit2 = _driver.session().read_transaction(
            query.next_comparison_node, token)
        return comparison, commit1, commit2, n
    except Exception as e:
        print(e)
        return None, None, None, n


def add_answer(*, comparison_id, valuable_commit, reason, token):
    if not _driver:
        init_driver()
    try:
        tx = _driver.session().begin_transaction()
        c1, c2 = query.delete_comparison_node(tx, comparison_id, token)
        if valuable_commit is None:
            tx.commit()
            return
        if c2 == valuable_commit:
            c1, c2 = c2, c1
        assert c1 == valuable_commit
        query.create_compared_relationship(
            tx, comparison_id, c1, c2, reason, token)
        tx.commit()
    except Exception as e:
        print(e)


def next_review(project_id, token):
    if not _driver:
        init_driver()
    n = -1
    try:
        n = _driver.session().read_transaction(
            query.count_reviewed_relationships, token)
        comparison_id, commit1, commit2 = _driver.session().read_transaction(
            query.next_compared_relationship, project_id, token)
        return comparison_id, commit1, commit2, n
    except Exception as e:
        print(e)
        return None, None, None, n


def add_label(name, genre, token):
    if not _driver:
        init_driver()
    lid = sha1(name.encode('utf-8')).hexdigest()
    try:
        res_lid = _driver.session().write_transaction(
            query.create_label_node, lid, name, genre, token)
        assert res_lid == lid
        return lid
    except Exception as e:
        print(e)


def list_labels(token):
    if not _driver:
        init_driver()
    try:
        rec_builtin, rec_custom = _driver.session().read_transaction(
            query.list_label_nodes, token)
        builtin = [{'id': r['label']['id'], 'name': r['label']['name']}
                   for r in rec_builtin]
        custom = [{'id': r['label']['id'], 'name': r['label']['name']}
                  for r in rec_custom]
        return builtin, custom
    except Exception as e:
        print(e)
        return None, None


def add_review(*, comparison_id, commit_id, label_ids, token):
    if not _driver:
        init_driver()
    try:
        _driver.session().write_transaction(
            query.create_label_relationship,
            comparison_id, commit_id, label_ids, token)
    except Exception as e:
        print(e)


def add_comment(comparison_id, comment, token):
    if not _driver:
        init_driver()
    try:
        _driver.session().write_transaction(
            query.create_comment_property, comparison_id, comment, token)
    except Exception as e:
        print(e)


def list_email_project():
    if not _driver:
        init_driver()
    try:
        return _driver.session().read_transaction(query.list_email_project)
    except Exception as e:
        print(e)


def developer_stats(token):
    if not _driver:
        init_driver()
    try:
        unanswered = _driver.session().read_transaction(
            query.count_comparison_nodes, token)
        answered = _driver.session().read_transaction(
            query.count_compared_relationships, token)
        return unanswered + answered, answered
    except Exception as e:
        print(e)
