# Standard Library
import datetime
import os
import time

# Third party
from bugboard.models import Comment, Member, Project, Tag, Task
from django.core.management.base import BaseCommand
import pytz
import requests


class Command(BaseCommand):
    """Add a new command in django admin command line utility. New command is the name of the file (updatebbdb, for "Update BugBoard DataBase").

    Arguments:
        BaseCommand {django.code.management.base.BaseCommand} -- Default command-handling class.

    Variables:
        help = Help string displayed when asking help with "python3 manage.py updateddbd --help."
        api_base = BugHerd api url.
        api_key = Api key loaded from /path/to/project/.env
        time_sleep = Time waited after every api request, to ensure all requests will work (thanks 60-requests-per-minute-limit!).
        projects_id_list = List populated inside update_project() and used in update_tasks() for retrieving ids of projects.
        task_tag_list = List populated inside update_project() and used in update_tag().
        task_assignee_list = List populated inside update_project() and used in update_assignee().

    Raises:
        EnvironmentError: Error raised if no api key is found in /path/to/project/.env file.
    """

    help = 'UpdateBBDB - Update BugBoard DataBase database with data from Bugherd api. Red dot during update is a "too much request" error.'
    api_base = "https://www.bugherd.com/api_v2/"
    api_key = ""
    time_sleep = 1.35
    projects_id_list = []
    task_tag_list = []
    task_assignee_list = []

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            action="store_true",
            help="Update all tasks (get admin urls, last update infos...).",
        )
        parser.add_argument(
            "-c", action="store_true",
            help="Update comments list for each stored task."
        )
        parser.add_argument(
            "--all", action="store_true",
            help="Launch all the updates provided by the other commands one after one."
        )

    def handle(self, *args, **options):
        """Default function that will be launched when calling the custom command. Will retrieve the api_key from /path/to/project/.env, call update_db(), and display some stats using django color codes.

        Raises:
            EnvironmentError: Error raised if no api key is found in /path/to/project/.env file.
        """
        self.api_key = os.environ.get("BUGHERD_API")
        # api key is not set in project/.env
        if not self.api_key:
            raise EnvironmentError(
                'You don\'t have any api key set in your environment variable.\nPlease add "BUGHERD_API=yourapikey" to your .env file.'
            )

        self.stdout.write(self.style.SUCCESS("Found api key."))

        if options["all"]:
            self.update_db(False)
            self.update_local_tasks()
            self.update_local_comments()
        elif options["t"]:
            self.update_local_tasks()
        elif options["c"]:
            self.update_local_comments()
        else:
            self.update_db()

    def update_db(self, update_tags=True):
        """Main function for creating local db, used later to update task list.
        """
        # collect stats
        users_before = Member.objects.all().count()
        projects_before = Project.objects.all().count()
        tasks_before = Task.objects.all().count()
        tags_before = Tag.objects.all().count()
        self.stdout.write("Launching update from bugboard project list...")

        self.update_users()
        self.update_projects()
        self.update_tasks()
        if update_tags:
            self.update_tags()
        self.update_assignees()

        # collect stats
        added_users = Member.objects.all().count() - users_before
        added_projects = Project.objects.all().count() - projects_before
        added_tasks = Task.objects.all().count() - tasks_before
        added_tags = Tag.objects.all().count() - tags_before

        # display stats
        self.stdout.write(self.style.SUCCESS("✅ local db updated."))
        self.stdout.write(
            self.style.SUCCESS(
                "   ➡ "
                + str(added_users)
                + " new "
                + self.pluralize(added_users, "member")
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "   ➡ "
                + str(added_projects)
                + " new "
                + self.pluralize(added_projects, "project")
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "   ➡ "
                + str(added_tasks)
                + " new "
                + self.pluralize(added_tasks, "task")
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "   ➡ " + str(added_tags) + " new " + self.pluralize(added_tags, "tag")
            )
        )

    def update_users(self):
        """Get json with users list, and call update_user().
        """
        page = 1

        # thx http://sametmax.com/alternative-au-do-while-en-python/ for the concept
        while "There is more content to download.":
            data = self.get_data(self.api_base + "users/members.json?page=" + str(page))

            for u in data["users"]:
                self.update_user(u)

            # here's the magic part: if there is no more content to load, exit the while loop
            if (data["meta"]["count"] / 100) < page:
                self.stdout.write(self.style.SUCCESS("\n✅ updated users/members.json"))
                break
            else:
                page += 1

    def update_user(self, user):
        """Create a Member object, and save its content in db.

        Arguments:
            user {dict} -- Dict with user data.
        """
        # update avatar from non-displayable svg to png
        if (
            user["avatar_url"]
            == "https://www.bugherd.com/images/sidebar/avatar-generic.svg"
        ):
            user["avatar_url"] = "https://i.imgur.com/1c85UxD.png"

        user = Member(
            id_member=user["id"],
            email=user["email"],
            display_name=user["display_name"],
            avatar_url=user["avatar_url"],
            member=user.get("member", True),
        )
        user.save()
        self.display_new_action()

    def update_guest(self, user):
        """Define user['member'] to False and call update_user().

        Arguments:
            user {dict} -- Dict with user data.
        """
        user["member"] = False
        self.update_user(user)

    def update_projects(self):
        """Iterate through active projects pages and get projects lists. Call update_project_details() for each active project found inside the list.
        """
        page = 1

        # thx http://sametmax.com/alternative-au-do-while-en-python/ for the concept
        while "There is more content to download.":
            data = self.get_data(
                self.api_base + "projects/active.json?page=" + str(page)
            )

            for p in data["projects"]:
                self.update_project_details(p)
                self.projects_id_list.append(p["id"])

            if (data["meta"]["count"] / 100) < page:
                self.stdout.write(self.style.SUCCESS("\n✅ updated projects.json"))
                break
            else:
                page += 1

    def update_project_details(self, project):
        """Get project content, create a Project object, and save it in db.

        Arguments:
            project {integer} -- Id of project.
        """
        p = self.get_data(self.api_base + "projects/" + str(project["id"]) + ".json")
        p = p["project"]  # initial json is like {project:{all the stuff}}

        project = Project(
            id_project=p["id"],
            name=p["name"],
            devurl=p["devurl"],
            api_key=p["api_key"],
            is_active=p["is_active"],
        )
        project.save()
        self.display_new_action()

        for u in p["guests"]:
            self.update_guest(u)

    def update_tasks(self):
        """Iterate through tasks pages for each project and get json of tasks lists. Call update_task_details() for each task found inside the list.
        """
        id_project = self.projects_id_list.pop()

        while "There is more projects to explore.":

            if not self.projects_id_list:
                break

            page = 1
            while "There is more pages to download.":
                data = self.get_data(
                    self.api_base
                    + "projects/"
                    + str(id_project)
                    + "/tasks.json?page="
                    + str(page)
                )

                for t in data["tasks"]:
                    if t["status_id"] != 5:
                        self.update_task_details(id_project, t)

                if (data["meta"]["count"] / 100) < page:
                    self.stdout.write(
                        self.style.SUCCESS(
                            "\n✅ updated projects/" + str(id_project) + "/tasks.json"
                        )
                    )
                    break
                else:
                    page += 1

            id_project = self.projects_id_list.pop()

    def update_task_details(self, id_project, t):
        """Create a Task object, save it in db, and populate task_tag_list & task_assignee_list.

        Arguments:
            t {dict} -- Dict that contains all task informations.
        """
        # update task
        try:
            task = Task.objects.get(id_task=t["id"])
            task.priority = t.get("priority", task.priority)
            task.priority_id = t["priority_id"]
            task.status_id = t["status_id"]
            task.status = t.get("status", task.status)
            task.admin_link = t.get("admin_link", task.admin_link)

            # only get id of assignees
            ids = [x['id'] for x in t.get("assignees", [])]
            # update assignees list
            self.task_assignee_list.append([t["id"], ids])

        # or create it if it doesn't exist
        except Task.DoesNotExist:
            task = Task(
                id_task=t["id"],
                project=Project.objects.get(id_project=id_project),
                # get correct datetime format from bugherg bugged date, then convert it to "aware" UTC date (and then let postgresql & django store it in 'Europe/Paris' format or whatever they want)
                created_at=pytz.UTC.fromutc(
                    (
                        datetime.datetime.strptime(
                            t["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        )
                    )
                ),
                updated_at=pytz.UTC.fromutc(
                    (
                        datetime.datetime.strptime(
                            t["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        )
                    )
                ),
                local_task_id=t["local_task_id"],
                priority_id=t["priority_id"],
                priority=t.get("priority", t["priority_id"]),
                status_id=t["status_id"],
                status=t.get("status_id", None),
                description=t["description"],
                external_id=t["external_id"],
                requester_id=t["requester_id"],
                requester_email=t["requester_email"],
                admin_link=t.get("admin_link", None),
                due_at=t["due_at"],
            )
            self.task_tag_list.append([t["id"], t["tag_names"]])
            self.task_assignee_list.append([t["id"], t["assignee_ids"]])

        # if updated task is closed or belongs to an inactive project, then delete it
        if task.status == "closed" or task.project.is_active is False:
            task.delete()
        # else save it
        else:
            task.save()

        self.display_new_action()

    def update_tags(self):
        """Iterate through task_tag_list list, create Tag objects & insert them in db.
        """

        while "There is more tags to update.":
            if not self.task_tag_list:
                break

            tag_list = self.task_tag_list.pop()

            for t in tag_list[1]:
                # try to get existing tag
                try:
                    tag = Tag.objects.get(name=t)
                # if it does not exists then create a new tag
                except Tag.DoesNotExist:
                    tag = Tag(name=t)
                    tag.save()
                # and link the tag to the task
                Task.objects.get(id_task=tag_list[0]).tag.add(tag)
                self.display_new_action()

        self.stdout.write(self.style.SUCCESS("\n✅ updated tags from tag list."))

    def update_assignees(self):
        """Iterate through task_assignee_list list, create Assignee objects & insert them in db.
        """
        while "There is more assignees to update.":
            if not self.task_assignee_list:
                break

            assignee_list = self.task_assignee_list.pop()

            for member in assignee_list[1]:
                Task.objects.get(id_task=assignee_list[0]).assignee.add(
                    Member.objects.get(id_member=member)
                )
                self.display_new_action()

        self.stdout.write(
            self.style.SUCCESS("\n✅ updated assignees from assignee list.")
        )

    def update_comments_details(self, task, comments):
        """Iterate through comments list and create/update comments in local db.

        Arguments:
            task {Task} -- Task.
            comments {dict} -- Dict of comments related to the task.
        """
        for c in comments:
            try:
                comment = Comment.objects.get(id_comment=c["id"])
            except Comment.DoesNotExist:

                try:
                    member = Member.objects.get(id_member=c["user_id"])
                # if account no longuer exists (deleted account), create an "anonymous" account for it
                except Member.DoesNotExist:
                    member = Member(
                        id_member=c["user_id"],
                        display_name="Anonymous#" + str(c["user_id"]),
                        member=False,
                    )
                    member.save()

                comment = Comment(
                    id_comment=c["id"],
                    created_at=c["created_at"],
                    text=c["text"],
                    member=member,
                )
                comment.save()
                task.comment.add(comment)
            self.display_new_action()

    def update_local_tasks(self):
        """Update tasks that are stored locally.
        """
        self.stdout.write("Launching update from local tasks...")

        tasks = Task.objects.all()
        for task in tasks:

            updated_task = self.get_data(
                self.api_base
                + "projects/"
                + str(task.project.id_project)
                + "/tasks/"
                + str(task.id_task)
                + ".json"
            )

            self.update_task_details(task.project.id_project, updated_task["task"])

        self.stdout.write(self.style.SUCCESS("\n✅ local db updated."))

    def update_local_comments(self):
        """Update comments relevant to locally-stored tasks.
        """

        self.stdout.write("Launching update for comments from local tasks...")

        tasks = Task.objects.all()
        for task in tasks:

            comments = self.get_data(
                self.api_base
                + "projects/"
                + str(task.project.id_project)
                + "/tasks/"
                + str(task.id_task)
                + "/comments.json"
            )

            self.update_comments_details(task, comments["comments"])

        self.stdout.write(self.style.SUCCESS("\n✅ local db updated."))

    def get_data(self, link):
        """Use requests to get data, sleep during time_sleep time, and return a dict with the data.
        Display a red dot if the data is a "Rate Limit Exceeded" error, wait 2*time_sleep and retry to get the data.

        Arguments:
            link {str} -- Link of the ressource on the internet.

        Returns:
            dict -- Dictionnary of the data returned by the website.
        """
        # try not to get 'Rate Limit Exceeded' error
        time.sleep(self.time_sleep)

        # get data from url
        data = requests.get(link, auth=(self.api_key, "x")).json()

        # if rate limit is exceeded, wait and retry
        while "error" in data:
            print(self.style.ERROR("."), end="", flush="True")
            time.sleep(self.time_sleep * 2)
            data = requests.get(link, auth=(self.api_key, "x")).json()

        return data

    def display_new_action(self):
        """Esthetic feature, will display a dot in the chat each time an update is performed on the db.
        """
        print(".", end="", flush="True")

    def pluralize(self, i, s):
        """Esthetic feature, will return the singular or plural form of a word (simply add a "S" at the end of the word).

        Arguments:
            i {int} -- number of entities
            s {str} -- word to be "pluralized"

        Returns:
            str -- "pluralized" word
        """
        if i > 1:
            return s + "s"
        return s
