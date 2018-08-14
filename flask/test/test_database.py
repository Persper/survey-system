#!/usr/bin/env python3.6

from database import *


def main():
    pid = add_project('Hotot', 'https://github.com/lyricat/Hotot')
    developer = add_developer('Lyric Wai', 'w@persper.org')
    reviewer = add_reviewer('jinglei@persper.org')

    # Loads built-in labels.
    add_label('tiny', 'Builtin', reviewer)
    label_small = add_label('small', 'Builtin', reviewer)
    assert(label_small == add_label('small', 'Builtin', reviewer))
    add_label('moderate', 'Builtin', reviewer)
    add_label('large', 'Builtin', reviewer)
    add_label('huge', 'Builtin', reviewer)

    # Loads the 1st question.
    # This is an out-of-order complicated path.
    add_commit(sha1_hex='915330ffc269eed821d652292993ff75b717a66b',
               title='new image for tweets which are retweeted by user',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    cid = add_comparison('b35414f93aa5caaff115791d4040271047df25b3',
                         '915330ffc269eed821d652292993ff75b717a66b',
                         'w@persper.org')
    q, c1, c2, n = next_comparison(developer)
    assert q['id'] == cid
    assert c1['id'] == '915330ffc269eed821d652292993ff75b717a66b'
    assert c2['id'] == 'b35414f93aa5caaff115791d4040271047df25b3'
    print('Added Question #%d: %s' % (n, cid))

    # Answers the 1st question.
    add_answer(comparison_id=cid,
               valuable_commit='b35414f93aa5caaff115791d4040271047df25b3',
               reason='第二个 commit 是 disable a feature，第一个是优化体验。',
               token=developer)
    add_commit(sha1_hex='b35414f93aa5caaff115791d4040271047df25b3',
               title='disable the position saving',
               author='Lyric Wai', email='5h3ll3x@gmail.com',
               project_id=pid)
    print('Answered Question #%d: %s' % (n, cid))
    test, _, _, next_n = next_comparison(developer)
    assert test is None  # No more questions.
    assert next_n == n + 1  # But the next question number is there.

    comp, c1, c2, n = next_review(pid, reviewer)
    assert comp['id'] == cid
    assert c1['id'] == 'b35414f93aa5caaff115791d4040271047df25b3'  # The selected one.
    assert c2['id'] == '915330ffc269eed821d652292993ff75b717a66b'

    answers = get_related_answers('b35414f93aa5caaff115791d4040271047df25b3', developer)
    len(answers) == 1
    answers = get_related_answers('915330ffc269eed821d652292993ff75b717a66b', developer)
    len(answers) == 1

    # Adds the 1st review.
    label_reduce_feature = add_label('reduce_feature', 'Customized', reviewer)
    label_improve_use = add_label('improve_use', 'Customized', reviewer)
    add_review(comparison_id=cid, commit_id=c1['id'],
               label_ids=[label_small, label_improve_use], token=reviewer)
    comp, _, _, next_n = next_review(pid, reviewer)
    assert comp['id'] == cid and next_n == n  # The current full review is not done yet.
    add_review(comparison_id=cid, commit_id=c2['id'],
               label_ids=[label_reduce_feature], token=reviewer)
    test, _, _, next_n = next_review(pid, reviewer)
    assert test is None and next_n == n + 1

    # Loads the 2nd question.
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

    # Loads the 3rd question.
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

    q, _, _, n = next_comparison(developer)
    next_q, _, _, next_n = next_comparison(developer)
    assert next_q['id'] == q['id'] and next_n == n

    answers = get_related_answers('84e9c84b6bfa6c51caaa402248bcc5b60b713668', developer)
    assert len(answers) == 0
    answers = get_related_answers('a37dde730e446402683aa2bf8647870c8446b34e', developer)
    assert len(answers) == 0

    # Answers the 3rd question (skipping the 2nd).
    add_answer(comparison_id=cid3, valuable_commit='84e9c84b6bfa6c51caaa402248bcc5b60b713668',
               reason='B is a small refactor; A is to notify errors.',
               token=developer)
    print('Answered Question #%d: %s' % (n, cid))

    q, _, _, next_n = next_comparison(developer)
    assert q['id'] == cid2 and next_n == n + 1

    comp, _, _, n = next_review(pid, reviewer)
    comp, _, _, next_n = next_review(pid, reviewer)
    assert cid3 == comp['id'] and next_n == n

    # Adds the 2nd review by commenting.
    add_comment(cid3, "This is a reviewer's comment", reviewer)

    test, _, _, next_n = next_review(pid, reviewer)
    assert test is None and next_n == n + 1

    builtin, customized = list_labels(reviewer)
    print(builtin, customized)

    # Loads the 4th question.
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

    # Loads the 5th question.
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

    # Loads the 6th question.
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
