# Generated by Django 4.0.3 on 2022-12-28 16:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0011_project_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=16)),
                ('text_color', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrum.project')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TaskTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrum.tag')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrum.task')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
