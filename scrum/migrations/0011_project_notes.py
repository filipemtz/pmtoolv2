# Generated by Django 4.0.3 on 2022-12-27 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0010_userguipreferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='notes',
            field=models.TextField(default=''),
        ),
    ]