# Django Restframework App

## User and Referral Code

In this project I've created models and views for user and referral code

## Run App

1. `cd referral`
2. `source ./bin/activate`
3. `cd app`
4. `python manage.py runserver`

### Steps

1. create app `django-admin startproject mysite`
2. add

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

3. run migration

```shell
python manage.py makemigrations
python manage.py migrate
```

4. run app

```shell
python manage.py runserver 0.0.0.0:8000
```

## How to create sub-apps

1. In `/referral/app` directory, two create two apps:

```shell
python manage.py startapp user
python manage.py startapp referral
```

## How to create superuser

```shell
python manage.py createsuperuser --email admin@example.com --username admin
```

## TODO

-   [ ] creating referral code has bug
