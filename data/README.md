This data set is stored in neo4j. You can restore the databases from graphdb.zip files ([instructions](https://docs.graphenedb.com/docs/importing-and-exporting-databases) for graphenedb.com or a local instance).

For the Linux and FreeBSD projects, run the following query to select all commit-pair comparisons that are regarded as ground truth. The result is dumped to `linux-freebsd-survey.csv`, containing 979 rows.

```Cypher
MATCH (e1:Email)-[:AUTHORS]->(c1:Commit)-[o:OUTVALUES*]->(c2:Commit)<-[:AUTHORS]-(e2:Email)
WHERE e1.email = e2.email AND ALL(x IN o WHERE x.email = e1.email)
WITH c1, c2, o
MATCH (c1)-[:COMMITTED_TO]->(p:Project)<-[:COMMITTED_TO]-(c2)
WHERE p.name = 'torvalds-linux' OR p.name = 'freebsd-freebsd'
RETURN p AS `Project`, c1 AS `High-value commit`, c2 AS `Low-value commit`, o AS `Reason(s)`
```

For the JavaScript projects, run the following query to select all commit-pair comparisons that are regarded as ground truth. The result is dumped to `js-survey.csv`, containing 441 data rows.

```Cypher
MATCH (e1:Email)-[:AUTHORS]->(c1:Commit)-[o:OUTVALUES*]->(c2:Commit)<-[:AUTHORS]-(e2:Email)
WHERE e1.email = e2.email AND ALL(x IN o WHERE x.email = e1.email)
MATCH (c1)-[:COMMITTED_TO]->(p:Project)<-[:COMMITTED_TO]-(c2)
RETURN p AS `Project`, c1 AS `High-value commit`, c2 AS `Low-value commit`, o AS `Reason(s)`
```

In the result, `id` of a commit is its Git hash value.

