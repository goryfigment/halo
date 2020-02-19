import json
from django.shortcuts import render
from base import models_to_dict
from halo.models import Player, Ranks


def most_kills(request):
    sorted_kills = list(Player.objects.all().values('gamertag', 'kills', 'matches').order_by('-kills'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_kills)})


