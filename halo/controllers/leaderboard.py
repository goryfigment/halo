import json
from django.shortcuts import render
from base import sort_list, get_base_url, models_to_dict
from django.db.models import F
from halo.models import Player, Ranks, Leaderboard, PcRanks, Season1, Season2, Season3, Season4, Season5, NewRanks, NewPcRanks
from django.http import JsonResponse


def record_leaderboard(player_id, attr_type, rank):
    leaderboard = Leaderboard.objects.filter(player_id=player_id)

    if leaderboard.exists():
        leaderboard = leaderboard[0]
    else:
        leaderboard = Leaderboard.objects.create(player_id=player_id)

    setattr(leaderboard, attr_type, rank)
    leaderboard.save()


# Gives ranks to database
def update_leaderboard(request):
    query_request = json.loads(request.body)
    leaderboards = query_request['leaderboards']
    index = query_request['index']

    for player in leaderboards:
        index += 1

        if 'id' in player:
            player_id = player['id']
        elif 'player__id' in player:
            player_id = player['player__id']
        elif 'player_id' in player:
            player_id = player['player_id']
        else:
            player_id = player['p_id']

        record_leaderboard(player_id, query_request['type'], index)

    print query_request['type']

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
        elif 'player__id' in player:
            player_id = player['player__id']
        elif 'player_id' in player:
            player_id = player['player_id']
        else:
            player_id = player['p_id']

        if type == 'epoch':
            type = 'playtime'

        record_leaderboard(player_id, type, index)

    return render(request, 'leaderboard.html', {'leaderboards': leaderboards})


