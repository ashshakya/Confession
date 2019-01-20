# Generated by Django 2.0.6 on 2019-01-20 17:37

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20190120_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='profiles'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='bio',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='intro',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
