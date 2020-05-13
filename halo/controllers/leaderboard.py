import json
from django.shortcuts import render
from base import sort_list, get_base_url, models_to_dict
from django.db.models import F
from halo.models import Player, Ranks, Leaderboard, PcRanks, Season1, Season2
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


# PLAYLIST
def rank_func(request, handlebars, amount_type, title):
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

    if 'pc_' in amount_type:
        amount_type = amount_type.replace('pc_', '')
        data['leaderboard'] = json.dumps(list(PcRanks.objects.filter(player__ban=False).values(amount=F(amount_type), verified=F('v_'+amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('player__wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb')).order_by('-amount', '-verified', '-exp')[first_record:last_record]))
    else:
        data['leaderboard'] = json.dumps(list(Ranks.objects.filter(player__ban=False).values(amount=F(amount_type), verified=F('v_'+amount_type), gamertag=F('player__gamertag'), player_id=F('player__id'), exp=F('player__wins'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb')).order_by('-amount', '-verified', '-exp')[first_record:last_record]))
    data['index'] = first_record

    return data


def h3_team_slayer(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'h3_team_slayer', 'Halo 3: Team Slayer'))


def h3_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'h3_team_hardcore', 'Halo 3: Team Hardcore'))


def h3_team_doubles(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'h3_team_doubles', 'Halo 3: Team Doubles'))


def ms_2v2_series(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'ms_2v2_series', 'Halo 3: MS 2v2 Series'))


def hce_team_doubles(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'hce_team_doubles', '(Xbox) Halo 1: Team Doubles'))


def hce_hardcore_doubles(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'hce_hardcore_doubles', '(Xbox) Halo 1: Hardcore Doubles'))


def h2c_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'h2c_team_hardcore', 'Halo 2 Classic: Team Hardcore'))


def halo_reach_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'halo_reach_team_hardcore', '(Xbox) Reach: Team Hardcore'))


def halo_reach_invasion(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'halo_reach_invasion', '(Xbox) Reach: Team Invasion'))


def halo_reach_team_slayer(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'halo_reach_team_slayer', '(Xbox) Reach: Team Slayer'))


# PC
def pc_reach_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_halo_reach_team_hardcore', '(PC) Reach: Team Hardcore'))


def pc_reach_invasion(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_halo_reach_invasion', '(PC) Reach: Team Invasion'))


def pc_reach_team_slayer(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_halo_reach_team_slayer', '(PC) Reach: Team Slayer'))


def pc_hce_hardcore_doubles(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_hce_hardcore_doubles', '(PC) Halo 1: Hardcore Doubles'))


def pc_h2c_team_hardcore(request):
    return render(request, 'leaderboard.html', rank_func(request, 'playlist', 'pc_h2c_team_hardcore', '(PC) Halo 2 Classic: Team Hardcore'))


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
