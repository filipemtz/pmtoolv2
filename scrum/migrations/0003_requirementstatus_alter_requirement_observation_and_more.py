# Generated by Django 4.0.3 on 2022-04-05 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0002_alter_requirement_options_alter_requirement_priority_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequirementStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='requirement',
            name='observation',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='workload',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scrum.requirementworkload'),
        ),
        migrations.AddField(
            model_name='requirement',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scrum.requirementstatus'),
        ),
    ]