from itertools import count
import ssl
from sys import flags
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
from video.models import Video
from video.views import *
import shutil

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
                fh.read(), content_type='video/mp4')
            response['Content-Disposition'] = "attachment; filename=%s" % (filename)
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
                fh.read(), content_type='video/mp4')
            response['Content-Disposition'] = "attachment; filename=%s" % (filename)
        return response

class downVideoAuthor(View):
    def post(self, request):
        
        # Lay sec_id tu nguoi dung de lay toan bo video
        save_info = {}
        url_author = request.POST['url_author']
        count_vid = request.POST['count_vid']
        checkbox_video = request.POST['checkbox_video']

        print('count_vid------ ' +  str(count_vid))
    
        sec_uid = get_sec_uid(url_author)
        
        # Lay danh sach video
        json_data = get_all_posts(sec_uid=sec_uid, count_vid=count_vid)

        print('aweme_list: ' + str(len(json_data['aweme_list'])) )

        # Kiem tra video co ton tai chua
        # Neu checkbox = true va chua ton tai thi tai
        nick_name = json_data['aweme_list'][0]['author']['nickname']
        short_id = json_data['aweme_list'][0]['author']['short_id']

        folder_name = "%s_%s_%d" % (
                nick_name, short_id, time.time_ns())

        folder_path = "assets/videos/%s" % (folder_name)
        # Tai video da co tren db
        if  checkbox_video == 'on': 
            print('status_checkbox: on')

            for json in json_data['aweme_list']:
                
                url_video = json['video']["play_addr"]['url_list'][2]
                id_video = json['aweme_id']
                
                # Neu video chua co tren db thi luu len db
                if not Video.objects.filter(id_video = id_video).exists():
                    video = Video.objects.create(id_video= id_video, sec_uid= sec_uid)
                    video.save()

                video_name = "%s_%d.mp4" % (short_id, int(time.time_ns()))

                video_path = "assets/videos/%s/%s" % (folder_name, video_name)
                # Tai video - luu ve may
                save_video_author(video_path=video_path, folder_path=folder_path,url_video=url_video)
                time.sleep(0.2)
        # Ko Tai video da luu
        else:
            print('status_checkbox: off')
            
            for json in json_data['aweme_list']:
                
                url_video = json['video']["play_addr"]['url_list'][2]
                id_video = json['aweme_id']
                
                #Kiem tra video da luu hay chua
                if not Video.objects.filter(id_video = id_video).exists(): #video chua duoc luu
                # Tai video - luu ve may
                    video_name = "%s_%d.mp4" % (short_id, int(time.time_ns()))
                    video_path = "assets/videos/%s/%s" % (folder_name, video_name)

                    save_video_author(video_path=video_path, folder_path=folder_path,url_video=url_video)
                    # Luu id video len db
                    video = Video.objects.create(id_video= id_video, sec_uid= sec_uid)
                    video.save()
                    time.sleep(0.2)    
            
        print("Đã lưu toàn bô video")
        try: # Neu co tai ve video tu author
            save_path =  shutil.make_archive(folder_name, 'zip', folder_path)
            response = HttpResponse(open(save_path, 'rb'))
            response['Content-Disposition'] = 'attachment; filename=%s' % (folder_name)
            response['Content-Type'] = 'application/zip'
            return response
        except:
            return HttpResponse('Không tồn tại video để tải về, vui lòng thử lại')
        print(save_path)

        # with open(save_path, 'rb') as fd:
        #     response = HttpResponse(fd.read(), content_type='application/x-zip-compressed')
        #     response['Content-Disposition'] = "attachment; filename=%s.zip" % folder_name
        


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
 