# Generated by Django 4.2.6 on 2024-01-14 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0015_alter_event_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
