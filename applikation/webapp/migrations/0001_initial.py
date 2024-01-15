# Generated by Django 4.2.6 on 2024-01-15 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BeachRound',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('bracket', models.CharField(max_length=10)),
                ('phase', models.CharField(max_length=10)),
                ('start_date', models.CharField()),
                ('end_date', models.CharField()),
                ('number', models.IntegerField(blank=True, null=True)),
                ('version', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BeachTournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.CharField(blank=True, null=True)),
                ('federation_code', models.CharField(blank=True, max_length=10, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('version', models.IntegerField(blank=True, null=True)),
                ('no', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'BeachTournaments',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('no', models.CharField(blank=True, max_length=100, null=True)),
                ('version', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Events',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('federation_code', models.CharField(max_length=5)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.IntegerField(choices=[(0, 'Male'), (1, 'Female'), (3, 'Other')])),
                ('plays_beach', models.BooleanField()),
                ('plays_volley', models.BooleanField()),
                ('team_name', models.CharField(max_length=100)),
                ('no', models.IntegerField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Players',
            },
        ),
        migrations.CreateModel(
            name='BeachTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('earned_points_team', models.PositiveIntegerField(blank=True, null=True)),
                ('earnings_team', models.PositiveIntegerField(blank=True, null=True)),
                ('no', models.PositiveIntegerField(unique=True)),
                ('version', models.PositiveIntegerField(blank=True, null=True)),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_as_player1', to='webapp.player')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_as_player2', to='webapp.player')),
            ],
            options={
                'verbose_name_plural': 'BeachTeams',
                'ordering': ['no'],
                'unique_together': {('player1', 'player2', 'name')},
            },
        ),
        migrations.CreateModel(
            name='BeachMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_in_tournament', models.IntegerField(blank=True, null=True)),
                ('local_date', models.CharField(blank=True, null=True)),
                ('local_time', models.CharField(blank=True, null=True)),
                ('court', models.CharField(blank=True, max_length=10, null=True)),
                ('match_points_a', models.CharField(blank=True, null=True)),
                ('match_points_b', models.CharField(blank=True, null=True)),
                ('points_team_a_set1', models.CharField(blank=True, null=True)),
                ('points_team_b_set1', models.CharField(blank=True, null=True)),
                ('points_team_a_set2', models.CharField(blank=True, null=True)),
                ('points_team_b_set2', models.CharField(blank=True, null=True)),
                ('points_team_a_set3', models.CharField(blank=True, null=True)),
                ('points_team_b_set3', models.CharField(blank=True, null=True)),
                ('duration_set1', models.CharField(blank=True, null=True)),
                ('duration_set2', models.CharField(blank=True, null=True)),
                ('duration_set3', models.CharField(blank=True, null=True)),
                ('no_round', models.CharField(blank=True, max_length=100, null=True)),
                ('no_tournament', models.CharField(blank=True, null=True)),
                ('no_player_a1', models.CharField(blank=True, max_length=100, null=True)),
                ('no_player_a2', models.CharField(blank=True, max_length=100, null=True)),
                ('no_player_b1', models.CharField(blank=True, max_length=100, null=True)),
                ('no_player_b2', models.CharField(blank=True, max_length=100, null=True)),
                ('team_a', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='team_a_matches', to='webapp.beachteam')),
                ('team_b', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='team_b_matches', to='webapp.beachteam')),
            ],
            options={
                'verbose_name_plural': 'Matches',
                'ordering': ['id'],
            },
        ),
    ]
