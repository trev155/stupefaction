# stupefaction
Purpose is to learn about how to scrape data from twitter API and then do some NLP on it.

Good Tutorial to get started on Twitter / Twitter API:
http://socialmedia-class.org/twittertutorial.html

Twitter Application account:
https://apps.twitter.com/app/15289640

## NOTES
- I probably don't even need to use a backend DB. What would I even store in it? I don't even know yet, haha.
I'll just leave it there for now I guess.

### brainstorming ideas
- classifying a tweet based on gender, age (with nltk or scikit fns)
- classifying a tweet based on PoS tags (spacy), or other features extracted from spacy
- sentiment analysis - classifying a tweet based on sentiment (use vader to get sentiment for training data? no idea how to do this)

train a model, scikit - persist a model

## Local Setup
This is a hobbyist project so yeah, everything is going to be done locally on my own machine.
These notes are mostly for myself.

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

### Requirements so far
Main packages to install (make sure to do it your virtualenv):
- tweepy
- spaCy
- nltk
- django
- mysqlclient

For spacy, have to download languages:
`python -m spacy download en`

### MySQL setup
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

### Django web app - views, routes, etc.


