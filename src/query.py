def create_project_node(tx, project_id, name, url):
    result = tx.run("MERGE (p:Project {name: $name}) "
                    "ON CREATE SET p.id = $pid, p.url = $url "
                    "RETURN p.id AS id, p.url AS url",
                    name=name, pid=project_id, url=url)
    record = result.single()
    return record['id'], record['url']


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


def create_comparison_node(tx, commit1, commit2, email):
    if commit1 > commit2:
        commit1, commit2 = commit2, commit1
    tx.run("MERGE (e:Email {email: $email}) "
           "MERGE (e)-[:COMPARES]->(c:Comparison {commit1: $commit1, commit2: $commit2})",
           commit1=commit1, commit2=commit2, email=email)


def count_compared(tx, email):
    result = tx.run("MATCH (:Commit)-[r:OUTVALUES {email: $email}]->(:Commit) "
                    "RETURN COUNT(r)", email=email)
    return result.single()[0]


def next_comparison_node(tx, email):
    result = tx.run("MATCH (:Email {email: $email})-[:COMPARES]->(c:Comparison) "
                    "WITH c ORDER BY c.commit1 LIMIT 1 "
                    "MATCH (c1:Commit {id: c.commit1}), (c2:Commit {id: c.commit2}) "
                    "RETURN c1, c2", email=email)
    record = result.single()
    return record['c1'], record['c2']


def delete_comparison_node(tx, commit1, commit2, email):
    if commit1 > commit2:
        commit1, commit2 = commit2, commit1
    tx.run("MATCH (:Email {email: $email})-[r:COMPARES]->(n:Comparison {commit1: $commit1, commit2: $commit2}) "
           "DELETE r, n", email=email, commit1=commit1, commit2=commit2)


def create_comparison_relationship(tx, more_valuable_commit,
                                   less_valuable_commit, reason, email):
    tx.run("MERGE (c1:Commit {id: $c1}) "
           "MERGE (c2:Commit {id: $c2}) "
           "MERGE (c1)-[r:OUTVALUES {email: $email}]->(c2) "
           "SET r.reason = $reason",
           c1=more_valuable_commit, c2=less_valuable_commit,
           email=email, reason=reason)


def create_label_node(tx, label_id, label_name, genre):
    result = tx.run("MERGE (l:Label:%s {name: $name}) "
                    "ON CREATE SET l.id = $id "
                    "RETURN l.id" % genre,
                    id=label_id, name=label_name)
    return result.single()[0]


def create_label_relationship(tx, commit_id, label_ids, email):
    for label_id in label_ids:
        tx.run("MATCH (c:Commit {id: $commit_id}) "
               "MATCH (l:Label {id: $label_id}) "
               "MERGE (c)-[:LABELED_WITH {email: $email}]->(l)",
               commit_id=commit_id, label_id=label_id, email=email)
