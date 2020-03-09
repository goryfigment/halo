import json, time
from django.shortcuts import render
from base import get_base_url, model_to_dict, decimal_format
from django.http import HttpResponseRedirect
from halo_handler import get_xbox_auth, halo_ranks, service_record
from halo.models import Player, Leaderboard, User, Season1
from halo.controllers.leaderboard import season1_func


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
        'mccs': season1_func(request, 'mccs', 'score', 'MCCS', 0, 10)
    }

    return render(request, 'home.html', data)


def donate(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'donate.html', data)


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

    players = list(Player.objects.all().values('id', 'gamertag', 'ban', 'donation', 'twitch', 'youtube', 'twitter', 'mixer', 'social', 'notes', 'color'))

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
