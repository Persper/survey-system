# Quick Start

The Persper survey system.

## Build The Front End

Install dependencies.
``` bash
npm install
```

Change the default config.
``` bash
nano src/config.js
# cp src/config.sample.js src/config.js
```

Build in one of the following ways.
``` bash
For hot reload at localhost:8080
npm run dev

# For production with minification
npm run build

# For production and view the bundle analyzer report
npm run build --report
```

Tips for [deployment on Heroku](https://devcenter.heroku.com/articles/getting-started-with-nodejs): Run the following after creating the app.
```bash
heroku buildpacks:set heroku/nodejs
heroku config:set NODE_ENV=staging
```

## Workflow for a Survey

### 1. Prepare for accessing the database

``` bash
# Clone target projects to, e.g., ~/repos/ (commands skipped here).

# Append the src dir to PYTHONPATH.
export PYTHONPATH=$PYTHONPATH:`pwd`/src
```

Create config.ini in the current dir.
```
[neo4j]
bolt=NEO4J_BOLT
user=NEO4J_USER
password=NEO4J_PASSWORD
```

### 2. Populate the database

Three parallel approaches are available. The third approach (2.3) is lately used and recommended.

#### 2.1 Use scan_emails.py to select recent emails, typically for a small project

``` bash
# Populate your database.
cd scripts
./scan_emails.py -d ~/repos/ --batch-mode
./scan_emails.py -d ~/repos/project/ -s 7

# (Optional) Connect to the database with a neo4j client:
neo4j-client -p {password} -u {username} bolt://{address}

# (optional) Run in the neo4j interactive shell to clear corner cases.
MATCH (c:Comparison) WHERE c.commit1 = c.commit2 DETACH DELETE c;
```

#### 2.2 Use populate_db.py with an email list, typically for a large project

This approach depends on [stats_commit.py](https://github.com/Persper/code-analytics/blob/master/tools/repo_stats/stats_commit.py).

```bash
# See more options with -h.
./stats_commit.py -d ~/repos/project/ -s > email.list

# Manually modify email.list if necessary (e.g., selecting authors with most commits).
# It is recommended to view the file with Excel.

# See more options with -h. The setup should match with the run of stats_commit.py.
./populate_db.py -d ~/repos/project/ -f email.list -n 50 -v  # without actually populating the database
# Check the output of the above command first.
./populate_db.py -d ~/repos/project/ -f email.list -n 50
```

#### 2.3 Use input_db.py with a JSON file, typically for multiple projects

The JSON file format should follow the output of [output_commits.py](https://github.com/Persper/survey-system/blob/master/flask/test/output_commits.py).

Prepare all repositories in a batch.
```bash
while read url; do git clone $url; done < github-urls.txt
for d in `ls`; do git -C $d fetch; done
```



### 3. Send out invitations

``` bash
# Set environmental variables for sendgrid.
source sendgrid.env

# Test and send out emails.
./db_notifier.py -f email.list --test
./db_notifier.py -f email.list --send
```

## Local Test 

1. Start up a local Flask service:

``` bash
cd flask
export FLASK_APP=flask_app.py
flask run
```

2. Run test scripts for a small sample database, in the following order:

``` bash
cd flask/test
./test_database.py
./test_flask_app.py -h # see the manual for more details
```

3. Manually test another small sample database:

```bash
./flask/test/output_commits.py -f scripts/sample_commits.json
cd scripts
./input_db.py -d ~/repos/ -f sample_commits.json --input
```
Visit the front end and check with the bottom comments in [output_commits.py](https://github.com/Persper/survey-system/blob/master/flask/test/output_commits.py).

4. After the front end is up locally, visit the page for test: http://localhost:8080/#/manually.

