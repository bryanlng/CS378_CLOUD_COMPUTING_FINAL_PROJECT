from __future__ import unicode_literals
from flask import escape
from flask import jsonify

from io import BytesIO
import youtube_dl
import traceback
import subprocess
from subprocess import Popen, PIPE
# import ffmpy
import ffmpeg



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
    #p = subprocess.Popen(['sudo', 'add-apt-repository', 'ppa:mc3man/trusty-media'], stdin=PIPE, shell=True)
    #p.communicate(input='\n')
    #print("pass 1\n\n\n")
    p = subprocess.Popen('sudo apt-get update', stdin=PIPE, shell=True)
    p.communicate(input='\n')
    print("Pass 2\n\n\n")
    p = subprocess.Popen('sudo apt-get install ffmpeg', stdin=PIPE, shell=True)
    p.communicate(input='\n')
    print("Pass 3\n\n\n")
    p = subprocess.Popen('sudo apt-get install frei0r-plugins', stdin=PIPE, shell=True)
    p.communicate(input='\n')
    print("Pass 4\n\n\n")
    p = subprocess.Popen('ffmpeg -i ' + str(filename) + ' ' + str(output_filename), shell=True)
    p.communicate(input='\n')
    print("Pass 5\n\n\n")

# def ffmpymine(filename, output_filename):
#     ff = ffmpy.FFmpeg(
#         inputs={filename: None},
#         outputs={output_filename: None}
#     )
#     ff.run()

def ffmpegkorenig(filename,output_filename):
    stream = ffmpeg.input(filename)
    stream = ffmpeg.output(stream, output_filename)
    ffmpeg.run(stream)

# test()
# subcalls()
# ffmpymine("spoderman.mp4", "spoderman.mp3")
# ffmpegkorenig("spoderman.mp4", "spoderman.mp3")

exec(open("ffmpeg.exe").read())
