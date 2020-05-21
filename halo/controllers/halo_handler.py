import re
import random
import json
import requests
import urllib3
import os
import time
from .. import settings_secret
from bs4 import BeautifulSoup
from base import decimal_format
from halo.models import Player, Ranks, Leaderboard, PcRanks, Season1Record, Season1, Season2Record, Season2


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WLID_USERNAME = settings_secret.USERNAME
WLID_PASSWORD = settings_secret.PASSWORD

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/38.0.2125.104 Safari/537.36'

R_PPFT = "<input type=\"hidden\" name=\"PPFT\" id=\"i0327\" value=\"(.+?)\"\/>"
R_PPSX = "o:'(.+?)"
R_URLPOST = "urlPost:'(.+?)'"

s = requests.Session()

oauth20_authorize = "https://login.live.com/oauth20_authorize.srf?client_id=000000004C0BD2F1&scope=xbox.basic+xbox.of" \
                    "fline_access&response_type=code&redirect_uri=https:%2f%2fwww.halowaypoint.com%2fauth%2fcallback&" \
                    "locale=en-us&display=touch&state=https%253a%252f%252fwww.halowaypoint.com%252fen-us%252fgames%25" \
                    "2fhalo-the-master-chief-collection%252fxbox-one%252fgame-history%253fgamertags%253dfuriousn00b%2" \
                    "526view%253dDataOnly"

cookie_json = os.path.join(os.path.dirname(__file__), '../cookies.json')


def write_json_file(cookie):
    with open(cookie_json, 'w') as f:
        f.write(json.dumps(cookie))


def item_log_json():
    return json.load(open(cookie_json))


def get_xbox_auth():
    response_one = s.get(oauth20_authorize,
                         headers={
                             'user-agent': USER_AGENT,
                             'host': 'login.live.com'
                         },
                         verify=False
    )

    try:
        ppft = re.search(R_PPFT, response_one.text).group(1)
        ppsx = re.search(R_PPSX, response_one.text).group(1)
        post = re.search(R_URLPOST, response_one.text).group(1)
    except AttributeError:
        response_one = s.get(oauth20_authorize, headers={'user-agent': USER_AGENT, 'host': 'login.live.com'}, verify=False)
        ppft = re.search(R_PPFT, response_one.text).group(1)
        ppsx = re.search(R_PPSX, response_one.text).group(1)
        post = re.search(R_URLPOST, response_one.text).group(1)

    response_two = s.post(post,
                          data={
                              'PPFT': ppft,
                              'login': WLID_USERNAME,
                              'passwd': WLID_PASSWORD,
                              'LoginOptions': '3',
                              'NewUser': '1',
                              'PPSX': ppsx,
                              'type': '11',
                              'i3': random.randrange(5000, 10000),
                              'm1': '1920',
                              'm2': '1080',
                              'm3': '0',
                              'i12': '1',
                              'i17': '0',
                              'i18': '__MobileLogin|1,',
                          },
                          headers={
                              'user-agent': USER_AGENT,
                              'referer': oauth20_authorize,
                              'host': 'login.live.com',
                              'origin': 'https://login.live.com'
                          },
                          verify=False,
                          allow_redirects=False
    )

    callback_url = response_two.headers['Location']

    response_three = s.get(callback_url,
                           headers={
                               'user-agent': USER_AGENT,
                               'referer': oauth20_authorize,
                               'host': 'www.halowaypoint.com'
                           },
                           verify=False,
                           allow_redirects=False
    )

    write_json_file(s.cookies.get_dict())


def halo_matches(gt, game_variant, game, num):
    endpoint = 'https://www.halowaypoint.com/en-us/games/halo-the-master-chief-collection/xbox-one/game-history?view=DataOnly&gamertags=' + gt

    if game_variant != '':
        endpoint += '&gameVariant=' + game_variant

    if game != '':
        endpoint += '&game=' + game

    hundred_matches = []

    for i in range(1, num):
        ten_matches = requests.get(endpoint + '&page=' + str(i),
                                     headers={
                                          'user-agent': USER_AGENT,
                                          'referer': oauth20_authorize,
                                          'host': 'www.halowaypoint.com'
                                      },
                                      verify=False,
                                      allow_redirects=False,
                                      cookies=json.load(open(cookie_json))
        ).json()

        hundred_matches += ten_matches[0]['Stats']

    return hundred_matches


