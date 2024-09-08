# Generated by Django 4.2.11 on 2024-05-12 11:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('street', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('zip_code', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('citizen_id', models.CharField(default='e802a1b2-eaa7-42c0-93a8-64647e24ce1a', max_length=255, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=255, unique=True)),
                ('nin_number', models.CharField(blank=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.CharField(default='cecd0dcf-e0ff-4f96-a7ae-d470b1bf9d92', max_length=255, primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('citizen_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citizen.citizen')),
            ],
        ),
    ]
