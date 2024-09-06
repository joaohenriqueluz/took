#!/bin/bash

BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo $BRANCH
MERGED_BRANCH=$(git reflog -1 --format=%B | awk '{print $NF}')
echo $MERGED_BRANCH

# Check if .took exists in the repository
if [ -d ".took" ]; then
    # Get the current branch name

    # Check if the current branch is 'main' or 'master'
    if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
        # Extract the branch name that was merged

        echo "Branch $MERGED_BRANCH has been merged into $BRANCH."

        # Call took to mark the task as done
        took done -t "$MERGED_BRANCH"

        echo "Task for branch $MERGED_BRANCH has been marked as done."
    fi
fi



