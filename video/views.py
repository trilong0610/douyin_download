import requests
import re
import os, urllib.request, time


header = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Upgrade-Insecure-Requests': '1',
}


def find_url(string):
    # Find url in string when you get url from douyin app
    # Example: 
    # From: 7.66 oda:/ 姗姗 最近睡眠好吗好久 没跟你说说话%%下雨天 %%治愈 %%助眠 %%设计案例分享   https://v.douyin.com/NxR9W5E/ 复制此链接，打开Dou音搜索，直接观看视频！
    # To: https://v.douyin.com/NxR9W5E/
    
    url = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url[0]


def get_id_video(url):
    
    # Get id video from url share
    data = requests.get(headers=header, url=url, timeout=15)
    vid = re.findall(r'\d+', data.url)
    return vid[0]


def get_info_video(id_video):
    # Response info video: url_video, author,id,..etc..
    response = requests.get(
        headers=header, url='https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + str(id_video))
    # item = response.json"().get("item_list")[0]
    item = response.json()
    # get url video no watermark
    # url_mp4 = item["item_list"][0]["video"]["play_addr"]["url_list"][0].replace(
    #     "playwm", "play")
    return item


def get_vid_no_watermark(id_video):
    json = get_info_video(id_video=id_video)
    url_mp4 = json["item_list"][0]["video"]["play_addr"]["url_list"][0].replace(
        "playwm", "play")
    return url_mp4


def get_all_posts(sec_uid, count_vid):
    #  Get all info videos of user(sec_uid) with url,author,id,...etc...
    print('get_all_posts_count: ' + str(count_vid))
    response = requests.get(
        headers=header, url='https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=%s&count=%s' % (sec_uid, count_vid))
    items = response.json()

    print('get_all_posts_count: ' + str(items['aweme_list']))

    return items


def save_video_author(url_video,folder_path, video_path):
    
    print('Đang tải video....')
    
    os.makedirs(folder_path,exist_ok=True)

    print('Đang lưu video....')
    # urllib.request.urlretrieve(url=url_mp4, filename=path_video)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url=url_video, filename=video_path)
    print('Đã lưu video....')


def get_sec_uid(url):
    if url.find('https://www.douyin.com/user/') > 0:
        sec_uid = re.findall(r'M.*\?', data.url)[0].replace('?','')
        return sec_uid
    else:   
        url = find_url(url)
        data = requests.get(headers=header, url=url, timeout=15)
        # 5- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/NxYudjQ/
        sec_uid = re.findall(r'M.*\?', data.url)[0].replace('?','')
        return sec_uid