# Generated by Django 4.2.4 on 2023-12-26 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='name',
            new_name='fullname',
        ),
    ]
