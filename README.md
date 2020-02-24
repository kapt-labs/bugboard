<p align="center">
  <img src="https://i.imgur.com/4W2ZkOo.png" alt="welcome to the bugboard" />
</p>

the bugboard updates and sort [bugherd](https://www.bugherd.com/)'s tasks and comments to improve efficiency

----

### Prerequisites

You will need `python3` (3.7, 3.8...) & `django` (2.2).

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

 * coming soon 🔧

 * step X: configure the `BUGBOARD_USER_LIST` in `settings.py`. The list is there to sort the assigned tasks by user, and the template file will loop over it to add the links in the menu.
   ```
   [
       {
           "id": "enter id of member here",
           "name": "enter name of member here",
           "avatar": "enter url of member here"
       },
       {
           "id": "enter id of member here",
           "name": "enter name of member here",
       },
   ]
  ```  
    *note: if no avatar is set, then the image "default_member.png" will be used*  
    *note2: you can use the following command to get the IDs & avatar urls of your members: `curl -u YOUR_BUGHERD_API_KEY_HERE:x https://www.bugherd.com/api_v2/users/members.json`*

----

### Can I have a screenshot ?
Sure:

![screenshot v0.1](https://i.imgur.com/MUZGVaY.png)

----

*This application was tested using django 2.2, python 3.7.3, and PostGreSQL 10.10 (on Xubuntu 18.04).*
