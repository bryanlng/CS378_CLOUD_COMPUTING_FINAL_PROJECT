import os
import time
from urllib.parse import urlparse

import requests
import json

from flask import request
from flask import Flask, render_template

import Validator
import CustomExceptions

application = Flask(__name__)
app = application


#Creds
YOUTUBE_DATA_API_V3 = os.environ.get("YOUTUBE_DATA_API_V3", None)





@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    test_url = "https://www.youtube.com/watch?v=URNN-_az-3g"
    test_url = "https://youtu.be/40BNY41SJCI"
    try:
        Validator.validate_youtube_url(test_url)
    except Exception as e:
        print(e)
    app.run(host='0.0.0.0')
