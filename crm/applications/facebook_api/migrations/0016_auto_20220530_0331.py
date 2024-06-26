# Generated by Django 3.2.2 on 2022-05-30 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_api', '0015_auto_20220530_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='credential',
            name='facebook_id',
            field=models.CharField(blank=True, db_column='Facebook ID', max_length=500),
        ),
        migrations.AlterField(
            model_name='credential',
            name='access_token',
            field=models.CharField(blank=True, db_column='Access Token', max_length=500),
        ),
        migrations.AlterField(
            model_name='credential',
            name='id',
            field=models.AutoField(db_column='Credential ID', primary_key=True, serialize=False),
        ),
    ]
