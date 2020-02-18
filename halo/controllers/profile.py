import time
import json
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from halo import get_xbox_auth, service_record as halo_service_record
from django.http import JsonResponse


def service_record(request):
    try:
        player_record = halo_service_record(request.GET['gt'])
    except:
        get_xbox_auth()
        player_record = halo_service_record(request.GET['gt'])

    return JsonResponse(player_record, safe=False)


