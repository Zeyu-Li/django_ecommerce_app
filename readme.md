# Django Ecommerce App

## General

This is the successor of [django_ecommerse_app_deprecated](https://github.com/Zeyu-Li/django_ecommerse_app_deprecated)

This is a Django Ecommerce App with login and a shopping cart



## How to use

To start, install the required packages using the requirement.txt
This step will require the [virtual ven module](https://docs.python.org/3/library/venv.html) (this might require admin access)

This can be done by entering in

```powershell
pip install -r requirements.txt
```

into powershell or terminal

Afterwards, move into the andrew_li_django_website directory and enter

```powershell
python manage.py runserver --settings=andrew_site.settings.dev
```

if you are on Windows

OR

```shell
python3 manage.py runserver --settings=andrew_site.settings.dev
```

if you are on Mac or Linux

If it is a production environment, use **prod** instead of **dev** in the end condition



## Dependencies/Modules

* [virtualenv](https://docs.python.org/3/tutorial/venv.html)
* [Django](https://www.djangoproject.com/)
* django-crispy-forms
* django-recaptcha
* django-svg-templatetag



## Reuse

This code is under MIT licence.

