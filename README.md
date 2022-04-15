# pmtoolv2
simple scrum management tool

# Instalation 

```
python -m pip install pip --upgrade
python -m pip install -r requirements.txt
```

# Setup (only in the fist run)

```
python manage.py makemigrations scrum
python manage.py migrate
python manage.py createsuperuser
```

Currently, the following models have to be initialized using the admin interface:

* project
* task_list


# Running

```
python manage.py runserver
```

# Learning Django 

The best resources I found are the following: 

* [Mozilla Dev Django Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication)
* [Django Tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/)
