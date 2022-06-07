# Generated by Django 3.2.2 on 2022-06-07 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_api', '0029_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.CharField(blank=True, max_length=500, verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender_id',
            field=models.CharField(blank=True, max_length=500, verbose_name='User Facebook ID'),
        ),
    ]
