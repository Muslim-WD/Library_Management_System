# Generated by Django 5.1.6 on 2025-03-10 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_remove_book_available_borrowedbook_returned_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowedbook',
            name='returned_at',
        ),
    ]
