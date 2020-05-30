import json, time, os
from django.shortcuts import render
from base import get_base_url, model_to_dict
from django.db.models import F
from django.http import HttpResponseRedirect
from halo_handler import get_xbox_auth, halo_ranks, service_record
from halo.models import Player, Leaderboard, User, Season1, RecentDonations, Season2, Ranks, PcRanks, Season3
from halo.controllers.leaderboard import season3_func, season3_playtime_func
from django.http import HttpResponse


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
        'mccs': season3_func(request, 'mccs', 'score', 'MCCS', 0, 10),
        'playtime': season3_playtime_func(request, 0, 10),
        'kills': season3_func(request, 'season1', 'kills', '(Season 3) Kills', 0, 10),
        'deaths': season3_func(request, 'season1', 'deaths', '(Season 3) Deaths', 0, 10),
        'wins': season3_func(request, 'season1', 'wins', '(Season 3) Wins', 0, 10),
        'losses': season3_func(request, 'season1', 'losses', '(Season 3) Losses', 0, 10),
        'matches': season3_func(request, 'season1', 'matches', '(Season 3) Matches', 0, 10),
        'kd': season3_func(request, 'season1_ratio', 'kd', '(Season 3) K/D Ratio', 0, 10),
        'wl': season3_func(request, 'season1_ratio', 'wl', '(Season 3) W/L Ratio', 0, 10),
        'assists': season3_func(request, 'season1', 'assists', '(Season 3) Assists', 0, 10),
        'betrayals': season3_func(request, 'season1', 'betrayals', '(Season 3) Betrayals', 0, 10),
        'headshots': season3_func(request, 'season1', 'headshots', '(Season 3) Headshots', 0, 10),

        'recent_donations': json.dumps(list(RecentDonations.objects.all().values(amount=F('player__donation'), gamertag=F('player__gamertag'), player_id=F('player__id'), emblem=F('player__emblem'), donation=F('player__donation'), twitch=F('player__twitch'), youtube=F('player__youtube'), twitter=F('player__twitter'), notes=F('player__notes'), color=F('player__color'),  social=F('player__social'), mixer=F('player__mixer'), glow=F('player__glow'), rgb=F('player__rgb')).order_by('-id')[0:5]))
    }

    return render(request, 'home.html', data)


def donate(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'donate.html', data)


def contact(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'contact.html', data)


def privacy_policy(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'privacy_policy.html', data)


def terms_conditions(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'terms_conditions.html', data)


def timer(request, game, type):
    games = ['h2a', 'h2', 'h3']
    types = ['radar', 'mlg']

    data = {
        'base_url': get_base_url(),
        'handlebars': game + '_' + type,
        'title': type.capitalize() + " Halo " + game.replace('h', '') + " Timers"
    }

    if game not in games or type not in types:
        return render(request, '404.html', data)
    else:
        file_path = os.path.join(os.path.dirname(__file__), 'static_data/timer.json')
        data['timers'] = json.dumps(json.loads(open(file_path).read())[game][type])
        return render(request, 'timer.html', data)


def about(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'about.html', data)


def resources(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, 'resources.html', data)


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

    players = list(Player.objects.all().values('id', 'gamertag', 'ban', 'donation', 'twitch', 'youtube', 'twitter', 'mixer', 'social', 'notes', 'color', 'rgb'))

    data = {
        'base_url': get_base_url(),
        'players': json.dumps(players)
    }

    return render(request, 'dashboard.html', data)


