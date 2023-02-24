PROJECT_NAME = ETL

all:
	@echo "make start - Запуск контейнеров."
	@echo "make stop - Выключение контейнера."
	@echo "make createsuperuser - Создание суперпользователя."
	@echo "make async_tests - Запуск тестов асинхронного сервиса."
	@echo "make auth_tests - Запуск тестов сервиса авторизации."
start:
	docker-compose up -d --build
stop:
	docker-compose down
createsuperuser:
	docker-compose exec django python manage.py createsuperuser
async_tests:
	docker-compose -f fastapi-solution/tests/functional/docker-compose.yml up --build --abort-on-container-exit
	docker-compose -f fastapi-solution/tests/functional/docker-compose.yml down
auth_tests:
	docker-compose -f auth-solution/tests/functional/docker-compose.yml up --build --abort-on-container-exit
	docker-compose -f auth-solution/tests/functional/docker-compose.yml down