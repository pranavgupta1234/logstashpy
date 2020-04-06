from logging import LogRecord
from logging.handlers import DatagramHandler
from logstash.serialization import Serializer
from logstash.formatters import default_formatter

class UDPLogstashHandler(DatagramHandler):

    def __init__(self, host, port=5959, logstash_formatter=default_formatter,
                 serialization_format='pickle', message_type='logstash',
                 tags=None, fqdn=False, version=0):
        super(UDPLogstashHandler, self).__init__(host, port)
        self._logstash_formatter = default_formatter
        self._data_serialization = serialization_format


    def makePickle(self, record: LogRecord) -> bytes:
        return Serializer.serialize(self._logstash_formatter(LogRecord),
                                    self._data_serialization)