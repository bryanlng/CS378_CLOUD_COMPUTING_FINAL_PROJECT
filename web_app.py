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
import YoutubeData
import BucketFileStorage
import CustomExceptions
from CustomExceptions import NotaYoutubeURLException, VideoChartNotFoundException, ForbiddenVideoException, VideoNotFoundException, VideoSnippetUnavailableException, VideoTitleUnavailableException, VideoThumbnailUnavailableException

application = Flask(__name__)
app = application


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    # Util.create_tables()
    # video_id = "7QBEIVuNrnQ"
    # t = YoutubeData.get_title(video_id)
    # th = YoutubeData.get_thumbnail(video_id)
    # print("Title: {}, Thumbnail url: {}".format(t,th))
    # create_file_structure()
    # BucketFileStorage.create_file_structure()
    app.run(host='0.0.0.0')
