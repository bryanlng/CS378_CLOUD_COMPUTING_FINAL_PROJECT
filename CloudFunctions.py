from __future__ import unicode_literals
from flask import escape
from flask import jsonify

from pytube import YouTube
# import youtube_dl
import traceback
import os
import sys
import BucketFileStorage
import Validator
from google.cloud import storage


def download_video(request):
    """
    Calls pytube

    Input:
    return jsonify(request.args)
    request object, which is a Flask Request object
    Extract the following parameters out from request.args:
    1. url:
        -the full url, not just the video id

    Ex:
    https://us-central1-cs378-final-project-media.cloudfunctions.net/download_video_cloud_function?url=https://www.youtube.com/watch?v=BotpJkJ0BKE
    """
    url = str(request.args.get("url"))
    info = {}
    try:
        yt = YouTube(url)
        result = yt.streams.filter(file_extension='mp4').first().download("/tmp")
        main_file = ""
        files_in_tmp = "Files: "
        dirs_in_tmp = " Dirs: "
        for root, dirs, files in os.walk("/tmp"):
            for filename in files:
                main_file += str(os.path.join(root, filename))
                files_in_tmp += str(os.path.join(root, filename))
            for dirname in dirs:
                dirs_in_tmp += str(os.path.join(root, dirname))
        info["files_and_dirs_in_tmp"] = files_in_tmp + dirs_in_tmp
        info["abs_path_to_file"] = os.path.abspath(yt.title + ".mp4")

        #Upload to Google Cloud Bucket
        video_id = Validator.extract_video_id(url)
        bucket_name = "cs378_final_raw_videos"
        source_file_name = main_file
        destination_blob_name = video_id + "::" + yt.title + ".mp4"
        info["video_id"] = video_id
        info["bucket_name"] = bucket_name
        info["source_file_name"] = source_file_name
        info["destination_blob_name"] = destination_blob_name
        BucketFileStorage.upload_object(bucket_name, source_file_name, destination_blob_name)


    except Exception as e:
        error = traceback.print_exc()
        info["problems_traceback"] = str(error)
        info["problems_just_e"] = str(e)

    return jsonify(info)



def convert_video(request):
    """
    Calls FFMPEG

    Requires the following params:
    1. url
    2. desired_format

    Input:
    request object, which is a Flask Request object
    Extract the following parameters out from request.args:
    1. url:
        -the full url, not just the video id
        -we'll use this to create the bucket filename
        -format: <video_id>::<title>.mp4

    2. desired_format:
        -choices:
            -mp3, aac, flac, avi, mov, mkv

    Ex:
    https://us-central1-cs378-final-project-media.cloudfunctions.net/convert_video_cloud_function?url=https://www.youtube.com/watch?v=BotpJkJ0BKE&desired_format=mkv
    """
    url = str(request.args.get("url"))
    desired_format = str(request.args.get("desired_format"))

    info = {}
    try:
        #Create filename
        video_id = Validator.extract_video_id(url)
        yt = YouTube(url)
        filename = video_id + "::" + yt.title + ".mp4"
        info[filename] = filename
        if desired_format != "mp4":
            #It's already in mp4, so we don't have to convert it. Make a copy of it and move it to the converted bucket
            source_bucket_name = "cs378_final_raw_videos"
            dest_bucket_name = "cs378_final_converted_videos"
            info["source_bucket_name"] = "cs378_final_raw_videos"
            info["dest_bucket_name"] = "cs378_final_converted_videos"
            BucketFileStorage.copy_and_write_object(source_bucket_name, filename, dest_bucket_name)
        else:
            

        #Regardless,
    except Exception as e:
        error = traceback.print_exc()
        info["problems_traceback"] = str(error)
        info["problems_just_e"] = str(e)

    return jsonify(info)




# def download_video_youtube_dl(request):
#     """
#     Calls youtube-dl
#
#     Input:
#     return jsonify(request.args)
#     request object, which is a Flask Request object
#     Extract the following parameters out from request.args:
#     1. URL:
#         -the full url, not just the video id
#     """
#
#     # raw = str(request.args["url"])
#     # encoded = raw.encode("utf-8")
#     # url = io.BytesIO(encoded)
#
#     url = str(request.args.get("url"))
#     info = {}
#     # info["type"] = str(type(url))
#     # info["python_version"] = str(sys.version)
#     # info["Version_info"] = str(sys.version_info)
#     # info["url"] = str(url)
#     s = "dummy"
#     info["dummy"] = s
#     try:
#         ydl_opts = {
#             'outtmpl': '/tmp/%(id)s'
#         }
#         ydl_opts = {}
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             result = ydl.download([url])
#
#     except Exception as e:
#         error = traceback.print_exc()
#         info["problems_traceback"] = str(error)
#         info["problems_just_e"] = str(e)
#
#     return jsonify(info)
