import unittest
import os, sys

sys.path.insert(0, os.path.join(os.getcwd(), "../logstash/"))

from logstash.serialization import (json_serializer,
                                    msgpack_serializer,
                                    append_newline_byte,
                                    append_newline
                                    )
import json

class SerializationTests(unittest.TestCase):

    def test_append_newline(self):
        somedata = "somedata"
        self.assertEqual(f'{somedata}\n', append_newline(somedata))

    def test_append_newline_bytes(self):
        somedata = b'somedata'
        self.assertEqual(somedata+b'\n', append_newline_byte(somedata))

    def test_json_serialization(self):
        sample_json = {
            'a' : 5,
            'b' : 6
        }
        input_str_for_logstash = bytes(json.dumps(sample_json)) + b'\n'
        self.assertEqual(json_serializer(json.dumps(sample_json)), input_str_for_logstash)
