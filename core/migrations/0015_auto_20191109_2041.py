# Generated by Django 2.2 on 2019-11-09 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_leads'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leads',
            old_name='extra1',
            new_name='fecha',
        ),
        migrations.RenameField(
            model_name='leads',
            old_name='extra2',
            new_name='hora',
        ),
    ]