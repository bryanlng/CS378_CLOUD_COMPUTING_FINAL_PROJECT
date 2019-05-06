from __future__ import unicode_literals
from flask import escape
from flask import jsonify

import youtube_dl
import traceback

import sys




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

    url = str(request.args.get("url"))
    info = {}
    # info["type"] = str(type(url))
    # info["python_version"] = str(sys.version)
    # info["Version_info"] = str(sys.version_info)
    # info["url"] = str(url)
    s = "dummy"
    info["dummy"] = s
    try:
        ydl_opts = {
            'outtmpl': '/tmp/%(id)s'
        }
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])

    except Exception as e:
        error = traceback.print_exc()
        info["problems_traceback"] = str(error)
        info["problems_just_e"] = str(e)

    return jsonify(info)
