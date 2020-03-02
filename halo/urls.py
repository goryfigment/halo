"""halo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from halo.controllers import site, profile, leaderboard, donate

urlpatterns = [
    url(r'^$', site.home, name='home'),
    url(r'^donate/$', site.donate, name='donate'),
    url(r'^profile/(?P<gt>.*)', site.profile),
    url(r'^404/$', site.error_page, name='404'),
    url(r'^500/$', site.server_error, name='500'),
    url(r'^database/(?P<gt>.*)', site.update_database),

    url(r'^service-record/', profile.service_record),
    url(r'^update-leaderboard/', leaderboard.update_leaderboard),
    url(r'^db-update/(?P<type>.*)', leaderboard.database_leaderboard),

    # DONATE
    url(r'^donate-message/', donate.donate_email),

    # GENERAL LEADERBOARDS
    url(r'^leaderboards/kills', leaderboard.most_kills),
    url(r'^leaderboards/deaths', leaderboard.most_deaths),
    url(r'^leaderboards/wins', leaderboard.most_wins),
    url(r'^leaderboards/losses', leaderboard.most_losses),
    url(r'^leaderboards/matches', leaderboard.most_matches),
    url(r'^leaderboards/wl', leaderboard.best_wl),
    url(r'^leaderboards/kd', leaderboard.best_kd),
    url(r'^leaderboards/playtime', leaderboard.most_playtime),

    url(r'^leaderboards/most-50s', leaderboard.all_most_50s),
    url(r'^leaderboards/xbox/most-50s', leaderboard.xbox_most_50s),
    url(r'^leaderboards/pc/most-50s', leaderboard.pc_most_50s),

    # PLAYLIST LEADERBOARDS
    url(r'^leaderboards/h3-team-slayer', leaderboard.h3_team_slayer),
    url(r'^leaderboards/h3-team-hardcore', leaderboard.h3_team_hardcore),
    url(r'^leaderboards/h3-team-doubles', leaderboard.h3_team_doubles),
    url(r'^leaderboards/ms-2v2-series', leaderboard.ms_2v2_series),
    url(r'^leaderboards/hce-team-doubles', leaderboard.hce_team_doubles),
    url(r'^leaderboards/h2c-team-hardcore', leaderboard.h2c_team_hardcore),
    url(r'^leaderboards/halo-reach-team-hardcore', leaderboard.halo_reach_team_hardcore),
    url(r'^leaderboards/halo-reach-invasion', leaderboard.halo_reach_invasion),
    url(r'^leaderboards/halo-reach-team-slayer', leaderboard.halo_reach_team_slayer),

    url(r'^leaderboards/pc/halo-reach-team-hardcore', leaderboard.pc_reach_team_hardcore),
    url(r'^leaderboards/pc/halo-reach-invasion', leaderboard.pc_reach_invasion),
    url(r'^leaderboards/pc/halo-reach-team-slayer', leaderboard.pc_reach_team_slayer),
]
