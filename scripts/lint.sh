#!/usr/bin/env bash

set -e
set -x

flake8 app user tests
black app user tests --check --diff
isort app user tests --check --diff