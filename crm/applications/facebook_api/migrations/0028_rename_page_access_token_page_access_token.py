# Generated by Django 3.2.2 on 2022-06-07 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_api', '0027_response'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='page_access_token',
            new_name='access_token',
        ),
    ]