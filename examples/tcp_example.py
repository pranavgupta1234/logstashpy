import sys

sys.path.insert(0,'../..')

import logging
from logstash.handlers.tcp_handler import TCPLogstashHandler

host = 'localhost'

test_logger = logging.getLogger('python-logstash-logger')
test_logger.setLevel(logging.INFO)
test_logger.addHandler(TCPLogstashHandler(host, 5959))

test_logger.error('python-logstash: test logstash error message.')
test_logger.info('python-logstash: test logstash info message.')
test_logger.warning('python-logstash: test logstash warning message.')

# add extra field to logstash message
extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}

test_logger.info('python-logstash: test extra fields', extra=extra)