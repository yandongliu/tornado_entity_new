from __future__ import absolute_import

from .base import BaseHandler


class MainHandler(BaseHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="My title", items=items)
