from __future__ import absolute_import

from uuid import uuid4

from .base import BaseHandler
from services.repositories.tag import TagRepository


class MainHandler(BaseHandler):
    def get(self):
        random_uuid = str(uuid4())
        tags = TagRepository.read_all()
        self.render("template.html", title="My title", tags=tags, random_uuid=random_uuid)
