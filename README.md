# Второй спринт

## Описание целей спринта 

Цель спринта - создать docker-compose, содержащий три контейнера:
1) контейнер с базой данных Postgre - database;
2) контейнер с самим приложением Django - service;
3) контейнер с nginx, через который мы общаемся с приложением - nginx;

Реализовать два api, описание которых представлено в файле `django_api/openapi.yaml` (Можно открыть его в [Swagger](https://editor.swagger.io/)).
1) `/api/v1/movies/` - постранично отображает информацию о фильмах;
2) `/api/v1/movies/{id}` - предоставляет информацию по конкретному фильму по его uuid;


## Запуск приложения

Для запуска приложения в локальных условиях необходимо проделать действия, описанные ниже. 
Файл настройки `docker-compose` располагается по пути `docker_compose/docker-compose.prod.yml`.
Контейнер `service` при запуске использует ENTRYPOINT, описанный в файле `docker_compose/whait-for-database.sh`:
в нем ожидается подключение к PostgreSQL. После этого накатываются миграции, создается суперпользователь и приложение стартует через gunicorn.

1) Перейти в папку `docker_compose`, из нее в консоли последовательно выполнить указанные команды.
2) Удаление контейнеров и томов (если уже устанавливали их ранее) - `docker-compose -f docker-compose.prod.yml down -v`
3) Запуск контейнеров с перестройкой image - `docker-compose -f docker-compose.prod.yml up -d --build`
4) Загрузка тестовых данных в БД (в базе появятся данные, необходимые для наглядной работы api) - `docker-compose -f docker-compose.prod.yml exec service python manage.py loaddata dumpdata.json`
5) Перейдите по ссылке [localhost/admin](http://127.0.0.1:80/admin/), для входа в админку воспользуйтесь парой `логин/пароль: admin/admin`


## Запуск редис

`docker-compose -f redis.yml up -d --build`