from __future__ import absolute_import

import httplib
import ujson as json

from tornado.web import RequestHandler


def _to_dict(message):
    if isinstance(message, dict):
        data = message
    elif isinstance(message, list):
        # import pdb; pdb.set_trace()
        data = [_to_dict(m) for m in message]
    else:
        data = dict(message=str(message))

    return data


class BaseHandler(RequestHandler):

    def json_response(self, message=None, code=httplib.OK):
        data = _to_dict(message)
        self.set_header("Content-Type", "application/json")
        self.set_status(code)
        self.write(json.dumps(data))
