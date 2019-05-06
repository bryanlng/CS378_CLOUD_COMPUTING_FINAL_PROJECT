import os
import time
from urllib.parse import urlparse

import requests
import json

from flask import request
from flask import Flask, render_template

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
    return CloudFunctions.download_video(request, app)
    # return 'Hello World!'
    # content_type = request.headers['content-type']
    # if content_type == 'application/json':
    #     request_json = request.get_json(silent=True)
    #     if request_json and 'name' in request_json:
    #         name = request_json['name']
    #     else:
    #         raise ValueError("JSON is invalid, or missing a 'name' property")
    # elif content_type == 'application/octet-stream':
    #     name = request.data
    # elif content_type == 'text/plain':
    #     name = request.data
    # elif content_type == 'application/x-www-form-urlencoded':
    #     name = request.form.get('name')
    # else:
    #     raise ValueError("Unknown content type: {}".format(content_type))
    # return 'Hello {}!'.format(escape(name))
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

    #Check if (video id, media format) pair exists in the converted bucket
    #If it does, find the video in the bucket



def download_video():
    #Make a HTTP get call to our cloud function
    response = None
    try:
        query = "https://www.googleapis.com/youtube/v3/videos/?part=snippet&id=" + video_id + "&key=" + GCP_CS378_MASTER_ADMIN_API_KEY
        response = requests.get(youtube_query)

    except Exception as e:
        print(e)
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
    # BucketFileStorage.get_object_from_bucket("doesntexist.txt", "cs378_final_raw_videos")
    app.run(host='0.0.0.0')
