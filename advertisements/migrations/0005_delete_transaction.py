# Generated by Django 3.2 on 2023-03-16 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0004_transaction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