def service_func(request, handlebars, amount_type, title):
    first_record = 0
    last_record = 100

    data = {
        'type': amount_type,
        'handlebars': handlebars,
        'title': title,
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    if amount_type == 'wl' or amount_type == 'kd':
        data['leaderboard'] = json.dumps(list(Player.objects.filter(matches__gte=1000, ban=False).values(amount=F(amount_type), exp=F('wins'), p_gamertag=F('gamertag'), p_id=F('id'), p_emblem=F('emblem'), p_donation=F('donation'), p_twitch=F('twitch'), p_youtube=F('youtube'), p_twitter=F('twitter'), p_notes=F('notes'), p_color=F('color'),  p_social=F('social'), p_mixer=F('mixer'), highest_rank=F('highest_skill'), p_glow=F('glow'), p_rgb=F('rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    elif amount_type == 'donation':
        data['leaderboard'] = json.dumps(list(Player.objects.filter(donation__gt=0).values(amount=F(amount_type), exp=F('wins'), p_gamertag=F('gamertag'), p_id=F('id'), p_emblem=F('emblem'), p_donation=F('donation'), p_twitch=F('twitch'), p_youtube=F('youtube'), p_twitter=F('twitter'), p_notes=F('notes'), p_color=F('color'),  p_social=F('social'), p_mixer=F('mixer'), p_glow=F('glow'), p_rgb=F('rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    else:
        data['leaderboard'] = json.dumps(list(Player.objects.filter(ban=False).values(amount=F(amount_type), exp=F('wins'), p_gamertag=F('gamertag'), p_id=F('id'), p_emblem=F('emblem'), p_donation=F('donation'), p_twitch=F('twitch'), p_youtube=F('youtube'), p_twitter=F('twitter'), p_notes=F('notes'), p_color=F('color'),  p_social=F('social'), p_mixer=F('mixer'), p_glow=F('glow'), p_rgb=F('rgb')).order_by('-amount', '-exp')[first_record:last_record]))

    data['index'] = first_record

    return data


def most_donations(request):
    return render(request, 'leaderboard.html', service_func(request, 'player', 'donation', 'Donation'))


def most_kills(request):
    return render(request, 'leaderboard.html', service_func(request, 'player', 'kills', 'Kills'))


def most_deaths(request):
    return render(request, 'leaderboard.html', service_func(request, 'player', 'deaths', 'Deaths'))


def most_wins(request):
    return render(request, 'leaderboard.html', service_func(request, 'player', 'wins', 'Wins'))


def most_losses(request):
    return render(request, 'leaderboard.html', service_func(request, 'player', 'losses', 'Losses'))


def most_matches(request):
    return render(request, 'leaderboard.html', service_func(request, 'player', 'matches', 'Matches'))


def best_wl(request):
    return render(request, 'leaderboard.html', service_func(request, 'player_ratio', 'wl', 'W/L Ratio'))


def best_kd(request):
    return render(request, 'leaderboard.html', service_func(request, 'player_ratio', 'kd', 'K/D Ratio'))


def most_assists(request):
    return render(request, 'leaderboard.html', service_func(request, 'player', 'assists', 'Assists'))


def most_betrayals(request):
    return render(request, 'leaderboard.html', service_func(request, 'player', 'betrayals', 'Betrayals'))


def most_headshots(request):
    return render(request, 'leaderboard.html', service_func(request, 'player', 'headshots', 'Headshots'))


def most_playtime(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'playtime',
        'handlebars': 'playtime',
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
    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'matches', 'emblem', 'id', 'playtime', 'epoch', 'donation', 'twitch', 'mixer', 'youtube', 'twitter', 'notes', 'color', 'social', 'glow', 'rgb')))

    return render(request, 'leaderboard.html', data)


# OLD PLAYLIST
def old_all_most_50s(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_50s',
        'handlebars': 'most_50s',
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
                                                 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow', 'player__rgb').order_by('-player__matches'))

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


def old_xbox_most_50s(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_50s',
        'handlebars': 'most_50s',
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
                                                 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow', 'player__rgb').order_by('-player__matches'))

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


def old_pc_most_50s(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_50s',
        'handlebars': 'most_50s',
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
                                                   'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow', 'player__rgb').order_by('-player__matches'))

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


def old_rank_func(request, handlebars, amount_type, title):
    first_record = 0
    last_record = 100

    data = {
        'type': 'old_' + amount_type,
        'handlebars': handlebars,
        'title': title,
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    if 'pc_' in amount_type:
        amount_type = amount_type.replace('pc_', '')
        data['leaderboard'] = json.dumps(list(PcRanks.objects.filter(player__ban=False).values(amount=F(amount_type), verified=F('v_'+amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('player__wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb')).order_by('-amount', '-verified', '-exp')[first_record:last_record]))
    else:
        data['leaderboard'] = json.dumps(list(Ranks.objects.filter(player__ban=False).values(amount=F(amount_type), verified=F('v_'+amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('player__wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb')).order_by('-amount', '-verified', '-exp')[first_record:last_record]))
    data['index'] = first_record

    return data


def old_h3_team_slayer(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'h3_team_slayer', '(Xbox) Halo 3: Team Slayer'))


def old_h3_team_hardcore(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'h3_team_hardcore', '(Xbox) Halo 3: Team Hardcore'))


def old_h3_team_doubles(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'h3_team_doubles', '(Xbox) Halo 3: Team Doubles'))


def old_ms_2v2_series(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'ms_2v2_series', '(Xbox) Halo 3: MS 2v2 Series'))


def old_hce_team_doubles(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'hce_team_doubles', '(Xbox) Halo 1: Team Doubles'))


def old_hce_hardcore_doubles(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'hce_hardcore_doubles', '(Xbox) Halo 1: Hardcore Doubles'))


def old_h2c_team_hardcore(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'h2c_team_hardcore', '(Xbox) Halo 2 Classic: Team Hardcore'))


def old_h2a_team_hardcore(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'h2a_team_hardcore', '(Xbox) H2A: Team Hardcore'))


def old_halo_reach_team_hardcore(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'halo_reach_team_hardcore', '(Xbox) Reach: Team Hardcore'))


def old_halo_reach_invasion(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'halo_reach_invasion', '(Xbox) Reach: Team Invasion'))


def old_halo_reach_team_slayer(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'halo_reach_team_slayer', '(Xbox) Reach: Team Slayer'))


# PC
def old_pc_reach_team_hardcore(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'pc_halo_reach_team_hardcore', '(PC) Reach: Team Hardcore'))


def old_pc_reach_invasion(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'pc_halo_reach_invasion', '(PC) Reach: Team Invasion'))


