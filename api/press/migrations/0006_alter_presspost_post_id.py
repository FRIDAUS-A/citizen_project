# Generated by Django 4.2.11 on 2024-05-07 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('press', '0005_alter_presspost_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presspost',
            name='post_id',
            field=models.CharField(default='3ccd912f-da94-4353-894b-c7f96d0cb37a', max_length=255, primary_key=True, serialize=False),
        ),
    ]
