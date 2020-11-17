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
    assists = models.IntegerField(default=0)
    betrayals = models.IntegerField(default=0)
    headshots = models.IntegerField(default=0)
    first_place = models.IntegerField(default=0)
    first_ratio = models.FloatField(default=0)

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
    rgb = models.BooleanField(default=False)

    class Meta:
        db_table = "player"


class RecentDonations(models.Model):
    player = models.ForeignKey(Player, default=None)

    class Meta:
        db_table = "recent_donations"


class NewPcRanks(models.Model):
    player = models.ForeignKey(Player, default=None)
    h3_recon_slayer = models.IntegerField(default=1)
    h3_team_slayer = models.IntegerField(default=1)
    h3_team_hardcore = models.IntegerField(default=1)
    h3_team_doubles = models.IntegerField(default=1)
    halo_reach_team_hardcore = models.IntegerField(default=1)
    halo_reach_invasion = models.IntegerField(default=1)
    hce_hardcore_doubles = models.IntegerField(default=1)
    h2c_team_hardcore = models.IntegerField(default=1)
    h2a_team_hardcore = models.IntegerField(default=1)

    v_h3_recon_slayer = models.BooleanField(default=0)
    v_h3_team_slayer = models.BooleanField(default=0)
    v_h3_team_hardcore = models.BooleanField(default=0)
    v_h3_team_doubles = models.BooleanField(default=0)
    v_halo_reach_team_hardcore = models.IntegerField(default=0)
    v_halo_reach_invasion = models.IntegerField(default=0)
    v_hce_hardcore_doubles = models.IntegerField(default=0)
    v_h2c_team_hardcore = models.IntegerField(default=0)
    v_h2a_team_hardcore = models.IntegerField(default=0)

    class Meta:
        db_table = "new_pc_ranks"


class NewRanks(models.Model):
    player = models.ForeignKey(Player, default=None)
    pc_ranks = models.ForeignKey(NewPcRanks, default=1)

    h3_recon_slayer = models.IntegerField(default=1)
    h3_team_slayer = models.IntegerField(default=1)
    h3_team_hardcore = models.IntegerField(default=1)
    h3_team_doubles = models.IntegerField(default=1)
    h2a_team_hardcore = models.IntegerField(default=1)
    h2c_team_hardcore = models.IntegerField(default=1)
    hce_hardcore_doubles = models.IntegerField(default=1)
    halo_reach_team_hardcore = models.IntegerField(default=1)
    halo_reach_invasion = models.IntegerField(default=1)
    h4_squad_battle = models.IntegerField(default=1)

    v_h3_recon_slayer = models.BooleanField(default=0)
    v_h3_team_slayer = models.BooleanField(default=0)
    v_h3_team_hardcore = models.BooleanField(default=0)
    v_h3_team_doubles = models.BooleanField(default=0)
    v_halo_reach_team_hardcore = models.BooleanField(default=0)
    v_halo_reach_invasion = models.BooleanField(default=0)
    v_h2c_team_hardcore = models.BooleanField(default=0)
    v_hce_hardcore_doubles = models.BooleanField(default=0)
    v_h2a_team_hardcore = models.IntegerField(default=0)
    v_h4_squad_battle = models.IntegerField(default=0)

    class Meta:
        db_table = "new_ranks"


class PcRanks(models.Model):
    player = models.ForeignKey(Player, default=None)
    halo_reach_team_hardcore = models.IntegerField(default=1)
    halo_reach_invasion = models.IntegerField(default=1)
    halo_reach_team_slayer = models.IntegerField(default=1)
    hce_hardcore_doubles = models.IntegerField(default=1)
    h2c_team_hardcore = models.IntegerField(default=1)
    h2a_team_hardcore = models.IntegerField(default=1)

    v_halo_reach_team_hardcore = models.IntegerField(default=0)
    v_halo_reach_invasion = models.IntegerField(default=0)
    v_hce_hardcore_doubles = models.IntegerField(default=0)
    v_halo_reach_team_slayer = models.BooleanField(default=0)
    v_h2c_team_hardcore = models.IntegerField(default=0)
    v_h2a_team_hardcore = models.IntegerField(default=0)

    class Meta:
        db_table = "pc_ranks"


