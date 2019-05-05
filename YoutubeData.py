import os
import requests
import json
import CustomExceptions
from CustomExceptions import VideoSnippetUnavailableException, VideoTitleUnavailableException, VideoThumbnailUnavailableException

#Creds
GCP_CS378_MASTER_ADMIN_API_KEY = os.environ.get("GCP_CS378_MASTER_ADMIN_API_KEY", None)

"""
Calls Youtube's Data API and returns a JSON containing data about the video,
in the snippet. Specifically, the dict that the json field "snippet" uses

This contains the data for the title and thumbnail, which will later be used in
get_titleget_title() and get_thumbnail()
"""
def get_video_snippet_data(video_id):
    response = {}
    try:
        # print("video_id:{}".format(video_id))
        youtube_query = "https://www.googleapis.com/youtube/v3/videos/?part=snippet&id=" + video_id + "&key=" + GCP_CS378_MASTER_ADMIN_API_KEY
        raw = requests.get(youtube_query)
        raw_json = raw.json()

        items = raw_json["items"]
        first_item = items[0]
        response = first_item["snippet"]

        # pretty_data = json.dumps(raw.json(), indent=4)
        # print(pretty_data)
    except Exception as e:
        raise VideoSnippetUnavailableException("Video snippet unavailable, see https://developers.google.com/youtube/v3/docs/videos/list. Actual Exception: {}".format(e))
    return response

"""
Gets the title of the video, using the data from the video snippet
"""
def get_title(video_id):
    title = ""
    try:
        snippet_data = get_video_snippet_data(video_id)
        title = snippet_data["title"]
        if title is None:
            raise VideoTitleUnavailableException("Video title unavailable, see https://developers.google.com/youtube/v3/docs/videos/list. Actual Exception: {}".format(e)")
    except Exception as e:
        print(e)
    return title


"""
Gets the best thumbnail for the videos
Thumbnails has 0-4 different types of thumbnails of varying quality:
Standard, high, medium, default. Sometimes, maxres

Keep going in that order. If we can't find one, go to the next one

Return the URL for the thumbnail image
"""
def get_thumbnail(video_id):
    thumbnail_image_url = ""
    try:
        snippet_data = get_video_snippet_data(video_id)
        thumbnails = snippet_data["thumbnails"]
        if thumbnails is None:
            raise VideoThumbnailUnavailableException("Video thumbnail unavailable, see https://developers.google.com/youtube/v3/docs/videos/list. Actual Exception: {}".format(e)")

        #Find the best thumbnail to use
        thumbnail_ordering = ["high", "maxres", "standard", "medium", "low"]
        index = 0
        found_thumbnail = False

        while found_thumbnail is False:
            thumbnail = thumbnail_ordering[index]
            thumbnail_dict = thumbnails[thumbnail]
            if thumbnail_dict is not None:
                thumbnail_image_url = thumbnail_dict["url"]
                found_thumbnail = True
            index+=1

    except Exception as e:
        print(e)

    return thumbnail_image_url
