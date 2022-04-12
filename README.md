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

