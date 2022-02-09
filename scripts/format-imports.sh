#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort app user task tests --force-single-line-imports
sh ./scripts/format.sh