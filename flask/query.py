def create_project_node(tx, project_id, name, github_url):
    result = tx.run("MERGE (p:Project {name: $name}) "
                    "ON CREATE SET p.id = $pid, p.github_url = $url, p.url = $url "
                    "RETURN p.id AS id, p.github_url AS github_url, p.url AS url",
                    name=name, pid=project_id, url=github_url)
    return result.single() if result is not None else None


def get_project_node(tx, project_id):
    result = tx.run("MATCH (p:Project {id: $project_id}) RETURN p",
                    project_id=project_id)
    record = result.single() if result is not None else None
    return record[0] if record is not None else None


def create_developer_email(tx, name, email, token):
    tx.run("MERGE (e:Email {email: $email}) "
           "SET e.token = $token "
           "MERGE (d:Developer {name: $name}) "
           "MERGE (e)-[:NAMED_TO]->(d)",
           email=email, name=name, token=token)


def get_developer_token(tx, email):
    result = tx.run("MATCH (e:Email {email: $email}) "
                    "RETURN e.token", email=email)
    record = result.single() if result is not None else None
    return record[0] if record is not None else None


def create_commit_node(tx, sha1_hex, title):
    tx.run("MERGE (c:Commit {id: $sha1_hex}) "
           "SET c.title = $title",
           sha1_hex=sha1_hex, title=title)


def link_project_commit(tx, commit_id, project_id):
    tx.run("MATCH (c:Commit {id: $commit_id}) "
           "MATCH (p:Project {id: $project_id}) "
           "MERGE (c)-[:COMMITTED_TO]->(p)",
           commit_id=commit_id, project_id=project_id)


def link_commit_author(tx, commit_id, email):
    tx.run("MATCH (c:Commit {id: $commit_id}) "
           "MERGE (e:Email {email: $email}) "
           "MERGE (e)-[:AUTHORS]->(c)",
           commit_id=commit_id, email=email)


def create_comparison_node(tx, comparison_id, commit1, commit2, email):
    tx.run("MERGE (e:Email {email: $email}) "
           "MERGE (:Commit {id: $c1}) "
           "MERGE (:Commit {id: $c2}) "
           "MERGE (e)-[:COMPARES]->(c:Comparison {id: $cid, commit1: $c1, commit2: $c2})",
           cid=comparison_id, c1=commit1, c2=commit2, email=email)


def next_comparison_node(tx, project_id, token):
    result = tx.run("MATCH (e:Email {token: $token})-[:COMPARES]->(c:Comparison) "
                    "WITH c "
                    "MATCH (c1:Commit {id: c.commit1})-[:COMMITTED_TO]->(:Project {id: $pid})"
                    "<-[:COMMITTED_TO]-(c2:Commit {id: c.commit2}) "
                    "RETURN c, c1, c2 ORDER BY c.id LIMIT 1",
                    pid=project_id, token=token)
    record = result.single() if result is not None else None
    return (record['c'], record['c1'], record['c2']) if record is not None else (None, None, None)


def next_other_comparison_node(tx, project_id, token):
    """
    Selects one comparison that is intended for a different developer.
    Run next_comparison_node first and guarantee no comparisons are intended for the caller.
    :param tx: the transaction to run this query
    :param project_id: the project to select commits from
    :param token: the credential of the caller
    :return: a selected comparison node and its two commits
    """
    result = tx.run("MATCH (e:Email {token: $token}) "
                    "MATCH  (c1:Commit)-[:COMMITTED_TO]->(:Project {id: $pid})<-[:COMMITTED_TO]-(c2:Commit) "
                    "WHERE ((:Comparison {commit1: c1.id, commit2: c2.id})<--() OR "
                    "       (:Comparison {commit1: c2.id, commit2: c1.id})<--()) AND "
                    "      (NOT (c1)-[:OUTVALUES {email: e.email}]-(c2)) "
                    "RETURN c1, c2 LIMIT 1",
                    pid=project_id, token=token)
    record = result.single() if result is not None else None
    return (record['c1'], record['c2']) if record is not None else (None, None)


def delete_comparison_node(tx, comparison_id, token):
    result = tx.run("MATCH (:Email {token: $token})-[:COMPARES]->(n:Comparison {id: $cid}) "
                    "WITH n, n.commit1 AS c1, n.commit2 AS c2 "
                    "DETACH DELETE n "
                    "RETURN c1, c2",
                    cid=comparison_id, token=token)
    record = result.single() if result is not None else None
    return (record['c1'], record['c2']) if record is not None else (None, None)


