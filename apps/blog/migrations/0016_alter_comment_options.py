# Generated by Django 4.2.4 on 2023-12-30 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
    ]
