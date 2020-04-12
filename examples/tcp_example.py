import sys

sys.path.insert(0,'../..')

import logging
from logstash.handlers.tcp_handler import TCPLogstashHandler

# Local Logstash server
host = 'localhost'

test_logger = logging.getLogger(__name__)
test_logger.setLevel(logging.INFO)
handler = TCPLogstashHandler(host, 5959)
test_logger.addHandler(handler)

test_logger.error('test logstash error message.')
test_logger.info('test logstash info message.')
test_logger.warning('test logstash warning message.')

# add extra field to logstash message
extra = {
    'test_string': 'cool!',
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}

test_logger.info('test extra fields', extra=extra)