def count_comparison_nodes(tx, token):
    result = tx.run("MATCH (:Email {token: $token})-[:COMPARES]->(c:Comparison) "
                    "RETURN count(c)", token=token)
    record = result.single() if result is not None else None
    return record[0] if record is not None else None


def create_compared_relationship(tx, comparison_id, more_valuable_commit,
                                 less_valuable_commit, reason, token):
    tx.run("MATCH (e:Email {token: $token}) "
           "MERGE (c1:Commit {id: $c1}) "
           "MERGE (c2:Commit {id: $c2}) "
           "MERGE (c1)-[r:OUTVALUES {id: $cid, email: e.email}]->(c2) "
           "SET r.reason = $reason",
           c1=more_valuable_commit, c2=less_valuable_commit,
           cid=comparison_id, token=token, reason=reason)


def create_reviewer_node(tx, email, token):
    tx.run("MERGE (r:Reviewer {email: $email}) "
           "SET r.token = $token",
           email=email, token=token)


def next_other_compared_relationship(tx, project_id, token, threshold):
    """
    Selects a pair of commits compared by their author but not sufficiently compared by others.
    :param tx: the transaction to run this query
    :param project_id: the project to select commits from
    :param token: the credential of the caller
    :param threshold: the max number of other developers that have compared the pair
    :return: a selected pair of commits
    """
    result = tx.run("MATCH (e:Email {token: $token}) "
                    "MATCH (:Project {id: $pid})<-[:COMMITTED_TO]-(c1:Commit)-[o:OUTVALUES]->"
                    "(c2:Commit)-[:COMMITTED_TO]->(:Project {id: $pid}) "
                    "WHERE (c1)<-[:AUTHORS]-(:Email {email: o.email})-[:AUTHORS]->(c2) AND "
                    "      (NOT (c1)-[:OUTVALUES {email: e.email}]-(c2)) "
                    "WITH c1, c2 "
                    "OPTIONAL MATCH (c1)-[o:OUTVALUES]-(c2) "
                    "WITH c1, c2, count(o) AS n "
                    "WHERE n - 1 <= $threshold "
                    "RETURN c1, c2 LIMIT 1",
                    pid=project_id, token=token, threshold=threshold)
    record = result.single() if result is not None else None
    return (record['c1'], record['c2']) if record is not None else (None, None)


def next_compared_relationship(tx, project_id, token):
    result = tx.run("MATCH (:Reviewer {token: $token}) "
                    "MATCH (c1:Commit)-[o:OUTVALUES]->(c2:Commit) "
                    "WHERE (c1)-[:COMMITTED_TO]->(:Project {id: $pid})<-[:COMMITTED_TO]-(c2) AND "
                    "      (NOT (c1)-[:LABELED_WITH {comparison_id: o.id}]->(:Label) OR "
                    "       NOT (c2)-[:LABELED_WITH {comparison_id: o.id}]->(:Label)) AND "
                    "      (NOT EXISTS(o.comment)) "
                    "RETURN o, c1, c2 LIMIT 1",
                    pid=project_id, token=token)
    record = result.single() if result is not None else None
    return (record['o'], record['c1'], record['c2']) if record is not None else (None, None, None)


def get_compared_relationships(tx, commit, token):
    result = tx.run("MATCH (e:Email {token: $token}) "
                    "MATCH (c1:Commit {id: $cid})-[o:OUTVALUES {email: e.email}]->(c2:Commit) "
                    "RETURN c1 AS commit1, o AS outvalues, c2 AS commit2 "
                    "UNION "
                    "MATCH (e:Email {token: $token}) "
                    "MATCH (c1:Commit)-[o:OUTVALUES {email: e.email}]->(c2:Commit {id: $cid}) "
                    "RETURN c1 AS commit1, o AS outvalues, c2 AS commit2",
                    token=token, cid=commit)
    return result.records()


def get_compared_relationships_unsafe(tx, commit):
    result = tx.run("MATCH (c1:Commit {id: $cid})-[o:OUTVALUES]->(c2:Commit) "
                    "RETURN c1 AS commit1, o AS outvalues, c2 AS commit2 "
                    "UNION "
                    "MATCH (c1:Commit)-[o:OUTVALUES]->(c2:Commit {id: $cid}) "
                    "RETURN c1 AS commit1, o AS outvalues, c2 AS commit2",
                    cid=commit)
    return result.records()


