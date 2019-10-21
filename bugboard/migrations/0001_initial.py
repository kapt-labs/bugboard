# Generated by Django 2.2.6 on 2019-10-09 14:24

# Third party
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Member",
            fields=[
                ("id_member", models.IntegerField(primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=254)),
                ("display_name", models.CharField(max_length=255)),
                ("avatar_url", models.URLField(max_length=255)),
                ("member", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id_project", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("devurl", models.URLField(max_length=255, null=True)),
                ("api_key", models.CharField(max_length=255, null=True)),
                ("is_active", models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id_task", models.IntegerField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField(null=True)),
                ("local_task_id", models.IntegerField(null=True)),
                ("priority_id", models.IntegerField(null=True)),
                ("assigned_to_id", models.IntegerField(null=True)),
                ("status_id", models.IntegerField(null=True)),
                ("description", models.TextField(null=True)),
                ("external_id", models.IntegerField(null=True)),
                ("requester_id", models.IntegerField(null=True)),
                ("requester_email", models.EmailField(max_length=254, null=True)),
                ("due_at", models.DateTimeField(null=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bugboard.Project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bugboard.Task"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Assignee",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_member", models.CharField(default="", max_length=255, null=True)),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bugboard.Task"
                    ),
                ),
            ],
        ),
    ]
