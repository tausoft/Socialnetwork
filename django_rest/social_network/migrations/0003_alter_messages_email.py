# Generated by Django 3.2.9 on 2021-11-07 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0002_remove_messages_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=254, verbose_name='user_auth.User'),
        ),
    ]