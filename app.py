from __future__ import absolute_import

import tornado.ioloop
import tornado.web

import config
from handlers import api, http_api
from handlers.async_fetch import AsyncFetchHandler
from handlers.main import MainHandler
from handlers.json_api import JsonApiHandler


def make_application():
    settings = config.get('tornado')
    _app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/json_api", JsonApiHandler),
        (r"/api/tag", api.TagHandler),
        (r"/api/tag/(?P<tag_uuid>[^\/]*)", api.TagHandler),
        (r"/http_api/tag/", http_api.TagHandler),
        (r"/http_api/tag/(?P<tag_uuid>[^\/]*)", http_api.TagHandler),
        (r"/http_api/delete_tag/(?P<tag_uuid>[^\/]*)", http_api.DeleteTagHandler),
        (r"/http_api/add_sub/", http_api.AddSubTagHandler),
        (r"/http_api/add_sub/(?P<tag_uuid>[^\/]*)", http_api.AddSubTagHandler),
        (r"/http_api/edit/", http_api.EditTagHandler),
        (r"/http_api/edit/(?P<tag_uuid>[^\/]*)", http_api.EditTagHandler),
        (r"/async_fetch", AsyncFetchHandler),
    ], **settings)
    return _app

if __name__ == "__main__":
    application = make_application()
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
