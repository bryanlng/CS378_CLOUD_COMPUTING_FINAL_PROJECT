import os
import time
from urllib.parse import urlparse

import requests
import json

from flask import request
from flask import Flask, render_template
from flask import jsonify

import Validator
import YoutubeData
import BucketFileStorage
import CloudFunctions
import CustomExceptions
from CustomExceptions import NotaYoutubeURLException, VideoChartNotFoundException, ForbiddenVideoException, VideoNotFoundException, VideoSnippetUnavailableException, VideoTitleUnavailableException, VideoThumbnailUnavailableException

application = Flask(__name__)
app = application


#####################
###Cloud Functions###
#####################
def download_video_cloud_function(request):
    """ Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>

    Ex:
        https://us-central1-cs378-final-project-media.cloudfunctions.net/download_video_cloud_function?url=no

    """
    return CloudFunctions.download_video(request)


def convert_video_cloud_function(request):
    """ Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>

    Ex:
        https://us-central1-cs378-final-project-media.cloudfunctions.net/download_video_cloud_function?url=no

    """
    return CloudFunctions.convert_video(request)
#####################
###Cloud Functions###
#####################


#######################################################################
###Web App Backend Functions###########################################
#######################################################################
@app.route("/convert_video")
def main_process():
    print("Main process")
    #Grab parameters (url, format to convert to, time stamps)

    #Validate URL

    #Check if (video id, media format) pair exists in the converted bucket
    #If it does, find the video in the bucket



def download_video(url):
    """
    Input:      Youtube URL
    Make a HTTP get call to our cloud function
    """
    response = {}
    try:
        query = "https://us-central1-cs378-final-project-media.cloudfunctions.net/download_video_cloud_function?url=" + url
        raw_response = requests.get(query)

        #Continually poll our bucket until the video we want exists in the raw bucket
        filename = Validator.extract_video_id(url) + ".mp4"
        bucket_name = "cs378_final_raw_videos"
        time_to_download = 0
        video_downloaded = False
        while video_downloaded is False:
            print("Polling raw bucket for {}".format(filename))
            video_downloaded = BucketFileStorage.get_object_from_bucket(filename, bucket_name) is not None
            time.sleep(1)
            time_to_download +=1

        print("Successfully downloaded video, output filename: {}, took {} seconds".format(filename, time_to_download))
        print("Download video cloud function output: {}".format(raw_response))
        response["successfully_downloaded"] = True
        response["time_to_download"] = time_to_download
        response["response"] = raw_response
    except Exception as e:
        response["error"] = str(e)

    return response


def convert_video(url, desired_format):
    """
    Input:      Youtube URL, desired_format
    Make a HTTP get call to our cloud function
    """
    response = {}
    try:
        query = "https://us-central1-cs378-final-project-media.cloudfunctions.net/convert_video_cloud_function?url=" + url + "&desired_format=" + desired_format
        raw_response = requests.get(query)

        #Continually poll our bucket until the video we want exists in the converted bucket
        filename = Validator.extract_video_id(url) + "." + desired_format
        bucket_name = "cs378_final_converted_videos"
        time_to_download = 0
        video_converted = False
        while video_converted is False:
            print("Polling converted bucket for {}".format(filename))
            video_converted = BucketFileStorage.get_object_from_bucket(filename, bucket_name) is not None
            time.sleep(1)
            time_to_download +=1

        print("Successfully converted video, output filename: {}, took {} seconds".format(filename, time_to_download))
        print("Convert video cloud function output: {}".format(raw_response))
        response["successfully_downloaded"] = True
        response["time_to_download"] = time_to_download
        response["response"] = raw_response
    except Exception as e:
        response["error"] = str(e)

    return response





def initialize():
    BucketFileStorage.create_file_structure()

@app.route("/")
def hello():
    return render_template('index.html')


#######################################################################
###Web App Backend Functions###########################################
#######################################################################

if __name__ == "__main__":
    app.debug = True
    # video_id = "7QBEIVuNrnQ"
    # video_id = "Y-DvKfsG18w"
    # t = YoutubeData.get_title(video_id)
    # th = YoutubeData.get_thumbnail(video_id)
    # print("Title: {}, Thumbnail url: {}".format(t,th))
    # BucketFileStorage.create_file_structure()
    initialize()
    url = "https://www.youtube.com/watch?v=BotpJkJ0BKE"
    desired_format = "mp3"
    download_video(url)
    convert_video(url, desired_format)
    # BucketFileStorage.get_object_from_bucket("doesntexist.txt", "cs378_final_raw_videos")
    app.run(host='0.0.0.0')
