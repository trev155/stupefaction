# stupefaction
Purpose is to learn about how to scrape data from twitter API and then do some NLP on it.

Good Tutorial to get started on Twitter / Twitter API:
http://socialmedia-class.org/twittertutorial.html

Twitter Application account:
https://apps.twitter.com/app/15289640

How to construct a query on Twitter:
- the API is the same as the search bar on the site
- see: https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators.html


## NOTES
### up next
- make an interactive front end in django that provides a UI for all the twitter/analysis functions

## Local Setup
These instructions are designed for my own machine.

### Twitter - Auth Keys
Recommended to keep a local file around called `auth` somewhere in the project.
Twitter API requires you to pass in authentication keys (4 values in total).
Don't commit this file, just keep it locally under a .gitignore.

### Virtual Environment
Setup a virtual environment in python3:
`virtualenv -p python3 venv`

Activate virtual environment: 
`source ./venv/bin/activate`

Deactivate virtual environment:
`deactivate`

List currently installed packages:
`./venv/bin/pip list`

Install a package:
`./venv/bin/pip install <package>`

Point PyCharm to the virtualenv:

- point it to /path-to-stupefaction-project/venv/bin/python

### Requirements
Install in your virtualenv
- `pip install -r requirements.txt`

To save your requirements:
- `pip freeze > requirements.txt`

### MySQL setup
(NOTE: I don't actually think I'll need MySQL for this, but here are instructions anyway)

Install MySQL on your machine.

I'm on Ubuntu 16.04, and using MySQL 5.7. If installation is failing, look at:
https://www.digitalocean.com/community/questions/mysql-installation-error-dpkg-error-processing-package-mysql-server-5-5-configure

On my local, I just use a user of `root` and a password of `root`.

Start / stop mysql server:
`service mysql start`
`service mysql stop`

Connect to MySQL from command line:
`mysql -u root -p`

Create database named `stupefaction`:
`create database stupefaction;`


### Getting started with Django
Tutorial I'm following:
https://docs.djangoproject.com/en/2.0/intro/tutorial01/

The repo has a single "project" (which is sort of like a "website").

Inside a project, you have one or more "apps".

The project also has a `manage.py` script, which is sort of like a command line tool.

For example, you can use the script to start the webserver, by doing:
`python manage.py runserver`

To start a project, do:
`django-admin startproject project`

To create an application:
`python manage.py startapp tweety`

which will create a directory called "tweety", representing an "app".

### Connect Django to MySQL
By default, Django seems to use Sqlite. We are going to change this to MySQL.

Go to `/project/project/settings.py`, and add / replace the following:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
        }
    }
}
```

This will tell the project to use a MySQL database, and it will get its config from `/etc/mysql/my.cnf`.
In `/etc/mysql/my.cnf`, add the following:
```
[client]
database = db_name
user = db_user
password = db_password
default-character-set = utf8
``` 
where as noted earlier,
our database name is `stupefaction`, we can use the `root` user, and our root pw is just `root`.


### Django Models
https://docs.djangoproject.com/en/2.0/intro/tutorial02/

A model describes how your data will be structured in your database.

There are 3 steps to updating models:
1. Change your models in models.py
2. Run `python manage.py makemigrations` to create a migration.
3. Run `python manage.py migrate` to apply the migrations.

### Django Admin
https://docs.djangoproject.com/en/2.0/intro/tutorial02/

Create a superuser:  
`python manage.py superuser`

then, create a user, pass, etc.

To access the admin route, go to `localhost:8000/admin`

In order to add your models to the admin page, you have to add it to `admin.py`.

For example,
```
from .models import Question
admin.site.register(Question)
```

### Adding Views
https://docs.djangoproject.com/en/2.0/intro/tutorial03/

Need to add code to both `views.py` and `urls.py`

For example,
```
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
```
```
# ex: /polls/5/
path('<int:question_id>/', views.detail, name='detail')
```

### View Templates
https://docs.djangoproject.com/en/2.0/intro/tutorial03/

Create a directory called `templates/<app_name>`.
Place html files in here, these are the templates that will get used.

Views receive objects from the route handlers in `views.py`.
For example,  
`return render(request, 'tweety/detail.html', {'question': question})`  
will send the `question` object to the `tweety/detail.html` view.  

In the `tweety/detail.html` view, you can access fields by:  
`{{ question.question_text }}`  

and you can do things like iteration, etc. by:  
`{% for choice in question.choice_set.all %}`
