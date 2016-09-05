from __future__ import absolute_import

import tornado.ioloop
import tornado.web

import config
from handlers import api, http_api_attr, http_api_entity
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
        (r"/http_api/entity/(?P<uuid>[^\/]*)", http_api_entity.ShowHandler),
        (r"/http_api/entity/delete/(?P<uuid>[^\/]*)", http_api_entity.DeleteHandler),
        (r"/http_api/entity/add_sub/(?P<uuid>[^\/]*)", http_api_entity.AddSubHandler),
        (r"/http_api/entity/edit/(?P<uuid>[^\/]*)", http_api_entity.EditHandler),
        (r"/http_api/attr/(?P<uuid>[^\/]*)", http_api_attr.ShowHandler),
        (r"/async_fetch", AsyncFetchHandler),
    ], **settings)
    return _app

if __name__ == "__main__":
    application = make_application()
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