def halo_ranks(gt):
    xbox = requests.get('https://www.halowaypoint.com/en-us/games/halo-the-master-chief-collection/xbox-one/skill-ranks?view=DataOnly&gamertags=' + gt,
                                 headers={
                                      'user-agent': USER_AGENT,
                                      'referer': oauth20_authorize,
                                      'host': 'www.halowaypoint.com'
                                  },
                                  verify=False,
                                  allow_redirects=False,
                                  cookies=json.load(open(cookie_json))
    )

    pc = requests.get('https://www.halowaypoint.com/en-us/games/halo-the-master-chief-collection/windows/skill-ranks?view=DataOnly&gamertags=' + gt,
                                 headers={
                                      'user-agent': USER_AGENT,
                                      'referer': oauth20_authorize,
                                      'host': 'www.halowaypoint.com'
                                  },
                                  verify=False,
                                  allow_redirects=False,
                                  cookies=json.load(open(cookie_json))
    )

    return {'xbox': xbox.json(), 'pc': pc.json()}


def service_record(gt, xbox_ranks, pc_ranks, highest_rank):
    endpoint = 'https://www.halowaypoint.com/en-us/games/halo-the-master-chief-collection/xbox-one/service-records/players/' + gt

    data = (requests.get(endpoint,
                              headers={
                                  'user-agent': USER_AGENT,
                                  'referer': oauth20_authorize,
                                  'host': 'www.halowaypoint.com'
                              },
                              verify=False,
                              allow_redirects=False,
                              cookies=json.load(open(cookie_json))
                         )).text

    soup = BeautifulSoup(data, 'html5lib')

    numeric_medium = soup.findAll("h3", {"class": "numeric--medium"})
    value_element = soup.findAll("div", {"class": "value"})
    emblem = soup.findAll("img", {"class": "emblem"})[0]['src']

    kills = int(value_element[0].get_text())
    deaths = int(value_element[1].get_text())

    playtime = numeric_medium[0].get_text().split(':')[0].replace('.', 'd ') + 'h'
    matches = int(numeric_medium[1].get_text())
    wins = int(value_element[2].get_text())
    losses = abs(matches - wins)

    # Handle an exception
    if wins > matches:
        win_holder = wins
        wins = matches
        matches = win_holder

    kd_ratio = decimal_format(float(kills)/float(deaths), 2, False)

    if losses == 0:
        wl_ratio = decimal_format(float(wins)/float(1), 2, False)
    else:
        wl_ratio = decimal_format(float(wins)/float(losses), 2, False)
    # Epoch
    playtime_txt = playtime.replace('h', '').replace('d ', '')
    epoch_hours = int(playtime_txt[-2:])*3600
    day_length = len(playtime_txt)-2

    if day_length > 0:
        epoch_days = int(playtime[0:day_length])*86400
        epoch = epoch_hours + epoch_days
    else:
        epoch = epoch_hours

    ######################
    player = Player.objects.filter(gamertag=gt)

    if player.exists():
        player = Player.objects.get(gamertag=gt)
        player.playtime = playtime
        player.emblem = emblem
        player.matches = matches
        player.wins = wins
        player.losses = losses
        player.kills = kills
        player.deaths = deaths
        player.last_updated = int(round(time.time()))
        player.kd = kd_ratio
        player.wl = wl_ratio
        player.epoch = epoch
        player.highest_skill = highest_rank
        player.save()

        rank_obj = Ranks.objects.get(player=player)
        rank_obj.h3_team_slayer = xbox_ranks["H3 Team Slayer"][0]['SkillRank']
        rank_obj.h3_team_hardcore = xbox_ranks["H3 Team Hardcore"][0]['SkillRank']
        rank_obj.ms_2v2_series = xbox_ranks["MS 2v2 Series"][0]['SkillRank']
        rank_obj.h3_team_doubles = xbox_ranks["H3 Team Doubles"][0]['SkillRank']
        rank_obj.halo_reach_team_hardcore = xbox_ranks["Halo: Reach Team Hardcore"][0]['SkillRank']
        rank_obj.halo_reach_invasion = xbox_ranks["Halo: Reach Invasion"][0]['SkillRank']
        rank_obj.h2c_team_hardcore = xbox_ranks["H2C Team Hardcore"][0]['SkillRank']
        rank_obj.hce_hardcore_doubles = xbox_ranks["HCE Hardcore Doubles"][0]['SkillRank']
        rank_obj.h2a_team_hardcore = xbox_ranks["H2A Team Hardcore"][0]['SkillRank']
        # rank_obj.halo_reach_team_slayer = xbox_ranks["Halo: Reach Team Slayer"][0]['SkillRank']
        rank_obj.save()

        pc_rank_obj = PcRanks.objects.get(player=player)
        # pc_rank_obj.halo_reach_team_slayer = pc_ranks["Halo: Reach Team Slayer"][0]['SkillRank']
        pc_rank_obj.halo_reach_team_hardcore = pc_ranks["Halo: Reach Team Hardcore"][0]['SkillRank']
        pc_rank_obj.halo_reach_invasion = pc_ranks["Halo: Reach Invasion"][0]['SkillRank']
        pc_rank_obj.hce_hardcore_doubles = pc_ranks["HCE Hardcore Doubles"][0]['SkillRank']
        pc_rank_obj.h2c_team_hardcore = pc_ranks["H2C Team Hardcore"][0]['SkillRank']
        pc_rank_obj.h2a_team_hardcore = pc_ranks["H2A Team Hardcore"][0]['SkillRank']
        pc_rank_obj.save()

        #Season 1
        season1_record = Season1Record.objects.get(player=player)
        season1 = Season1.objects.get(player=player)

        #Season 2
        season2_record = Season2Record.objects.get(player=player)
        season2 = Season2.objects.get(player=player)
    else:
        player = Player.objects.create(
            gamertag=gt,
            playtime=playtime,
            emblem=emblem,
            matches=matches,
            wins=wins,
            losses=losses,
            kills=kills,
            deaths=deaths,
            kd=kd_ratio,
            wl=wl_ratio,
            epoch=epoch
        )

        pc_rank_obj = PcRanks.objects.create(
            player=player,
            halo_reach_team_hardcore=pc_ranks["Halo: Reach Team Hardcore"][0]['SkillRank'],
            halo_reach_invasion=pc_ranks["Halo: Reach Invasion"][0]['SkillRank'],
            hce_hardcore_doubles=pc_ranks["HCE Hardcore Doubles"][0]['SkillRank'],
            h2c_team_hardcore=pc_ranks["H2C Team Hardcore"][0]['SkillRank'],
            h2a_team_hardcore=pc_ranks["H2A Team Hardcore"][0]['SkillRank'],
        )

        rank_obj = Ranks.objects.create(
            pc_ranks=pc_rank_obj,
            player=player,
            h3_team_slayer=xbox_ranks["H3 Team Slayer"][0]['SkillRank'],
            h3_team_hardcore=xbox_ranks["H3 Team Hardcore"][0]['SkillRank'],
            ms_2v2_series=xbox_ranks["MS 2v2 Series"][0]['SkillRank'],
            h3_team_doubles=xbox_ranks["H3 Team Doubles"][0]['SkillRank'],
            halo_reach_team_hardcore=xbox_ranks["Halo: Reach Team Hardcore"][0]['SkillRank'],
            halo_reach_invasion=xbox_ranks["Halo: Reach Invasion"][0]['SkillRank'],
            h2c_team_hardcore=xbox_ranks["H2C Team Hardcore"][0]['SkillRank'],
            hce_hardcore_doubles=xbox_ranks["HCE Hardcore Doubles"][0]['SkillRank'],
            h2a_team_hardcore=xbox_ranks["H2A Team Hardcore"][0]['SkillRank'],
        )

        Leaderboard.objects.create(player=player)

        # Create Season 1
        season1_record = Season1Record.objects.create(
            player=player,
            playtime=playtime,
            matches=matches,
            wins=wins,
            losses=losses,
            kills=kills,
            deaths=deaths,
            epoch=epoch
        )
        season1 = Season1.objects.create(player=player)

        # Create Season 2
        season2_record = Season2Record.objects.create(
            player=player,
            playtime=playtime,
            matches=matches,
            wins=wins,
            losses=losses,
            kills=kills,
            deaths=deaths,
            epoch=epoch
        )
        season2 = Season2.objects.create(player=player)
        epoch = 0

    ##### SEASON CALCULATIONS ######
    # s2_kills = kills - season2_record.kills
    # s2_matches = matches - season2_record.matches
    # s2_deaths = deaths - season2_record.deaths
    # s2_wins = wins - season2_record.wins
    # s2_loses = losses - season2_record.losses
    #
    # try:
    #     s2_kd = decimal_format(float(s2_kills)/float(s2_deaths), 2, False)
    # except ZeroDivisionError:
    #     s2_kd = decimal_format(float(s2_kills)/float(1), 2, False)
    #
    # try:
    #     s2_wl = decimal_format(float(s2_wins)/float(s2_loses), 2, False)
    # except ZeroDivisionError:
    #     s2_wl = decimal_format(float(s2_wins)/float(1), 2, False)
    #
    # s2_epoch = epoch - season2_record.epoch
    # s2_total_hours = s2_epoch / 3600
    #
    # if s2_epoch <= 0:
    #     s2_playtime = '0h'
    #     s2_epoch = 0
    # else:
    #     s2_playtime = str(s2_total_hours/24) + 'd ' + str(s2_total_hours % 24) + 'h'
    ##### SEASON CALCULATIONS ######

    total_levels = 0
    total_50s = 0

    for key, rank in xbox_ranks.iteritems():
        current_rank = rank[0]['SkillRank']
        total_levels += current_rank

        if current_rank == 50:
            total_50s += 1

    avail_pc = ["HCE Hardcore Doubles", "Halo: Reach Invasion", "Halo: Reach Team Hardcore", "H2C Team Hardcore", "H2A Team Hardcore"]
    for key, rank in pc_ranks.iteritems():
        if key in avail_pc:
            current_rank = rank[0]['SkillRank']
            total_levels += current_rank

            if current_rank == 50:
                total_50s += 1

    # Add discontinued playlist
    total_levels += rank_obj.halo_reach_team_slayer + pc_rank_obj.halo_reach_team_slayer

    #### SEASON CALCULATIONS ####
    # # Every 50 = 50points
    # bonus_points = (total_50s * 100)
    # s2_score = int(round((s2_wins*0.5) + (s2_kills*0.1) + (total_levels*20)) + bonus_points)
    # # Save it to Season 2 Database!
    # season2.kills = s2_kills
    # season2.matches = s2_matches
    # season2.deaths = s2_deaths
    # season2.wins = s2_wins
    # season2.losses = s2_loses
    # season2.kd = s2_kd
    # season2.wl = s2_wl
    # season2.epoch = s2_epoch
    # season2.playtime = s2_playtime
    # season2.score = s2_score
    # season2.save()
    #### SEASON CALCULATIONS ####

    return {
        'emblem': emblem,
        'playtime': playtime,
        'matches': matches,
        'kills': kills,
        'deaths': deaths,
        'kd': kd_ratio,
        'wins': wins,
        'losses': losses,
        'wl': wl_ratio,
        'highest_rank': highest_rank,
        'epoch': epoch,
        'ban': player.ban,
        'season': {
            'playtime': season1.playtime,
            'matches': season1.matches,
            'kills': season1.kills,
            'deaths': season1.deaths,
            'kd': season1.kd,
            'wins': season1.wins,
            'losses': season1.losses,
            'wl': season1.wl,
            'score': season1.score
        },
        'season2': {
            'playtime': season2.playtime,
            'matches': season2.matches,
            'kills': season2.kills,
            'deaths': season2.deaths,
            'kd': season2.kd,
            'wins': season2.wins,
            'losses': season2.losses,
            'wl': season2.wl,
            'score': season2.score
        }
    }

