import logging
import msgpack
import json

supported_serializers = [
    'pickle',
    'msgpack'
]

def append_newline(data):
    return data+"\n"

def append_newline_byte(data):
    return data+b'\n'

def get_serializer(format):
    if format == 'pickle':
        return json_serializer
    elif format == 'msgpack':
        return msgpack_serializer
    else:
        raise ValueError(format)

def json_serializer(data):
    if type(data) is bytes:
        return append_newline_byte(data)

    if type(data) is dict:
        data = json.dumps(data)

    return bytes(append_newline(data), 'utf-8')

def msgpack_serializer(data):
    record_dict = json.loads(data)
    return msgpack.packb(record_dict)


class Serializer():
    @classmethod
    def serialize(cls, data, format='pickle'):
        serializer = get_serializer(format)
        return serializer(data)

