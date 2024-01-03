# Generated by Django 4.2.4 on 2023-12-27 09:19

import apps.blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.FileField(upload_to='images/article_cover/', validators=[apps.blog.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='category',
            name='cover',
            field=models.FileField(upload_to='images/category_cover/', validators=[apps.blog.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(upload_to='images/user_avatar/', validators=[apps.blog.models.validate_file_extension]),
        ),
    ]