class Ranks(models.Model):
    player = models.ForeignKey(Player, default=None)
    pc_ranks = models.ForeignKey(PcRanks, default=1)
    h3_team_slayer = models.IntegerField(default=1)
    h3_team_hardcore = models.IntegerField(default=1)
    ms_2v2_series = models.IntegerField(default=1)
    h3_team_doubles = models.IntegerField(default=1)
    halo_reach_team_hardcore = models.IntegerField(default=1)
    halo_reach_invasion = models.IntegerField(default=1)
    h2c_team_hardcore = models.IntegerField(default=1)
    hce_team_doubles = models.IntegerField(default=1)
    hce_hardcore_doubles = models.IntegerField(default=1)
    halo_reach_team_slayer = models.IntegerField(default=1)
    h2a_team_hardcore = models.IntegerField(default=1)

    v_h3_team_slayer = models.BooleanField(default=0)
    v_h3_team_hardcore = models.BooleanField(default=0)
    v_ms_2v2_series = models.BooleanField(default=0)
    v_h3_team_doubles = models.BooleanField(default=0)
    v_halo_reach_team_hardcore = models.BooleanField(default=0)
    v_halo_reach_invasion = models.BooleanField(default=0)
    v_h2c_team_hardcore = models.BooleanField(default=0)
    v_hce_hardcore_doubles = models.BooleanField(default=0)
    v_hce_team_doubles = models.BooleanField(default=0)
    v_halo_reach_team_slayer = models.BooleanField(default=0)
    v_h2a_team_hardcore = models.IntegerField(default=0)

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
    assists = models.IntegerField(default=0)
    betrayals = models.IntegerField(default=0)
    headshots = models.IntegerField(default=0)
    first_place = models.IntegerField(default=0)
    first_ratio = models.IntegerField(default=0)

    # Leaderboard placement
    s1_score = models.IntegerField(default=0)
    s1_playtime = models.IntegerField(default=0)
    s1_kills = models.IntegerField(default=0)
    s1_deaths = models.IntegerField(default=0)
    s1_wins = models.IntegerField(default=0)
    s1_losses = models.IntegerField(default=0)
    s1_matches = models.IntegerField(default=0)
    s1_wl = models.FloatField(default=0)
    s1_kd = models.FloatField(default=0)

    # Leaderboard placement
    s2_score = models.IntegerField(default=0)
    s2_playtime = models.IntegerField(default=0)
    s2_kills = models.IntegerField(default=0)
    s2_deaths = models.IntegerField(default=0)
    s2_wins = models.IntegerField(default=0)
    s2_losses = models.IntegerField(default=0)
    s2_matches = models.IntegerField(default=0)
    s2_wl = models.FloatField(default=0)
    s2_kd = models.FloatField(default=0)

    # Leaderboard placement
    s3_score = models.IntegerField(default=0)
    s3_playtime = models.IntegerField(default=0)
    s3_kills = models.IntegerField(default=0)
    s3_deaths = models.IntegerField(default=0)
    s3_wins = models.IntegerField(default=0)
    s3_losses = models.IntegerField(default=0)
    s3_matches = models.IntegerField(default=0)
    s3_wl = models.FloatField(default=0)
    s3_kd = models.FloatField(default=0)
    s3_assists = models.FloatField(default=0)
    s3_betrayals = models.FloatField(default=0)
    s3_headshots = models.FloatField(default=0)

    # Leaderboard placement
    s4_score = models.IntegerField(default=0)
    s4_playtime = models.IntegerField(default=0)
    s4_kills = models.IntegerField(default=0)
    s4_deaths = models.IntegerField(default=0)
    s4_wins = models.IntegerField(default=0)
    s4_losses = models.IntegerField(default=0)
    s4_matches = models.IntegerField(default=0)
    s4_wl = models.FloatField(default=0)
    s4_kd = models.FloatField(default=0)
    s4_assists = models.FloatField(default=0)
    s4_betrayals = models.FloatField(default=0)
    s4_headshots = models.FloatField(default=0)

    # Leaderboard placement
    s5_score = models.IntegerField(default=0)
    s5_playtime = models.IntegerField(default=0)
    s5_kills = models.IntegerField(default=0)
    s5_deaths = models.IntegerField(default=0)
    s5_wins = models.IntegerField(default=0)
    s5_losses = models.IntegerField(default=0)
    s5_matches = models.IntegerField(default=0)
    s5_wl = models.FloatField(default=0)
    s5_kd = models.FloatField(default=0)
    s5_assists = models.FloatField(default=0)
    s5_betrayals = models.FloatField(default=0)
    s5_headshots = models.FloatField(default=0)

    # NEW
    new_h3_recon_slayer = models.IntegerField(default=0)
    new_h3_team_slayer = models.IntegerField(default=0)
    new_h3_team_hardcore = models.IntegerField(default=0)
    new_h3_team_doubles = models.IntegerField(default=0)
    new_h2c_team_hardcore = models.IntegerField(default=0)
    new_hce_hardcore_doubles = models.IntegerField(default=0)
    new_halo_reach_team_hardcore = models.IntegerField(default=0)
    new_halo_reach_invasion = models.IntegerField(default=0)
    new_h2a_team_hardcore = models.IntegerField(default=0)
    new_h4_squad_battle = models.IntegerField(default=0)

    new_pc_h3_recon_slayer = models.IntegerField(default=0)
    new_pc_h3_team_slayer = models.IntegerField(default=0)
    new_pc_h3_team_hardcore = models.IntegerField(default=0)
    new_pc_h3_team_doubles = models.IntegerField(default=0)
    new_pc_h2c_team_hardcore = models.IntegerField(default=0)
    new_pc_hce_hardcore_doubles = models.IntegerField(default=0)
    new_pc_halo_reach_team_hardcore = models.IntegerField(default=0)
    new_pc_halo_reach_invasion = models.IntegerField(default=0)
    new_pc_h2a_team_hardcore = models.IntegerField(default=0)
    # NEW

    # OLD
    old_h3_team_slayer = models.IntegerField(default=0)
    old_h3_team_hardcore = models.IntegerField(default=0)
    old_ms_2v2_series = models.IntegerField(default=0)
    old_h3_team_doubles = models.IntegerField(default=0)
    old_h2c_team_hardcore = models.IntegerField(default=0)
    old_hce_team_doubles = models.IntegerField(default=0)
    old_hce_hardcore_doubles = models.IntegerField(default=0)
    old_halo_reach_team_hardcore = models.IntegerField(default=0)
    old_halo_reach_invasion = models.IntegerField(default=0)
    old_halo_reach_team_slayer = models.IntegerField(default=0)
    old_h2a_team_hardcore = models.IntegerField(default=0)

    old_pc_halo_reach_team_hardcore = models.IntegerField(default=0)
    old_pc_halo_reach_invasion = models.IntegerField(default=0)
    old_pc_halo_reach_team_slayer = models.IntegerField(default=0)
    old_pc_hce_hardcore_doubles = models.IntegerField(default=0)
    old_pc_h2a_team_hardcore = models.IntegerField(default=0)
    # OLD

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


