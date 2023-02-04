PROJECT_NAME = ETL

all:
	@echo "make start - Запуск контейнеров."
	@echo "make stop - Выключение контейнера."
	@echo "make createsuperuser - Создание суперпользователя."
	@echo "make tests - Запуск тестов."
start:
	docker-compose up -d --build
stop:
	docker-compose down
createsuperuser:
	docker-compose exec django python manage.py createsuperuser
tests:
	docker-compose -f fastapi-solution/tests/functional/docker-compose.yml up --build