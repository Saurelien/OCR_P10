# Generated by Django 4.2.5 on 2023-09-14 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_remove_user_access_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
