from __future__ import unicode_literals
from flask import escape
from flask import jsonify

from io import BytesIO
import youtube_dl
import traceback

application = Flask(__name__)
app = application



def test():
    request = {
        "url": "https://us-central1-cs378-final-project-media.cloudfunctions.net/download_video_cloud_function?url=https://www.youtube.com/watch?v=jnQ4V-wajLY"
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
    url = str(request.args["url"])
    info = {}
    try:
        ydl_opts = {
            'outtmpl': '/tmp/%(id)s'
        }
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download(str('https://www.youtube.com/watch?v=dP15zlyra3c'))


        info["url"] = url
    except Exception as e:
        error = traceback.print_exc()
        info["problems_traceback"] = str(error)
        info["problems_just_e"] = str(e)

    return jsonify(info)



if __name__ == "__main__":
    app.debug = True
    test()
    app.run(host='0.0.0.0')
