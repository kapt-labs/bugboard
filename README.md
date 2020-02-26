<p align="center">
  <img src="https://i.imgur.com/4W2ZkOo.png" alt="welcome to the bugboard" />
</p>

the bugboard updates and sort [bugherd](https://www.bugherd.com/)'s tasks and comments to improve efficiency

----

### Prerequisites

This application uses `python3`, `django2` & `postgresql` (*psycopg2*).

### Install

1. Clone this repo.

2. Install required packages:
   ```
   pipenv install
   ```

3. Create a psql database for this project.

4. Create a `.env` file with the following content:

   ```
   export DJANGO_SETTINGS_MODULE=website.settings
   export BUGHERD_API=put your bugherd secret key here
   export SECRET_KEY='put your django secret key here'

   # database config
   export DB_ENGINE=django.db.backends.postgresql_psycopg2
   export DB_NAME='your db name'
   export DB_USER='username'
   export DB_PASSWORD='password'
   export DB_HOST='your psql endpoint'

   export STATIC_URL='your static url, /static/ for local dev'

   export DOMAIN_NAME='your domain name, 127.0.0.1 for local dev'

   # let it empty if you don't use sentry
   export SENTRY_DSN=''
   ```

5. Edit the file `bugboard_users.json`:
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
   * The list is here to sort the assigned tasks by user, and the template file will loop over it to add the links in the menu.

   * If no avatar is set, then the image "default_member.png" will be used
   * You can use the following command to get the IDs & avatar urls of your members:
      ```
      curl -u YOUR_BUGHERD_API_KEY_HERE:x https://www.bugherd.com/api_v2/users/members.json
      ```

----

## Features

* See only unnassigned tasks in a list (order by most oldest/newest task).
* See last commented tasks (**very** useful if the task is in *Done* category and you don't check it every day).
* See all more recent tasks (order by most oldest/newest task).
* See *assigned to me* tasks (using `bugboard_users.json` file).
* See *all* tasks that are nor closed (order by most oldest/newest task).

----

## Commands

Make a simple `manage.py ubdatebbdb --all` to get the latest version of your tasks, members, assignees & comments.

More commands (& informations on what they do) are available in [the wiki](https://github.com/kapt-labs/bugboard/wiki/Update-scripts).

----

### Can I have a screenshot or two ?

* Sure, here is the web interface:
   ![screenshot web interface](https://i.imgur.com/GSpMlhT.png)

* And here the `updatebbdb` command line output:
   ![screenshot updatebbdb](https://i.imgur.com/GiRZbLx.png)
