# Generated by Django 3.2.2 on 2022-06-02 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_api', '0024_page_post_respondidos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='post_respondidos',
            new_name='posts_respondidos',
        ),
    ]