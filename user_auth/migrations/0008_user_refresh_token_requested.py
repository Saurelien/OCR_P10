# Generated by Django 4.2.5 on 2023-09-14 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0007_user_access_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='refresh_token_requested',
            field=models.BooleanField(default=False),
        ),
    ]