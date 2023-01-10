# webtronics test task

## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) 

## Backend local development

* Для запуска проекта:

```bash
docker-compose up -d --build
```


## Проект по адресу http://localhost/docs
## Создание юзера http://localhost/api/v1/users/open
# Данные для бд и т.д в файле .env

# Для запуска тестов 

```Bash
docker-compose exec backend /app/tests-start.sh
```
