import os
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from userprocess import faceswap
from watten.settings import MEDIA_ROOT, MEDIA_URL
import pybase64

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
        print(type(imgdata))
        header, encoded = imgdata.split(",", 1)
        imgdata_stripped = pybase64.b64decode(encoded)
        userdirectory = randomString()
        userpath = os.path.join(MEDIA_ROOT, userdirectory)
        os.mkdir(userpath)
        with open(os.path.join(userpath, 'image.jpg'), "wb") as f:
            f.write(imgdata_stripped)
        faceswap.main(userdirectory)
        user_url = MEDIA_URL + userdirectory + '/' + 'output.jpg'
        return HttpResponse(user_url)
        #return render(request, 'home.html', {'userpath': userpath})
        #return HttpResponse("$('#convertedimage').prop('src', 'media/' + userdirectory + '/output.jpg?' + new Date().valueOf())", content_type="application/x-javascript")
