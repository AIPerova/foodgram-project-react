# [Foodgram](https://foodforyou.hopto.org)
«Фудграм» — сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

# Для проверки работоспособности:

IP: 158.160.30.11;

name_foodgram: https://foodforyou.hopto.org/;

login: hhh@hhh.hhh;

password: wowowo23;

Стек: Python 3, Django 3, Django REST Framework, SQLite3, PostgreSQL, gunicorn, nginx, Яндекс.Облако (Ubuntu 18.04)

# Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AIPerova/foodgram-project-react
```
```
cd foodgram-project-react
```
Создайте файл .env командой touch .env. Шаблон наполнения env-файла:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
Запустите docker-compose командой
```
sudo docker-compose up -d
```
Создайте миграции:
```
docker-compose exec backend python manage.py migrate --noinput
```
Соберите статику проекта командой:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
Создайте суперпользователя Django:
```
sudo docker-compose exec web python manage.py createsuperuser
```
Загрузите тестовые данные в базу данных командой:
```
sudo docker -compose exec backend python manage.py load_ingredients
```
