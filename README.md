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

# Для запуска тестов 

```Bash
docker-compose exec backend /app/tests-start.sh
```
