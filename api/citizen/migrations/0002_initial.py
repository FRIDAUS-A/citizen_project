# Generated by Django 4.2.11 on 2024-05-12 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('citizen', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('press', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='press.presspost'),
        ),
        migrations.AddField(
            model_name='citizen',
            name='address_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='citizen.address'),
        ),
        migrations.AddField(
            model_name='citizen',
            name='groups',
            field=models.ManyToManyField(related_name='citizen_groups', to='auth.group'),
        ),
        migrations.AddField(
            model_name='citizen',
            name='user_permissions',
            field=models.ManyToManyField(related_name='citizen_user_permissions', to='auth.permission'),
        ),
    ]
