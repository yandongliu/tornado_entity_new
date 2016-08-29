from __future__ import absolute_import

from tornado import gen
from tornado import httpclient
from tornado.web import RequestHandler


@gen.coroutine
def fetch_coroutine(url):
    http_client = httpclient.AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)


class AsyncFetchHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        url = self.get_argument('url', 'http://www.google.com')
        resp = yield fetch_coroutine(url)
        self.write(resp)
