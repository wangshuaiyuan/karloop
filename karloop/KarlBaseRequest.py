# coding=utf-8

__author__ = 'karl'


class BaseRequest(object):
    # init method
    def __init__(self, data_list):
        self.data_list = data_list
        self.convert_data_list = dict({})
        self.convert_data_list["method"] = data_list[0].split(" ")[0].lower()
        self.convert_data_list["url"] = data_list[0].split(" ")[1].split("?")[0]
        self.convert_data_list["http_version"] = data_list[0].split(" ")[2]
        for data in data_list:
            if "Cookie" in data:
                self.convert_data_list["cookie"] = data.split("Cookie: ")[1]
            if "Range: bytes=" in data:
                self.convert_data_list["content_range"] = data.replace("Range: bytes=", "").split("-")[0]

    # get content range
    def get_content_range(self):
        if "content_range" in self.convert_data_list.keys():
            return self.convert_data_list["content_range"]
        return None

    # get request method
    def get_request_method(self):
        return self.convert_data_list["method"]

    # get request url
    def get_request_url(self):
        return self.convert_data_list["url"]

    # get http version
    def get_http_version(self):
        return self.convert_data_list["http_version"]

    # get http cookie data and parameter data
    def get_http_data(self):
        # define the return data's structure
        data = {
            "cookie": {},
            "parameter": {}
        }
        # get the parameters in url
        param_url = self.data_list[0].split(" ")[1].split("?")
        if len(param_url) > 1:
            param_url = param_url[1].split("&")
            for param in param_url:
                param_key_value = param.split("=")
                if len(param_key_value) > 1:
                    key = param_key_value[0]
                    value = param_key_value[1]
                else:
                    key = param_key_value[0]
                    value = ""
                data["parameter"][key] = value
        # get the parameters in body
        param_body = self.data_list[-1]
        if param_body:
            param_body = param_body.split("&")
            for param in param_body:
                param_key_value = param.split("=")
                if len(param_key_value) > 1:
                    key = param_key_value[0]
                    value = param_key_value[1]
                else:
                    key = param_key_value[0]
                    value = ""
                data["parameter"][key] = value
        if "cookie" in self.convert_data_list.keys():
            cookie_list = self.convert_data_list["cookie"].split("; ")
            for cookie in cookie_list:
                for i in range(len(cookie)):
                    if cookie[i] == "=":
                        key = cookie[0: i]
                        value = cookie[i+1: len(cookie)]
                        data["cookie"][key] = value
        return data
