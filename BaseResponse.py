# coding=utf-8

__author__ = 'karl'


import datetime
from Security import DES


class BaseResponse(object):
    # init method
    def __init__(self, data):
        self.des = DES()
        self.des.input_key('123456789')
        self.response_head = "HTTP/1.1 %s %s\r\n" \
                             "Date: %s\r\n" \
                             "Content-Type: text/html;charset=UTF-8\r\n" \
                             "Cookie: server=run; \r\n\r\n"
        self.data = data

    # set cookie to response
    def set_cookie(self, key, value):
        key = str(key)
        value = str(value)
        cookie_string = '%s="%s";' % (key, value)
        cookie_string_replace = "server=run; " + cookie_string
        self.response_head.replace("server=run; ", cookie_string_replace)

    # get the cookie from request
    def get_cookie(self, key):
        return self.data["cookie"][key]

    # set cookie encrypted by DES
    def set_security_cookie(self, key, value):
        value = self.des.encode(value)
        self.set_cookie(key, value)

    # get cookie encrypted by DES
    def get_security_cookie(self, key):
        cookie = self.data["cookie"][key]
        return self.des.decode(cookie)

    # get the argument
    def get_argument(self, key):
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
        now_time = now.strftime("%a %d %m %Y %H:%M:%S")
        response_data = self.response_head % (status, status_m, now_time)
        response_data += body
        return response_data

    # set head
    def set_head(self, value):
        self.response_head.replace("text/html;charset=UTF-8", value)