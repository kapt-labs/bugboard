<p align="center">
  <img src="https://i.imgur.com/4W2ZkOo.png" alt="welcome to the bugboard" />
</p>

the bugboard updates and sort [bugherd](https://www.bugherd.com/)'s tasks and comments to improve efficiency

----

### Prerequisites

You will need `python` 3 & `django`.

Some sensitive data are read using `os.environ('KEY')`, you will need to `export` them in order to successfully launch the bugboard:
 * `BUGHERD_API` : The access key used to get content from bugherd.com/api_v2/
 * `SECRET_KEY` : The django secret key.
 * `DB_USER` : PSQL username.
 * `DB_PASS` : PSQL password.

### Install

Just put the application inside your django project, create one url from your project `urls.py` file, make the migrations, migrate the db, and you're done.

----

### Can I have a screenshot ?
Sure:

![screenshot v0.1](https://i.imgur.com/MUZGVaY.png)

----

*This application was tested using django 2.2, python 3.7.3, and PostGreSQL 10.10 (on Xubuntu 18.04).*
