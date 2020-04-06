from logging import LogRecord
from logging.handlers import SocketHandler
from logstash.serialization import Serializer
from logstash.formatters.base_formatter import DefaultLogstashFormatter

import logging
import socket

logger = logging.getLogger(__name__)


class TCPLogstashHandler(SocketHandler):
    '''
    host :          Logstash host instance
    port :          Default port for logstash
    formatter :     By default when a handler is created no formatter is attached, similarly if no
                    handler is specified python default formatter will be used. To use bundled formatter
                    specify explicitly
    serialization : serialization format to be used, default is pickle
    '''

    def __init__(self, host, port=5959, logstash_formatter=DefaultLogstashFormatter, serializer='pickle', message_type='logstash', tags=None):
        super(TCPLogstashHandler, self).__init__(host, port)
        self._host = host
        self._port = port
        self._data_serialization = serializer
        self._message_type = message_type
        self._logstash_formatter = logstash_formatter()
        self.tags = tags



    def makePickle(self, record: LogRecord) -> bytes:
        return Serializer.serialize(self._logstash_formatter.format(record), self._data_serialization)

