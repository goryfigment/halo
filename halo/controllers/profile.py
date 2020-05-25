import json
from halo_handler import halo_matches, service_record as halo_service_record, upd_emblem
from django.http import JsonResponse
from halo.decorators import login_required, data_required
from halo.models import Player, Ranks, PcRanks
from base import model_to_dict


def service_record(request):
    query_request = json.loads(request.body)
    player_record = halo_service_record(query_request['gt'], query_request['xbox_ranks'],  query_request['pc_ranks'], query_request['highest_rank'])
    #     try:
    #         player_record = halo_service_record(query_request['gt'], query_request['ranks'])
    #     except:
    #         get_xbox_auth()
    #         player_record = halo_service_record(query_request['gt'], query_request['ranks'])

    return JsonResponse(player_record, safe=False)


@data_required(['gt'], 'GET')
def update_emblem(request):
    gt = request.GET['gt']

    return JsonResponse(upd_emblem(gt), safe=False)


@data_required(['gt', 'req'], 'GET')
def player_matches(request):
    gt = request.GET['gt']
    matches = halo_matches(gt, '', '', int(request.GET['req']))
    matches = sorted(matches, key=lambda k: k['DateTime'], reverse=True)

    return JsonResponse({'gt': gt, 'matches': matches}, safe=False)


@data_required(['gt', 'game_variant', 'game', 'req'], 'GET')
def game_matches(request):
    gt = request.GET['gt']
    game_variant = request.GET['game_variant']
    game = request.GET['game']
    matches = halo_matches(gt, game_variant, game, int(request.GET['req']))

    return JsonResponse({'gt': gt, 'matches': matches}, safe=False)


@login_required
@data_required(['id', 'ban', 'donation', 'twitch', 'youtube', 'twitter', 'mixer', 'social', 'color', 'notes'], 'POST')
def edit_player(request):
    player_id = request.POST['id']

    player = Player.objects.get(id=player_id)
    player.ban = json.loads(request.POST['ban'])
    player.donation = request.POST['donation']
    player.twitch = request.POST['twitch']
    player.youtube = request.POST['youtube']
    player.twitter = request.POST['twitter']
    player.mixer = request.POST['mixer']
    player.social = request.POST['social']
    player.color = request.POST['color']
    player.notes = request.POST['notes']
    player.save()

    return JsonResponse({'id': player.id, 'player': model_to_dict(player), 'success_msg': 'Player successfully saved!'}, safe=False)


@login_required
@data_required(['id', 'key', 'type', 'value'], 'POST')
def verify_player(request):
    player_id = request.POST['id']
    console_type = request.POST['type']
    key = request.POST['key']

    if console_type == 'xbox':
        rank = Ranks.objects.filter(player_id=player_id)[0]
    else:
        rank = PcRanks.objects.filter(player_id=player_id)[0]

    rank.__dict__[request.POST['key']] = json.loads(request.POST['value'])
    rank.save()

    return JsonResponse({'success_msg': key.replace('v_', '').replace('_', ' ').title() + ' successfully saved!'}, safe=False)