def old_pc_reach_team_slayer(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'pc_halo_reach_team_slayer', '(PC) Reach: Team Slayer'))


def old_pc_hce_hardcore_doubles(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'pc_hce_hardcore_doubles', '(PC) Halo 1: Hardcore Doubles'))


def old_pc_h2c_team_hardcore(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'pc_h2c_team_hardcore', '(PC) Halo 2 Classic: Team Hardcore'))


def old_pc_h2a_team_hardcore(request):
    return render(request, 'leaderboard.html', old_rank_func(request, 'playlist', 'pc_h2a_team_hardcore', '(PC) H2A: Team Hardcore'))
# OLD PLAYLIST


# NEW PLAYLIST
def all_most_50s(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_50s',
        'handlebars': 'most_50s',
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

    sorted_50s = list(NewRanks.objects.filter(player__ban=False).values('player__gamertag', 'player__matches', 'h3_team_slayer', 'h3_team_hardcore', 'h3_team_doubles', 'h2a_team_hardcore', 'hce_hardcore_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore', 'halo_reach_invasion',
    'pc_ranks__h3_team_slayer', 'pc_ranks__h3_team_hardcore', 'pc_ranks__h3_team_doubles', 'pc_ranks__h2a_team_hardcore', 'pc_ranks__hce_hardcore_doubles', 'pc_ranks__h2c_team_hardcore', 'pc_ranks__halo_reach_team_hardcore', 'pc_ranks__halo_reach_invasion',
                                                 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__emblem',
                                                 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow', 'player__rgb').order_by('-player__matches'))

    list_50s = []
    playlists = ['h3_team_slayer', 'h3_team_hardcore', 'h3_team_doubles', 'h2a_team_hardcore', 'hce_hardcore_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore', 'halo_reach_invasion',
    'pc_ranks__h3_team_slayer', 'pc_ranks__h3_team_hardcore', 'pc_ranks__h3_team_doubles', 'pc_ranks__h2a_team_hardcore', 'pc_ranks__hce_hardcore_doubles', 'pc_ranks__h2c_team_hardcore', 'pc_ranks__halo_reach_team_hardcore', 'pc_ranks__halo_reach_invasion',]

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
        'handlebars': 'most_50s',
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

    sorted_50s = list(NewRanks.objects.filter(player__ban=False).values('h3_team_slayer', 'h3_team_hardcore', 'h3_team_doubles', 'h2a_team_hardcore', 'hce_hardcore_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore', 'halo_reach_invasion',
                                                 'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__emblem', 'player__gamertag', 'player__matches',
                                                 'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow', 'player__rgb').order_by('-player__matches'))

    list_50s = []
    playlists = ['h3_team_slayer', 'h3_team_hardcore', 'h3_team_doubles', 'h2a_team_hardcore', 'hce_hardcore_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore', 'halo_reach_invasion']

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
        'handlebars': 'most_50s',
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

    sorted_50s = list(NewPcRanks.objects.filter(player__ban=False).values(
                                                   'h3_team_slayer', 'h3_team_hardcore', 'h3_team_doubles', 'h2a_team_hardcore', 'hce_hardcore_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore', 'halo_reach_invasion',
                                                   'player__donation', 'player__twitch', 'player__youtube', 'player__twitter', 'player__emblem', 'player__gamertag', 'player__matches',
                                                   'player__notes', 'player__color', 'player__social', 'player__mixer', 'player__glow', 'player__rgb').order_by('-player__matches'))

    list_50s = []
    playlists = ['h3_team_slayer', 'h3_team_hardcore', 'h3_team_doubles', 'h2a_team_hardcore', 'hce_hardcore_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore', 'halo_reach_invasion']

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


def rank_func(request, handlebars, amount_type, title, first, last):
    first_record = first
    last_record = last

    data = {
        'type': 'new_' + amount_type,
        'handlebars': handlebars,
        'title': title,
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    if 'pc_' in amount_type:
        amount_type = amount_type.replace('pc_', '')
        data['leaderboard'] = json.dumps(list(NewPcRanks.objects.filter(player__ban=False).values(amount=F(amount_type), verified=F('v_'+amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('player__wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb')).order_by('-amount', '-verified', '-exp')[first_record:last_record]))
    else:
        data['leaderboard'] = json.dumps(list(NewRanks.objects.filter(player__ban=False).values(amount=F(amount_type), verified=F('v_'+amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('player__wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb')).order_by('-amount', '-verified', '-exp')[first_record:last_record]))
    data['index'] = first_record

    return data


def h3_team_slayer(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'h3_team_slayer', '(Xbox) Halo 3: Team Slayer', 0, 100))


def h3_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'h3_team_hardcore', '(Xbox) Halo 3: Team Hardcore', 0, 100))


def h3_team_doubles(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'h3_team_doubles', '(Xbox) Halo 3: Team Doubles', 0, 100))


def hce_hardcore_doubles(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'hce_hardcore_doubles', '(Xbox) Halo 1: Hardcore Doubles', 0, 100))


def h2c_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'h2c_team_hardcore', '(Xbox) Halo 2 Classic: Team Hardcore', 0, 100))


