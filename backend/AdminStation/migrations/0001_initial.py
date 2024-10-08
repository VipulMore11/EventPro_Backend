# Generated by Django 5.0.6 on 2024-08-03 19:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('UserprofileStation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserprofileStation.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserprofileStation.userprofile')),
            ],
            options={
                'db_table': 'AdminStation_admin',
            },
        ),
    ]
