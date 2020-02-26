import json
from halo_handler import get_xbox_auth, service_record as halo_service_record
from django.http import JsonResponse


def service_record(request):
    query_request = json.loads(request.body)
    player_record = halo_service_record(query_request['gt'], query_request['ranks'], query_request['highest_rank'])
#     try:
#         player_record = halo_service_record(query_request['gt'], query_request['ranks'])
#     except:
#         get_xbox_auth()
#         player_record = halo_service_record(query_request['gt'], query_request['ranks'])

    return JsonResponse(player_record, safe=False)


