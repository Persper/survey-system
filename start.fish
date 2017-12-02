#!/usr/bin/env fish
set -x NEO4J_BOLT bolt://hobby-ifakifjiedbegbkeliefldpl.dbs.graphenedb.com:24786
set -x NEO4J_USER survey-system
set -x NEO4J_PASSWORD b.WS2qb6sfYWS1.qOlWiC9O6gHae9nR
cd src
set -x FLASK_APP flask_app.py
flask run
