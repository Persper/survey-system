def create_project_node(tx, project_id, name, url):
    result = tx.run("MERGE (p:Project {name: $name}) "
                    "ON CREATE SET p.id = $pid, p.url = $url "
                    "RETURN p.id AS id, p.url AS url",
                    name=name, pid=project_id, url=url)
    record = result.single()
    return record['id'], record['url']


def get_project_node(tx, project_id):
    result = tx.run("MATCH (p:Project {id: $project_id}) RETURN p",
                    project_id=project_id)
    return result.single()[0]


def create_developer_email(tx, name, email):
    tx.run("MERGE (e:Email {email: $email}) "
           "MERGE (d:Developer {name: $name}) "
           "MERGE (e)-[:NAMED_TO]->(d)",
           email=email, name=name)


def create_commit_node(tx, sha1_hex, title):
    tx.run("MERGE (c:Commit {id: $sha1_hex}) "
           "SET c.title = $title ",
           sha1_hex=sha1_hex, title=title)


def link_project_commit(tx, commit_id, project_id):
    tx.run("MATCH (c:Commit {id: $commit_id}) "
           "MATCH (p:Project {id: $project_id}) "
           "MERGE (c)-[:COMMITTED_TO]->(p)",
           commit_id=commit_id, project_id=project_id)


def link_commit_author(tx, commit_id, email):
    tx.run("MATCH (c:Commit {id: $commit_id}) "
           "MATCH (e:Email {email: $email}) "
           "MERGE (e)-[:AUTHORS]->(c)",
           commit_id=commit_id, email=email)


def create_comparison_node(tx, comparison_id, commit1, commit2, email):
    tx.run("MERGE (e:Email {email: $email}) "
           "MERGE (:Commit {id: $c1}) "
           "MERGE (:Commit {id: $c2}) "
           "MERGE (e)-[:COMPARES]->(c:Comparison {id: $cid, commit1: $c1, commit2: $c2})",
           cid=comparison_id, c1=commit1, c2=commit2, email=email)


def next_comparison_node(tx, email):
    result = tx.run("MATCH (:Email {email: $email})-[:COMPARES]->(c:Comparison) "
                    "WITH c ORDER BY c.id LIMIT 1 "
                    "MATCH (c1:Commit {id: c.commit1}), (c2:Commit {id: c.commit2}) "
                    "RETURN c, c1, c2",
                    email=email)
    record = result.single()
    return record['c'], record['c1'], record['c2']


def delete_comparison_node(tx, comparison_id):
    result = tx.run("MATCH (n:Comparison {id: $cid}) "
                    "WITH n, n.commit1 AS c1, n.commit2 AS c2 "
                    "DETACH DELETE n "
                    "RETURN c1, c2",
                    cid=comparison_id)
    record = result.single()
    return record['c1'], record['c2']


def create_compared_relationship(tx, comparison_id, more_valuable_commit,
                                 less_valuable_commit, reason, email):
    tx.run("MERGE (c1:Commit {id: $c1}) "
           "MERGE (c2:Commit {id: $c2}) "
           "MERGE (c1)-[r:OUTVALUES {id: $cid, email: $email}]->(c2) "
           "SET r.reason = $reason",
           c1=more_valuable_commit, c2=less_valuable_commit,
           cid=comparison_id, email=email, reason=reason)


def next_compared_relationship(tx, project_id):
    result = tx.run("MATCH (c1:Commit)-[r:OUTVALUES]->(c2:Commit) "
                    "WHERE (c1)-[:COMMITTED_TO]->(:Project {id: $pid}) "
                    "AND NOT (c1)-[:LABELED_WITH {comparison_id: r.id}]->(:Label) "
                    "OR (c2)-[:COMMITTED_TO]->(:Project {id: $pid}) "
                    "AND NOT (c2)-[:LABELED_WITH {comparison_id: r.id}]->(:Label) "
                    "RETURN r.id, c1, c2 ORDER BY r.id LIMIT 1", pid=project_id)
    record = result.single()
    return record['r.id'], record['c1'], record['c2']


def count_compared_relationships(tx, email):
    result = tx.run("MATCH (:Commit)-[r:OUTVALUES {email: $email}]->(:Commit) "
                    "RETURN COUNT(r)", email=email)
    return result.single()[0]


def create_label_node(tx, label_id, label_name, genre):
    result = tx.run("MERGE (l:Label:%s {name: $name}) "
                    "ON CREATE SET l.id = $id "
                    "RETURN l.id" % genre,
                    id=label_id, name=label_name)
    return result.single()[0]


def list_label_nodes(tx):
    result = tx.run("MATCH (builtin:Builtin) "
                    "MATCH (customized:Customized) "
                    "RETURN builtin, customized")
    return result.records()


def create_label_relationship(tx, comparison_id, commit_id, label_ids, email):
    for label_id in label_ids:
        tx.run("MATCH (c:Commit {id: $commit_id}) "
               "MATCH (l:Label {id: $label_id}) "
               "MERGE (c)-[:LABELED_WITH {comparison_id: $cid, email: $email}]->(l)",
               commit_id=commit_id, label_id=label_id,
               cid=comparison_id, email=email)


def create_comment_relationship(tx, comparison_id, comment, email):
    tx.run("MATCH (c1:Commit)-[:OUTVALUES {id: $cid}]->(c2:Commit) "
           "MERGE (l:Label {name: 'unknown'}) "
           "MERGE (c1)-[r1:LABELED_WITH {comparison_id: $cid, email: $email}]->(l) "
           "SET r1.comment = $comment "
           "MERGE (c2)-[r2:LABELED_WITH {comparison_id: $cid, email: $email}]->(l) "
           "SET r2.comment = $comment",
           cid=comparison_id, comment=comment, email=email)


def count_reviewed_relationships(tx, email):
    result = tx.run("MATCH (:Commit)-[r:LABELED_WITH {email: $email}]->(:LABEL) "
                    "RETURN count(DISTINCT r.id)", email=email)
    return result.single()[0]
