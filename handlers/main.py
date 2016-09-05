from __future__ import absolute_import

from uuid import uuid4

from .base import BaseHandler
from services.repositories.base import EntityRepository


class MainHandler(BaseHandler):
    def get(self):
        random_uuid = str(uuid4())
        root_uuid = 'b0a026a3-2c46-457a-aa24-6b44fc250c82'
        entities = EntityRepository.read_node_chain(root_uuid)
        print entities
        self.render("entity/show.html", title="My title", entities=entities, random_uuid=random_uuid, root_uuid=root_uuid)
