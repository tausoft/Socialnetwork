# Generated by Django 3.2.9 on 2021-11-07 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0003_alter_messages_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='email',
            field=models.EmailField(max_length=150),
        ),
    ]
