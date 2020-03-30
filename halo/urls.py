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
from django.views.generic import TemplateView
from halo.controllers import site, profile, leaderboard, donate, account_handler, xbox_handler

urlpatterns = [
    url(r'^$', site.home, name='home'),
    url(r'^donate/$', site.donate, name='donate'),
    url(r'^profile/(?P<gt>.*)', site.profile),
    url(r'^404/$', site.error_page, name='404'),
    url(r'^500/$', site.server_error, name='500'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
    url(r'^database/(?P<gt>.*)', site.update_database),

    url(r'^privacy-policy/$', site.privacy_policy, name='privacy_policy'),
    url(r'^about/$', site.about, name='about'),

    # XBOX CLIPS
    url(r'^xbox-clips/', xbox_handler.xbox_clips),

    # DATABASE
    url(r'^update-leaderboard/', leaderboard.update_leaderboard),
    url(r'^db-update/(?P<type>.*)', leaderboard.database_leaderboard),

    # USER
    # url(r'^register/$', site.register, name='register_page'),
    url(r'^login/$', site.login, name='login_page'),
    url(r'^forgot_password/$', site.forgot_password, name='forgot_password'),
    url(r'^dashboard/$', site.dashboard, name='dashboard'),

    # PROFILE
    url(r'^edit-player/$', profile.edit_player, name='edit_player'),
    url(r'^service-record/', profile.service_record),
    url(r'^player-matches/', profile.player_matches),

    # Account Handler
    # url(r'^account/register/$', account_handler.register, name='register'),
    url(r'^account/login/$', account_handler.user_login, name='login'),
    url(r'^account/reset_password/$', account_handler.reset_password, name='reset_password'),
    url(r'^account/change_password/$', account_handler.change_password, name='change_password'),
    url(r'^logout/$', account_handler.user_logout, name='logout'),

    # DONATE
    url(r'^donate-message/', donate.donate_email),

    # SEASON1 LEADERBOARDS
    url(r'^leaderboards/s1/mccs', leaderboard.s1_score),
    url(r'^leaderboards/s1/kills', leaderboard.s1_kills),
    url(r'^leaderboards/s1/deaths', leaderboard.s1_deaths),
    url(r'^leaderboards/s1/wins', leaderboard.s1_wins),
    url(r'^leaderboards/s1/losses', leaderboard.s1_losses),
    url(r'^leaderboards/s1/matches', leaderboard.s1_matches),
    url(r'^leaderboards/s1/wl', leaderboard.s1_wl),
    url(r'^leaderboards/s1/kd', leaderboard.s1_kd),
    url(r'^leaderboards/s1/playtime', leaderboard.s1_playtime),

    # GENERAL LEADERBOARDS
    url(r'^leaderboards/donations', leaderboard.most_donations),
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
    url(r'^leaderboards/hce-hardcore-doubles', leaderboard.hce_hardcore_doubles),
    url(r'^leaderboards/hce-team-doubles', leaderboard.hce_team_doubles),
    url(r'^leaderboards/h2c-team-hardcore', leaderboard.h2c_team_hardcore),
    url(r'^leaderboards/halo-reach-team-hardcore', leaderboard.halo_reach_team_hardcore),
    url(r'^leaderboards/halo-reach-invasion', leaderboard.halo_reach_invasion),
    url(r'^leaderboards/halo-reach-team-slayer', leaderboard.halo_reach_team_slayer),

    url(r'^leaderboards/pc/halo-reach-team-hardcore', leaderboard.pc_reach_team_hardcore),
    url(r'^leaderboards/pc/halo-reach-invasion', leaderboard.pc_reach_invasion),
    url(r'^leaderboards/pc/halo-reach-team-slayer', leaderboard.pc_reach_team_slayer),
    url(r'^leaderboards/pc/hce-hardcore-doubles', leaderboard.pc_hce_hardcore_doubles),
]
