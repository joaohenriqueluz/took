#!/bin/sh
# .git/hooks/post-checkout

# Check if .took exists in the repository
if [ -d ".took" ]; then
    # Start a new task based on the branch name
    BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
    took start --task "$BRANCH_NAME"
fi
