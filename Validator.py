import os
import time
from urllib.parse import urlparse

import requests
import json
from CustomExceptions import NotaYoutubeURLException, VideoChartNotFoundException, ForbiddenVideoException, VideoNotFoundException, VideoSnippetUnavailableException, VideoTitleUnavailableException, VideoThumbnailUnavailableException

#Creds
YOUTUBE_DATA_API_V3 = os.environ.get("YOUTUBE_DATA_API_V3", None)


youtube_share_urls = ["youtu.be", "www.youtu.be"]
youtube_reg_urls = ["www.youtube.com", "youtube.com"]


"""
Validates the hostname of the url
Takes in a URL in the form of a string
Also the lists that contain the youtube urls
"""
def validate_hostname(url):
    data = urlparse(url)
    hostname = str(data.hostname).lower()
    acceptable_hostnames = youtube_share_urls + youtube_reg_urls
    if(hostname is None or hostname not in acceptable_hostnames):
        raise NotaYoutubeURLException("URL {} is not a proper Youtube URL".format(hostname))

"""
Extracts the video id out of the url
Takes in a URL in the form of a string
"""
def extract_video_id(url):
    data = urlparse(url)
    hostname = str(data.hostname).lower()

    video_id = ""
    if hostname in youtube_share_urls:
        video_id = str(data.path)[1:]       #ex: /URNN-_az-3g
    else:
        parts = str(data.query).split("&")  #ex: v=URNN-_az-3g&t=40
        for part in parts:
            if part[0:2] == "v=":
                video_id = part[2:]
    return video_id

"""
Check if video has been blocked, by querying Youtube's Data API videos api
Takes in the video id:
Ex:
    If youtube url:     https://www.youtube.com/watch?v=URNN-_az-3g
    Then video id is:   URNN-_az-3g
"""
def check_video_accessible(video_id):
    print("video_id:{}".format(video_id))
    youtube_query = "https://www.googleapis.com/youtube/v3/videos?part=id&id=" + video_id + "&key=" + YOUTUBE_DATA_API_V3

    try:
        raw = requests.get(youtube_query)
        if raw.status_code == 400:
            raise VideoChartNotFoundException("video chart not found, see https://developers.google.com/youtube/v3/docs/videos/list?authuser=0")
        elif raw.status_code == 403:
            raise ForbiddenVideoException("video is forbidden, see https://developers.google.com/youtube/v3/docs/videos/list?authuser=0")
        elif raw.status_code == 404:
            raise VideoNotFoundException("video not found, see https://developers.google.com/youtube/v3/docs/videos/list?authuser=0")
        else:
            response = raw.json()
            pretty_data = json.dumps(raw.json(), indent=4)
            print(pretty_data)

            if len(response["items"]) == 0:
                raise VideoNotFoundException("video not found, see https://developers.google.com/youtube/v3/docs/videos/list?authuser=0")
    except Exception as e:
        raise e


"""
Validates the youtube URL
Takes in a url in the form of a string, then does the following:
1. Check if hostname is youtube.com
2. Check if video has been blocked
"""
def validate_youtube_url(url):
    try:
        validate_hostname(url)
        video_id = extract_video_id(url)
        check_video_accessible(video_id)
    except Exception as e:
        raise e
