import xbox, json
from halo.settings_secret import USERNAME, PASSWORD
from django.http import JsonResponse, HttpResponseBadRequest


def xbox_authenticate():
    xbox.client.authenticate(login=USERNAME, password=PASSWORD)


def xbox_clips(request):
    try:
        gamertag = xbox.GamerProfile.from_gamertag(request.GET['gt'])
    except:
        xbox_authenticate()
        gamertag = xbox.GamerProfile.from_gamertag(request.GET['gt'])

    try:
        clips = list(gamertag.clips())
    except:
        data = {'success': False,  'error_msg': 'Users has no videos.'}
        return HttpResponseBadRequest(json.dumps(data), 'application/json')

    halo_list = []

    for clip in clips:
        clip_dictionary = clip.raw_json

        if clip_dictionary['titleName'] == 'Halo: The Master Chief Collection':
            halo_list.append(clip_dictionary)

    return JsonResponse({'clips': halo_list}, safe=False)

