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
import ffmpy
import subprocess
from subprocess import Popen, run, PIPE

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

        source_bucket_name = "cs378_final_raw_videos"
        dest_bucket_name = "cs378_final_converted_videos"
        info["source_bucket_name"] = source_bucket_name
        info["dest_bucket_name"] = dest_bucket_name
        info["filename"] = filename
        info["desired_format"] = desired_format


        if desired_format == "mp4":
            #It's already in mp4, so we don't have to convert it. Make a copy of it and move it to the converted bucket
            BucketFileStorage.copy_and_write_object(source_bucket_name, filename, dest_bucket_name)
        else:
            #Get file from raw bucket
            BucketFileStorage.download_object(filename, source_bucket_name, "/tmp/" + filename)

            filename_in_tmp = ""
            files_in_tmp = "Files: "
            dirs_in_tmp = " Dirs: "
            for root, dirs, files in os.walk("/tmp"):
                for filename in files:
                    filename_in_tmp += str(os.path.join(root, filename))
                    files_in_tmp += str(os.path.join(root, filename)) + ", "
                for dirname in dirs:
                    dirs_in_tmp += str(os.path.join(root, dirname))
            info["before_files_and_dirs_in_tmp"] = files_in_tmp + dirs_in_tmp
            info["filename_in_tmp"] = filename_in_tmp
            output_filename = filename[:len(filename)-len(desired_format)] + desired_format
            info["output_filename"] = output_filename

            #Run the ffmpeg command using the os.popen command
            # os.popen("ffmpeg -i '{input}' '{output}'.'{format}'".format(input = filename, output = output_filename, format = desired_format))
            # cmds = ['ffmpeg', '-i', filename, output_filename]
            # subprocess.Popen(cmds)
            # p = subprocess.Popen('sudo apt-get update', stdin=PIPE, shell=True, encoding='utf8')
            p = subprocess.run('sudo apt-get update', stdout=PIPE, input='\n', shell=True, encoding='ascii')
            # info["Pass .5"] = "yes"
            # p.communicate(input="\n")
            info["Pass 1: sudo apt-get update"] = "yes"
            # p = subprocess.Popen('sudo apt-get install ffmpeg', stdin=PIPE, shell=True, encoding='utf8')
            p = subprocess.run('sudo apt-get install ffmpeg', stdout=PIPE, input='\n', shell=True, encoding='ascii')
            # p.communicate(input='\n')
            info["Pass 2: sudo apt-get install ffmpeg"] = "yes"
            # p = subprocess.Popen('sudo apt-get install frei0r-plugins', stdin=PIPE, shell=True, encoding='utf8')
            p = subprocess.run('sudo apt-get install frei0r-plugins', stdout=PIPE, input='\n', shell=True, encoding='ascii')
            # p.communicate(input='\n')
            info["Pass 3: sudo apt-get install frei0r-plugins"] = "yes"
            # p = subprocess.Popen('ffmpeg -i ' + str(filename) + ' ' + str(output_filename), shell=True, encoding='utf8')
            p = subprocess.run('ffmpeg -i ' + str(filename) + ' ' + str(output_filename), stdout=PIPE, input='\n', shell=True, encoding='ascii')
            p.communicate(input=None, timeout=None)
            info["Pass 4: ffmpeg -i filename output_filename"] = "yes"

            files_in_tmp = "Files: "
            dirs_in_tmp = " Dirs: "
            for root, dirs, files in os.walk("/tmp"):
                for filename in files:
                    files_in_tmp += str(os.path.join(root, filename)) + ", "
                for dirname in dirs:
                    dirs_in_tmp += str(os.path.join(root, dirname)) + ", "
            info["after_files_and_dirs_in_tmp"] = files_in_tmp + dirs_in_tmp

            output_filename_new_format_in_tmp = filename_in_tmp[:len(filename_in_tmp)-len(desired_format)] + desired_format
            info["output_filename_new_format_in_tmp"] = output_filename_new_format_in_tmp
            # ff = ffmpy.FFmpeg(
            #     inputs={filename: None},
            #     outputs={output_filename: None}
            # )
            # ff.run()

            #Upload to Google Cloud Bucket
            BucketFileStorage.upload_object(source_bucket_name, output_filename_new_format_in_tmp, output_filename)

            #Make a copy of it and move it to the converted bucket
            BucketFileStorage.copy_and_write_object(source_bucket_name, output_filename, dest_bucket_name)

            #Delete the copy of it inside cs378_final_raw_videos bucket
            BucketFileStorage.delete_object(source_bucket_name, output_filename)


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
