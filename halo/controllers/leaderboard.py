import json
from django.shortcuts import render
from base import decimal_format, sort_list, get_base_url, sort_float, model_to_dict
from halo.models import Player, Ranks, Leaderboard


def record_leaderboard(player, attr_type, rank):
    if type(player) == 'int':
        player = Player.objects.get(id=player)

    leaderboard = Leaderboard.objects.filter(player=player)

    if leaderboard.exists():
        leaderboard = leaderboard[0]
    else:
        leaderboard = Leaderboard.objects.create(player=player)

    setattr(leaderboard, attr_type, rank)
    leaderboard.save()


def most_kills(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_kills',
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

    leaderboards = Player.objects.filter(kills__gt=0).order_by('-kills')[first_record:last_record]
    data['index'] = first_record

    for player in leaderboards:
        first_record += 1
        record_leaderboard(player, 'kills', first_record)

    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'kills', 'matches', 'emblem')))

    return render(request, 'leaderboard.html', data)


def most_deaths(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_deaths',
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

    leaderboards = Player.objects.filter(deaths__gt=0).order_by('-deaths')[first_record:last_record]
    data['index'] = first_record

    for player in leaderboards:
        first_record += 1
        record_leaderboard(player, 'deaths', first_record)

    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'deaths', 'matches', 'emblem')))

    return render(request, 'leaderboard.html', data)


def most_wins(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_wins',
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

    leaderboards = Player.objects.filter(wins__gt=0).order_by('-wins')[first_record:last_record]
    data['index'] = first_record

    for player in leaderboards:
        first_record += 1
        record_leaderboard(player, 'wins', first_record)

    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'wins', 'matches', 'emblem')))

    return render(request, 'leaderboard.html', data)


def most_losses(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_losses',
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

    leaderboards = Player.objects.filter(losses__gt=0).order_by('-losses')[first_record:last_record]
    data['index'] = first_record

    for player in leaderboards:
        first_record += 1
        record_leaderboard(player, 'losses', first_record)

    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'losses', 'matches', 'emblem')))

    return render(request, 'leaderboard.html', data)


