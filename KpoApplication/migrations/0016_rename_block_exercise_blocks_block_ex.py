# Generated by Django 4.1.4 on 2022-12-25 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("KpoApplication", "0015_rename_blocks_exercise_block_remove_block_ex"),
    ]

    operations = [
        migrations.RenameField(
            model_name="exercise",
            old_name="block",
            new_name="blocks",
        ),
        migrations.AddField(
            model_name="block",
            name="ex",
            field=models.ManyToManyField(to="KpoApplication.block"),
        ),
    ]