def h2a_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'h2a_team_hardcore', '(Xbox) H2A: Team Hardcore', 0, 100))


def halo_reach_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'halo_reach_team_hardcore', '(Xbox) Reach: Team Hardcore', 0, 100))


def halo_reach_invasion(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'halo_reach_invasion', '(Xbox) Reach: Team Invasion', 0, 100))


# PC
def pc_h3_team_slayer(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_h3_team_slayer', '(PC) Halo 3: Team Slayer', 0, 100))


def pc_h3_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_h3_team_hardcore', '(PC) Halo 3: Team Hardcore', 0, 100))


def pc_h3_team_doubles(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_h3_team_doubles', '(PC) Halo 3: Team Doubles', 0, 100))


def pc_halo_reach_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_halo_reach_team_hardcore', '(PC) Reach: Team Hardcore', 0, 100))


def pc_halo_reach_invasion(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_halo_reach_invasion', '(PC) Reach: Team Invasion', 0, 100))


def pc_hce_hardcore_doubles(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_hce_hardcore_doubles', '(PC) Halo 1: Hardcore Doubles', 0, 100))


def pc_h2c_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_h2c_team_hardcore', '(PC) Halo 2 Classic: Team Hardcore', 0, 100))


def pc_h2a_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_h2a_team_hardcore', '(PC) H2A: Team Hardcore', 0, 100))
# NEW PLAYLIST


def season1_func(request, handlebars, amount_type, title, first=None, last=None):
    if first is not None and last is not None:
        first_record = first
        last_record = last
    else:
        first_record = 0
        last_record = 100

    data = {
        'type': 's1_' + amount_type,
        'handlebars': handlebars,
        'title': title,
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0,
        'season': 1
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page
    if amount_type == 'wl' or amount_type == 'kd':
        data['leaderboard'] = json.dumps(list(Season1.objects.filter(matches__gte=250, player__ban=False).values(amount=F(amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), highest_rank=F('player__highest_skill'), rgb=F('player__rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    else:
        data['leaderboard'] = json.dumps(list(Season1.objects.filter(player__ban=False).values(amount=F(amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), highest_rank=F('player__highest_skill'), rgb=F('player__rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    data['index'] = first_record

    return data


def season1_playtime_func(request, first, last):
    first_record = first
    last_record = last

    data = {
        'type': 's1_playtime',
        'handlebars': 'playtime',
        'title': '(Season 1) Playtime',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Season1.objects.filter(player__ban=False).order_by('-epoch')[first_record:last_record]
    data['index'] = first_record
    data['leaderboard'] = json.dumps(list(leaderboards.values('playtime', gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb'))))

    return data


def s1_score(request):
    return render(request, 'leaderboard.html', season1_func(request, 'mccs', 'score', '(Season 1) MCC Score'))


def s1_kills(request):
    return render(request, 'leaderboard.html', season1_func(request, 'season1', 'kills', '(Season 1) Kills'))


def s1_deaths(request):
    return render(request, 'leaderboard.html', season1_func(request, 'season1', 'deaths', '(Season 1) Deaths'))


def s1_wins(request):
    return render(request, 'leaderboard.html', season1_func(request, 'season1', 'wins', '(Season 1) Wins'))


def s1_losses(request):
    return render(request, 'leaderboard.html', season1_func(request, 'season1', 'losses', '(Season 1) Losses'))


def s1_matches(request):
    return render(request, 'leaderboard.html', season1_func(request, 'season1', 'matches', '(Season 1) Matches'))


def s1_wl(request):
    return render(request, 'leaderboard.html', season1_func(request, 'season1_ratio', 'wl', '(Season 1) W/L Ratio'))


def s1_kd(request):
    return render(request, 'leaderboard.html', season1_func(request, 'season1_ratio', 'kd', '(Season 1) K/D Ratio'))


def s1_playtime(request):
    return render(request, 'leaderboard.html', season1_playtime_func(request, 0, 100))


def season2_func(request, handlebars, amount_type, title, first=None, last=None):
    if first is not None and last is not None:
        first_record = first
        last_record = last
    else:
        first_record = 0
        last_record = 100

    data = {
        'type': 's2_' + amount_type,
        'handlebars': handlebars,
        'title': title,
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0,
        'season': 2
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page
    if amount_type == 'wl' or amount_type == 'kd':
        data['leaderboard'] = json.dumps(list(Season2.objects.filter(matches__gte=250, player__ban=False).values(amount=F(amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), highest_rank=F('player__highest_skill'), rgb=F('player__rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    else:
        data['leaderboard'] = json.dumps(list(Season2.objects.filter(player__ban=False).values(amount=F(amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), highest_rank=F('player__highest_skill'), rgb=F('player__rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    data['index'] = first_record

    return data


def season2_playtime_func(request, first, last):
    first_record = first
    last_record = last

    data = {
        'type': 's2_playtime',
        'handlebars': 'playtime',
        'title': '(Season 2) Playtime',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Season2.objects.filter(player__ban=False).order_by('-epoch')[first_record:last_record]
    data['index'] = first_record
    data['leaderboard'] = json.dumps(list(leaderboards.values('playtime', gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb'))))

    return data


def s2_score(request):
    return render(request, 'leaderboard.html', season2_func(request, 'mccs', 'score', '(Season 2) MCC Score'))


def s2_kills(request):
    return render(request, 'leaderboard.html', season2_func(request, 'season1', 'kills', '(Season 2) Kills'))


def s2_deaths(request):
    return render(request, 'leaderboard.html', season2_func(request, 'season1', 'deaths', '(Season 2) Deaths'))


def s2_wins(request):
    return render(request, 'leaderboard.html', season2_func(request, 'season1', 'wins', '(Season 2) Wins'))


def s2_losses(request):
    return render(request, 'leaderboard.html', season2_func(request, 'season1', 'losses', '(Season 2) Losses'))


def s2_matches(request):
    return render(request, 'leaderboard.html', season2_func(request, 'season1', 'matches', '(Season 2) Matches'))


def s2_wl(request):
    return render(request, 'leaderboard.html', season2_func(request, 'season1_ratio', 'wl', '(Season 2) W/L Ratio'))


def s2_kd(request):
    return render(request, 'leaderboard.html', season2_func(request, 'season1_ratio', 'kd', '(Season 2) K/D Ratio'))


def s2_playtime(request):
    return render(request, 'leaderboard.html', season2_playtime_func(request, 0, 100))


def season3_func(request, handlebars, amount_type, title, first=None, last=None):
    if first is not None and last is not None:
        first_record = first
        last_record = last
    else:
        first_record = 0
        last_record = 100

    data = {
        'type': 's3_' + amount_type,
        'handlebars': handlebars,
        'title': title,
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0,
        'season': 3
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page
    if amount_type == 'wl' or amount_type == 'kd':
        data['leaderboard'] = json.dumps(list(Season3.objects.filter(matches__gte=250, player__ban=False).values(amount=F(amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), highest_rank=F('player__highest_skill'), rgb=F('player__rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    else:
        data['leaderboard'] = json.dumps(list(Season3.objects.filter(player__ban=False).values(amount=F(amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), highest_rank=F('player__highest_skill'), rgb=F('player__rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    data['index'] = first_record

    return data


def season3_playtime_func(request, first, last):
    first_record = first
    last_record = last

    data = {
        'type': 's3_playtime',
        'handlebars': 'playtime',
        'title': '(Season 4) Playtime',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Season3.objects.filter(player__ban=False).order_by('-epoch')[first_record:last_record]
    data['index'] = first_record
    data['leaderboard'] = json.dumps(list(leaderboards.values('playtime', gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb'))))

    return data


def s3_score(request):
    return render(request, 'leaderboard.html', season3_func(request, 'mccs', 'score', '(Season 3) MCC Score'))


def s3_kills(request):
    return render(request, 'leaderboard.html', season3_func(request, 'season1', 'kills', '(Season 3) Kills'))


def s3_deaths(request):
    return render(request, 'leaderboard.html', season3_func(request, 'season1', 'deaths', '(Season 3) Deaths'))


def s3_wins(request):
    return render(request, 'leaderboard.html', season3_func(request, 'season1', 'wins', '(Season 3) Wins'))


def s3_losses(request):
    return render(request, 'leaderboard.html', season3_func(request, 'season1', 'losses', '(Season 3) Losses'))


def s3_matches(request):
    return render(request, 'leaderboard.html', season3_func(request, 'season1', 'matches', '(Season 3) Matches'))


def s3_wl(request):
    return render(request, 'leaderboard.html', season3_func(request, 'season1_ratio', 'wl', '(Season 3) W/L Ratio'))


def s3_kd(request):
    return render(request, 'leaderboard.html', season3_func(request, 'season1_ratio', 'kd', '(Season 3) K/D Ratio'))


def s3_assists(request):
    return render(request, 'leaderboard.html', season3_func(request, 'season1', 'assists', '(Season 3) Assists'))


def s3_betrayals(request):
    return render(request, 'leaderboard.html', season3_func(request, 'season1', 'betrayals', '(Season 3) Betrayals'))


def s3_headshots(request):
    return render(request, 'leaderboard.html', season3_func(request, 'season1', 'headshots', '(Season 3) Headshots'))


def s3_playtime(request):
    return render(request, 'leaderboard.html', season3_playtime_func(request, 0, 100))


def season4_func(request, handlebars, amount_type, title, first=None, last=None):
    if first is not None and last is not None:
        first_record = first
        last_record = last
    else:
        first_record = 0
        last_record = 100

    data = {
        'type': 's4_' + amount_type,
        'handlebars': handlebars,
        'title': title,
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0,
        'season': 4
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page
    if amount_type == 'wl' or amount_type == 'kd':
        data['leaderboard'] = json.dumps(list(Season4.objects.filter(matches__gte=250, player__ban=False).values(amount=F(amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), highest_rank=F('player__highest_skill'), rgb=F('player__rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    else:
        data['leaderboard'] = json.dumps(list(Season4.objects.filter(player__ban=False).values(amount=F(amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), highest_rank=F('player__highest_skill'), rgb=F('player__rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    data['index'] = first_record

    return data


def season4_playtime_func(request, first, last):
    first_record = first
    last_record = last

    data = {
        'type': 's4_playtime',
        'handlebars': 'playtime',
        'title': '(Season 4) Playtime',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Season4.objects.filter(player__ban=False).order_by('-epoch')[first_record:last_record]
    data['index'] = first_record
    data['leaderboard'] = json.dumps(list(leaderboards.values('playtime', gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb'))))

    return data


def s4_score(request):
    return render(request, 'leaderboard.html', season4_func(request, 'mccs', 'score', '(Season 4) MCC Score'))


def s4_kills(request):
    return render(request, 'leaderboard.html', season4_func(request, 'season1', 'kills', '(Season 4) Kills'))


def s4_deaths(request):
    return render(request, 'leaderboard.html', season4_func(request, 'season1', 'deaths', '(Season 4) Deaths'))


def s4_wins(request):
    return render(request, 'leaderboard.html', season4_func(request, 'season1', 'wins', '(Season 4) Wins'))


def s4_losses(request):
    return render(request, 'leaderboard.html', season4_func(request, 'season1', 'losses', '(Season 4) Losses'))


def s4_matches(request):
    return render(request, 'leaderboard.html', season4_func(request, 'season1', 'matches', '(Season 4) Matches'))


def s4_wl(request):
    return render(request, 'leaderboard.html', season4_func(request, 'season1_ratio', 'wl', '(Season 4) W/L Ratio'))


def s4_kd(request):
    return render(request, 'leaderboard.html', season4_func(request, 'season1_ratio', 'kd', '(Season 4) K/D Ratio'))


def s4_assists(request):
    return render(request, 'leaderboard.html', season4_func(request, 'season1', 'assists', '(Season 4) Assists'))


def s4_betrayals(request):
    return render(request, 'leaderboard.html', season4_func(request, 'season1', 'betrayals', '(Season 4) Betrayals'))


def s4_headshots(request):
    return render(request, 'leaderboard.html', season4_func(request, 'season1', 'headshots', '(Season 4) Headshots'))


def s4_playtime(request):
    return render(request, 'leaderboard.html', season4_playtime_func(request, 0, 100))


def season5_func(request, handlebars, amount_type, title, first=None, last=None):
    if first is not None and last is not None:
        first_record = first
        last_record = last
    else:
        first_record = 0
        last_record = 100

    data = {
        'type': 's5_' + amount_type,
        'handlebars': handlebars,
        'title': title,
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0,
        'season': 5
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page
    if amount_type == 'wl' or amount_type == 'kd':
        data['leaderboard'] = json.dumps(list(Season5.objects.filter(matches__gte=250, player__ban=False).values(amount=F(amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), highest_rank=F('player__highest_skill'), rgb=F('player__rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    else:
        data['leaderboard'] = json.dumps(list(Season5.objects.filter(player__ban=False).values(amount=F(amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), highest_rank=F('player__highest_skill'), rgb=F('player__rgb')).order_by('-amount', '-exp')[first_record:last_record]))
    data['index'] = first_record

    return data


def season5_playtime_func(request, first, last):
    first_record = first
    last_record = last

    data = {
        'type': 's5_playtime',
        'handlebars': 'playtime',
        'title': '(Season 5) Playtime',
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    leaderboards = Season5.objects.filter(player__ban=False).order_by('-epoch')[first_record:last_record]
    data['index'] = first_record
    data['leaderboard'] = json.dumps(list(leaderboards.values('playtime', gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb'))))

    return data


def s5_score(request):
    return render(request, 'leaderboard.html', season5_func(request, 'mccs', 'score', '(Season 5) MCC Score'))


def s5_kills(request):
    return render(request, 'leaderboard.html', season5_func(request, 'season1', 'kills', '(Season 5) Kills'))


def s5_deaths(request):
    return render(request, 'leaderboard.html', season5_func(request, 'season1', 'deaths', '(Season 5) Deaths'))


def s5_wins(request):
    return render(request, 'leaderboard.html', season5_func(request, 'season1', 'wins', '(Season 5) Wins'))


def s5_losses(request):
    return render(request, 'leaderboard.html', season5_func(request, 'season1', 'losses', '(Season 5) Losses'))


def s5_matches(request):
    return render(request, 'leaderboard.html', season5_func(request, 'season1', 'matches', '(Season 5) Matches'))


def s5_wl(request):
    return render(request, 'leaderboard.html', season5_func(request, 'season1_ratio', 'wl', '(Season 5) W/L Ratio'))


def s5_kd(request):
    return render(request, 'leaderboard.html', season5_func(request, 'season1_ratio', 'kd', '(Season 5) K/D Ratio'))


def s5_assists(request):
    return render(request, 'leaderboard.html', season5_func(request, 'season1', 'assists', '(Season 5) Assists'))


def s5_betrayals(request):
    return render(request, 'leaderboard.html', season5_func(request, 'season1', 'betrayals', '(Season 5) Betrayals'))


def s5_headshots(request):
    return render(request, 'leaderboard.html', season5_func(request, 'season1', 'headshots', '(Season 5) Headshots'))


def s5_playtime(request):
    return render(request, 'leaderboard.html', season5_playtime_func(request, 0, 100))
