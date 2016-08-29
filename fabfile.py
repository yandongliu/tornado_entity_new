from __future__ import absolute_import

from fabric.api import task, local
from fabric.colors import green
import sqlalchemy_utils

from entities import Item, User
from models.base import (
    create_all_tables,
    engine,
    ro_transaction,
    rw_transaction,
)
from models import Item as ModelItem, User as ModelUser


@task
def create_database(environment='development'):
    """Create the database."""
    if not sqlalchemy_utils.database_exists(engine.url):
        sqlalchemy_utils.create_database(engine.url)
    else:
        print green('Database {} already exists'.format(engine.url.database))


@task
def drop_database(environment='development'):
    """Drop the database."""
    if sqlalchemy_utils.database_exists(engine.url):
        sqlalchemy_utils.drop_database(engine.url)
    else:
        print green('Database {} doesn\'t exists'.format(engine.url.database))


@task
def create_tables(environment='development'):
    """Create all tables."""
    create_all_tables()


@task
def drop_table(table):
    """Drop the database."""

    print green('Dropping table %s' % table)
    with rw_transaction() as session:
        session.execute('drop table %s' % table)
        session.commit()
    # Item.drop(engine)


@task
def print_database(environment='development'):
    """print the database."""

    print green('Printing database')
    with ro_transaction() as session:
        rows = session.query(ModelItem).all()
        for row in rows:
            print row.to_dict()


@task
def fake_item(environment='development'):
    """Create fake item."""

    print green('Fake items')
    with rw_transaction() as session:
        user = User.get_mock_object()
        item = Item.get_mock_object()
        item.user_uuid = user.uuid
        print 'Inserting user {}'.format(user.to_primitive())
        print 'Inserting item {}'.format(item.to_primitive())
        model_user = ModelUser(**user.to_primitive())
        model_item = ModelItem(**item.to_primitive())
        session.add(model_user)
        session.add(model_item)


@task
def lint():
    local('flake8')


@task
def serve():
    local('python app.py')
