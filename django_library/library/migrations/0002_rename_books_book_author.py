# Generated by Django 5.0.6 on 2024-05-14 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='books',
            new_name='author',
        ),
    ]
