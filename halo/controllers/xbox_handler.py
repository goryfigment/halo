import xbox
from .. import settings_secret
from django.http import JsonResponse


def xbox_authenticate():
    xbox.client.authenticate(login=settings_secret.USERNAME, password=settings_secret.PASSWORD)


def xbox_clips(request):



    try:
        gamertag = xbox.GamerProfile.from_gamertag(request.GET['gt'])
    except:
        xbox_authenticate()
        gamertag = xbox.GamerProfile.from_gamertag(request.GET['gt'])

    clips = list(gamertag.clips())
    halo_list = []

    for clip in clips:
        clip_dictionary = clip.raw_json

        if clip_dictionary['titleName'] == 'Halo: The Master Chief Collection':
            halo_list.append(clip_dictionary)

    return JsonResponse({'clips': halo_list}, safe=False)

