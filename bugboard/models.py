# Third party
from django.db import models


class Member(models.Model):
    """Member structure that allow storing data returned by BugHerd api.

    Arguments:
        models {django.db.models.Model} -- Default django model.
    """

    id_member = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=254, null=True)
    display_name = models.CharField(max_length=255)
    avatar_url = models.URLField(
        max_length=255, default="https://i.imgur.com/1c85UxD.png"
    )
    member = models.BooleanField()

    def __str__(self):
        return self.email


class Project(models.Model):
    """Project structure that allow storing data returned by BugHerd api.

    Arguments:
        models {django.db.models.Model} -- Default django model.
    """

    id_project = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    devurl = models.URLField(max_length=255, null=True)
    api_key = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(null=True)


class Task(models.Model):
    """Task structure that allow storing data returned by BugHerd api.

    Arguments:
        models {django.db.models.Model} -- Default django model.
    """

    id_task = models.IntegerField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    local_task_id = models.IntegerField(null=True)
    priority_id = models.IntegerField(null=True)
    priority = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True)
    external_id = models.IntegerField(null=True)
    requester_id = models.IntegerField(null=True)
    requester_email = models.EmailField(max_length=254, null=True)
    due_at = models.DateTimeField(null=True)
    admin_link = models.URLField(max_length=70, default="#", null=True)
    assignee = models.ManyToManyField("Member")
    tag = models.ManyToManyField("Tag")
    comment = models.ManyToManyField("Comment")


class Tag(models.Model):
    """Tag structure that allow storing data returned by BugHerd api.

    Arguments:
        models {django.db.models.Model} -- Default django model.
    """

    name = models.CharField(max_length=255)


class Comment(models.Model):
    """Comments structure that allow storing data returned by BugHerd api.

    Arguments:
        models {django.db.models.Model} -- Default django model.
    """

    id_comment = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    text = models.TextField(null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
