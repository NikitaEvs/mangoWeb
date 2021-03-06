# Generated by Django 3.0.5 on 2020-05-10 17:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=100)),
                ('task_priority', models.IntegerField(blank=True, default=None, null=True)),
                ('duration', models.DurationField(blank=True, default=datetime.timedelta(0), null=True)),
                ('date_start', models.DateTimeField(blank=True, default=None, null=True)),
                ('date_finish', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_running', models.BooleanField(blank=True, default=False, null=True)),
                ('is_complete', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
