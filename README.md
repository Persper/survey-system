# persper-survey

The Persper survey system

## Build

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

## Database Script

``` bash
# clear database
MATCH (n) DETACH DELETE n;

# remove comparions between same commits
MATCH (c:Comparison) WHERE c.commit1 = c.commit2 DETACH DELETE c;

# inspect database
MATCH (n) RETURN n LIMIT 25;
```

## Workflow

``` bash
# clone repos (skipped here)

# append the src dir to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:`pwd`/src

# set environmental variables NEO4J_BOLT, NEO4J_USER, and NEO4J_PASSWORD
# for accessing the database
source neo4j.env

# populate database
cd scripts
./scan_emails.py -d ../repos/ --batch-mode
./scan_emails.py -d ../special_repos/chinese-newcomers-service-center/ -s 7
./scan_emails.py -d ../special_repos/coursequestionbank/ 

# connect to database with neo4j client
neo4j-client -p {password} -u hezheng bolt://hobby-hkhdigaajbbfgbkegfgmfepl.dbs.graphenedb.com:24786

# run in neo4j interactive shell
MATCH (c:Comparison) WHERE c.commit1 = c.commit2 DETACH DELETE c;

# souce env for sendgrid
source sendgrid.env

# test and send out emails
./notifier.py -t
./notifier.py -s
```

