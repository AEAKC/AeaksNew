# Generated by Django 4.1.4 on 2022-12-25 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("KpoApplication", "0014_rename_block_exercise_blocks_block_ex"),
    ]

    operations = [
        migrations.RenameField(
            model_name="exercise",
            old_name="blocks",
            new_name="block",
        ),
        migrations.RemoveField(
            model_name="block",
            name="ex",
        ),
    ]
