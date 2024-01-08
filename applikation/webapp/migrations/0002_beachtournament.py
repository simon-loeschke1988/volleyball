# Generated by Django 4.2.6 on 2024-01-08 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeachTournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('federation_code', models.CharField(blank=True, max_length=10, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('version', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'BeachTournaments',
                'ordering': ['code'],
            },
        ),
    ]
