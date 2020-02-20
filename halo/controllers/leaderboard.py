import json
from django.shortcuts import render
from base import decimal_format, sort_list
from halo.models import Player, Ranks


def most_kills(request):
    sorted_kills = list(Player.objects.all().values('gamertag', 'kills', 'matches').order_by('-kills'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_kills), 'type': 'most_kills', 'title': 'Kills'})


def most_deaths(request):
    sorted_deaths = list(Player.objects.all().values('gamertag', 'deaths', 'matches').order_by('-deaths'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_deaths), 'type': 'most_deaths', 'title': 'Deaths'})


def most_wins(request):
    sorted_wins = list(Player.objects.all().values('gamertag', 'wins', 'matches').order_by('-wins'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_wins), 'type': 'most_wins', 'title': 'Wins'})


def most_losses(request):
    sorted_losses = list(Player.objects.all().values('gamertag', 'losses', 'matches').order_by('-losses'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_losses), 'type': 'most_losses', 'title': 'Losses'})


def most_matches(request):
    sorted_matches = list(Player.objects.all().values('gamertag', 'matches').order_by('-matches'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_matches), 'type': 'most_matches', 'title': 'Matches'})


def best_wl(request):
    sorted_wl = list(Player.objects.all().values('gamertag', 'wins', 'losses', 'matches'))

    for player in sorted_wl:
        player['wl_ratio'] = decimal_format(float(player['wins'])/float(player['losses']), 2, False)

    sorted_wl = sort_list(sorted_wl, 'wl_ratio')

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_wl), 'type': 'best_wl', 'title': 'W/L Ratio'})


def best_kd(request):
    sorted_kd = list(Player.objects.all().values('gamertag', 'kills', 'deaths', 'matches'))

    for player in sorted_kd:
        player['kd_ratio'] = decimal_format(float(player['kills'])/float(player['deaths']), 2, False)

    sorted_kd = sort_list(sorted_kd, 'kd_ratio')

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_kd), 'type': 'best_kd', 'title': 'K/D Ratio'})


def most_playtime(request):
    sorted_playtime = list(Player.objects.all().values('gamertag', 'playtime', 'matches'))

    for player in sorted_playtime:
        playtime = player['playtime'].replace(' hours', '').replace(' days ', '')
        epoch_hours = int(playtime[-2:])*3600
        epoch_days = int(playtime[:-2])*86400

        player['epoch'] = epoch_hours + epoch_days

    sorted_playtime = sort_list(sorted_playtime, 'epoch')

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_playtime), 'type': 'most_playtime', 'title': 'Playtime'})


def most_50s(request):
    sorted_50s = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'h3_team_slayer',
                                                  'h3_team_hardcore', 'h3_team_doubles', 'ms_2v2_series',
                                                  'hce_team_doubles', 'h2c_team_hardcore', 'halo_reach_team_hardcore',
                                                  'halo_reach_invasion', 'halo_reach_team_slayer').order_by('-player__matches'))

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

    sorted_50s = sort_list(sorted_50s, 'fifty')

    print sorted_50s

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_50s), 'type': 'most_50s', 'title': "Most 50's"})


# PLAYLIST
def h3_team_slayer(request):
    sorted_rank = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'h3_team_slayer').order_by('-h3_team_slayer', '-player__matches'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_rank), 'type': 'h3_team_slayer', 'title': 'Halo 3: Team Slayer'})


def h3_team_hardcore(request):
    sorted_rank = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'h3_team_hardcore').order_by('-h3_team_hardcore', '-player__matches'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_rank), 'type': 'h3_team_hardcore', 'title': 'Halo 3: Team Hardcore'})


def h3_team_doubles(request):
    sorted_rank = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'h3_team_doubles').order_by('-h3_team_doubles', '-player__matches'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_rank), 'type': 'h3_team_doubles', 'title': 'Halo 3: Team Doubles'})


def ms_2v2_series(request):
    sorted_rank = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'ms_2v2_series').order_by('-ms_2v2_series', '-player__matches'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_rank), 'type': 'ms_2v2_series', 'title': 'Halo 3: MS 2v2 Series'})


def hce_team_doubles(request):
    sorted_rank = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'hce_team_doubles').order_by('-hce_team_doubles', '-player__matches'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_rank), 'type': 'hce_team_doubles', 'title': 'Halo 1: Team Doubles'})


def h2c_team_hardcore(request):
    sorted_rank = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'h2c_team_hardcore').order_by('-h2c_team_hardcore', '-player__matches'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_rank), 'type': 'h2c_team_hardcore', 'title': 'Halo 2 Classic: Team Hardcore'})


def halo_reach_team_hardcore(request):
    sorted_rank = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'halo_reach_team_hardcore').order_by('-halo_reach_team_hardcore', '-player__matches'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_rank), 'type': 'halo_reach_team_hardcore', 'title': 'Halo Reach: Team Hardcore'})


def halo_reach_invasion(request):
    sorted_rank = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'halo_reach_invasion').order_by('-halo_reach_invasion', '-player__matches'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_rank), 'type': 'halo_reach_invasion', 'title': 'Halo Reach: Team Invasion'})


def halo_reach_team_slayer(request):
    sorted_rank = list(Ranks.objects.all().values('player__gamertag', 'player__matches', 'halo_reach_team_slayer').order_by('-halo_reach_team_slayer', '-player__matches'))

    return render(request, 'leaderboard.html', {'leaderboard': json.dumps(sorted_rank), 'type': 'halo_reach_team_slayer', 'title': 'Halo Reach: Team Slayer'})