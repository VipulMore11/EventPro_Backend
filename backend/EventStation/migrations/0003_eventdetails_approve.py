# Generated by Django 5.0.6 on 2024-08-09 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventStation', '0002_approvals'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdetails',
            name='approve',
            field=models.BooleanField(default=False),
        ),
    ]
