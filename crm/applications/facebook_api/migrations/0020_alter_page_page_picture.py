# Generated by Django 3.2.2 on 2022-06-02 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_api', '0019_rename_owner_id_page_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page_picture',
            field=models.CharField(blank=True, max_length=500, verbose_name='Facebook Page Picture'),
        ),
    ]