def most_matches(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_matches',
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

    leaderboards = Player.objects.all().order_by('-matches')[first_record:last_record]
    data['index'] = first_record

    for player in leaderboards:
        first_record += 1
        record_leaderboard(player, 'matches', first_record)

    data['leaderboard'] = json.dumps(list(leaderboards.values('gamertag', 'matches', 'emblem')))

    return render(request, 'leaderboard.html', data)


def best_wl(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'best_wl',
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

    sorted_wl = list(Player.objects.filter(matches__gte=250).values('gamertag', 'wins', 'losses', 'matches', 'emblem', 'id'))

    for player in sorted_wl:
        player['wl_ratio'] = decimal_format(float(player['wins'])/float(player['losses']), 2, False)
        ranks = model_to_dict(Ranks.objects.get(player=player['id']))
        del ranks['player']
        del ranks['id']
        rank_list = []

        for playlist, rank in ranks.iteritems():
            rank_list.append({'rank': rank})

        player['ranks'] = sort_list(rank_list, 'rank')

    sorted_wl = sort_float(sorted_wl, 'wl_ratio')[first_record:last_record]
    data['index'] = first_record

    for player in sorted_wl:
        player_obj = Player.objects.get(id=player['id'])
        first_record += 1
        record_leaderboard(player_obj, 'wl', first_record)

    data['leaderboard'] = json.dumps(sorted_wl)

    return render(request, 'leaderboard.html', data)


def best_kd(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'best_kd',
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

    sorted_kd = list(Player.objects.filter(matches__gte=250).values('gamertag', 'kills', 'deaths', 'matches', 'emblem', 'id', 'wins'))

    for player in sorted_kd:
        player['kd_ratio'] = decimal_format(float(player['kills'])/float(player['deaths']), 2, False)
        ranks = model_to_dict(Ranks.objects.get(player=player['id']))
        del ranks['player']
        del ranks['id']
        rank_list = []

        for playlist, rank in ranks.iteritems():
            rank_list.append({'rank': rank})

        player['ranks'] = sort_list(rank_list, 'rank')

    sorted_kd = sort_float(sorted_kd, 'kd_ratio')[first_record:last_record]
    data['index'] = first_record

    for player in sorted_kd:
        player_obj = Player.objects.get(id=player['id'])
        first_record += 1
        record_leaderboard(player_obj, 'kd', first_record)

    data['leaderboard'] = json.dumps(sorted_kd)

    return render(request, 'leaderboard.html', data)


def most_playtime(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_playtime',
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

    sorted_playtime = list(Player.objects.all().values('gamertag', 'playtime', 'matches', 'emblem', 'id'))

    playtime_list = []

    for player in sorted_playtime:
        playtime = player['playtime'].replace(' hours', '').replace(' days ', '')
        epoch_hours = int(playtime[-2:])*3600

        day_length = len(playtime)-2

        if day_length > 0:
            epoch_days = int(playtime[0:day_length])*86400
            total_epoch = epoch_hours + epoch_days
        else:
            total_epoch = epoch_hours

        if total_epoch > 0:
            player['epoch'] = total_epoch
            playtime_list.append(player)

    playtime_list = sort_list(playtime_list, 'epoch')[first_record:last_record]
    data['index'] = first_record

    for player in sorted_playtime:
        player_obj = Player.objects.get(id=player['id'])
        first_record += 1
        record_leaderboard(player_obj, 'playtime', first_record)

    data['leaderboard'] = json.dumps(playtime_list)

    return render(request, 'leaderboard.html', data)


def most_50s(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'most_50s',
        'title': "Most 50's",
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

    sorted_50s = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'h3_team_slayer',
                                                  'h3_team_hardcore', 'h3_team_doubles', 'ms_2v2_series',
                                                  'hce_team_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore',
                                                  'halo_reach_invasion', 'halo_reach_team_slayer', 'player__emblem').order_by('-player__matches'))

    list_50s = []

    for player in sorted_50s:
        fifty = 0

        if player['h3_team_slayer'] == 50:
            fifty += 1

        if player['h3_team_hardcore'] == 50:
            fifty += 1

        if player['h3_team_doubles'] == 50:
            fifty += 1

        if player['ms_2v2_series'] == 50:
            fifty += 1

        if player['hce_team_doubles'] == 50:
            fifty += 1

        if player['h2c_team_hardcore'] == 50:
            fifty += 1

        if player['halo_reach_team_hardcore'] == 50:
            fifty += 1

        if player['halo_reach_invasion'] == 50:
            fifty += 1

        if player['halo_reach_team_slayer'] == 50:
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

    rank_list = list(Ranks.objects.all().values('player__gamertag', 'player__id', 'player__matches', 'h3_team_slayer', 'player__emblem').order_by('-h3_team_slayer', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    for rank_player in rank_list:
        first_record += 1
        record_leaderboard(int(rank_player['player__id']), 'h3_team_slayer', first_record)

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

    rank_list = list(Ranks.objects.all().values('player__gamertag', 'player__id', 'player__matches', 'h3_team_hardcore', 'player__emblem').order_by('-h3_team_hardcore', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    for rank_player in rank_list:
        first_record += 1
        record_leaderboard(int(rank_player['player__id']), 'h3_team_hardcore', first_record)

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

    rank_list = list(Ranks.objects.all().values('player__gamertag', 'player__id', 'player__matches', 'h3_team_doubles', 'player__emblem').order_by('-h3_team_doubles', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    for rank_player in rank_list:
        first_record += 1
        record_leaderboard(int(rank_player['player__id']), 'h3_team_doubles', first_record)

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

    rank_list = list(Ranks.objects.all().values('player__gamertag', 'player__id', 'player__matches', 'ms_2v2_series', 'player__emblem').order_by('-ms_2v2_series', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    for rank_player in rank_list:
        first_record += 1
        record_leaderboard(int(rank_player['player__id']), 'ms_2v2_series', first_record)

    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def hce_team_doubles(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'hce_team_doubles',
        'title': "Halo 1: Team Doubles",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.all().values('player__gamertag', 'player__id', 'player__matches', 'hce_team_doubles', 'player__emblem').order_by('-hce_team_doubles', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    for rank_player in rank_list:
        first_record += 1
        record_leaderboard(int(rank_player['player__id']), 'hce_team_doubles', first_record)

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

    rank_list = list(Ranks.objects.all().values('player__gamertag', 'player__id', 'player__matches', 'h2c_team_hardcore', 'player__emblem').order_by('-h2c_team_hardcore', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    for rank_player in rank_list:
        first_record += 1
        record_leaderboard(int(rank_player['player__id']), 'h2c_team_hardcore', first_record)

    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def halo_reach_team_hardcore(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'halo_reach_team_hardcore',
        'title': "Halo Reach: Team Hardcore",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.all().values('player__gamertag', 'player__id', 'player__matches', 'halo_reach_team_hardcore', 'player__emblem').order_by('-halo_reach_team_hardcore', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    for rank_player in rank_list:
        first_record += 1
        record_leaderboard(int(rank_player['player__id']), 'halo_reach_team_hardcore', first_record)

    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def halo_reach_invasion(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'halo_reach_invasion',
        'title': "Halo Reach: Team Invasion",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.all().values('player__gamertag', 'player__id', 'player__matches', 'halo_reach_invasion', 'player__emblem').order_by('-halo_reach_invasion', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    for rank_player in rank_list:
        first_record += 1
        record_leaderboard(int(rank_player['player__id']), 'halo_reach_invasion', first_record)

    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)


def halo_reach_team_slayer(request):
    first_record = 0
    last_record = 100

    data = {
        'type': 'halo_reach_team_slayer',
        'title': "Halo Reach: Team Slayer",
        'base_url': get_base_url(),
        'page': 1,
        'rank': 0
    }

    if 'page' in request.GET:
        page = int(request.GET['page'])
        first_record += (page - 1) * 100
        last_record += (page - 1) * 100
        data['page'] = page

    rank_list = list(Ranks.objects.all().values('player__gamertag', 'player__id', 'player__matches', 'halo_reach_team_slayer', 'player__emblem').order_by('-halo_reach_team_slayer', '-player__matches')[first_record:last_record])
    data['index'] = first_record

    for rank_player in rank_list:
        first_record += 1
        record_leaderboard(int(rank_player['player__id']), 'halo_reach_team_slayer', first_record)

    data['leaderboard'] = json.dumps(rank_list)

    return render(request, 'leaderboard.html', data)
