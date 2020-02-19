import json
from django.shortcuts import render
from base import get_base_url, model_to_dict, decimal_format
from halo_handler import get_xbox_auth, halo_ranks
from halo.models import Player, Ranks


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


def sort_ranks(ranks):
    return sorted(ranks, key=lambda i: i['rank'], reverse=True)


def profile(request, gt):
    try:
        ranks = halo_ranks(gt)
    except:
        get_xbox_auth()
        ranks = halo_ranks(gt)

    player = Player.objects.filter(gamertag=gt)

    if player.exists():
        player = model_to_dict(player[0])
        player['kd_ratio'] = decimal_format(float(player['kills'])/float(player['deaths']), 2, False)
        player['wl_ratio'] = decimal_format(float(player['wins'])/float(player['losses']), 2, False)
    else:
        player = {}

    data = {
        'base_url': get_base_url(),
        'ranks': json.dumps(ranks),
        'gt': ranks['H3 Team Slayer'][0]['Gamertag'],
        'player': json.dumps(player)
    }

    return render(request, 'profile.html', data)
