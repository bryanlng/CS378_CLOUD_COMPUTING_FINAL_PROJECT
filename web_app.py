import os
import time
from urllib.parse import urlparse

import requests
import json

from flask import request
from flask import Flask, render_template


application = Flask(__name__)
app = application

#Creds
YOUTUBE_DATA_API_V3 = os.environ.get("YOUTUBE_DATA_API_V3", None)

"""
Validates the youtube URL
Takes in a url in the form of a string, then does the following:
1. Check if hostname is youtube.com
2. Check if video has been blocked

"""
def validate_youtube_url(url):
    #Validate hostname. Check if it is a youtube url
    data = urlparse(url)
    youtube_share_urls = ["youtu.be", "www.youtu.be"]
    youtube_reg_urls = ["www.youtube.com", "youtube.com"]
    acceptable_hostnames = youtube_share_urls + youtube_reg_urls

    hostname = str(data.hostname).lower()
    if(hostname is None or hostname not in acceptable_hostnames):
        print("bad")

    #Extract out video id
    video_id = ""
    if hostname in youtube_share_urls:
        video_id = str(data.path)[1:]       #ex: /URNN-_az-3g
    else:
        parts = str(data.query).split("&")  #ex: v=URNN-_az-3g&t=40
        for part in parts:
            if part[0:2] == "v=":
                video_id = part[2:]

    #Check if video has been blocked, by querying Youtube's Data API videos api
    print("video_id:{}".format(video_id))
    youtube_query = "https://www.googleapis.com/youtube/v3/videos?part=id&id=" + video_id + "&key=" + YOUTUBE_DATA_API_V3

    try:
        raw = requests.get(youtube_query)
        if raw.status_code == 400:
            print("videoChart not found")
        elif raw.status_code == 403:
            print("forbidden")
        elif raw.status_code == 404:
            print("video not found")
        else:
            response = raw.json()
            pretty_data = json.dumps(raw.json(), indent=4)
            print(pretty_data)

            if len(response["items"]) == 0:
                print("video deleted")
    except Exception as e:
        print(e)



@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    test_url = "https://www.youtube.com/watch?v=URNN-_az-3g"
    validate_youtube_url(test_url)
    app.run(host='0.0.0.0')
