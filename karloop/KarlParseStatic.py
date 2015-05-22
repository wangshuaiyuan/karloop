# coding=utf-8

__author__ = 'karl'

import sys
import datetime
from Security import DES
from karloop.base_configure import base_settings


class ParseStatic(object):
    # define the common response head
    header = "HTTP/1.1 %s %s\r\n" \
             "Host: %s\r\n" \
             "Connection: keep-alive\r\n" \
             "Date: %s\r\n" \
             "Content-Type: %s\r\n\r\n"

    # define the media response head
    media_header = "HTTP/1.1 %s %s\r\n" \
                   "Host: %s\r\n" \
                   "Accept-Ranges: bytes\r\n" \
                   "Content-Length: %s\r\n" \
                   "Content-Range: bytes %s\r\n" \
                   "Etag: \"%s\"\r\n" \
                   "Date: %s\r\n" \
                   "Content-Type: %s\r\n\r\n"

    # define static file content type
    content_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "css": "text/css",
        "js": "text/js",
        "mp3": "audio/mpeg",
        "ogg": "audio/ogg",
        "mp4": "video/mp4"
    }

    # init method
    def __init__(self, settings=None):
        if settings:
            self.settings = settings
        else:
            self.settings = {}

    # read the static files
    def parse_static(self, file_url, media_range=None):
        file_abstract_path = self.settings["static"] + file_url
        f = open(file_abstract_path)
        if media_range:
            media_range = int(media_range)
            f.seek(media_range)
        data = f.read()
        f.close()
        file_extension = file_url.split(".")[-1]
        file_extension = file_extension.lower()
        now = datetime.datetime.now()
        now_time = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        security = DES()
        security.input_key('123456789')
        element_tag = security.encode(file_url)
        content_type = self.content_type[file_extension] if (file_extension in self.content_type) else ""
        content_length = sys.getsizeof(data)
        if media_range is None:
            media_range = 0
        content_range = "%s-%s/%s" % (media_range, media_range+content_length-38, media_range+content_length-37)
        if file_extension in ["mp3", "mp4", "ogg"]:
            header = self.media_header % (
                206,
                "Partial Content",
                base_settings["host"],
                content_length-37,
                content_range,
                element_tag,
                now_time,
                content_type
            )
        else:
            header = self.header % (
                200,
                "OK",
                base_settings["host"],
                now_time,
                content_type
            )
        header += data
        return header
