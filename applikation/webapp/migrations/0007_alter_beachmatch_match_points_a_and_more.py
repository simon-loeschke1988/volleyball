# Generated by Django 4.2.6 on 2024-01-11 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_alter_beachmatch_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beachmatch',
            name='match_points_a',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='beachmatch',
            name='match_points_b',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='beachmatch',
            name='points_team_a_set1',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='beachmatch',
            name='points_team_a_set2',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='beachmatch',
            name='points_team_a_set3',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='beachmatch',
            name='points_team_b_set1',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='beachmatch',
            name='points_team_b_set2',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='beachmatch',
            name='points_team_b_set3',
            field=models.CharField(blank=True, null=True),
        ),
    ]
