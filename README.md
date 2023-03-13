Online-cinema backend with Django, Nginx, ElasticSearch, PostgreSQL, FastAPI and Flask services
================================================================================================
This application includes an Admin Panel written in Django framework, an asynchronous backend containing business logic using FastAPI  
and authentication API using Flask
----------------------------------------------------------------------------------------------------------------------------------------

## Requirements
- Docker
- Docker Compose

## Installation
1. Clone the repository `git clone git@github.com:salliko/async_api.git`
2. Create .env file in the `root directory` with template from example.env
3. Run `make start` in the root directory to start the application
4. Run `make createsuperuser` the root directory to create superuser
5. Run `make stop` in the root directory to stop the application

## Usage
- The Django admin will be available at http://127.0.0.1/admin
- The FastAPI documentation will be available at http://127.0.0.1/api/openapi Check the documentation for more information about the API

## Developers
- Гребенников Илья (salliko)
- Казмин Вадим (vimjk)
- Журавков Владислав (Shuich1)
