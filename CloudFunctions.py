from flask import escape
from flask import jsonify

import youtube_dl

def download_video(request, app):
    """
    Calls youtube-dl

    Input:
    return jsonify(request.args)
    request object, which is a Flask Request object
    Extract the following parameters out from request.args:
    1. URL:
        -the full url, not just the video id
    """

    url = str(request.args["URL"])
    # ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    # with ydl:
    #     result = ydl.extract_info(
    #         url,
    #         download=True # We just want to extract the info
    #     )
    #
    # if 'entries' in result:
    #     # Can be a playlist or a list of videos
    #     video = result['entries'][0]
    # else:
    #     # Just a video
    #     video = result

    # video_url = video['url']
    info = {}
    info["url"] = url
    info["type(request.args["URL"])"] = type(request.args["URL"])

    return jsonify(info)
