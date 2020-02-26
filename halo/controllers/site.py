import json
from django.shortcuts import render
from base import get_base_url, model_to_dict, decimal_format
from halo_handler import get_xbox_auth, halo_ranks, service_record
from halo.models import Player, Leaderboard


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
        'base_url': get_base_url()
    }

    return render(request, 'home.html', data)


def donate(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'donate.html', data)


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
        player_obj = Player.objects.get(gamertag=gt)
        player_obj.hits += 1
        player_obj.save()
        player = model_to_dict(player_obj)
        player['kd_ratio'] = decimal_format(float(player['kills'])/float(player['deaths']), 2, False)
        player['wl_ratio'] = decimal_format(float(player['wins'])/float(player['losses']), 2, False)

        leaderboard = Leaderboard.objects.filter(player=player_obj)

        if leaderboard.exists():
            leaderboard = model_to_dict(leaderboard[0])
        else:
            leaderboard = {}
    else:
        player = {}
        leaderboard = {}

    data = {
        'base_url': get_base_url(),
        'ranks': json.dumps(ranks),
        'gt': ranks['H3 Team Slayer'][0]['Gamertag'],
        'player': json.dumps(player),
        'leaderboard': json.dumps(leaderboard),
        'player_count': Player.objects.all().count()
    }

    return render(request, 'profile.html', data)


def update_database(request, gt):
    try:
        ranks = halo_ranks(gt)

        rank_list = [ranks["H3 Team Slayer"][0]['SkillRank'],
        ranks["H3 Team Hardcore"][0]['SkillRank'],
        ranks["MS 2v2 Series"][0]['SkillRank'],
        ranks["H3 Team Doubles"][0]['SkillRank'],
        ranks["Halo: Reach Team Hardcore"][0]['SkillRank'],
        ranks["Halo: Reach Invasion"][0]['SkillRank'],
        ranks["H2C Team Hardcore"][0]['SkillRank'],
        ranks["HCE Team Doubles"][0]['SkillRank'],
        ranks["Halo: Reach Team Slayer"][0]['SkillRank']]

        service_record(gt, ranks, max(rank_list))
    except:
        get_xbox_auth()
        ranks = halo_ranks(gt)

    player_obj = Player.objects.filter(gamertag=gt)

    if player_obj.exists():
        player_obj = Player.objects.get(gamertag=gt)
        player_obj.hits += 1
        player_obj.save()
        player = model_to_dict(player_obj)
        player['kd_ratio'] = decimal_format(float(player['kills'])/float(player['deaths']), 2, False)
        player['wl_ratio'] = decimal_format(float(player['wins'])/float(player['losses']), 2, False)
    else:
        player = {}

    data = {
        'base_url': get_base_url(),
        'ranks': json.dumps(ranks),
        'gt': gt,
        'player': player
    }

    return render(request, 'profile.html', data)
