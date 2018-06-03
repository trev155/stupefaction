# stupefaction
Purpose is to learn about how to scrape data from twitter API and then do some NLP on it.

Good Tutorial to get started on Twitter / Twitter API:
http://socialmedia-class.org/twittertutorial.html

Twitter Application account:
https://apps.twitter.com/app/15289640

## NOTES
### up next
- output files should contain the query of the twitter api search on the first line, so that readers know what query was used for that file
- more basic analytics

### short term idea
- twitter api (streaming, or regular search)-> get tweets -> save to mysql db
    - query: either automatically fetch some trending hashtag, or just manually enter a query

- get all tweets about some topic, like trump
- compute sentiments (eg. vader) for these tweets
- look at the users / profiles of these tweets, and do a text analysis of these users / user descriptions / etc.
    - what are these people tweeting about in general? etc.

### long term ideas
- make an interactive front end in some framework that pretty much does all of my short term ideas

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

### Requirements
Install in your virtualenv
- `pip install -r requirements.txt`

To save your requirements:
- `pip freeze > requirements.txt`

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
next up...
