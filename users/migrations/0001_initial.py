# Generated by Django 4.1.13 on 2023-11-18 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_from', models.DateTimeField()),
                ('date_to', models.DateTimeField()),
                ('active_account', models.BooleanField(default=True)),
                ('password', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]