# Generated by Django 4.2.16 on 2024-12-04 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('mySql', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='usuarios_set', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='usuarios_permissions_set', to='auth.permission'),
        ),
    ]
