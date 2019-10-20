import json
from abc import ABCMeta

import cattr
import yaml


class ObjectBase(object):
    __metaclass__ = ABCMeta

    def __repr__(self):
        fields = []
        for field in self._fields:
            fields.append('{}={}'.format(
                field, getattr(self, field)))

        return "{}({})".format(type(self).__name__,
                               ', '.join(fields))

    def to_dict(self):
        return cattr.unstructure(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def _walk(self, node):
        for key, item in node.items():
            if isinstance(item, dict):
                for sitem in self._walk(item):
                    yield key, sitem
            else:
                yield key, item

    def to_parseble(self):
        parsable = []

        for key, item in self._walk(self.to_dict()):
            if isinstance(item, tuple):
                key = '.'.join([key, item[0]])
                item = item[1]

            parsable.append("{}={}".format(key, item))

        return ' '.join(parsable)

    @classmethod
    def from_dict(cls, dict_):
        return cattr.structure(
            json_loads_byteified(dict_), cls)

    @classmethod
    def from_json(cls, json_):
        return cls.from_dict(yaml.safe_load(
            json.dumps(json_)))


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts=False):
    # # if this is a unicode string, return its string representation
    # if isinstance(data, str):
    #     if data[0:2] == "b'" and data[-1:] == "'":
    #         return data[2:-1]

    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }
    # if it's anything else, return it in its original form
    return data
