# Generated by Django 4.2 on 2025-01-03 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySql', '0002_alter_usuario_groups_alter_usuario_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='especialidad',
            name='owner_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
