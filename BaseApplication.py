# coding=utf-8

__author__ = 'karl'


import socket
import struct
import fcntl
import time


class BaseApplication(object):
    # url mapping
    handlers = {}

    # http response headers
    headers = "HTTP/1.1 %s %s\r\nDate: %s\r\nContent-Type: text/html;charset=UTF-8\r\n"

    # init method
    def __init__(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        name = socket.getfqdn(host_name)
        self.ip = socket.gethostbyname(name)
        self.port = 8008
        sock_f = self.socket_server.fileno()
        socket_io_address = 0x8915
        if_req = struct.pack('16sH14s', "eth0", socket.AF_INET, '\x00'*14)
        res = fcntl.ioctl(sock_f, socket_io_address, if_req)
        ip = struct.unpack('16sH2x4s8x', res)[2]
        self.ip = socket.inet_ntoa(ip)

    # listen the port and set max request number
    def listen(self, port=None):
        if port:
            self.port = port
        self.socket_server.bind((self.ip, self.port))
        self.socket_server.listen(10)

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
        buffer_data_convert = buffer_data.split("\r\n")
        request_method = buffer_data_convert[0].split(" ")[0]
        request_url = buffer_data_convert[0].split(" ")[1]
        url_list = self.handlers.keys()
        if request_url not in url_list:
            pass
        print "-----------------------------------------"
        print len(buffer_data_convert)
        print buffer_data
        print "-----------------------------------------"
        print self.handlers
        return "HTTP/1.1 200 OK\r\nDate: Sat, 31 Dec 2005 23:59:59 GMT\r\nContent-Type: text/html;charset=UTF-8\r\nContent-Length: 800\r\nConnection: keep-alive\n\r\n\r<html><head><title>Wrox Homepage</title></head><body>hello world!%s</body></html>" % self.handlers[request_url]