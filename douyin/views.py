import imp
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from moviepy.video.fx import crop
from moviepy.editor import VideoFileClip, vfx
import requests
import urllib.request
import time
from django.conf import settings
import os
from douyin.settings import MEDIA_ROOT
import mimetypes


class upload_url(View):
    def get(self, request):
        return render(request, 'douyin/login.html', {})

    def post(self, request):
        # Lấy link tiktok
        url = request.POST['url']

        # Lấy link tải video từ api
        json = get_info_video(url=url)

        info_video = resize_video(json)

        # fill these variables with real values
        filename = info_video['name_video']
        filepath = info_video['path_video']
        with open(filepath, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type='application/adminupload')
            response['Content-Disposition'] = "inline; filename=%s" % filename
        return response


def get_info_video(url):
    _res = requests.get('https://douyin.wtf/api?url=' + url)

    name_video = "%s_%s.mp4" % (
        _res.json()['video_author_id'], str(time.time()))

    path_video = "%s/%s" % (MEDIA_ROOT, name_video)

    urllib.request.urlretrieve(
        _res.json()['video_url'], path_video)

    return {
        "path_video": path_video,
        "video_author_id": _res.json()['video_author_id']
    }


def resize_video(info_video):
    # import video
    clip = VideoFileClip(info_video['path_video'])

#   x1,y2: Goc tren trai
#   x2,y2: Goc duoi phai

    x1 = clip.w * 0.015 // 1
    y1 = clip.h * 0.015 // 1
    x2 = clip.w - clip.w * 0.015 // 1
    y2 = clip.h - clip.h * 0.015 // 1

    # Lật ngược video
    clip = clip.fx(vfx.mirror_x)

    # Cắt video
    clip = crop(clip=clip, x1=x1, y1=y1, x2=x2, y2=y2)

    name_video = "%s_%s.mp4" % (
        info_video['video_author_id'], str(time.time()))

    path_video = "%s/%s" % (MEDIA_ROOT, name_video)

    clip.write_videofile(path_video)

    os.remove(info_video['path_video'])

    return {
        "path_video": path_video,
        "name_video": name_video
    }
