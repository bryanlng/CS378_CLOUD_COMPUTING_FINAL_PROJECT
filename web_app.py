import os
import time
from urllib.parse import urlparse

import requests
import json

from flask import request
from flask import Flask, render_template
import mysql.connector
from mysql.connector import errorcode

import Util
import Validator
import CustomExceptions
from CustomExceptions import NotaYoutubeURLException, VideoChartNotFoundException, ForbiddenVideoException, VideoNotFoundException, VideoSnippetUnavailableException, VideoTitleUnavailableException, VideoThumbnailUnavailableException

from google.cloud import storage


application = Flask(__name__)
app = application

#Creds
YOUTUBE_DATA_API_V3 = os.environ.get("YOUTUBE_DATA_API_V3", None)



def create_file_structure():
    storage_client = storage.Client()

    # Check if the buckets have already been created
    b = storage_client.list_buckets()
    required_number_buckets = 2
    required_buckets = ["cs378_final_converted_videos", "cs378_final_raw_videos"]
    num_buckets = 0
    found_buckets = []
    for bucket in storage_client.list_buckets():
        found_buckets.append(bucket.name)
        num_buckets+=1
    found_buckets.sort()

    print("num_buckets: {}, found_buckets: {}".format(num_buckets, found_buckets))

    #If we haven't created the buckets yet, create them
    if num_buckets != required_number_buckets or found_buckets != required_buckets:
        # Delete all the current buckets, for idempotency
        for bucket in storage_client.list_buckets():
            bucket.delete()

        # Create buckets with the appropriate file directory structure
        converted = storage_client.create_bucket("cs378_final_converted_videos")
        raw = storage_client.create_bucket("cs378_final_raw_videos")













"""
Calls Youtube's Data API and returns a JSON containing data about the video,
in the snippet. Specifically, the dict that the json field "snippet" uses

This contains the data for the title and thumbnail, which will later be used in
get_titleget_title() and get_thumbnail()
"""
def get_video_snippet_data(video_id):
    response = {}
    try:
        # print("video_id:{}".format(video_id))
        youtube_query = "https://www.googleapis.com/youtube/v3/videos/?part=snippet&id=" + video_id + "&key=" + YOUTUBE_DATA_API_V3
        raw = requests.get(youtube_query)
        raw_json = raw.json()

        items = raw_json["items"]
        first_item = items[0]
        response = first_item["snippet"]

        # pretty_data = json.dumps(raw.json(), indent=4)
        # print(pretty_data)
    except Exception as e:
        raise VideoSnippetUnavailableException("Video snippet unavailable, see https://developers.google.com/youtube/v3/docs/videos/list")
    return response

"""
Gets the title of the video, using the data from the video snippet
"""
def get_title(video_id):
    title = ""
    try:
        snippet_data = get_video_snippet_data(video_id)
        title = snippet_data["title"]
        if title is None:
            raise VideoTitleUnavailableException("Video title unavailable, see https://developers.google.com/youtube/v3/docs/videos/list")

    except Exception as e:
        print(e)

    return title


"""
Gets the best thumbnail for the videos
Thumbnails has 0-4 different types of thumbnails of varying quality:
Standard, high, medium, default. Sometimes, maxres

Keep going in that order. If we can't find one, go to the next one

Return the URL for the thumbnail image
"""
def get_thumbnail(video_id):
    thumbnail_image_url = ""
    try:
        snippet_data = get_video_snippet_data(video_id)
        thumbnails = snippet_data["thumbnails"]
        if thumbnails is None:
            raise VideoThumbnailUnavailableException("Video thumbnail unavailable, see https://developers.google.com/youtube/v3/docs/videos/list")

        #Find the best thumbnail to use
        thumbnail_ordering = ["high", "maxres", "standard", "medium", "low"]
        index = 0
        found_thumbnail = False

        while found_thumbnail is False:
            thumbnail = thumbnail_ordering[index]
            thumbnail_dict = thumbnails[thumbnail]
            if thumbnail_dict is not None:
                thumbnail_image_url = thumbnail_dict["url"]
                found_thumbnail = True
            index+=1

    except Exception as e:
        print(e)

    return thumbnail_image_url
@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    # Util.create_tables()
    # video_id = "7QBEIVuNrnQ"
    # t = get_title(video_id)
    # th = get_thumbnail(video_id)
    # print("Title: {}, Thumbnail url: {}".format(t,th))
    create_file_structure()
    app.run(host='0.0.0.0')
