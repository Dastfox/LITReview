# Generated by Django 3.1.4 on 2023-03-15 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20230315_1729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='body',
            new_name='r_description',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='title',
            new_name='r_title',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='description',
            new_name='t_description',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='title',
            new_name='t_title',
        ),
    ]