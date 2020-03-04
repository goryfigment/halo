import json
from django.shortcuts import render
from base import decimal_format, sort_list, get_base_url, sort_float, models_to_dict
from halo.models import Player, Ranks, Leaderboard, PcRanks
from django.http import JsonResponse


def record_leaderboard(player_id, attr_type, rank):
    leaderboard = Leaderboard.objects.filter(player_id=player_id)

    if leaderboard.exists():
        leaderboard = leaderboard[0]
    else:
        leaderboard = Leaderboard.objects.create(player_id=player_id)

    setattr(leaderboard, attr_type, rank)
    leaderboard.save()


def update_leaderboard(request):
    query_request = json.loads(request.body)
    leaderboards = query_request['leaderboards']
    index = query_request['index']

    for player in leaderboards:
        index += 1

        if 'id' in player:
            player_id = player['id']
        else:
            player_id = player['player__id']

        record_leaderboard(player_id, query_request['type'], index)

    return JsonResponse({'success': True}, safe=False)


def database_leaderboard(request, type):
    if type == 'playtime':
        type = 'epoch'

    rank = ['hce_hardcore_doubles', 'h2c_team_hardcore', 'h3_team_slayer', 'h3_team_hardcore', 'h3_team_doubles', 'ms_2v2_series', 'halo_reach_team_hardcore', 'halo_reach_invasion', 'halo_reach_team_slayer']

    print type

    if type in rank:
        leaderboards = list(Ranks.objects.all().values('player__id', 'player__matches', 'hce_hardcore_doubles', 'h2c_team_hardcore', 'h3_team_slayer', 'h3_team_hardcore', 'h3_team_doubles', 'ms_2v2_series', 'halo_reach_team_hardcore', 'halo_reach_invasion', 'halo_reach_team_slayer').order_by('-' + type, '-player__matches'))
    else:
        leaderboards = list(models_to_dict(Player.objects.all().order_by('-' + type)))

    index = 0

    for player in leaderboards:
        index += 1

        if 'id' in player:
            player_id = player['id']
        else:
            player_id = player['player__id']

        if type == 'epoch':
            type = 'playtime'

        record_leaderboard(player_id, type, index)

    return render(request, 'leaderboard.html', {'leaderboards': leaderboards})


def most_kills(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'kills',
        'title': 'Kills',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = list(Player.objects.filter(kills__gt=0, ban=False).values('gamertag', 'kills', 'matches', 'emblem', 'id', 'donation', 'twitch', 'youtube', 'twitter', 'mixer', 'notes', 'color', 'social', 'glow').order_by('-kills')[first_record:last_record])
    data['index'] = first_record
    data['leaderboard'] = json.dumps(leaderboards)

    return render(request, 'leaderboard.html', data)


def most_deaths(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'deaths',
        'title': 'Deaths',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Player.objects.filter(deaths__gt=0, ban=False).order_by('-deaths')[first_record:last_record]
    data['index'] = first_record
    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'deaths', 'matches', 'emblem', 'id', 'donation', 'twitch', 'youtube', 'twitter', 'mixer', 'notes', 'color', 'social', 'glow')))

    return render(request, 'leaderboard.html', data)


def most_wins(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'wins',
        'title': 'Wins',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    data['leaderboard'] = json.dumps(list(Player.objects.filter(wins__gt=0, ban=False).values('gamertag', 'wins', 'matches', 'emblem', 'id', 'donation', 'twitch', 'youtube', 'twitter', 'mixer', 'notes', 'color', 'social', 'glow').order_by('-wins')[first_record:last_record]))
    data['index'] = first_record

    # for player in leaderboards:
    #     first_record += 1
    #     record_leaderboard(player, 'wins', first_record)

    return render(request, 'leaderboard.html', data)


def most_losses(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'losses',
        'title': 'Losses',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Player.objects.filter(losses__gt=0, ban=False).order_by('-losses')[first_record:last_record]
    data['index'] = first_record

    # for player in leaderboards:
    #     first_record += 1
    #     record_leaderboard(player, 'losses', first_record)

    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'losses', 'matches', 'emblem', 'id', 'donation', 'twitch', 'mixer', 'youtube', 'twitter', 'notes', 'color', 'social', 'glow')))

    return render(request, 'leaderboard.html', data)


def most_matches(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'matches',
        'title': 'Matches',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Player.objects.filter(ban=False).order_by('-matches')[first_record:last_record]
    data['index'] = first_record

    # for player in leaderboards:
    #     first_record += 1
    #     record_leaderboard(player, 'matches', first_record)

    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'matches', 'emblem', 'id', 'donation', 'twitch', 'mixer', 'youtube', 'twitter', 'notes', 'color', 'social', 'glow')))

    return render(request, 'leaderboard.html', data)


