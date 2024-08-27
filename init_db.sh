#!/bin/bash
set -e
set -x
sqlite3 db/database.sqlite "$(cat src/schema.sql)"