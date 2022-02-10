#!/usr/bin/env bash

set -e
set -x

flake8 app task user tests
black app task user tests --check --diff
isort app task user tests --check --diff