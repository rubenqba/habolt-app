# Generated by Django 2.2 on 2019-10-29 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20191029_0358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='status',
        ),
    ]