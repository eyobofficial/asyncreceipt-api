# Generated by Django 3.1.7 on 2021-03-20 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0004_auto_20210320_0719'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='receipt_file',
            new_name='pdf',
        ),
    ]
