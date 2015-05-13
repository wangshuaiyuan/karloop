# coding=utf-8

__author__ = 'karl'


from BaseApplication import BaseApplication


class Application(BaseApplication):
    def __init__(self):
        super(Application, self).__init__()
        self.handlers = {
            "/hello": "world"
        }


if __name__ == '__main__':
    application = Application()
    application.listen(8421)
    application.run()