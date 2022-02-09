#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app tests task user --exclude=__init__.py
black app user task tests
isort app user task tests