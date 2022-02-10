# TaskManager

## How to start

Simply enough:

`docker-compose up --build`

## How to test

To run all unit tests:

`docker-compose run app pytest -vvv`

> Please keep in mind that the tests are not optimized to run locally

Also, you can find postman exported json file in this repo, just import it in Postman and you will have necessary endpoints to test.
The file name is `Task.postman_collection.json`.

## Project dependencies

The project dependency management is based on `Poetry`.

## Migrations

Peewee migrations are managed by `peewee-migrations` package.
Migrations located in migrations folder and settings is `migrations.json`.

## Additional notes

There is a scripts folder where I have defined helper bash scripts for formatting and linting the code base.
All codebase was formatted using black, flake8 and isort.

You can run it manually:

`./scripts/format-imports.sh`

Also there is a `lint.sh` file which can be added to the Github workflow.

This action was defined as pre-commit hook, at each commit it will reformat your code base.
For activating pre-commit run locally:
`pre-commit install`

At each commit you will have nicely formatted code base.