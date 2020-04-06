import logging
import msgpack
import json

supported_serializers = [
    'pickle',
    'msgpack'
]

def get_serializer(format):
    if format == 'pickle':
        return json_serializer
    elif format == 'msgpack':
        return msgpack_serializer
    else:
        raise ValueError(format)

def json_serializer(data):
    return bytes(json.dumps(data), 'utf-8')

def msgpack_serializer(data):
    return msgpack.packb(data)

class Serializer():
    @classmethod
    def serialize(cls, data, format='pickle'):
        serializer = get_serializer(format)
        return serializer(data)

