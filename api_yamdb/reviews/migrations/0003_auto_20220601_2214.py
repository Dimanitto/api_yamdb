# Generated by Django 2.2.16 on 2022-06-01 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_userauth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userauth',
            old_name='user',
            new_name='username',
        ),
    ]