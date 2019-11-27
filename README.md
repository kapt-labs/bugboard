<p align="center">
  <img src="https://i.imgur.com/4W2ZkOo.png" alt="welcome to the bugboard" />
</p>

the bugboard updates and sort [bugherd](https://www.bugherd.com/)'s tasks and comments to improve efficiency

----

### Prerequisites

You will need `python3.7` & `django`.

Some sensitive data are read using `os.environ('KEY')`, you will need to `export` them in order to successfully launch the bugboard:
 * `DJANGO_SETTINGS_MODULE`
 * `PYTHONPATH`
 * `BUGHERD_API`
 * `SECRET_KEY`
 * `DB_ENGINE`
 * `DB_NAME`
 * `DB_USER`
 * `DB_PASSWORD`
 * `DB_HOST`
 * `EMAIL_HOST`
 * `EMAIL_HOST_USER`
 * `EMAIL_HOST_PASSWORD`
 * `STATIC_URL`
 * `DOMAIN_NAME`
 * `ADMIN_URL`
 * `SENTRY_DSN`

### Install

coming soon 🔧

----

### Can I have a screenshot ?
Sure:

![screenshot v0.1](https://i.imgur.com/MUZGVaY.png)

----

*This application was tested using django 2.2, python 3.7.3, and PostGreSQL 10.10 (on Xubuntu 18.04).*
