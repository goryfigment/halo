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
from halo.models import Player, Ranks


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


def halo_ranks(gt):
    r = requests.get('https://www.halowaypoint.com/en-us/games/halo-the-master-chief-collection/xbox-one/skill-ranks?view=DataOnly&gamertags=' + gt,
                                 headers={
                                      'user-agent': USER_AGENT,
                                      'referer': oauth20_authorize,
                                      'host': 'www.halowaypoint.com'
                                  },
                                  verify=False,
                                  allow_redirects=False,
                                  cookies=json.load(open(cookie_json))
    )

    return r.json()


def service_record(gt, ranks):
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
    matches = numeric_medium[1].get_text()
    wins = int(value_element[2].get_text())
    losses = int(value_element[3].get_text())
    kd_ratio = decimal_format(float(kills)/float(deaths), 2, False)
    wl_ratio = decimal_format(float(wins)/float(losses), 2, False)

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
        player.hits += 1
        player.last_updated = int(round(time.time()))
        player.save()

        rank_obj = Ranks.objects.get(player=player)
        rank_obj.h3_team_slayer = ranks["H3 Team Slayer"][0]['SkillRank']
        rank_obj.h3_team_hardcore = ranks["H3 Team Hardcore"][0]['SkillRank']
        rank_obj.ms_2v2_series = ranks["MS 2v2 Series"][0]['SkillRank']
        rank_obj.h3_team_doubles = ranks["H3 Team Doubles"][0]['SkillRank']
        rank_obj.halo_reach_team_hardcore = ranks["Halo: Reach Team Hardcore"][0]['SkillRank']
        rank_obj.halo_reach_invasion = ranks["Halo: Reach Invasion"][0]['SkillRank']
        rank_obj.h2c_team_hardcore = ranks["H2C Team Hardcore"][0]['SkillRank']
        rank_obj.hce_team_doubles = ranks["HCE Team Doubles"][0]['SkillRank']
        rank_obj.halo_reach_team_slayer = ranks["Halo: Reach Team Slayer"][0]['SkillRank']
        rank_obj.save()
    else:
        player = Player.objects.create(
            gamertag=gt,
            playtime=playtime,
            emblem=emblem,
            matches=matches,
            wins=wins,
            losses=losses,
            kills=kills,
            deaths=deaths
        )

        Ranks.objects.create(
            player=player,
            h3_team_slayer=ranks["H3 Team Slayer"][0]['SkillRank'],
            h3_team_hardcore=ranks["H3 Team Hardcore"][0]['SkillRank'],
            ms_2v2_series=ranks["MS 2v2 Series"][0]['SkillRank'],
            h3_team_doubles=ranks["H3 Team Doubles"][0]['SkillRank'],
            halo_reach_team_hardcore=ranks["Halo: Reach Team Hardcore"][0]['SkillRank'],
            halo_reach_invasion=ranks["Halo: Reach Invasion"][0]['SkillRank'],
            h2c_team_hardcore=ranks["H2C Team Hardcore"][0]['SkillRank'],
            hce_team_doubles=ranks["HCE Team Doubles"][0]['SkillRank'],
            halo_reach_team_slayer=ranks["Halo: Reach Team Slayer"][0]['SkillRank']
        )

    return {
        'emblem': emblem,
        'playtime': playtime,
        'matches': matches,
        'kills': kills,
        'deaths': deaths,
        'kd_ratio': kd_ratio,
        'wins': wins,
        'losses': losses,
        'wl_ratio': wl_ratio
    }
