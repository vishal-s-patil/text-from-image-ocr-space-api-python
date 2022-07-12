from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import requests
from PIL import Image, ImageDraw, ImageFont
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
                    'isOverlayRequired': True,
                    'apikey': 'K86490431088957'
                }
        with open('uploads/' + file.name, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={file.name: f},
                              data=options,
                            )

        content = json.loads(r.content.decode())

        with open("uploads/sample.json", "w") as outfile:
            json.dump(content, outfile)

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

@csrf_exempt
def getoverlay(req):
    if req.method == "POST":
        TINT_COLOR = (255, 255, 0)
        TRANSPARENCY = .70  # Degree of transparency, 0-100%
        OPACITY = int(255 * TRANSPARENCY)

        img = Image.open('uploads/1.png')
        img = img.convert("RGBA")
        overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
        draw = ImageDraw.Draw(overlay)

        with open('uploads/sample.json', encoding="utf8") as data_file:
            data = json.load(data_file)

        for pr in data["ParsedResults"]:
            for line in pr["TextOverlay"]["Lines"]:
                for w in line["Words"]:
                    x1 = (w["Left"], w["Top"])
                    x2 = (x1[0] + w["Width"], x1[1] + w["Height"])

                    font_size = abs(x1[1] - x2[1])
                    unicode_font_name = "./Arial Unicode.ttf"
                    font = ImageFont.load_default()

                    draw.rectangle((x1, x2), fill=TINT_COLOR+(OPACITY,))

                    text = w["WordText"]
                    draw.text(x1, text, fill=(255, 0, 0, 255), font=font)

                    img = Image.alpha_composite(img, overlay)

                    img.save('uploads/overlay.png')

        img.show()

    return HttpResponse('success')
