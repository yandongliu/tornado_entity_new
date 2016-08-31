from __future__ import absolute_import

from .base import BaseHandler
from services.repositories.tag import TagRepository


class MainHandler(BaseHandler):
    def get(self):
        tags = TagRepository.read_all()
        self.render("template.html", title="My title", tags=tags)
