# Generated by Django 1.11.14 on 2018-09-07 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0030_karixbackend'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirtelTCLBackend',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('sms.sqlsmsbackend',),
        ),
    ]
