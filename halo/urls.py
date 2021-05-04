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
from halo.controllers import site, profile, leaderboard, donate, account_handler, xbox_handler, halo_handler

urlpatterns = [
    url(r'^$', site.home, name='home'),
    url(r'^donate/$', site.donate, name='donate'),
    url(r'^profile/(?P<gt>.*)', site.profile),
    url(r'^404/$', site.error_page, name='404'),
    url(r'^500/$', site.server_error, name='500'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    url(r'^ads\.txt$', TemplateView.as_view(template_name="ads.txt", content_type='text/plain')),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
    url(r'^database/(?P<gt>.*)', site.update_database),

    url(r'^privacy-policy/$', site.privacy_policy, name='privacy_policy'),
    url(r'^terms-conditions/$', site.terms_conditions, name='terms_conditions'),
    url(r'^contact/$', site.contact, name='contact'),
    url(r'^about/$', site.about, name='about'),
    url(r'^timer/(?P<game>.*)/(?P<type>.*)$', site.timer, name='h3_radar'),
    url(r'^resources/$', site.resources, name='resources'),
    url(r'^halo-population/$', halo_handler.halo_population, name='population'),
    url(r'article/(?P<id>\d+)', site.article, name='article'),

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
    url(r'^ban/dashboard/$', site.ban_dashboard, name='ban_dashboard'),
    url(r'^verified/$', site.verified, name='verified'),

    # PROFILE
    url(r'^edit-player/$', profile.edit_player, name='edit_player'),
    url(r'^verify-player/$', profile.verify_player, name='verify_player'),
    url(r'^service-record/', profile.service_record),
    url(r'^player-matches/', profile.player_matches),
    url(r'^game-matches/', profile.game_matches),
    url(r'^update-emblem/', profile.update_emblem),

    # Account Handler
    # url(r'^account/register/$', account_handler.register, name='register'),
    url(r'^account/login/$', account_handler.user_login, name='login'),
    url(r'^account/reset_password/$', account_handler.reset_password, name='reset_password'),
    url(r'^account/change_password/$', account_handler.change_password, name='change_password'),
    url(r'^logout/$', account_handler.user_logout, name='logout'),

    # DONATE
    url(r'^donate-message/', donate.donate_email),
    url(r'^contact-message/', donate.contact_email),

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

    # SEASON2 LEADERBOARDS
    url(r'^leaderboards/s2/mccs', leaderboard.s2_score),
    url(r'^leaderboards/s2/kills', leaderboard.s2_kills),
    url(r'^leaderboards/s2/deaths', leaderboard.s2_deaths),
    url(r'^leaderboards/s2/wins', leaderboard.s2_wins),
    url(r'^leaderboards/s2/losses', leaderboard.s2_losses),
    url(r'^leaderboards/s2/matches', leaderboard.s2_matches),
    url(r'^leaderboards/s2/wl', leaderboard.s2_wl),
    url(r'^leaderboards/s2/kd', leaderboard.s2_kd),
    url(r'^leaderboards/s2/playtime', leaderboard.s2_playtime),

    # SEASON3 LEADERBOARDS
    url(r'^leaderboards/s3/mccs', leaderboard.s3_score),
    url(r'^leaderboards/s3/kills', leaderboard.s3_kills),
    url(r'^leaderboards/s3/deaths', leaderboard.s3_deaths),
    url(r'^leaderboards/s3/wins', leaderboard.s3_wins),
    url(r'^leaderboards/s3/losses', leaderboard.s3_losses),
    url(r'^leaderboards/s3/matches', leaderboard.s3_matches),
    url(r'^leaderboards/s3/wl', leaderboard.s3_wl),
    url(r'^leaderboards/s3/kd', leaderboard.s3_kd),
    url(r'^leaderboards/s3/playtime', leaderboard.s3_playtime),
    url(r'^leaderboards/s3/assists', leaderboard.s3_assists),
    url(r'^leaderboards/s3/betrayals', leaderboard.s3_betrayals),
    url(r'^leaderboards/s3/headshots', leaderboard.s3_headshots),


    # SEASON4 LEADERBOARDS
    url(r'^leaderboards/s4/mccs', leaderboard.s4_score),
    url(r'^leaderboards/s4/kills', leaderboard.s4_kills),
    url(r'^leaderboards/s4/deaths', leaderboard.s4_deaths),
    url(r'^leaderboards/s4/wins', leaderboard.s4_wins),
    url(r'^leaderboards/s4/losses', leaderboard.s4_losses),
    url(r'^leaderboards/s4/matches', leaderboard.s4_matches),
    url(r'^leaderboards/s4/wl', leaderboard.s4_wl),
    url(r'^leaderboards/s4/kd', leaderboard.s4_kd),
    url(r'^leaderboards/s4/playtime', leaderboard.s4_playtime),
    url(r'^leaderboards/s4/assists', leaderboard.s4_assists),
    url(r'^leaderboards/s4/betrayals', leaderboard.s4_betrayals),
    url(r'^leaderboards/s4/headshots', leaderboard.s4_headshots),

    # SEASON5 LEADERBOARDS
    url(r'^leaderboards/s5/mccs', leaderboard.s5_score),
    url(r'^leaderboards/s5/kills', leaderboard.s5_kills),
    url(r'^leaderboards/s5/deaths', leaderboard.s5_deaths),
    url(r'^leaderboards/s5/wins', leaderboard.s5_wins),
    url(r'^leaderboards/s5/losses', leaderboard.s5_losses),
    url(r'^leaderboards/s5/matches', leaderboard.s5_matches),
    url(r'^leaderboards/s5/wl', leaderboard.s5_wl),
    url(r'^leaderboards/s5/kd', leaderboard.s5_kd),
    url(r'^leaderboards/s5/playtime', leaderboard.s5_playtime),
    url(r'^leaderboards/s5/assists', leaderboard.s5_assists),
    url(r'^leaderboards/s5/betrayals', leaderboard.s5_betrayals),
    url(r'^leaderboards/s5/headshots', leaderboard.s5_headshots),

    # SEASON6 LEADERBOARDS
    url(r'^leaderboards/s6/mccs', leaderboard.s6_score),
    url(r'^leaderboards/s6/kills', leaderboard.s6_kills),
    url(r'^leaderboards/s6/deaths', leaderboard.s6_deaths),
    url(r'^leaderboards/s6/wins', leaderboard.s6_wins),
    url(r'^leaderboards/s6/losses', leaderboard.s6_losses),
    url(r'^leaderboards/s6/matches', leaderboard.s6_matches),
    url(r'^leaderboards/s6/wl', leaderboard.s6_wl),
    url(r'^leaderboards/s6/kd', leaderboard.s6_kd),
    url(r'^leaderboards/s6/playtime', leaderboard.s6_playtime),
    url(r'^leaderboards/s6/assists', leaderboard.s6_assists),
    url(r'^leaderboards/s6/betrayals', leaderboard.s6_betrayals),
    url(r'^leaderboards/s6/headshots', leaderboard.s6_headshots),

    # SEASON7 LEADERBOARDS
    url(r'^leaderboards/s7/mccs', leaderboard.s7_score),
    url(r'^leaderboards/s7/kills', leaderboard.s7_kills),
    url(r'^leaderboards/s7/deaths', leaderboard.s7_deaths),
    url(r'^leaderboards/s7/wins', leaderboard.s7_wins),
    url(r'^leaderboards/s7/losses', leaderboard.s7_losses),
    url(r'^leaderboards/s7/matches', leaderboard.s7_matches),
    url(r'^leaderboards/s7/wl', leaderboard.s7_wl),
    url(r'^leaderboards/s7/kd', leaderboard.s7_kd),
    url(r'^leaderboards/s7/playtime', leaderboard.s7_playtime),
    url(r'^leaderboards/s7/assists', leaderboard.s7_assists),
    url(r'^leaderboards/s7/betrayals', leaderboard.s7_betrayals),
    url(r'^leaderboards/s7/headshots', leaderboard.s7_headshots),

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
    url(r'^leaderboards/assists', leaderboard.most_assists),
    url(r'^leaderboards/betrayals', leaderboard.most_betrayals),
    url(r'^leaderboards/headshots', leaderboard.most_headshots),
    url(r'^leaderboards/first-place', leaderboard.most_first_place),

    # OLD PLAYLIST LEADERBOARDS
    url(r'^leaderboards/before-reset/most-50s', leaderboard.old_all_most_50s),
    url(r'^leaderboards/before-reset/xbox/most-50s', leaderboard.old_xbox_most_50s),
    url(r'^leaderboards/before-reset/pc/most-50s', leaderboard.old_pc_most_50s),

    url(r'^leaderboards/before-reset/h3-team-slayer', leaderboard.old_h3_team_slayer),
    url(r'^leaderboards/before-reset/h3-team-hardcore', leaderboard.old_h3_team_hardcore),
    url(r'^leaderboards/before-reset/h3-team-doubles', leaderboard.old_h3_team_doubles),
    url(r'^leaderboards/before-reset/ms-2v2-series', leaderboard.old_ms_2v2_series),
    url(r'^leaderboards/before-reset/hce-hardcore-doubles', leaderboard.old_hce_hardcore_doubles),
    url(r'^leaderboards/before-reset/hce-team-doubles', leaderboard.old_hce_team_doubles),
    url(r'^leaderboards/before-reset/h2a-team-hardcore', leaderboard.old_h2a_team_hardcore),
    url(r'^leaderboards/before-reset/h2c-team-hardcore', leaderboard.old_h2c_team_hardcore),
    url(r'^leaderboards/before-reset/halo-reach-team-hardcore', leaderboard.old_halo_reach_team_hardcore),
    url(r'^leaderboards/before-reset/halo-reach-invasion', leaderboard.old_halo_reach_invasion),
    url(r'^leaderboards/before-reset/halo-reach-team-slayer', leaderboard.old_halo_reach_team_slayer),

    url(r'^leaderboards/before-reset/pc/halo-reach-team-hardcore', leaderboard.old_pc_reach_team_hardcore),
    url(r'^leaderboards/before-reset/pc/halo-reach-invasion', leaderboard.old_pc_reach_invasion),
    url(r'^leaderboards/before-reset/pc/halo-reach-team-slayer', leaderboard.old_pc_reach_team_slayer),
    url(r'^leaderboards/before-reset/pc/hce-hardcore-doubles', leaderboard.old_pc_hce_hardcore_doubles),
    url(r'^leaderboards/before-reset/pc/h2c-team-hardcore', leaderboard.old_pc_h2c_team_hardcore),
    url(r'^leaderboards/before-reset/pc/h2a-team-hardcore', leaderboard.old_pc_h2a_team_hardcore),

    # NEW PLAYLIST LEADERBOARDS
    url(r'^leaderboards/most-50s', leaderboard.all_most_50s),
    url(r'^leaderboards/xbox/most-50s', leaderboard.xbox_most_50s),
    url(r'^leaderboards/pc/most-50s', leaderboard.pc_most_50s),

    url(r'^leaderboards/xbox/h3-recon-slayer', leaderboard.h3_recon_slayer),
    url(r'^leaderboards/xbox/h3-team-slayer', leaderboard.h3_team_slayer),
    url(r'^leaderboards/xbox/h3-team-hardcore', leaderboard.h3_team_hardcore),
    url(r'^leaderboards/xbox/h3-team-doubles', leaderboard.h3_team_doubles),
    url(r'^leaderboards/xbox/hce-hardcore-doubles', leaderboard.hce_hardcore_doubles),
    url(r'^leaderboards/xbox/h2a-team-hardcore', leaderboard.h2a_team_hardcore),
    url(r'^leaderboards/xbox/h2c-team-hardcore', leaderboard.h2c_team_hardcore),
    url(r'^leaderboards/xbox/halo-reach-team-hardcore', leaderboard.halo_reach_team_hardcore),
    url(r'^leaderboards/xbox/halo-reach-invasion', leaderboard.halo_reach_invasion),
    url(r'^leaderboards/xbox/h4-squad-battle', leaderboard.h4_squad_battle),
    url(r'^leaderboards/xbox/h3-hardcore-doubles', leaderboard.h3_hardcore_doubles),

    url(r'^leaderboards/pc/h3-recon-slayer', leaderboard.pc_h3_recon_slayer),
    url(r'^leaderboards/pc/h3-team-slayer', leaderboard.pc_h3_team_slayer),
    url(r'^leaderboards/pc/h3-team-hardcore', leaderboard.pc_h3_team_hardcore),
    url(r'^leaderboards/pc/h3-team-doubles', leaderboard.pc_h3_team_doubles),
    url(r'^leaderboards/pc/hce-hardcore-doubles', leaderboard.pc_hce_hardcore_doubles),
    url(r'^leaderboards/pc/h2a-team-hardcore', leaderboard.pc_h2a_team_hardcore),
    url(r'^leaderboards/pc/h2c-team-hardcore', leaderboard.pc_h2c_team_hardcore),
    url(r'^leaderboards/pc/halo-reach-team-hardcore', leaderboard.pc_halo_reach_team_hardcore),
    url(r'^leaderboards/pc/halo-reach-invasion', leaderboard.pc_halo_reach_invasion),
]
