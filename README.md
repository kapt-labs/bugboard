<p align="center">
  <img src="https://i.imgur.com/4W2ZkOo.png" alt="welcome to the bugboard" />
</p>

the bugboard updates and sort [bugherd](https://www.bugherd.com/)'s tasks and comments to improve efficiency

----

### Prerequisites

You will need `python3.7` & `django`.

Some sensitive data are read using `os.environ('KEY')`, you will need to `export` them in order to successfully launch the bugboard:
 * `BUGHERD_API` : The access key used to get content from bugherd.com/api_v2/
 * `SECRET_KEY` : The django secret key.
 * `DB_USER` : PSQL username.
 * `DB_PASSWORD` : PSQL password.
 * `DB_ENGINE` : `django.db.backends.postgresql_psycopg2` if you're using PSQL
 * `DB_NAME` : PSQL database name (*bugboard seems to be a good name*)
 * `DB_HOST` : Host UNIX entry point
 * `ADMIN_URL` : Custom admin url (default is `admin/`)

### Install

Just put the application inside your django project, create one url from your project `urls.py` file, store all the data in previous section inside your `.env` (if you're using `pipenv`), collect the static files, serve them, make the migrations, migrate the db, and you're done.

----

### Can I have a screenshot ?
Sure:

![screenshot v0.1](https://i.imgur.com/MUZGVaY.png)

----

*This application was tested using django 2.2, python 3.7.3, and PostGreSQL 10.10 (on Xubuntu 18.04).*
