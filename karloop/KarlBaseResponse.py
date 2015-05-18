# coding=utf-8

__author__ = 'karl'

import datetime

from karloop.Security import DES
from karloop.KarlRender import Render
from karloop.base_configure import base_settings


class BaseResponse(object):
    # init method
    def __init__(self, data, settings):
        self.des = DES()
        self.des.input_key('123456789')
        self.response_head = "HTTP/1.1 %s %s\r\n" \
                             "Host: %s\r\n" \
                             "Date: %s\r\n" \
                             "Connection: keep-alive\r\n" \
                             "Content-Type: text/html;charset=UTF-8\r\n" \
                             "Set-Cookie: server=run; path=/\r\n"
        self.data = data
        self.settings = settings

    # set cookie to response
    def set_cookie(self, key, value, expires_days=1):
        key = str(key)
        value = str(value)
        now_time = datetime.datetime.now()
        expires_days = now_time + datetime.timedelta(days=expires_days)
        expires_days = expires_days.strftime("%a, %d %b %Y %H:%M:%S GMT")
        cookie_string = 'Set-Cookie: %s="%s"; expires=%s; Path=/\r\n' % (key, value, expires_days)
        self.response_head = self.response_head.replace("Set-Cookie: server=run; path=/\r\n", cookie_string)

    # get the cookie from request
    def get_cookie(self, key):
        if key not in self.data["cookie"]:
            return ""
        cookie = self.data["cookie"][key]
        if cookie.startswith('"') and cookie.endswith('"'):
            cookie = cookie[1:len(cookie)-1]
            return cookie
        return cookie

    # set cookie encrypted by DES
    def set_security_cookie(self, key, value):
        value = self.des.encode(value)
        self.set_cookie(key, value)

    # get cookie encrypted by DES
    def get_security_cookie(self, key):
        cookie = self.get_cookie(key)
        return self.des.decode(cookie)

    # get the argument
    def get_argument(self, key):
        if key not in self.data["parameter"]:
            return ""
        return self.data["parameter"][key]

    # get method
    def get(self):
        pass

    # post method
    def post(self):
        pass

    # options method
    def options(self):
        pass

    # head method
    def head(self):
        pass

    # put method
    def put(self):
        pass

    # delete method
    def delete(self):
        pass

    # response to the request
    def response(self, body=None):
        status = 200
        status_m = "OK"
        now = datetime.datetime.now()
        now_time = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response_data = self.response_head % (status, status_m, base_settings["host"], now_time)
        response_data += "\r\n"
        response_data += body
        return response_data

    # set head
    def set_head(self, value):
        self.response_head = self.response_head.replace("text/html;charset=UTF-8", value)

    # render method
    def render(self, template_path, parameter_dit=None):
        abstract_path = self.settings["template"] + template_path if ("template" in self.settings) else template_path
        r = Render(template=abstract_path)
        return r.parse_template(parameter_dit)
