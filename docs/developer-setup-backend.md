# PHX - Developer setup - Backend

[&laquo; Back](../README.md)

How to install the app locally.


## Requirements

* Python 3
* PostgreSQL


Once you have cloned this repo, run through the following steps:


## Python

This project has been developed in Python 3.6.5 - to check what version of Python you are running in your console run:

```
python --version
python3 --version
```

Please install Python 3.6.5 if you do not have it. We suggest using [pyenv](https://github.com/pyenv/pyenv) to manage python versions easily.


### Install pyenv using Homebrew

```
brew update
brew install pyenv
```

Add the following to your `.bash_profile` and reload terminal session:

```
eval "$(pyenv init -)"
```


### Install Python 3.6.5 with pyenv

```
pyenv install 3.6.5
```


### Virtualenv

When developing Python apps a virtual environment can be used to keep all your dependencies sandboxed for just this project.

First, install `virtualenv`:

```
pip install virtualenv
```

Create the virtualenv:

```
virtualenv env --python=$HOME/.pyenv/versions/3.6.5/bin/python
```

To activate the virtualenv, run:

```
source env/bin/activate
```


### Dependencies

Python dependencies are installed using `pip`. This project uses `pip-tools` to help manage dependencies.

- Pip tools: https://github.com/jazzband/pip-tools
- See: https://jamescooke.info/a-successful-pip-tools-workflow-for-managing-python-package-requirements.html


#### Installing dependencies

Install pip-tools:

```
pip install pip-tools
```

Install local dependencies, via the local.txt requirements file (this includes base and test requirements):

```
cd requirements && pip-sync local.txt
```

#### Adding a new dependency

Add dependency to corresponding `.in` in the requirements directory file and then run:

```
cd requirements && make all
```

Then run `pip-sync` again:

```
pip-sync local.txt
```

#### Updating a dependency

Remove the dependency from the relevant `.txt` file(s) and re-run `make all`.

If it doesn't work as expected, remove from the `.in` file, run `pip-sync` to update the `.txt` files, then re-add and re-run again.


### Social media accounts

The site can post news articles and results to Twitter and Facebook. To do this, accounts/apps need to be set up for both social networks. The relevant access details for these accounts should then be added into the config files.


#### Twitter

* [Register a new app](https://developer.twitter.com/) with the relevant twitter account - take a note of the four different keys listed below, and make sure the app has read and write access. (Give it read and write access before creating your access tokens so they share this access, to check see [here](https://twitter.com/settings/applications))


#### Facebook

To post to Facebook, set up an [If This Then That account](https://ifttt.com/) to automatically post to a Facebook page when a new message is posted to Twitter.


### Cron

The site uses [Django-extensions](https://django-extensions.readthedocs.io/en/latest/jobs_scheduling.html) Job Scheduling to periodically post new content to the social media accounts above.

In order to set this up, the following `crontab` should be set up on the server:

```
# https://crontab.tech/every-hour
0 * * * * ./phx-social-cron.sh
```

Create a file in the root: `nano ~/phx-social-cron.sh`

```
cd phx
source env/bin/activate
cd phx
python manage.py runjobs hourly --settings=phx.settings.production >> /home/phx/crons.log
```

Ensure this file is executable:

```
chmod -x phx-social-cron.sh
```


## CI

A config for Circle CI has been set up to run linting and testing on every push to Github


## PostGres

This project requires PostgreSQL 9.4+ to support some features.

The easiest way to install PostgresSQL on macOS is to use [Postgresapp](http://postgresapp.com/). Make sure you download the version running Postgres 9.4 and follow installation instructions on the Posgresapp site.

You can either run `psql` from a terminal, or select 'open psql' from the menu if you click on the icon in the macOS menu bar

Once you have opened `psql`, create a database for the project:

```
CREATE DATABASE phxdb;
CREATE USER phxuser WITH PASSWORD 'phxpw';
GRANT ALL PRIVILEGES ON DATABASE phxdb TO phxuser;
```

A few other useful psql commands...

To list databases:

```
\l
```

To select a database:

```
\c [database name]
```

List tables:

```
\d
\dt
```

Note: To quit the psql shell use `\q`