# For S1 leaderboards
class Season1(models.Model):
    player = models.ForeignKey(Player, default=None)
    score = models.IntegerField(default=0)
    playtime = models.CharField(max_length=255, default='0 days 0 hours')
    epoch = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    kd = models.FloatField(default=0)
    wl = models.FloatField(default=0)

    class Meta:
        db_table = "season1"


# Screenshot of that given day stats to subtract from
class Season1Record(models.Model):
    player = models.ForeignKey(Player, default=None)

    playtime = models.CharField(max_length=255, default='0 days 0 hours')
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    epoch = models.IntegerField(default=0)

    class Meta:
        db_table = "season1_record"


# For S2 leaderboards
class Season2(models.Model):
    player = models.ForeignKey(Player, default=None)
    score = models.IntegerField(default=0)
    playtime = models.CharField(max_length=255, default='0 days 0 hours')
    epoch = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    kd = models.FloatField(default=0)
    wl = models.FloatField(default=0)

    class Meta:
        db_table = "season2"


# Screenshot of that given day stats to subtract from
class Season2Record(models.Model):
    player = models.ForeignKey(Player, default=None)

    playtime = models.CharField(max_length=255, default='0 days 0 hours')
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    epoch = models.IntegerField(default=0)

    class Meta:
        db_table = "season2_record"


# For S3 leaderboards
class Season3(models.Model):
    player = models.ForeignKey(Player, default=None)
    score = models.IntegerField(default=0)
    playtime = models.CharField(max_length=255, default='0 days 0 hours')
    epoch = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    kd = models.FloatField(default=0)
    wl = models.FloatField(default=0)
    assists = models.IntegerField(default=0)
    betrayals = models.IntegerField(default=0)
    headshots = models.IntegerField(default=0)

    class Meta:
        db_table = "season3"


# Screenshot of that given day stats to subtract from
class Season3Record(models.Model):
    player = models.ForeignKey(Player, default=None)

    playtime = models.CharField(max_length=255, default='0 days 0 hours')
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    epoch = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    betrayals = models.IntegerField(default=0)
    headshots = models.IntegerField(default=0)

    class Meta:
        db_table = "season3_record"


# For S4 leaderboards
class Season4(models.Model):
    player = models.ForeignKey(Player, default=None)
    score = models.IntegerField(default=0)
    playtime = models.CharField(max_length=255, default='0 days 0 hours')
    epoch = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    kd = models.FloatField(default=0)
    wl = models.FloatField(default=0)
    assists = models.IntegerField(default=0)
    betrayals = models.IntegerField(default=0)
    headshots = models.IntegerField(default=0)

    class Meta:
        db_table = "season4"


# Screenshot of that given day stats to subtract from
class Season4Record(models.Model):
    player = models.ForeignKey(Player, default=None)

    playtime = models.CharField(max_length=255, default='0 days 0 hours')
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    epoch = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    betrayals = models.IntegerField(default=0)
    headshots = models.IntegerField(default=0)

    class Meta:
        db_table = "season4_record"


# For S5 leaderboards
class Season5(models.Model):
    player = models.ForeignKey(Player, default=None)
    score = models.IntegerField(default=0)
    playtime = models.CharField(max_length=255, default='0 days 0 hours')
    epoch = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    kd = models.FloatField(default=0)
    wl = models.FloatField(default=0)
    assists = models.IntegerField(default=0)
    betrayals = models.IntegerField(default=0)
    headshots = models.IntegerField(default=0)

    class Meta:
        db_table = "season5"


# Screenshot of that given day stats to subtract from
class Season5Record(models.Model):
    player = models.ForeignKey(Player, default=None)

    playtime = models.CharField(max_length=255, default='0 days 0 hours')
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    epoch = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    betrayals = models.IntegerField(default=0)
    headshots = models.IntegerField(default=0)

    class Meta:
        db_table = "season5_record"