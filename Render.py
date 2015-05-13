# coding=utf-8

__author__ = 'karl'


import datetime


class Render(object):
    # init method
    def __init__(self, template):
        self.template = template
        self.header = "HTTP/1.1 %s %s\r\n" \
                      "Date: %s\r\n" \
                      "Content-Type: text/html;charset=UTF-8\r\n" \
                      "Cookie: server=run;\r\n\r\n"

    # read the template file
    def parse_template(self, value_dict):
        now = datetime.datetime.now()
        now_time = now.strftime("%a %d %m %Y %H:%M:%S")
        try:
            f = open(self.template)
            template_data = f.read()
            f.close()
        except IOError:
            header = self.header % (500, "template error", now_time)
            return header
        value_keys = value_dict.keys()
        if not value_keys:
            header = self.header % (200, "OK", now_time)
            data = header + template_data
            return data
        for key in value_keys:
            template_data = template_data.replace("{{"+key+"}}", value_dict[key])
            header = self.header % (200, "OK", now_time)
            data = header + template_data
            return data