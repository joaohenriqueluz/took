#!/bin/sh
# .git/hooks/post-commit

# Check if .took exists in the repository
if [ -d ".took" ]; then
    # Show the current status (optional)
    took status

fi
