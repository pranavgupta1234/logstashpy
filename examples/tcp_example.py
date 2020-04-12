import sys

sys.path.insert(0,'../..')

import logging
from logstashpy.handlers.tcp_handler import TCPLogstashHandler

# Local Logstash server
host = 'localhost'

test_logger = logging.getLogger(__name__)
test_logger.setLevel(logging.INFO)
handler = TCPLogstashHandler(host, 5959)
test_logger.addHandler(handler)

test_logger.error('test logstashpy error message.')
test_logger.info('test logstashpy info message.')
test_logger.warning('test logstashpy warning message.')

# add extra field to logstashpy message
extra = {
    'test_string': 'cool!',
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}

test_logger.info('test extra fields', extra=extra)