def verified(request):
    current_user = request.user

    # Only go to overview if user is logged in
    if not current_user.is_authenticated():
        return HttpResponseRedirect('/login/')

    xbox_ranks = list(Ranks.objects.all().values('player__gamertag', 'player__id', 'v_h3_team_slayer', 'v_h3_team_hardcore', 'v_ms_2v2_series', 'v_h3_team_doubles', 'v_halo_reach_team_hardcore', 'v_halo_reach_invasion', 'v_h2c_team_hardcore', 'v_hce_hardcore_doubles', 'v_hce_team_doubles', 'v_halo_reach_team_slayer', 'v_h2a_team_hardcore'))
    pc_ranks = list(PcRanks.objects.all().values('player__gamertag', 'player__id', 'v_halo_reach_team_hardcore', 'v_halo_reach_invasion', 'v_hce_hardcore_doubles', 'v_halo_reach_team_slayer', 'v_h2a_team_hardcore', 'v_h2c_team_hardcore'))

    xbox_dict = {}
    pc_dict = {}

    for xbox in xbox_ranks:
        xbox_dict[xbox['player__id']] = xbox

    for pc in pc_ranks:
        pc_dict[pc['player__id']] = pc

    data = {
        'base_url': get_base_url(),
        'xbox_ranks': json.dumps(xbox_dict),
        'pc_ranks': json.dumps(pc_dict)
    }

    return render(request, 'verified.html', data)


