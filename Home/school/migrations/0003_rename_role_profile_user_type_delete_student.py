# Generated by Django 5.2.3 on 2025-06-16 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='role',
            new_name='user_type',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
