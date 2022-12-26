# Generated by Django 4.1.4 on 2022-12-22 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("KpoApplication", "0010_block_number_of_block"),
    ]

    operations = [
        migrations.AddField(
            model_name="block",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="KpoApplication.courses",
                verbose_name="Курс",
            ),
        ),
    ]