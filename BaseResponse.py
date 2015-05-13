# coding=utf-8

__author__ = 'karl'


class BaseResponse(object):
    # init method
    def __init__(self, head=None, body=None):
        pass

    # set cookie to response
    def set_cookie(self):
        pass

    # get the cookie from request
    def get_cookie(self):
        pass

    # get the argument
    def get_argument(self):
        pass

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
    def response(self):
        pass