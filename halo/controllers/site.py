import time
import json
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from base import get_base_url
from halo import get_xbox_auth, halo_ranks


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

    rank_list = []

    for playlist, rank in ranks.iteritems():
        rank_list.append({'playlist': playlist, 'rank': rank[0]['SkillRank']})

    data = {
        'base_url': get_base_url(),
        'ranks': json.dumps(sort_ranks(rank_list)),
        'gt': ranks['H3 Team Slayer'][0]['Gamertag']
    }

    return render(request, 'profile.html', data)
