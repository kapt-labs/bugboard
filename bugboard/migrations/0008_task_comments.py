# Generated by Django 2.2.6 on 2019-10-16 11:06

# Third party
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("bugboard", "0007_comment")]

    operations = [
        migrations.AddField(
            model_name="task",
            name="comments",
            field=models.ManyToManyField(to="bugboard.Comment"),
        )
    ]
