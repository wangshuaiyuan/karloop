# coding=utf-8

__author__ = 'karl'


from BaseApplication import BaseApplication
from BaseResponse import BaseResponse
import json


class World(BaseResponse):
    def post(self):
        value = self.get_argument("hello")
        self.set_head("application/json;charset=UTF-8")
        data = {
            "value": value
        }
        return self.response(json.dumps(data))


class Application(BaseApplication):
    def __init__(self):
        super(Application, self).__init__()
        self.handlers = {
            "/hello": World
        }


if __name__ == '__main__':
    application = Application()
    application.listen(8421)
    application.run()