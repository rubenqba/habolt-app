# Generated by Django 2.2 on 2019-12-02 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20191202_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]