# Generated by Django 4.0.3 on 2022-04-13 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0003_task_status_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='observation',
            field=models.TextField(blank=True, default=''),
        ),
    ]
