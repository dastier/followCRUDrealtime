# Test Task (Python/Flask/Postgres/Websockets/Docker)

## Webapp that shows CRUD operations on users via websockets in real time

### Endpoints

default hostname: localhost/127.0.0.1

default port: 5000

| Method | URL             | Description                                |
| ------ | --------------- | -------------------------------------------|
| GET  | http://[host:port]/ | main "Operations log" page  |
| GET  | http://[host:port]/users | Retrieve list of users |
| GET  | http://[host:port]/user/\<id> | Retrieve specific user info |
| POST | http://[host:port]/add> | Create a new user |
| PUT  | http://[host:port]/update/\<id>?name=<new_name> | Update an existing user |
| DELETE | http://[host:port]/delete/\<id> | Delete a user |

### Examples

```sh
curl --request POST --url 'http://127.0.0.1:5000/add?name=Added%20Name'

curl --request DELETE --url 'http://127.0.0.1:5000/delete/1'

curl --request PUT --url 'http://127.0.0.1:5000/update/30?name=Changed%20Name'

curl --request GET --url 'http://127.0.0.1:5000/users'

curl --request GET --url 'http://127.0.0.1:5000/user/7'
```

### How to run this app

1. install Docker and  Docker Compose

2. run the following commands:

```sh
  $ git clone https://github.com/dastier/followCRUDrealtime.git
  $ cd followCRUDrealtime/
  $ docker-compose up --build
```

### Demo screenshot

![Screenshot](/images/demo_image.png)

### Tech

* [Python 3.8]
* [Flask 1.1]
* [SQLAlchemy]
* [Postgres 12.1]
* [Docker]
* [Socket.IO]

### things to improve

* cover by unit tests

* use any production-ready WSGI server

* less hardcode

* better code structure

* etc..

[//]: # (reference links )

   [Python 3.8]: <https://www.python.org/>
   [Flask 1.1]: <https://www.palletsprojects.com/p/flask/>
   [SQLAlchemy]: <https://www.sqlalchemy.org/>
   [Postgres 12.1]: <https://www.postgresql.org/>
   [Socket.IO]: <https://socket.io/>
   [Docker]: <https://github.com/markdown-it/markdown-it>