def best_wl(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'wl',
        'title': 'W/L Ratio',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Player.objects.filter(matches__gte=250, ban=False).order_by('-wl')[first_record:last_record]
    data['index'] = first_record

    # for player in leaderboards:
    #     first_record += 1
    #     record_leaderboard(player, 'wl', first_record)

    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'wl', 'matches', 'emblem', 'id', 'highest_skill', 'wins', 'donation', 'twitch', 'mixer', 'youtube', 'twitter', 'notes', 'color', 'social', 'glow')))

    return render(request, 'leaderboard.html', data)


def best_kd(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'kd',
        'title': 'K/D Ratio',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Player.objects.filter(matches__gt=250, ban=False).order_by('-kd')[first_record:last_record]
    data['index'] = first_record

    # for player in leaderboards:
    #     first_record += 1
    #     record_leaderboard(player, 'kd', first_record)

    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'kd', 'matches', 'emblem', 'id', 'highest_skill', 'wins', 'donation', 'twitch', 'youtube', 'mixer', 'twitter', 'notes', 'color', 'social', 'glow')))

    return render(request, 'leaderboard.html', data)


def most_playtime(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'playtime',
        'title': 'Playtime',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Player.objects.filter(ban=False).order_by('-epoch')[first_record:last_record]
    data['index'] = first_record

    # for player in leaderboards:
    #     first_record += 1
    #     record_leaderboard(player, 'epoch', first_record)

    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'matches', 'emblem', 'id', 'playtime', 'epoch', 'donation', 'twitch', 'mixer', 'youtube', 'twitter', 'notes', 'color', 'social', 'glow')))

    return render(request, 'leaderboard.html', data)


