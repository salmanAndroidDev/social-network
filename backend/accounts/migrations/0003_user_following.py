# Generated by Django 3.2.5 on 2021-10-21 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='accounts.Contact', to='accounts.User'),
        ),
    ]
