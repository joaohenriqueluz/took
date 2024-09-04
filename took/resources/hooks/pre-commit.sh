#!/bin/sh
# .git/hooks/pre-commit

# Check if .took exists in the repository
if [ -d ".took" ]; then
    # Pause the current task
    took status
fi
