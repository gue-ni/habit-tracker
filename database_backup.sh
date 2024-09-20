#!/bin/bash

set -e
set -x


datestamp="$(date +%Y-%m-%d)"

primary_database="/srv/www/habit-tracker/db/database.sqlite"
backup_directory="/root/backup/habit-tracker/$datestamp"

backup_database="$backup_directory/database.sqlite"
backup_dump="$backup_directory/dump.sql"
backup_schema="$backup_directory/schema.sql"

mkdir -p $backup_directory


sqlite3 $primary_database ".backup '$backup_database'"
sqlite3 $primary_database .dump   > $backup_dump
sqlite3 $primary_database .schema > $backup_schema

