# Generated by Django 3.2.2 on 2022-06-02 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_api', '0020_alter_page_page_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page_id',
            field=models.BigIntegerField(verbose_name='Facebook Page ID'),
        ),
    ]