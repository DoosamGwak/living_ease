# Generated by Django 4.2 on 2024-10-15 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("boards", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="boardimage",
            name="noticeboard",
        ),
    ]