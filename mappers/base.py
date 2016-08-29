from __future__ import absolute_import


class EntityMapper(object):
    """Base mapper for creating models automatically from a resource map."""
    _entity = None
    _strict = False
    field_source = {}

    @classmethod
    def to_entity(cls, resource):
        """Return a standard model entity.
        :param resource:
        """
        if cls._entity is None:
            raise ValueError('_entity must be specified.')

        map_ = {}
        cls.build_map(map_, resource)
        entity = cls._entity(map_)
        # entity.validate(strict=cls._strict) # TODO
        return entity

    @classmethod
    def build_map(cls, map_, resource):
        """Return a map containing just the mixin component."""
        for name, field in cls._entity.fields.iteritems():
            resource_key = cls.field_source.get(name, name)
            value = resource.get(resource_key)
            if value is None:
                map_[name] = None
            else:
                map_[name] = field.to_native(value)

    @classmethod
    def to_record(cls, entity):
        """Converts schematics object into object consumed by gateways/repositories.
        :param entity:
        :return:
        :rtype dict
        """
        if cls._entity is None:
            raise ValueError('_entity must be specified.')
        if not isinstance(entity, cls._entity):
            raise TypeError('Expected instance of {0}'.format(cls._entity))
        entity.validate()
        return cls._to_record(entity)

    @classmethod
    def _to_record(cls, entity):
        """Convert an entity into primitives (dict)
        :param entity:
        :return:
        :rtype dict
        """
        record = {}
        for name, field in cls._entity.fields.iteritems():
            value = getattr(entity, name)
            resource_key = cls.field_source.get(name, name)
            if value is None:
                record[resource_key] = None
            else:
                record[resource_key] = field.to_primitive(value)
        return record

    @classmethod
    def to_entity_from_obj(cls, obj_resource):
        return cls.to_entity(dict(obj_resource.items()))

