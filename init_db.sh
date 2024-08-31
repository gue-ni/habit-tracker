#!/bin/bash
set -e
set -x
mkdir -p db
sqlite3 db/database.sqlite "$(cat app/schema.sql)"