def ban_dashboard(request):
    current_user = request.user

    # Only go to overview if user is logged in
    if not current_user.is_authenticated():
        return HttpResponseRedirect('/login/')

    players = list(Player.objects.filter(ban=True).values('id', 'gamertag', 'ban', 'donation', 'twitch', 'youtube', 'twitter', 'mixer', 'social', 'notes', 'color', 'rgb'))

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
    player_obj = Player.objects.filter(gamertag=gt)

    try:
        ranks = halo_ranks(gt)
        waypoint = "Online"
    except:
        try:
            get_xbox_auth()
            ranks = halo_ranks(gt)
            waypoint = "Online"
        except:
            waypoint = "Offline"
            if player_obj.exists():
                xbox_ranks = model_to_dict(Ranks.objects.filter(player=player_obj)[0])
                pc_ranks = model_to_dict(PcRanks.objects.filter(player=player_obj)[0])

                ranks = {
                    "xbox": {
                        "H3 Team Slayer": [{
                            "Gamertag": gt,
                            "SkillRank": xbox_ranks['h3_team_slayer']
                        }],
                        "H3 Team Hardcore": [{"SkillRank": xbox_ranks['h3_team_hardcore']}],
                        "MS 2v2 Series": [{"SkillRank": xbox_ranks['ms_2v2_series']}],
                        "H3 Team Doubles": [{"SkillRank": xbox_ranks['h3_team_doubles']}],
                        "Halo: Reach Team Hardcore": [{"SkillRank": xbox_ranks['halo_reach_team_hardcore']}],
                        "Halo: Reach Invasion": [{"SkillRank": xbox_ranks['halo_reach_invasion']}],
                        "H2C Team Hardcore": [{"SkillRank": xbox_ranks['h2c_team_hardcore']}],
                        "HCE Hardcore Doubles": [{"SkillRank": xbox_ranks['hce_hardcore_doubles']}],
                        "H2A Team Hardcore": [{"SkillRank": xbox_ranks['h2a_team_hardcore']}]
                    },
                    "pc": {
                        "Halo: Reach Team Hardcore": [{"SkillRank": pc_ranks['halo_reach_team_hardcore']}],
                        "Halo: Reach Invasion": [{"SkillRank": pc_ranks['halo_reach_invasion']}],
                        "HCE Hardcore Doubles": [{"SkillRank": pc_ranks['hce_hardcore_doubles']}],
                        "H2C Team Hardcore": [{"SkillRank": pc_ranks['h2c_team_hardcore']}],
                        "H2A Team Hardcore": [{"SkillRank": pc_ranks['h2a_team_hardcore']}]
                    }
                }
            else:
                ranks = {
                    "xbox": {
                        "H3 Team Slayer": [{
                            "Gamertag": gt,
                            "SkillRank": 1
                        }],
                        "H3 Team Hardcore": [{"SkillRank": 1}],
                        "MS 2v2 Series": [{"SkillRank": 1}],
                        "H3 Team Doubles": [{"SkillRank": 1}],
                        "Halo: Reach Team Hardcore": [{"SkillRank": 1}],
                        "Halo: Reach Invasion": [{"SkillRank": 1}],
                        "H2C Team Hardcore": [{"SkillRank": 1}],
                        "HCE Hardcore Doubles": [{"SkillRank": 1}],
                        "H2A Team Hardcore": [{"SkillRank": 1}]
                    },
                    "pc": {
                        "Halo: Reach Team Hardcore": [{"SkillRank": 1}],
                        "Halo: Reach Invasion": [{"SkillRank": 1}],
                        "HCE Hardcore Doubles": [{"SkillRank": 1}],
                        "H2C Team Hardcore": [{"SkillRank": 1}],
                        "H2A Team Hardcore": [{"SkillRank": 1}]
                    }
                }

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

        xbox_ranks = Ranks.objects.filter(player=player_obj)
        pc_ranks = PcRanks.objects.filter(player=player_obj)
        if xbox_ranks.exists() and pc_ranks.exists():
            saved_ranks = {
                'xbox': model_to_dict(xbox_ranks[0]),
                'pc': model_to_dict(pc_ranks[0])
            }
        else:
            saved_ranks = {
                'xbox': {},
                'pc': {}
            }

        player['season'] = model_to_dict(Season1.objects.get(player=player_obj))
        player['season2'] = model_to_dict(Season2.objects.get(player=player_obj))
        season3 = Season3.objects.filter(player=player_obj)

        if season3.exists():
            player['season3'] = model_to_dict(season3[0])
        else:
            player['season3'] = model_to_dict(Season3.objects.create(player=player_obj))

    else:
        player = {
            "wl": 0,
            "kills": 0,
            "deaths": 0,
            "matches": 0,
            "wins": 0,
            "losses": 0,
            "player": 10,
            "epoch": 0,
            "score": 0,
            "kd": 0,
            "assists": 0,
            "betrayals": 0,
            "headshots": 0,
            "playtime": "0h",
            'season': {
                "wl": 0,
                "kills": 0,
                "deaths": 0,
                "matches": 0,
                "wins": 0,
                "losses": 0,
                "player": 10,
                "epoch": 0,
                "score": 0,
                "kd": 0,
                "playtime": "0h"
            },
            'season2': {
                "wl": 0,
                "kills": 0,
                "deaths": 0,
                "matches": 0,
                "wins": 0,
                "losses": 0,
                "player": 10,
                "epoch": 0,
                "score": 0,
                "kd": 0,
                "playtime": "0h"
            },
            'season3': {
                "wl": 0,
                "kills": 0,
                "deaths": 0,
                "matches": 0,
                "wins": 0,
                "losses": 0,
                "player": 10,
                "epoch": 0,
                "score": 0,
                "kd": 0,
                "assists": 0,
                "betrayals": 0,
                "headshots": 0,
                "playtime": "0h"
            }
        }
        leaderboard = {}
        saved_ranks = {}

    data = {
        'base_url': get_base_url(),
        'saved_ranks': json.dumps(saved_ranks),
        'xbox_ranks': json.dumps(ranks['xbox']),
        'pc_ranks': json.dumps(ranks['pc']),
        'gt': ranks['xbox']['H3 Team Slayer'][0]['Gamertag'],
        'player': json.dumps(player),
        'leaderboard': json.dumps(leaderboard),
        'player_count': Player.objects.all().count(),
        'waypoint': waypoint
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


def article(request, id):
    file_path = os.path.join(os.path.dirname(__file__), 'static_data/article.json')
    articles = json.loads(open(file_path).read().decode('latin-1'))

    if id in articles:
        return render(request, 'article.html', articles[id])
    else:
        return render(request, '404.html', {'base_url': get_base_url()})