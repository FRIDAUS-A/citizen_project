# Generated by Django 4.2.11 on 2024-05-07 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('press', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presspost',
            name='post_id',
            field=models.CharField(default='7e6dd0f1-9c80-4054-9679-c164e73b769a', max_length=255, primary_key=True, serialize=False),
        ),
    ]