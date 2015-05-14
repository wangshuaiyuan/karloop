# coding=utf-8

__author__ = 'karl'


import socket
import struct
import fcntl
import time
import datetime
import platform
from BaseRequest import BaseRequest
from ParseStatic import ParseStatic


class BaseApplication(object):
    # url mapping
    handlers = {}

    # template and static files settings
    settings = {}

    # http response headers
    headers = "HTTP/1.1 %s %s\r\n" \
              "Date: %s\r\n" \
              "Connection: keep-alive\r\n" \
              "Content-Type: text/html;charset=UTF-8\r\n" \
              "Cookie: server=run;\r\n\r\n"

    # static file name list
    static_file_extension = ["jpeg", "jpg", "gif", "png", "css", "js", "mp3", "ogg", "mp4"]

    # init method
    def __init__(self, handlers=None, settings=None):
        if handlers:
            self.handlers = handlers
        if settings:
            self.settings = settings
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        platform_system = platform.system()
        self.port = 8008
        if platform_system.lower() == "windows":
            host_name = socket.gethostname()
            name = socket.getfqdn(host_name)
            self.ip = socket.gethostbyname(name)
        elif platform_system.lower() == "linux":
            sock_f = self.socket_server.fileno()
            socket_io_address = 0x8915
            if_req = struct.pack('16sH14s', "eth0", socket.AF_INET, '\x00'*14)
            res = fcntl.ioctl(sock_f, socket_io_address, if_req)
            ip = struct.unpack('16sH2x4s8x', res)[2]
            self.ip = socket.inet_ntoa(ip)
        else:
            host_name = socket.gethostname()
            self.ip = socket.gethostbyname(host_name)
        self.parse_static = ParseStatic(settings=settings)

    # listen the port and set max request number
    def listen(self, port=None):
        if port:
            self.port = port
        self.socket_server.bind((self.ip, self.port))
        self.socket_server.listen(50)

    # run the server
    def run(self):
        print "run the server on:", self.ip, ":", self.port
        while True:
            conn, address = self.socket_server.accept()
            conn.settimeout(5)
            try:
                buffer_data = conn.recv(4096)
                response_data = self.parse_data(buffer_data=buffer_data)
                conn.send(response_data)
            except socket.timeout:
                print "time out"
            print "close conn"
            time.sleep(0.5)
            conn.close()

    def parse_data(self, buffer_data):
        now = datetime.datetime.now()
        now_time = now.strftime("%a %d %m %Y %H:%M:%S")
        if not buffer_data:
            return self.headers % (200, "OK", now_time)
        buffer_data_convert = buffer_data.split("\r\n")
        request = BaseRequest(buffer_data_convert)
        method = request.get_request_method()
        url = request.get_request_url()
        extension_name = url.split(".")[-1]
        if extension_name in self.static_file_extension:
            static_file_data = self.parse_static.parse_static(file_url=url)
            return static_file_data
        url_list = self.handlers.keys()
        data = request.get_http_data()
        if url not in url_list:
            response = self.headers % (404, '"request url not found"', now_time)
            return response
        handler = self.handlers[url]
        init_handler = handler(data, self.settings)
        expression = "init_handler." + method + "()"
        try:
            result = eval(expression)
        except Exception:
            response = self.headers % (500, '"server error"', now_time)
            return response
        if result is None:
            response = self.headers % (405, '"request method not found"', now_time)
            return response
        return result