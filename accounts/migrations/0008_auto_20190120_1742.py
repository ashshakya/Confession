# Generated by Django 2.0.6 on 2019-01-20 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20190120_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(blank=True, default='/profiles/python.png', upload_to='profiles'),
        ),
    ]
