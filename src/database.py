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
        n = _driver.session().read_transaction(
            query.count_compared_relationships, email)
        comparison, commit1, commit2 = _driver.session().read_transaction(
            query.next_comparison_node, email)
        return comparison, commit1, commit2, n
    except Exception as e:
        print(e)
        return None, None, None, None


def add_reason(*, comparison_id, valuable_commit, reason, email):
    if not _driver:
        init_driver()
    try:
        tx = _driver.session().begin_transaction()
        c1, c2 = query.delete_comparison_node(tx, comparison_id)
        if c2 == valuable_commit:
            c1, c2 = c2, c1
        assert c1 == valuable_commit
        query.create_compared_relationship(
            tx, comparison_id, c1, c2, reason, email)
        tx.commit()
    except Exception as e:
        print(e)


def next_review(project_id, email):
    if not _driver:
        init_driver()
    try:
        n = _driver.session().read_transaction(
            query.count_reviewed_relationships, email)
        comparison_id, commit1, commit2 = _driver.session().read_transaction(
            query.next_compared_relationship, project_id)
        return comparison_id, commit1, commit2, n
    except Exception as e:
        print(e)
        return None, None, None, None


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


def list_labels():
    if not _driver:
        init_driver()
    try:
        records = _driver.session().read_transaction(query.list_label_nodes)
        builtin = []
        customized = []
        for r in records:
            builtin.append({'id': r['builtin']['id'],
                            'name': r['builtin']['name']})
            customized.append({'id': r['customized']['id'],
                               'name': r['customized']['name']})
        return builtin, customized
    except Exception as e:
        print(e)
        return None, None


def add_review(*, comparison_id, commit_id, label_ids, email):
    if not _driver:
        init_driver()
    try:
        _driver.session().write_transaction(
            query.create_label_relationship,
            comparison_id, commit_id, label_ids, email)
    except Exception as e:
        print(e)


def add_comment(comparison_id, comment, email):
    if not _driver:
        init_driver()
    try:
        _driver.session().write_transaction(
            query.create_comment_relationship, comparison_id, comment, email)
    except Exception as e:
        print(e)


def main():
    pid = add_project('Hotot', 'https://github.com/lyricat/Hotot')
    add_developer('Lyric Wai', 'w@persper.org')
    # The first pair for test
    add_commit(sha1_hex='915330ffc269eed821d652292993ff75b717a66b',
               title='new image for tweets which are retweeted by user',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    cid = add_comparison('b35414f93aa5caaff115791d4040271047df25b3',
                         '915330ffc269eed821d652292993ff75b717a66b',
                         'w@persper.org')
    comp, c1, c2, n = next_comparison('w@persper.org')
    assert comp['id'] == cid
    print('Answering:', n, comp['id'], c1['id'], c2['id'])
    add_reason(comparison_id=cid,
               valuable_commit='b35414f93aa5caaff115791d4040271047df25b3',
               reason='第二个 commit 是 disable a feature，第一个是优化体验。',
               email='w@persper.org')
    add_commit(sha1_hex='b35414f93aa5caaff115791d4040271047df25b3',
               title='disable the position saving',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    test, _, _, _ = next_comparison('w@persper.org')
    assert test is None

    cid, c1, c2, n = next_review(pid, 'jinglei@persper.org')
    assert cid == comp['id']
    selected = c1['id']
    if c1['id'] > c2['id']:
        c1, c2 = c2, c1
    print('Reviewing: ', n, cid, c1['id'], c2['id'], selected)
    label_small = add_label('small', 'Builtin')
    label_reduce_feature = add_label('reduce_feature')
    label_improve_use = add_label('improve_use')
    add_review(comparison_id=cid, commit_id=c1['id'],
               label_ids=[label_small, label_improve_use],
               email='jinglei@persper.org')
    test, _, _, _ = next_review(pid, 'jinglei@persper.org')
    assert test == cid
    add_review(comparison_id=cid, commit_id=c2['id'],
               label_ids=[label_reduce_feature],
               email='jinglei@persper.org')
    test, _, _, _ = next_review(pid, 'jinglei@persper.org')
    assert test is None

    # The second pair for test
    add_commit(sha1_hex='810b5bdd1b6010867c8f8c04589633796a7e4362',
               title='Closes #445 - preferences window now showing for statusnet accounts',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    add_commit(sha1_hex='d135f46d4149d1dd3b7fad92c737b1ab96991821',
               title='Fixed #93',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    cid2 = add_comparison('810b5bdd1b6010867c8f8c04589633796a7e4362',
                          'd135f46d4149d1dd3b7fad92c737b1ab96991821',
                          'w@persper.org')
    # The third pair for test
    add_commit(sha1_hex='84e9c84b6bfa6c51caaa402248bcc5b60b713668',
               title='use notification to popup errors.',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    add_commit(sha1_hex='a37dde730e446402683aa2bf8647870c8446b34e',
               title='minor improvements',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    cid3 = add_comparison('a37dde730e446402683aa2bf8647870c8446b34e',
                          '84e9c84b6bfa6c51caaa402248bcc5b60b713668',
                          'w@persper.org')

    comp_tmp, _, _, n_tmp = next_comparison('w@persper.org')
    comp, c1, c2, n = next_comparison('w@persper.org')
    assert comp['id'] == comp_tmp['id'] and n == n_tmp
    print('Answering: ', n, comp['id'], c1['id'], c2['id'])
    add_reason(comparison_id=cid3, valuable_commit='84e9c84b6bfa6c51caaa402248bcc5b60b713668',
               reason='B is a small refactor; A is to notify errors.', email='w@persper.org')

    comp, c1, c2, n = next_comparison('w@persper.org')
    assert comp['id'] == cid2

    cid_tmp, _, _, n_tmp = next_review(pid, 'jinglei@persper.org')
    cid, c1, c2, n = next_review(pid, 'jinglei@persper.org')
    assert cid == cid_tmp and n == n_tmp
    add_comment(cid, 'TODO', 'jinglei@persper.org')

    test, _, _, _ = next_review(pid, 'jinglei@persper.org')
    assert test is None

    builtin, customized = list_labels()
    print(builtin, customized)


if __name__ == '__main__':
    main()
