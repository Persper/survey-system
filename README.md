# persper-survey

The Persper survey system

## Build The Front End

``` bash
# install dependencies
npm install

# make a config file
cp src/config.sample.js src/config.js
# change any config
nano src/config.js

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

## Database Script

``` bash
# clear database (DANGEROUS!)
MATCH (n) DETACH DELETE n;

# remove comparions between same commits
MATCH (c:Comparison) WHERE c.commit1 = c.commit2 DETACH DELETE c;

# inspect database
MATCH (n) RETURN n LIMIT 25;
```

## Workflow for a Survey

1. Prepare for accessing the database.

``` bash
# clone target projects to, e.g., ~/repos/ (commands skipped here)

# append the src dir to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:`pwd`/src
```

Create config.ini in the current dir.
```
[neo4j]
bolt=NEO4J_BOLT
user=NEO4J_USER
password=NEO4J_PASSWORD
```

2. Populate the database.

``` bash
# populate database
cd scripts
./scan_emails.py -d ~/repos/ --batch-mode
./scan_emails.py -d ~/repos/project/ -s 7

# (optional) connect to database with neo4j client
neo4j-client -p {password} -u {username} bolt://{address}

# (optional) run in neo4j interactive shell to clear corner cases
MATCH (c:Comparison) WHERE c.commit1 = c.commit2 DETACH DELETE c;
```

3. Send out invitations.

``` bash
# set environmental variables for sendgrid
source sendgrid.env

# test and send out emails
./notifier.py -t
./notifier.py -s
```

## Local Test 

1. Follow the first two steps of the above workflow. To populate the database, another way is to directly run (as `scan_emails.py` does internally):

``` bash
./populate_db.py -d ~/repos/project -e {author email} -n 50
```

2. Start up a local Flask service:

``` bash
cd src
export FLASK_APP=flask_app.py
flask run
```

3. (Optional) Run test scripts for a small sample database, in the following order:

``` bash
cd test
./test_database.py
./test_flask_app.py -h # see the manual for more details
```

4. After the front end is up locally, visit the page for test: http://localhost:8080/#/manually.
