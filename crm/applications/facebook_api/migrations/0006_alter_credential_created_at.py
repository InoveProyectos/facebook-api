# Generated by Django 3.2.2 on 2022-05-27 04:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_api', '0005_alter_credential_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 27, 4, 38, 28, 223210, tzinfo=utc)),
        ),
    ]
