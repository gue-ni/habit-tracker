#!/bin/bash
set -e

BRANCH=$(git rev-parse --abbrev-ref HEAD)
REMOTE="origin"

git fetch $REMOTE

LOCAL=$(git rev-parse $BRANCH)
REMOTE_REF=$(git rev-parse $REMOTE/$BRANCH)
BASE=$(git merge-base $BRANCH $REMOTE/$BRANCH)

if [ $LOCAL = $REMOTE_REF ]; then
  echo "The local branch '$BRANCH' is up to date with '$REMOTE/$BRANCH'. No action needed."

elif [ $LOCAL = $BASE ]; then
  echo "The local branch '$BRANCH' is behind '$REMOTE/$BRANCH'. Pulling latest changes and rebuilding containers."

  git pull $REMOTE $BRANCH

  docker compose down
  docker compose build
  docker compose up -d
else
  echo "No pull required or branches have diverged."
fi


