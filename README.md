Online-cinema backend with Django, Nginx, ElasticSearch and PostgreSQL and FastAPI services
================================================================================================
This application includes an Admin Panel written in Django framework and an asynchronous backend containing business logic using FastAPI
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
- The Django admin will be available at http://127.0.0.1:8000/admin
- The Django API will be available at http://127.0.0.1:8000/api/v1/movies and http://127.0.0.1:8000/api/v1/movies/{id}
- The FastAPI documentation will be available at http://127.0.0.1:8001/api/openapi Check the documentation for more information about the API
