# Generated by Django 3.2.2 on 2022-05-26 20:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_api', '0002_remove_credential_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 26, 20, 54, 6, 51053, tzinfo=utc)),
        ),
    ]
