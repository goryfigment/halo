import json, time
from django.shortcuts import render
from base import get_base_url, model_to_dict
from django.db.models import F
from django.http import HttpResponseRedirect
from halo_handler import get_xbox_auth, halo_ranks, service_record
from halo.models import Player, Leaderboard, User, Season1, RecentDonations, Season2
from halo.controllers.leaderboard import season2_func, season2_playtime_func


def error_page(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, '404.html', data)


def server_error(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, '500.html', data)


def home(request):
    data = {
        'base_url': get_base_url(),
        'mccs': season2_func(request, 'mccs', 'score', 'MCCS', 0, 10),
        'playtime': season2_playtime_func(request, 0, 10),
        'kills': season2_func(request, 'season1', 'kills', '(Season 2) Kills', 0, 10),
        'deaths': season2_func(request, 'season1', 'deaths', '(Season 2) Deaths', 0, 10),
        'wins': season2_func(request, 'season1', 'wins', '(Season 2) Wins', 0, 10),
        'losses': season2_func(request, 'season1', 'losses', '(Season 2) Losses', 0, 10),
        'matches': season2_func(request, 'season1', 'matches', '(Season 2) Matches', 0, 10),
        'kd': season2_func(request, 'season1_ratio', 'kd', '(Season 2) K/D Ratio', 0, 10),
        'wl': season2_func(request, 'season1_ratio', 'wl', '(Season 2) W/L Ratio', 0, 10),

        'recent_donations': json.dumps(list(RecentDonations.objects.all().values(amount=F('player__donation'), gamertag=F('player__gamertag'), player_id=F('player__id'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb')).order_by('-id')[0:5]))
    }

    return render(request, 'home.html', data)


def donate(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'donate.html', data)


def privacy_policy(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'privacy_policy.html', data)


def timer(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'timer.html', data)


def about(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'about.html', data)


def resources(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'resources.html', data)


def register(request):
    data = {
        'base_url': get_base_url()
    }

    # If user is login redirect to overview
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    return render(request, 'register.html', data)


def login(request):
    data = {
        'base_url': get_base_url()
    }

    # If user is login redirect to overview
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    return render(request, 'login.html', data)


def dashboard(request):
    current_user = request.user

    # Only go to overview if user is logged in
    if not current_user.is_authenticated():
        return HttpResponseRedirect('/login/')

    players = list(Player.objects.all().values('id', 'gamertag', 'ban', 'donation', 'twitch', 'youtube', 'twitter', 'mixer', 'social', 'notes', 'color', 'rgb'))

    data = {
        'base_url': get_base_url(),
        'players': json.dumps(players)
    }

    return render(request, 'dashboard.html', data)


def ban_dashboard(request):
    current_user = request.user

    # Only go to overview if user is logged in
    if not current_user.is_authenticated():
        return HttpResponseRedirect('/login/')

    players = list(Player.objects.filter(ban=True).values('id', 'gamertag', 'ban', 'donation', 'twitch', 'youtube', 'twitter', 'mixer', 'social', 'notes', 'color', 'rgb'))

    data = {
        'base_url': get_base_url(),
        'players': json.dumps(players)
    }

    return render(request, 'dashboard.html', data)


def forgot_password(request):
    data = {
        'base_url': get_base_url(),
        'expired': False
    }

    if 'code' in request.GET:
        current_user = User.objects.get(reset_link=request.GET['code'])

        if (int(round(time.time())) - current_user.reset_date) > 86400:
            data['expired'] = True

    # If user is login redirect to overview
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    return render(request, 'forgot_password.html', data)


def sort_ranks(ranks):
    return sorted(ranks, key=lambda i: i['rank'], reverse=True)


def profile(request, gt):
    try:
        ranks = halo_ranks(gt)
    except:
        get_xbox_auth()
        ranks = halo_ranks(gt)

    player_obj = Player.objects.filter(gamertag=gt)

    if player_obj.exists():
        player_obj = player_obj[0]
        player_obj.hits += 1
        player_obj.save()
        player = model_to_dict(player_obj)

        leaderboard = Leaderboard.objects.filter(player=player_obj)

        if leaderboard.exists():
            leaderboard = model_to_dict(leaderboard[0])
        else:
            leaderboard = {}

        player['season'] = model_to_dict(Season1.objects.get(player=player_obj))
        player['season2'] = model_to_dict(Season2.objects.get(player=player_obj))
    else:
        player = {'season': {}}
        leaderboard = {}

    data = {
        'base_url': get_base_url(),
        'xbox_ranks': json.dumps(ranks['xbox']),
        'pc_ranks': json.dumps(ranks['pc']),
        'gt': ranks['xbox']['H3 Team Slayer'][0]['Gamertag'],
        'player': json.dumps(player),
        'leaderboard': json.dumps(leaderboard),
        'player_count': Player.objects.all().count()
    }

    return render(request, 'profile.html', data)


def update_database(request, gt):
    try:
        ranks = halo_ranks(gt)

        xbox_ranks = ranks['xbox']
        pc_ranks = ranks['pc']

        rank_list = [xbox_ranks["H3 Team Slayer"][0]['SkillRank'],
        xbox_ranks["H3 Team Hardcore"][0]['SkillRank'],
        xbox_ranks["MS 2v2 Series"][0]['SkillRank'],
        xbox_ranks["H3 Team Doubles"][0]['SkillRank'],
        xbox_ranks["Halo: Reach Team Hardcore"][0]['SkillRank'],
        xbox_ranks["Halo: Reach Invasion"][0]['SkillRank'],
        xbox_ranks["H2C Team Hardcore"][0]['SkillRank'],
        xbox_ranks["HCE Hardcore Doubles"][0]['SkillRank'],
        xbox_ranks["Halo: Reach Team Slayer"][0]['SkillRank'],
        pc_ranks["Halo: Reach Team Slayer"][0]['SkillRank'],
        pc_ranks["Halo: Reach Invasion"][0]['SkillRank'],
        pc_ranks["Halo: Reach Team Hardcore"][0]['SkillRank']]

        service_record(gt, xbox_ranks, pc_ranks, max(rank_list))
    except:
        get_xbox_auth()
        ranks = halo_ranks(gt)

    data = {
        'base_url': get_base_url(),
        'ranks': json.dumps(ranks),
        'gt': gt
    }

    return render(request, 'profile.html', data)
