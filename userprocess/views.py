import os
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from userprocess import faceswap
from watten.settings import MEDIA_ROOT, MEDIA_URL
import pybase64
import json
cards = [
        'eichel_sechs', 'eichel_sieben', 'eichel_acht', 'eichel_neun', 'eichel_unter', 'eichel_koenig',
        'herz_acht',
        ]

# complete:
# cards = [
#         'eichel_sechs', 'eichel_sieben', 'eichel_acht', 'eichel_neun', 'eichel_zehn', 'eichel_unter', 'eichel_ober', 'eichel_koenig', 'eichel_ass',
#         'herz_sechs', 'herz_sieben', 'herz_acht', 'herz_neun', 'herz_zehn', 'herz_unter', 'herz_ober', 'herz_koenig', 'herz_ass',
#         'weli', 'schell_sieben', 'schell_acht', 'schell_neun', 'schell_zehn', 'schell_unter', 'schell_ober', 'schell_koenig', 'schell_ass',
#         'laub_sechs', 'laub_sieben', 'laub_acht', 'laub_neun', 'laub_zehn', 'laub_unter', 'laub_ober', 'laub_koenig', 'laub_ass',
#         ]

def home(request):
    return render(request, 'home.html')

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

@csrf_exempt
def process_image(request):
    if 'imgdata' in request.POST:
        imgdata = request.POST['imgdata']
        userdirectory = request.POST['userdirectory']
        imgnmb = str(request.POST['imgnmb'])
        header, encoded = imgdata.split(",", 1)
        imgdata_stripped = pybase64.b64decode(encoded)
        if userdirectory == 'False':
            userdirectory = randomString()
            userpath = os.path.join(MEDIA_ROOT, userdirectory)
            os.mkdir(userpath)
        else:
            userpath = os.path.join(MEDIA_ROOT, userdirectory)
        with open(os.path.join(userpath, 'userimage' + imgnmb + '.jpg'), "wb") as f:
            f.write(imgdata_stripped)
        faceswap.main(userdirectory, imgnmb, cards[int(imgnmb)-1])
        user_url = MEDIA_URL + userdirectory + '/' + imgnmb + '.jpg'
        imgnmb = int(imgnmb)
        userdict = { 'userdirectory': userdirectory, 'user_url': user_url, 'imgnmb': imgnmb }
        return HttpResponse(json.dumps(userdict))
        #return render(request, 'home.html', {'userpath': userpath})
        #return HttpResponse("$('#convertedimage').prop('src', 'media/' + userdirectory + '/output.jpg?' + new Date().valueOf())", content_type="application/x-javascript")
