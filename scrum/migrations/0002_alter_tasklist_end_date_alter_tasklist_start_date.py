# Generated by Django 4.0.3 on 2022-04-12 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklist',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
