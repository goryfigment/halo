import json
from halo_handler import halo_matches, service_record as halo_service_record
from django.http import JsonResponse
from halo.decorators import login_required, data_required
from halo.models import Player
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


@login_required
@data_required(['gt'], 'GET')
def player_matches(request):
    gt = request.GET['gt']
    matches = halo_matches(gt)

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
