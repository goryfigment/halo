from django.db import models
import time
from django.contrib.auth.models import AbstractBaseUser


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
    highest_skill = models.IntegerField(default=1)
    kd = models.FloatField(default=0)
    wl = models.FloatField(default=0)
    epoch = models.IntegerField(default=0)

    hits = models.IntegerField(default=1)
    last_updated = models.IntegerField(default=get_utc_epoch_time, blank=True)
    twitch = models.CharField(max_length=255, default='')
    youtube = models.CharField(max_length=255, default='')
    twitter = models.CharField(max_length=255, default='')
    mixer = models.CharField(max_length=255, default='')
    social = models.CharField(max_length=255, default='')
    donation = models.IntegerField(default=0)
    notes = models.CharField(max_length=255, default='')
    color = models.CharField(max_length=255, default='')
    ban = models.BooleanField(default=False)
    glow = models.BooleanField(default=False)

    class Meta:
        db_table = "player"


class PcRanks(models.Model):
    player = models.ForeignKey(Player, default=None)
    halo_reach_team_hardcore = models.IntegerField(default=0)
    halo_reach_invasion = models.IntegerField(default=0)
    halo_reach_team_slayer = models.IntegerField(default=0)
    hce_hardcore_doubles = models.IntegerField(default=1)

    class Meta:
        db_table = "pc_ranks"


class Ranks(models.Model):
    player = models.ForeignKey(Player, default=None)
    pc_ranks = models.ForeignKey(PcRanks, default=1)
    h3_team_slayer = models.IntegerField(default=0)
    h3_team_hardcore = models.IntegerField(default=0)
    ms_2v2_series = models.IntegerField(default=0)
    h3_team_doubles = models.IntegerField(default=0)
    halo_reach_team_hardcore = models.IntegerField(default=0)
    halo_reach_invasion = models.IntegerField(default=0)
    h2c_team_hardcore = models.IntegerField(default=0)
    hce_hardcore_doubles = models.IntegerField(default=0)
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

    s1_playtime = models.IntegerField(default=0)
    s1_kills = models.IntegerField(default=0)
    s1_deaths = models.IntegerField(default=0)
    s1_wins = models.IntegerField(default=0)
    s1_losses = models.IntegerField(default=0)
    s1_matches = models.IntegerField(default=0)
    s1_wl = models.IntegerField(default=0)
    s1_kd = models.IntegerField(default=0)

    h3_team_slayer = models.IntegerField(default=0)
    h3_team_hardcore = models.IntegerField(default=0)
    ms_2v2_series = models.IntegerField(default=0)
    h3_team_doubles = models.IntegerField(default=0)
    h2c_team_hardcore = models.IntegerField(default=0)
    hce_hardcore_doubles = models.IntegerField(default=0)
    halo_reach_team_hardcore = models.IntegerField(default=0)
    halo_reach_invasion = models.IntegerField(default=0)
    halo_reach_team_slayer = models.IntegerField(default=0)
    pc_halo_reach_team_hardcore = models.IntegerField(default=0)
    pc_halo_reach_invasion = models.IntegerField(default=0)
    pc_halo_reach_team_slayer = models.IntegerField(default=0)
    pc_hce_hardcore_doubles = models.IntegerField(default=0)

    class Meta:
        db_table = "leaderboard"


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    username = models.CharField(max_length=15, unique=True)
    reset_link = models.CharField(default=None, null=True, max_length=255)
    reset_date = models.IntegerField(default=None, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    # password = models.CharField(max_length=255)
    # last_login = models.DateTimeField(default=timezone.now, blank=True)

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        db_table = "user"


# Screenshot of that given day stats to subtract from
class Season1(models.Model):
    player = models.ForeignKey(Player, default=None)

    playtime = models.CharField(max_length=255)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    epoch = models.IntegerField(default=0)

    class Meta:
        db_table = "season1"


# For S1 leaderboards
class Season1Stats(models.Model):
    player = models.ForeignKey(Player, default=None)

    playtime = models.CharField(max_length=255)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    epoch = models.IntegerField(default=0)
