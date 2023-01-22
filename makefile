PROJECT_NAME = ETL

all:
	@echo "make start - Запуск контейнеров."
	@echo "make stop - Выключение контейнера."

start:
	docker-compose up -d --build
stop:
	docker-compose down
