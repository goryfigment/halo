from django.db import models
import time


def get_utc_epoch_time():
    return int(round(time.time()))


# class Season1(models.Model):
#     playtime = models.CharField(max_length=255)
#     kills = models.IntegerField(default=0)
#     deaths = models.IntegerField(default=0)
#     wins = models.IntegerField(default=0)
#     losses = models.IntegerField(default=0)
#     matches = models.IntegerField(default=0)
#     wl = models.FloatField(default=0)
#     kd = models.FloatField(default=0)
#     epoch = models.IntegerField(default=0)
#
#     class Meta:
#         db_table = "season1"


class Player(models.Model):
    # season1 = models.ForeignKey(Season1, default=None)

    gamertag = models.CharField(unique=True, max_length=20)
    playtime = models.CharField(max_length=255)
    emblem = models.CharField(max_length=255)
    matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    highest_skill = models.IntegerField(default=1)
    kd = models.FloatField(default=0)
    wl = models.FloatField(default=0)
    epoch = models.IntegerField(default=0)

    hits = models.IntegerField(default=1)
    last_updated = models.IntegerField(default=get_utc_epoch_time, blank=True)
    twitch = models.CharField(max_length=255, default='')
    youtube = models.CharField(max_length=255, default='')
    twitter = models.CharField(max_length=255, default='')
    social = models.CharField(max_length=255, default='')
    donation = models.IntegerField(default=0)
    notes = models.CharField(max_length=255, default='')
    color = models.CharField(max_length=255, default='')
    ban = models.BooleanField(default=False)

    class Meta:
        db_table = "player"


class PcRanks(models.Model):
    player = models.ForeignKey(Player, default=None)
    halo_reach_team_hardcore = models.IntegerField(default=0)
    halo_reach_invasion = models.IntegerField(default=0)
    halo_reach_team_slayer = models.IntegerField(default=0)

    class Meta:
        db_table = "pc_ranks"


class Ranks(models.Model):
    player = models.ForeignKey(Player, default=None)
    pc_ranks = models.ForeignKey(PcRanks, default=None)
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


class Leaderboard(models.Model):
    player = models.ForeignKey(Player, default=None)

    most_50s = models.IntegerField(default=0)
    playtime = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    wl = models.IntegerField(default=0)
    kd = models.IntegerField(default=0)

    h3_team_slayer = models.IntegerField(default=0)
    h3_team_hardcore = models.IntegerField(default=0)
    ms_2v2_series = models.IntegerField(default=0)
    h3_team_doubles = models.IntegerField(default=0)
    h2c_team_hardcore = models.IntegerField(default=0)
    hce_team_doubles = models.IntegerField(default=0)
    halo_reach_team_hardcore = models.IntegerField(default=0)
    halo_reach_invasion = models.IntegerField(default=0)
    halo_reach_team_slayer = models.IntegerField(default=0)
    pc_halo_reach_team_hardcore = models.IntegerField(default=0)
    pc_halo_reach_invasion = models.IntegerField(default=0)
    pc_halo_reach_team_slayer = models.IntegerField(default=0)

    class Meta:
        db_table = "leaderboard"

# class Trophy(models.Model):
#     player = models.ForeignKey(Player, default=None)
#     worlds_1st_ffa = models.ForeignKey(Player, default=None)
#     twitch = ''
#
#     class Meta:
#         db_table = "trophy"
