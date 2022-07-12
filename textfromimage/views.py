from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import requests
import json
import ocrspace


def home(req):
    return render(req, 'index.html')

# extracting text using ocr api

# from local image files
# method-1 : making post request to https://api.ocr.space/parse/image using requests.post

@csrf_exempt
def gettextlocal(req):
    if req.method == "POST":
        file = req.FILES['image']
        fs = FileSystemStorage()
        fs.save(file.name, file)

        options = {
                    'isOverlayRequired': False,
                    'apikey': 'K86490431088957'
                }
        with open('uploads/' + file.name, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={file.name: f},
                              data=options,
                            )
        content = json.loads(r.content.decode())
        print(content['ParsedResults'][0]['ParsedText'])
        return HttpResponse(content['ParsedResults'][0]['ParsedText'])
    else:
        return HttpResponse('method should be post')

# method-2 : using ocrspace module

# @csrf_exempt
# def gettextlocal(req):
#     if req.method == "POST":
#         api = ocrspace.API()
#         file = req.FILES['image']
#         fs = FileSystemStorage()
#         fs.save(file.name, file)
#
#         img_path = 'uploads/' + file.name
#         # with file path
#         # print(api.ocr_file(img_path))
#         # # With file pointer
#         text = api.ocr_file(open(img_path, 'rb'))
#         print(text)
#         return HttpResponse(text)
#     else:
#         return HttpResponse('method should be post')

# form image url

# metohde-1 :

@csrf_exempt
def gettexturl(req):
    if req.method == "POST":
        url = 'https://images-na.ssl-images-amazon.com/images/I/71ovNJN1URL._SL1244_.jpg'
        options = {
                    'url': url,
                    'isOverlayRequired': False,
                    'apikey': 'K86490431088957'
                }
        r = requests.post('https://api.ocr.space/parse/image', data=options)
        content = json.loads(r.content.decode())
        print(content['ParsedResults'][0]['ParsedText'])
        return HttpResponse(content['ParsedResults'][0]['ParsedText'])
    else:
       return HttpResponse('method should be post')


#method-2 :

# @csrf_exempt
# def gettexturl(req):
#     if req.method == "POST":
#         api = ocrspace.API()
#         img_url = 'https://images-na.ssl-images-amazon.com/images/I/71ovNJN1URL._SL1244_.jpg'
#
#         # copy image to local storage
#         with open('uploads/dummy.jpg', 'wb') as f:
#             r = requests.get(img_url)
#             r.raw.decode_content = True
#             f.write(r.content)
#
#         text = api.ocr_url(img_url)
#         print(text)
#         return HttpResponse(text)
#     else:
#         return HttpResponse('method should be post')