def list_project_compared_relationships(tx, project_name):
    result = tx.run("MATCH (c1:Commit)-[o:OUTVALUES]->(c2:Commit)"
                    "-[:COMMITTED_TO]->(:Project {name: $name}) "
                    "RETURN c1 AS commit1, o AS outvalues, c2 AS commit2",
                    name=project_name)
    return result.records()


def list_compared_relationships(tx):
    result = tx.run("MATCH (e:Email)-[:AUTHORS]->(c1:Commit)-[o:OUTVALUES]->(c2:Commit)-[:COMMITTED_TO]->(p:Project) "
                    "RETURN e AS author, c1 AS commit1, c2 AS commit2, o AS relation, p AS project")
    return result.records()


def count_compared_relationships(tx, project_id, token):
    result = tx.run("MATCH (e:Email {token: $token}) "
                    "MATCH (c1:Commit)-[r:OUTVALUES {email: e.email}]->(c2:Commit) "
                    "WHERE (c1)-[:COMMITTED_TO]->(:Project {id: $project})<-[:COMMITTED_TO]-(c2) "
                    "RETURN count(r)", token=token, project=project_id)
    record = result.single() if result is not None else None
    return record[0] if record is not None else None


def create_label_node(tx, label_id, label_name, genre, token):
    result = tx.run("MATCH (:Reviewer {token: $token}) "
                    "MERGE (l:Label:%s {name: $name}) "
                    "ON CREATE SET l.id = $id "
                    "RETURN l.id" % genre,
                    id=label_id, name=label_name, token=token)
    record = result.single() if result is not None else None
    return record[0] if record is not None else None


def list_label_nodes(tx, token):
    builtin = tx.run("MATCH (:Reviewer {token: $token}) "
                     "MATCH (label:Builtin) RETURN label", token=token)
    customized = tx.run("MATCH (:Reviewer {token: $token}) "
                        "MATCH (label:Customized) RETURN label", token=token)
    return builtin.records(), customized.records()


def create_label_relationship(tx, comparison_id, commit_id, label_ids, token):
    for label_id in label_ids:
        tx.run("MATCH (r:Reviewer {token: $token}) "
               "MATCH (c:Commit {id: $commit_id}) "
               "MATCH (l:Label {id: $label_id}) "
               "MERGE (c)-[:LABELED_WITH {comparison_id: $cid, email: r.email}]->(l)",
               commit_id=commit_id, label_id=label_id,
               cid=comparison_id, token=token)


def create_comment_property(tx, comparison_id, comment, token):
    tx.run("MATCH (r:Reviewer {token: $token}) "
           "MATCH (:Commit)-[o:OUTVALUES {id: $cid}]->(:Commit) "
           "SET o.comment = $comment",
           cid=comparison_id, comment=comment, token=token)


def count_reviewed_relationships(tx, token):
    result = tx.run("MATCH (r:Reviewer {token: $token}) "
                    "MATCH (c1:Commit)-[o:OUTVALUES]->(c2:Commit) "
                    "WHERE ((c1)-[:LABELED_WITH {email: r.email}]->(:Label) AND "
                    "       (c2)-[:LABELED_WITH {email: r.email}]->(:Label)) OR "
                    "      EXISTS(o.comment)"
                    "RETURN count(o.id)", token=token)
    record = result.single() if result is not None else None
    return record[0] if record is not None else None


def list_email_project(tx):
    result = tx.run("MATCH (e:Email)-[:AUTHORS]->(:Commit)-[:COMMITTED_TO]->(p:Project) "
                    "RETURN DISTINCT e.email AS email, e.token AS token, p.name AS project_name, p.id AS project_id")
    return result.records()


def count_project_compared_relationships(tx, project_name):
    result = tx.run("MATCH (e:Email) WITH e "
                    "MATCH (Project {name: $name})<-[:COMMITTED_TO]-(:Commit)-[o:OUTVALUES {email: e.email}]->"
                    "(:Commit)-[:COMMITTED_TO]->(Project {name: $name}) "
                    "RETURN e.email AS email, count(o) AS count ORDER BY e.email",
                    name=project_name)
    return result.records()


def count_compared_relationships_by_email(tx):
    result = tx.run("MATCH (e:Email) WITH e "
                    "MATCH (:Commit)-[o:OUTVALUES {email: e.email}]->(:Commit) "
                    "RETURN e.email AS email, count(o) AS count ORDER BY e.email")
    return result.records()
