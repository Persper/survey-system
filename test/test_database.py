#!/usr/bin/env python3

from database import *


def main():
    pid = add_project('Hotot', 'https://github.com/lyricat/Hotot')
    add_developer('Lyric Wai', 'w@persper.org')

    # Inputs the 1st pair of commits for test.
    # This is an out-of-order complicated path. See other pairs for reference.
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
    add_answer(comparison_id=cid,
               valuable_commit='b35414f93aa5caaff115791d4040271047df25b3',
               reason='第二个 commit 是 disable a feature，第一个是优化体验。',
               email='w@persper.org')
    add_commit(sha1_hex='b35414f93aa5caaff115791d4040271047df25b3',
               title='disable the position saving',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    test, _, _, n_1 = next_comparison('w@persper.org')
    assert test is None and n_1 == n + 1

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
    test, _, _, n_1 = next_review(pid, 'jinglei@persper.org')
    assert test == cid and n_1 == n  # The current full review is not done yet.
    add_review(comparison_id=cid, commit_id=c2['id'],
               label_ids=[label_reduce_feature],
               email='jinglei@persper.org')
    test, _, _, n_1 = next_review(pid, 'jinglei@persper.org')
    assert test is None and n_1 == n + 1

    # Inputs the 2nd pair of commits for test.
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

    # Inputs the 3rd pair of commits for test.
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
    add_answer(comparison_id=cid3, valuable_commit='84e9c84b6bfa6c51caaa402248bcc5b60b713668',
               reason='B is a small refactor; A is to notify errors.', email='w@persper.org')

    comp, c1, c2, n = next_comparison('w@persper.org')
    assert comp['id'] == cid2 and n == n_tmp + 1

    cid_tmp, _, _, n_tmp = next_review(pid, 'jinglei@persper.org')
    cid, c1, c2, n = next_review(pid, 'jinglei@persper.org')
    assert cid == cid_tmp and n == n_tmp
    add_comment(cid, 'TODO', 'jinglei@persper.org')

    test, _, _, n = next_review(pid, 'jinglei@persper.org')
    assert test is None and n == n_tmp + 1

    builtin, customized = list_labels()
    print(builtin, customized)

    # Inputs the 4th pair of commits for test.
    add_commit(sha1_hex='873bbd8eaf1bf12121e56f009324e1b29a9154d2',
               title='remove useless styles',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    add_commit(sha1_hex='f2e0f99fd07be21d535d96279d614ccbfc89ad02',
               title="change my_profile_btn's opacity to 100% when mouse hover on it.",
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    add_comparison('873bbd8eaf1bf12121e56f009324e1b29a9154d2',
                   'f2e0f99fd07be21d535d96279d614ccbfc89ad02',
                   'w@persper.org')

    # Inputs the 5th pair of commits for test.
    add_commit(sha1_hex='fe857cbb4893f57b7cd7b4f4daff9ad8e61f463b',
               title='Chrome app bump to 0.9.7.21',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    add_commit(sha1_hex='3cdd92c6f819004e1a36713a4551fd29e878497a',
               title='remove useless image',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    add_comparison('fe857cbb4893f57b7cd7b4f4daff9ad8e61f463b',
                   '3cdd92c6f819004e1a36713a4551fd29e878497a',
                   'w@persper.org')

    # Inputs the 6th pair of commits for test.
    add_commit(sha1_hex='2b5015bcc0a7d5ac2521c7dbfe8243a356b9cffa',
               title='support to swap Quote/Retweet button.',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    add_commit(sha1_hex='6decc9b03b259cf01214a610d3d50893cc6dcaea',
               title='fixed: Issue 354',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    add_comparison('2b5015bcc0a7d5ac2521c7dbfe8243a356b9cffa',
                   '6decc9b03b259cf01214a610d3d50893cc6dcaea',
                   'w@persper.org')


if __name__ == '__main__':
    main()
