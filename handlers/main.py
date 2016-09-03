from __future__ import absolute_import

from uuid import uuid4

from .base import BaseHandler
from services.repositories.tag import TagRepository


class MainHandler(BaseHandler):
    def get(self):
        random_uuid = str(uuid4())
        root_uuid = '3bf2125d-e289-4afe-a0ab-584eb378e9d1'
        tags = TagRepository.read_chain(root_uuid)
        self.render("template.html", title="My title", tags=tags, random_uuid=random_uuid, root_uuid=root_uuid)
