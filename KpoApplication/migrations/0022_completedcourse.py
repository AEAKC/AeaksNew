# Generated by Django 4.1.4 on 2022-12-25 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("KpoApplication", "0021_remove_block_first"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompletedCourse",
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
                ("course_done", models.BooleanField(default=False)),
                (
                    "competed_course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="KpoApplication.courses",
                    ),
                ),
                (
                    "user_in_current_course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
