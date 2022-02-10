# TaskManager

This project was generated via [manage-fastapi](https://ycd.github.io/manage-fastapi/)! :tada:

Welcome to my project. First of all, I would like to inform you that new generation technologies have been used in this project, and below I will present you a list of those technologies.

```angular2html
Python 3.9
FastAPI
fastapi-jwt-auth for JWT auth
Peewee
Celery + RabbitMQ
RestAPI
Swagger
Unit test
Docker
```

Now let's move on to the main idea of ​​the project. Project 2 consists of a section Users and Tasks section. A new user is created. Then a token is generated when that user logs in. If that token becomes invalid, then the reflesh token is generated. Then the user creates a task (IP request: https://ipdata.co/)
This task is saved to the database. You can then use the status endpoint to view the status of that task.

Now let's talk about how to start this project.

#git clone

```
$ git@github.com: cavidanhasanli / TaskManager.git
```

#docker build up

```
$ docker-compose up --build
```

The project is available in the test section:

```angular2html
$ 
```