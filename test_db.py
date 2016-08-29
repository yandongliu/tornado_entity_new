import random

from models.base import session
from models.item import Item


def random_text():
    return 5 * random.choice('asdfsd3432sdf'.split())

new_record = Item('Genius', random_text())
session.add(new_record)
session.commit()

all_records = session.query(Item).all()
print all_records
