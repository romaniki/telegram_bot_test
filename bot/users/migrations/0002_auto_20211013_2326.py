# Generated by Django 3.2.8 on 2021-10-13 23:26

from django.db import migrations
import multiselectfield.db.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='answer',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Вариант №1'), (2, 'Вариант №2'), (3, 'Вариант №3')], max_length=3),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
