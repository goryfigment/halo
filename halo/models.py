from django.db import models
import time


def get_utc_epoch_time():
    return int(round(time.time()))


class Player(models.Model):
    gamertag = models.CharField(unique=True, max_length=20)
    playtime = models.CharField(max_length=255)
    emblem = models.CharField(max_length=255)
    matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)

    hits = models.IntegerField(default=1)
    last_updated = models.IntegerField(default=get_utc_epoch_time, blank=True)

    class Meta:
        db_table = "player"


class Ranks(models.Model):
    player = models.ForeignKey(Player, default=None)
    h3_team_slayer = models.IntegerField(default=0)
    h3_team_hardcore = models.IntegerField(default=0)
    ms_2v2_series = models.IntegerField(default=0)
    h3_team_doubles = models.IntegerField(default=0)
    halo_reach_team_hardcore = models.IntegerField(default=0)
    halo_reach_invasion = models.IntegerField(default=0)
    h2c_team_hardcore = models.IntegerField(default=0)
    hce_team_doubles = models.IntegerField(default=0)
    halo_reach_team_slayer = models.IntegerField(default=0)

    class Meta:
        db_table = "ranks"


# class Trophy(models.Model):
#     player = models.ForeignKey(Player, default=None)
#     worlds_1st_ffa = models.ForeignKey(Player, default=None)
#     twitch = ''
#
#     class Meta:
#         db_table = "trophy"
