# stupefaction
Purpose is to learn about how to scrape data from twitter API.

Twitter Application account:
https://apps.twitter.com/app/15289640

Good Tutorial:
http://socialmedia-class.org/twittertutorial.html


## local setup
setup a virtual environment in python3:

`virtualenv -p python3 venv`

activate virtual environment:

`source ./venv/bin/activate`

deactivate virtual environment:

`deactivate`

list currently installed packages:

`./venv/bin/pip list`

install a package:

`./venv/bin/pip install <package>`

point PyCharm to the virtualenv:

- point it to /path-to-stupefaction-project/venv/bin/python

### Requirements so far
I'll be using:
- tweepy
- spaCy

Make sure to install them in your venv.

For spacy, have to download languages:

`python -m spacy download en`

## Operation
so far my idea is:
- use tweepy to get tweets, write to file
- some other script reads these files, use spacy to analyze