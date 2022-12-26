# Generated by Django 4.1.4 on 2022-12-22 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("KpoApplication", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Courses",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("text", models.TextField(max_length=1000)),
                (
                    "difficulty",
                    models.CharField(
                        choices=[
                            ("EASY", "Нет аккаунта на сайте"),
                            ("MEDIUM", "Не оформил триал"),
                            ("HARD", "Триал оформлен"),
                        ],
                        default=None,
                        max_length=255,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="exercise",
            name="course",
            field=models.ForeignKey(
                default=None, on_delete=django.db.models.deletion.CASCADE, to="KpoApplication.courses"
            ),
        ),
    ]
