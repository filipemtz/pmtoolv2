# Generated by Django 4.0.3 on 2022-04-07 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0004_task_taskstatusupdatehistory_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaskWorkEstimate',
            new_name='TaskWorkload',
        ),
    ]
