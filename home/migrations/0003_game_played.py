# Generated by Django 5.0.4 on 2024-05-07 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='played',
            field=models.BooleanField(default=False),
        ),
    ]