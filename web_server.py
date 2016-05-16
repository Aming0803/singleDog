#!/usr/bin/env python
import logging
import os

from tornado.web import Application
from admin.urls import admin_handlers
from apps.urls import apps_handlers
import tornado
from tornado.options import define
from tornado.options import options

import sys
reload(sys)
sys.setdefaultencoding("utf8")


define("port", default=8881, help="run on the given port", type=int)
tornado.options.parse_command_line()


handlers = []
handlers.extend(admin_handlers)
handlers.extend(apps_handlers)

current_path = os.path.dirname(__file__)
static_path = os.path.join(current_path, 'static')
template_path = os.path.join(current_path, 'templates')

settings = dict(
    title=u"",
    desc=u"",
    static_path=static_path,
    template_path=template_path,
    cookie_secret='D/RKv/hSQQqs5I26h3BjkZHhhWc+UUo8gYQNMjNvJuY=',
    login_url='/login',
    xsrf_cookies=False,
    debug=True,
    autoreload = True,
    xheaders=True
)

if __name__ == "__main__":
    app = Application(handlers, **settings)
    app.listen(port = options.port)
    print "Starting server: http://localhost:%s" % (options.port)
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)

    tornado.options.options.logging = "debug"
    tornado.log.LogFormatter(color=True,
                             fmt='%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s',
                             datefmt='%y%m%d %H:%M:%S', colors={40: 1, 10: 4, 20: 2, 30: 3})
    tornado.ioloop.IOLoop.instance().start()