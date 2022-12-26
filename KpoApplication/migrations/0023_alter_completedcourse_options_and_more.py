# Generated by Django 4.1.4 on 2022-12-25 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("KpoApplication", "0022_completedcourse"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="completedcourse",
            options={
                "verbose_name": "Законченый курс",
                "verbose_name_plural": "Законченные курсы",
            },
        ),
        migrations.RemoveField(
            model_name="completedcourse",
            name="competed_course",
        ),
        migrations.AddField(
            model_name="completedcourse",
            name="current_course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="KpoApplication.courses",
                verbose_name="Текущий курс",
            ),
        ),
        migrations.AlterField(
            model_name="completedcourse",
            name="course_done",
            field=models.BooleanField(default=False, verbose_name="Курс пройден"),
        ),
        migrations.AlterField(
            model_name="completedcourse",
            name="user_in_current_course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
