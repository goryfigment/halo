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
from halo.models import Player, Ranks, Leaderboard, PcRanks, Season1Record, Season1


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


def halo_matches(gt):
    endpoint = 'https://www.halowaypoint.com/en-us/games/halo-the-master-chief-collection/xbox-one/game-history?view=DataOnly&gamertags=' + gt

    hundred_matches = []

    for i in range(1, 11):
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
    playtime = numeric_medium[0].get_text().split(':')[0].replace('.', ' days ') + ' hours'
    matches = int(numeric_medium[1].get_text())
    wins = int(value_element[2].get_text())
    losses = int(value_element[3].get_text())

    kd_ratio = decimal_format(float(kills)/float(deaths), 2, False)
    wl_ratio = decimal_format(float(wins)/float(losses), 2, False)
    # Epoch
    playtime_txt = playtime.replace(' hours', '').replace(' days ', '')
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
        # rank_obj.hce_hardcore_doubles = xbox_ranks["HCE Hardcore Doubles"][0]['SkillRank']
        rank_obj.halo_reach_team_slayer = xbox_ranks["Halo: Reach Team Slayer"][0]['SkillRank']
        rank_obj.save()

        pc_rank_obj = PcRanks.objects.get(player=player)
        pc_rank_obj.halo_reach_team_slayer = pc_ranks["Halo: Reach Team Slayer"][0]['SkillRank']
        pc_rank_obj.halo_reach_team_hardcore = pc_ranks["Halo: Reach Team Hardcore"][0]['SkillRank']
        pc_rank_obj.halo_reach_invasion = pc_ranks["Halo: Reach Invasion"][0]['SkillRank']
        pc_rank_obj.hce_hardcore_doubles = pc_ranks["HCE Hardcore Doubles"][0]['SkillRank']
        pc_rank_obj.save()

        #Season 1
        season1_record = Season1Record.objects.get(player=player)
        season1 = Season1.objects.get(player=player)
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

        created_rank = PcRanks.objects.create(
            player=player,
            halo_reach_team_hardcore=pc_ranks["Halo: Reach Team Hardcore"][0]['SkillRank'],
            halo_reach_invasion=pc_ranks["Halo: Reach Invasion"][0]['SkillRank'],
            halo_reach_team_slayer=pc_ranks["Halo: Reach Team Slayer"][0]['SkillRank'],
            hce_hardcore_doubles=pc_ranks["HCE Hardcore Doubles"][0]['SkillRank']
        )

        Ranks.objects.create(
            pc_ranks=created_rank,
            player=player,
            h3_team_slayer=xbox_ranks["H3 Team Slayer"][0]['SkillRank'],
            h3_team_hardcore=xbox_ranks["H3 Team Hardcore"][0]['SkillRank'],
            ms_2v2_series=xbox_ranks["MS 2v2 Series"][0]['SkillRank'],
            h3_team_doubles=xbox_ranks["H3 Team Doubles"][0]['SkillRank'],
            halo_reach_team_hardcore=xbox_ranks["Halo: Reach Team Hardcore"][0]['SkillRank'],
            halo_reach_invasion=xbox_ranks["Halo: Reach Invasion"][0]['SkillRank'],
            h2c_team_hardcore=xbox_ranks["H2C Team Hardcore"][0]['SkillRank'],
            hce_hardcore_doubles=xbox_ranks["HCE Hardcore Doubles"][0]['SkillRank'],
            halo_reach_team_slayer=xbox_ranks["Halo: Reach Team Slayer"][0]['SkillRank']
        )

        Leaderboard.objects.create(player=player)

        # Create Season1
        season1_record = Season1Record.objects.create(player=player)
        season1 = Season1.objects.create(player=player)
        epoch = 0

    # Calculations!
    s1_kills = kills - season1_record.kills
    s1_matches = matches - season1_record.matches
    s1_deaths = deaths - season1_record.deaths
    s1_wins = wins - season1_record.wins
    s1_loses = losses - season1_record.losses

    try:
        s1_kd = decimal_format(float(s1_kills)/float(s1_deaths), 2, False)
    except ZeroDivisionError:
        s1_kd = 0

    try:
        s1_wl = decimal_format(float(s1_wins)/float(s1_loses), 2, False)
    except ZeroDivisionError:
        s1_wl = 0

    s1_epoch = epoch - season1_record.epoch
    s1_total_hours = s1_epoch / 3600
    s1_playtime = str(s1_total_hours/24) + ' days ' + str(s1_total_hours % 24) + ' hours'

    total_levels = 0

    for key, rank in xbox_ranks.iteritems():
        total_levels += rank[0]['SkillRank']

    avail_pc = ["HCE Hardcore Doubles", "Halo: Reach Team Slayer", "Halo: Reach Invasion", "Halo: Reach Team Hardcore"]
    for key, rank in pc_ranks.iteritems():
        if key in avail_pc:
            total_levels += rank[0]['SkillRank']

    s1_score = int(round((s1_wins*0.5) + (s1_kills*0.1) + (total_levels*10)))
    # Save it to Season 1 Database!
    season1.kills = s1_kills
    season1.matches = s1_matches
    season1.deaths = s1_deaths
    season1.wins = s1_wins
    season1.losses = s1_loses
    season1.kd = s1_kd
    season1.wl = s1_wl
    season1.epoch = s1_epoch
    season1.playtime = s1_playtime
    season1.score = s1_score
    season1.save()

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
        'season': {
            'playtime': s1_playtime,
            'matches': s1_matches,
            'kills': s1_kills,
            'deaths': s1_deaths,
            'kd': s1_kd,
            'wins': s1_wins,
            'losses': s1_loses,
            'wl': s1_wl,
            'score': s1_score
        }
    }

