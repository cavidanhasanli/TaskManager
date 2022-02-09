#!/usr/bin/env bash

set -e
set -x

flake8 backend
black backend --check --diff
isort backend --check --diff