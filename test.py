from __future__ import unicode_literals
from flask import escape
from flask import jsonify

from io import BytesIO
import youtube_dl
import traceback
import subprocess
from subprocess import Popen, PIPE


def test():
    request = {
        "url": "https://www.youtube.com/watch?v=jnQ4V-wajLY"
    }
    download_video(request)

def download_video(request):
    """
    Calls youtube-dl

    Input:
    return jsonify(request.args)
    request object, which is a Flask Request object
    Extract the following parameters out from request.args:
    1. URL:
        -the full url, not just the video id
    """

    # raw = str(request.args["url"])
    # encoded = raw.encode("utf-8")
    # url = io.BytesIO(encoded)
    #url = str(request.args["url"])
    url = request["url"]
    info = {}
    try:
        ydl_opts = {
            'outtmpl': '/tmp/%(id)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])


        info["url"] = url
    except Exception as e:
        error = traceback.print_exc()
        info["problems_traceback"] = str(error)
        info["problems_just_e"] = str(e)

    return info

def subcalls():
    filename = "mac_mac_test.mp4"
    output_filename = "mac_mac_test.mkv"
    p = subprocess.Popen(['sudo', 'add-apt-repository', 'ppa:mc3man/trusty-media'], stdin=PIPE, shell=True)
    p.communicate(input='\n')
    p = subprocess.Popen(['sudo', 'apt-get', 'update'], stdin=PIPE, shell=True)
    p.communicate(input='\n')
    p = subprocess.call(['sudo', 'apt-get', 'install', 'ffmpeg'], stdin=PIPE, shell=True)
    p.communicate(input='\n')
    p = subprocess.call(['sudo', 'apt-get', 'install', 'frei0r-plugins'], stdin=PIPE, shell=True)
    p.communicate(input='\n')
    p = subprocess.call(['ffmpeg', '-i', filename, output_filename], stdin=PIPE, shell=True)
    # p = subprocess.call('ffmpeg -i ' + str(filename) + ' ' + str(output_filename), shell=True)

# test()
subcalls()
