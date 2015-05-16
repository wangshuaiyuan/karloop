# coding=utf-8

__author__ = 'karl'

import socket
import struct
import fcntl
import time
import sys
import datetime
import platform
import threading

from base_configure import base_settings
from karloop.KarlBaseRequest import BaseRequest
from karloop.KarlParseStatic import ParseStatic


class BaseApplication(object):
    # init method
    def __init__(self, handlers=None, settings=None):
        if handlers:
            self.handlers = handlers
        if settings:
            self.settings = settings
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = base_settings["port"]
        if "ip" in settings.keys():
            self.ip = settings["ip"]
            base_settings["ip"] = self.ip
        else:
            self.__set_ip()

    # set IP address
    def __set_ip(self):
        platform_system = platform.system()
        if platform_system.lower() == "windows":
            host_name = socket.gethostname()
            name = socket.getfqdn(host_name)
            self.ip = socket.gethostbyname(name)
            base_settings["ip"] = self.ip
        elif platform_system.lower() == "linux":
            sock_f = self.socket_server.fileno()
            socket_io_address = 0x8915
            if_req = struct.pack('16sH14s', "eth0", socket.AF_INET, '\x00'*14)
            res = fcntl.ioctl(sock_f, socket_io_address, if_req)
            ip = struct.unpack('16sH2x4s8x', res)[2]
            self.ip = socket.inet_ntoa(ip)
            base_settings["ip"] = self.ip
        else:
            host_name = socket.gethostname()
            self.ip = socket.gethostbyname(host_name)
            base_settings["ip"] = self.ip

    # listen the port and set max request number
    def listen(self, port=None):
        if port:
            self.port = port
        base_settings["host"] = str(self.ip) + ":" + str(self.port)
        self.socket_server.bind((self.ip, self.port))
        self.socket_server.listen(50)

    # run the server
    def run(self):
        print "run the server on:", self.ip, ":", self.port
        while True:
            conn, address = self.socket_server.accept()
            buffer_data = conn.recv(4096)
            async_parse_data = AsyncParseData(conn, buffer_data, self.handlers, self.settings)
            async_parse_data.run()


class AsyncParseData(threading.Thread):
    def __init__(self, connection, data, handlers, settings):
        threading.Thread.__init__(self)
        self.connection = connection
        self.data = data
        self.parse_data = ParseData(handlers=handlers, settings=settings)

    def run(self):
        response_data = self.parse_data.parse_data(buffer_data=self.data)
        response_data_size = sys.getsizeof(response_data)
        lock_time = response_data_size / (1024 * 256)
        response_url = self.data.split("\r\n")[0].split(" ")[1]
        if response_url.endswith(".mp3") or response_url.endswith(".ogg") or response_url.endswith(".mp4"):
            self.connection.settimeout(None)
        else:
            self.connection.settimeout(lock_time + 5)
        try:
            self.connection.sendall(response_data)
            time.sleep(lock_time)
        except socket.timeout:
            print "time out"
        print "connection close"
        self.connection.close()


class ParseData(object):
    # url mapping
    handlers = {}

    # template and static files settings
    settings = {}

    # http response headers
    headers = "HTTP/1.1 %s %s\r\n" \
              "Date: %s\r\n" \
              "Host: %s\r\n" \
              "Connection: keep-alive\r\n" \
              "Content-Type: text/html;charset=UTF-8\r\n" \
              "Set-Cookie: server=run;\r\n\r\n"

    # static file name list
    static_file_extension = ["jpeg", "jpg", "gif", "png", "css", "js", "mp3", "ogg", "mp4"]

    # init method
    def __init__(self, handlers, settings):
        self.handlers = handlers
        self.parse_static = ParseStatic(settings=settings)
        self.settings = settings

    # parse the data from client
    def parse_data(self, buffer_data):
        now = datetime.datetime.now()
        now_time = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        if not buffer_data:
            return self.headers % (200, "OK", now_time, base_settings["host"])
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
            response = self.headers % (404, '"request url not found"', now_time, base_settings["host"])
            return response
        handler = self.handlers[url]
        init_handler = handler(data, self.settings)
        expression = "init_handler." + method + "()"
        try:
            result = eval(expression)
        except Exception:
            response = self.headers % (500, '"server error"', now_time, base_settings["host"])
            return response
        if result is None:
            response = self.headers % (405, '"request method not allowed"', now_time, base_settings["host"])
            return response
        return result