#!/usr/bin/env python3

from neo4j.v1 import basic_auth
from neo4j.v1 import GraphDatabase
from os.path import isfile
from os.path import join
from os import listdir
import random
from hashlib import sha1
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
    bolt = 'bolt://hobby-ifakifjiedbegbkeliefldpl.dbs.graphenedb.com:24786'
    usr, pwd = local_credential('../neo4j-user')
    _driver = GraphDatabase.driver(bolt, auth=basic_auth(usr, pwd))
    print('INFO: the Neo4j driver is initialized.')


def add_project(name, url):
    if not _driver:
        init_driver()
    pid = sha1(name.encode('utf-8')).hexdigest()
    try:
        res_pid, res_url = _driver.session().write_transaction(
            query.create_project_node, pid, name, url)
        assert res_pid == pid
        if res_url != url:
            print('WARN: an existing project with a different URL {name: %s} '
                  '{url: %s} => {url: %s}' % (name, res_url, url))
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
        _driver.session().write_transaction(
            query.create_developer_email, name, email)
    except Exception as e:
        print(e)


def add_commit(*, sha1_hex, title, author, email, project_id):
    if not _driver:
        init_driver()
    try:
        add_developer(author, email)
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


def next_comparison(email):
    if not _driver:
        init_driver()
    try:
        n = _driver.session().read_transaction(query.count_compared, email)
        comparison, commit1, commit2 = _driver.session().read_transaction(
            query.next_comparison_node, email)
        return comparison, commit1, commit2, n
    except Exception as e:
        print(e)


def add_reason(*, comparison_id, valuable_commit, reason, email):
    if not _driver:
        init_driver()
    try:
        tx = _driver.session().begin_transaction()
        c1, c2 = query.delete_comparison_node(tx, comparison_id)
        if c2 == valuable_commit:
            c1, c2 = c2, c1
        assert c1 == valuable_commit
        query.create_value_relationship(tx, c1, c2, reason, email)
        tx.commit()
    except Exception as e:
        print(e)


def add_label(name, genre='Customized'):
    if not _driver:
        init_driver()
    lid = sha1(name.encode('utf-8')).hexdigest()
    try:
        res_lid = _driver.session().write_transaction(
            query.create_label_node, lid, name, genre)
        assert res_lid == lid
        return lid
    except Exception as e:
        print(e)


def add_review(commit_id, label_ids, email):
    if not _driver:
        init_driver()
    try:
        _driver.session().write_transaction(
            query.create_label_relationship, commit_id, label_ids, email)
    except Exception as e:
        print(e)


def main():
    project_id = add_project('Hotot', 'https://github.com/lyricat/Hotot')
    add_developer('Lyric Wai', 'w@persper.org')
    add_commit(sha1_hex='915330ffc269eed821d652292993ff75b717a66b',
               title='new image for tweets which are retweeted by user',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=project_id)
    cid = add_comparison('b35414f93aa5caaff115791d4040271047df25b3',
                   '915330ffc269eed821d652292993ff75b717a66b',
                   'w@persper.org')
    comp, c1, c2, n = next_comparison('w@persper.org')
    print(comp['id'], c1['id'], c2['id'], n)
    add_reason(comparison_id=cid,
               valuable_commit='b35414f93aa5caaff115791d4040271047df25b3',
               reason='第二个 commit 是 disable a feature，第一个是优化体验。',
               email='w@persper.org')
    add_commit(sha1_hex='b35414f93aa5caaff115791d4040271047df25b3',
               title='disable the position saving',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=project_id)
    label_id_small = add_label('small', 'Builtin')
    label_id_maintenance = add_label('reduce_feature')
    label_id_improvement = add_label('improve_use')
    add_review('915330ffc269eed821d652292993ff75b717a66b',
               [label_id_small, label_id_improvement],
               'jinglei@persper.org')
    add_review('b35414f93aa5caaff115791d4040271047df25b3',
               [label_id_maintenance], 'jinglei@persper.org')


if __name__ == '__main__':
    main()
