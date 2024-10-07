# Generated by Django 4.2 on 2024-10-04 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PetCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PetCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "PCID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="petcodes",
                        to="pets.petcategory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("1", "사용자"), ("2", "반려동물")], max_length=1
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PetWikiImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="pets/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "PID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="pet_images",
                        to="pets.petcode",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Choice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content_type",
                    models.CharField(
                        choices=[
                            ("1", "TEXT"),
                            ("2", "RANGE"),
                            ("3", "RADIO"),
                            ("4", "CHECK"),
                        ],
                        max_length=1,
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "QID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="choices",
                        to="pets.question",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "QID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="q_answers",
                        to="pets.question",
                    ),
                ),
                (
                    "UID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="u_answers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AIHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.TextField()),
                ("answer", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "UID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="aihistorys",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
