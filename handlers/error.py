from __future__ import absolute_import

from .base import BaseHandler


class ErrorHandler(BaseHandler):

    def prepare(self):
        self.set_status(404)

    def write_error(self, status_code, **kwargs):
        self.write("<html><body><h1>We've got an error.</h1></body></html>")
