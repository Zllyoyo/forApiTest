# Generated by Django 4.0.5 on 2024-07-09 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.IntegerField(choices=[(0, 'Option 0'), (1, 'Option 1')], default=0, unique=True),
        ),
    ]
