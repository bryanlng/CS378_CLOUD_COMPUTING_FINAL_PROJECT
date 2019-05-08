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
@app.route("/convert_video", methods = ['GET'])
def main_process():
    #Grab parameters (url, format to convert to, time stamps)
    url = str(request.args.get("url"))
    desired_format = str(request.args.get("desired_format"))

    info = {}
    info["url"] = url
    info["desired_format"] = desired_format
    converted_video = None
    try:
        #Validate URL
        Validator.validate_youtube_url(url)

        #Check if (video id, media format) pair exists in the converted bucket
        converted_filename = Validator.extract_video_id(url) + "." + desired_format
        converted_bucket = "cs378_final_converted_videos"
        converted_file = BucketFileStorage.get_object_from_bucket(converted_filename, converted_bucket)

        #If the video doesn't exist in the converted bucket:
        if converted_file is None:
            #Check if video id pair exists in the raw bucket
            raw_filename = Validator.extract_video_id(url) + "." + desired_format
            raw_bucket = "cs378_final_raw_videos"
            raw_file = BucketFileStorage.get_object_from_bucket(raw_filename, raw_bucket)

            #If the video hasn't been downloaded yet, make a call to our download cloud function to download it
            if raw_file is None:
                download_video(url)

            #Aftewards, convert the video into
            convert_video(url, desired_format)

        #Download video from converted bucket
        BucketFileStorage.download_object(converted_filename, converted_bucket, converted_filename)

    except Exception as e:
        print(e)

    return jsonify(info)




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
        response["response"] = str(raw_response.json())
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
        response["response"] = str(raw_response.json())
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
    initialize()
    app.run(host='0.0.0.0')