def all_most_50s(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_50s',
        'title': "(All Platforms) Most 50's",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

        if page > 1:
            data['rank'] = 3

    sorted_50s = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__matches', 'h3_team_slayer',
                                                 'h3_team_hardcore', 'h3_team_doubles', 'ms_2v2_series',
                                                 'hce_hardcore_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore',
                                                 'halo_reach_invasion', 'halo_reach_team_slayer', 'pc_ranks__halo_reach_team_hardcore',
                                                 'pc_ranks__halo_reach_invasion', 'pc_ranks__halo_reach_team_slayer', 'player__emblem',
                                                 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter',
                                                 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-player__matches'))

    list_50s = []
    playlists = ['h3_team_slayer', 'h3_team_hardcore', 'h3_team_doubles', 'ms_2v2_series', 'hce_hardcore_doubles', 'h2c_team_hardcore',
                 'halo_reach_team_hardcore', 'halo_reach_invasion', 'halo_reach_team_slayer', 'pc_ranks__halo_reach_team_hardcore',
                 'pc_ranks__halo_reach_invasion', 'pc_ranks__halo_reach_team_slayer']

    for player in sorted_50s:
        fifty = 0

        for playlist in playlists:
            if player[playlist] == 50:
                fifty += 1

        player['fifty'] = fifty

        if fifty > 0:
            list_50s.append(player)

    data['leaderboard'] = json.dumps(sort_list(list_50s, 'fifty')[first_record:last_record])
    data['index'] = first_record

    return render(request, 'leaderboard.html', data)


def xbox_most_50s(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_50s',
        'title': "(Xbox) Most 50's",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

        if page > 1:
            data['rank'] = 3

    sorted_50s = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__matches', 'h3_team_slayer',
                                                 'h3_team_hardcore', 'h3_team_doubles', 'ms_2v2_series',
                                                 'hce_hardcore_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore',
                                                 'halo_reach_invasion', 'halo_reach_team_slayer', 'player__emblem',
                                                 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter',
                                                 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-player__matches'))

    list_50s = []
    playlists = ['h3_team_slayer', 'h3_team_hardcore', 'h3_team_doubles', 'ms_2v2_series', 'hce_hardcore_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore', 'halo_reach_invasion', 'halo_reach_team_slayer']

    for player in sorted_50s:
        fifty = 0

        for playlist in playlists:
            if player[playlist] == 50:
                fifty += 1

        player['fifty'] = fifty

        if fifty > 0:
            list_50s.append(player)

    data['leaderboard'] = json.dumps(sort_list(list_50s, 'fifty')[first_record:last_record])
    data['index'] = first_record

    return render(request, 'leaderboard.html', data)


def pc_most_50s(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_50s',
        'title': "(PC) Most 50's",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

        if page > 1:
            data['rank'] = 3

    sorted_50s = list(PcRanks.objects.filter(player__ban=False).values('player__gamertag', 'player__matches', 'halo_reach_team_hardcore',
                                                   'halo_reach_invasion', 'halo_reach_team_slayer', 'player__emblem',
                                                   'player__donation', 'player__twitch', 'player__youtube', 'player__twitter',
                                                   'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-player__matches'))

    list_50s = []
    playlists = ['halo_reach_team_hardcore', 'halo_reach_invasion', 'halo_reach_team_slayer']

    for player in sorted_50s:
        fifty = 0

        for playlist in playlists:
            if player[playlist] == 50:
                fifty += 1

        player['fifty'] = fifty

        if fifty > 0:
            list_50s.append(player)

    data['leaderboard'] = json.dumps(sort_list(list_50s, 'fifty')[first_record:last_record])
    data['index'] = first_record

    return render(request, 'leaderboard.html', data)


# PLAYLIST
def h3_team_slayer(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'h3_team_slayer',
        'title': "Halo 3: Team Slayer",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'h3_team_slayer', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-h3_team_slayer', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    # for rank_player in rank_list:
    #     first_record += 1
    #     record_leaderboard(int(rank_player['player__id']), 'h3_team_slayer', first_record)

    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def h3_team_hardcore(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'h3_team_hardcore',
        'title': "Halo 3: Team Hardcore",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'h3_team_hardcore', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-h3_team_hardcore', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    # for rank_player in rank_list:
    #     first_record += 1
    #     record_leaderboard(int(rank_player['player__id']), 'h3_team_hardcore', first_record)

    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def h3_team_doubles(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'h3_team_doubles',
        'title': "Halo 3: Team Doubles",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'h3_team_doubles', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-h3_team_doubles', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    # for rank_player in rank_list:
    #     first_record += 1
    #     record_leaderboard(int(rank_player['player__id']), 'h3_team_doubles', first_record)

    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def ms_2v2_series(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'ms_2v2_series',
        'title': "Halo 3: MS 2v2 Series",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'ms_2v2_series', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-ms_2v2_series', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    # for rank_player in rank_list:
    #     first_record += 1
    #     record_leaderboard(int(rank_player['player__id']), 'ms_2v2_series', first_record)

    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def hce_hardcore_doubles(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'hce_hardcore_doubles',
        'title': "(Xbox) Halo 1: Hardcore Doubles",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'hce_hardcore_doubles', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-hce_hardcore_doubles', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    # for rank_player in rank_list:
    #     first_record += 1
    #     record_leaderboard(int(rank_player['player__id']), 'hce_hardcore_doubles', first_record)

    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def h2c_team_hardcore(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'h2c_team_hardcore',
        'title': "Halo 2 Classic: Team Hardcore",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'h2c_team_hardcore', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-h2c_team_hardcore', '-player__matches')[first_record:last_record])
    data['index'] = first_record
    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def halo_reach_team_hardcore(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'halo_reach_team_hardcore',
        'title': "(Xbox) Reach: Team Hardcore",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'halo_reach_team_hardcore', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-halo_reach_team_hardcore', '-player__matches')[first_record:last_record])
    data['index'] = first_record
    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def halo_reach_invasion(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'halo_reach_invasion',
        'title': "(Xbox) Reach: Team Invasion",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'halo_reach_invasion', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-halo_reach_invasion', '-player__matches')[first_record:last_record])
    data['index'] = first_record
    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def halo_reach_team_slayer(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'halo_reach_team_slayer',
        'title': "(Xbox) Reach: Team Slayer",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'halo_reach_team_slayer', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-halo_reach_team_slayer', '-player__matches')[first_record:last_record])
    data['index'] = first_record
    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def pc_reach_team_hardcore(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'halo_reach_team_hardcore',
        'title': "(PC) Reach: Team Hardcore",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0,
        'platform': 'pc_'
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(PcRanks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'halo_reach_team_hardcore', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-halo_reach_team_hardcore', '-player__matches')[first_record:last_record])
    data['index'] = first_record
    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def pc_reach_invasion(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'halo_reach_invasion',
        'title': "(PC) Reach: Team Invasion",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0,
        'platform': 'pc_'
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(PcRanks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'halo_reach_invasion', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-halo_reach_invasion', '-player__matches')[first_record:last_record])
    data['index'] = first_record
    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def pc_reach_team_slayer(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'halo_reach_team_slayer',
        'title': "(PC) Reach: Team Slayer",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0,
        'platform': 'pc_'
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(PcRanks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'halo_reach_team_slayer', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-halo_reach_team_slayer', '-player__matches')[first_record:last_record])
    data['index'] = first_record
    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def pc_hce_hardcore_doubles(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'hce_hardcore_doubles',
        'title': "(PC) Halo 1: Hardcore Doubles",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0,
        'platform': 'pc_'
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(PcRanks.objects.filter(player__ban=False).values('player__gamertag', 'player__id', 'player__matches', 'hce_hardcore_doubles', 'player__emblem', 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow').order_by('-hce_hardcore_doubles', '-player__matches')[first_record:last_record])
    data['index'] = first_record
    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)
