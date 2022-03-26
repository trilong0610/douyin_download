import ssl
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from moviepy.video.fx import crop
from moviepy.editor import VideoFileClip, vfx
import requests
import re
import urllib.request
import time
from django.conf import settings
import os
from douyin.settings import MEDIA_ROOT
import mimetypes

header = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Upgrade-Insecure-Requests': '1',
}


class downVideoEdit(View):
    def get(self, request):
        return render(request, 'douyin/login.html', {})

    def post(self, request):
        # Lấy link tiktok
        req_url = request.POST['url']
        url = find_url(req_url)

        id_video = get_redirect_url(url)
        # # Lấy link tải video từ api
        json = save_video(id_video=id_video)

        info_video = resize_video(json)

        # # fill these variables with real values
        filename = info_video['name_video']

        filepath = info_video['path_video']

        with open(filepath, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type='application/adminupload')
            response['Content-Disposition'] = "inline; filename=%s" % filename
        return response


class downVideoNoEdit(View):
    def post(self, request):
        # Lấy link tiktok
        req_url = request.POST['url']

        url = find_url(req_url)

        # # # Lấy link tải video từ api
        id_video = get_redirect_url(url)

        # # # Lấy link tải video từ api
        json = save_video(id_video=id_video)

        # # fill these variables with real values

        filename = json['name_video']
        filepath = json['path_video']
        with open(filepath, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type='application/adminupload')
            response['Content-Disposition'] = "inline; filename=%s" % filename
        return response


def get_info_video(url):
    _res = requests.get(
        'https://dy.nisekoo.com/api/?url=' + str(url))

    name_video = "%s_%s.mp4" % (
        _res.json()['id'], str(time.time()))

    print(name_video)

    path_video = "%s/%s" % (MEDIA_ROOT, name_video)

    urllib.request.urlretrieve(
        _res.json()['mp4'], path_video)

    return {
        "path_video": path_video,
        "video_author_id": _res.json()['id'],
        "name_video": name_video
    }


def resize_video(info_video):
    # import video
    clip = VideoFileClip(info_video['path_video'])

    #   x1,y2: Goc tren trai
    #   x2,y2: Goc duoi phai

    x1 = clip.w * 0.01 // 1
    y1 = clip.h * 0.01 // 1
    x2 = clip.w - clip.w * 0.01 // 1
    y2 = clip.h - clip.h * 0.01 // 1

    # Lật ngược video
    clip = clip.fx(vfx.mirror_x)

    # Cắt video
    clip = crop(clip=clip, x1=x1, y1=y1, x2=x2, y2=y2)

    name_video = "%s.mp4" % (str(time.time()))

    path_video = "%s/cropped/%s" % (MEDIA_ROOT, name_video)

    clip.write_videofile(path_video, codec='mpeg4',
                         audio_bitrate='240k', threads=2)

    clip.close()

    os.remove(info_video['path_video'])

    return {
        "path_video": path_video,
        "name_video": name_video
    }


def find_url(string):
    # Parse the link in the Douyin share password and return to the list
    url = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url[0]


def get_redirect_url(url):

    data = requests.get(headers=header, url=url, timeout=15)
    vid = re.findall(r'\d+', data.url)
    return vid[0]


def save_video(id_video):
    response = requests.get(
        headers=header, url='https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + str(id_video))
    # item = response.json"().get("item_list")[0]

    item = response.json()

    #  Lay link tai video tu response
    url_mp4 = item["item_list"][0]["video"]["play_addr"]["url_list"][0].replace(
        "playwm", "play")

    #  Lay id tac gia video tu response
    author_id = item["item_list"][0]["author_user_id"]

    context = ssl._create_unverified_context

    name_video = "%s.mp4" % (str(time.time()))

    path_video = "%s/%s" % (MEDIA_ROOT, name_video)

    opener = urllib.request.URLopener()

    opener.addheader(header)

    # urllib.request.urlretrieve(url=url_mp4, filename=path_video)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url=url_mp4, filename=path_video)

    return {
        "path_video": path_video,
        "name_video": name_video
    }
