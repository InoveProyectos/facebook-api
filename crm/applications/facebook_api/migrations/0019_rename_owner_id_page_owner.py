# Generated by Django 3.2.2 on 2022-06-02 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_api', '0018_auto_20220602_1258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='owner_id',
            new_name='owner',
        ),
    ]
