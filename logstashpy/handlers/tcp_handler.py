from logging import LogRecord, Formatter
from logging.handlers import SocketHandler
from logstashpy.serialization import Serializer
from logstashpy.formatters.base_formatter import DefaultLogstashFormatter
from logstashpy.formatters.ecs_formatter import ECSStdlibFormatter
from ecs_logging import StdlibFormatter

import logging
import ssl

logger = logging.getLogger(__name__)


class TCPLogstashHandler(SocketHandler):
    '''
    :param fqdn; Indicates whether to show fully qualified domain name or not (default False).
    :param version: version of logstashpy event schema (default is 0).	    :param version: version of logstashpy event schema (default is 0).
    :param tags: list of tags for a logger (default is None).	    :param tags: list of tags for a logger (default is None).
    :param ssl: Should SSL be enabled for the connection? Default is True.
    :param ssl_verify: Should the server's SSL certificate be verified?
    :param keyfile: The path to client side SSL key file (default is None).
    :param certfile: The path to client side SSL certificate file (default is None).
    :param ca_certs: The path to the file containing recognised CA certificates. System wide CA certs are used if omitted.
    '''

    def __init__(self, host, port=5959, serializer='pickle', message_type='logstashpy', tags=None,
                 fqdn=False, ssl = True, ssl_verify=False, keyfile=None, certfile=None, ca_certs=None):
        super(TCPLogstashHandler, self).__init__(host, port)
        self._host = host
        self._port = port
        self._data_serialization = serializer
        self._message_type = message_type
        self.tags = tags
        self._fqdn = fqdn
        self._ssl = ssl
        self.formatter = StdlibFormatter()
        self._ssl_verify = ssl_verify
        self._keyfile = keyfile
        self._certfile = certfile
        self._ca_certs = ca_certs

    def makePickle(self, record: LogRecord) -> bytes:
        return Serializer.serialize(self.formatter.format(record), self._data_serialization)

    def makeSocket(self, timeout=1):
        s = super(TCPLogstashHandler, self).makeSocket()

        if not self._ssl:
            return s

        context = ssl.create_default_context(cafile=self._ca_certs)
        context.verify_mode = ssl.CERT_REQUIRED
        if not self._ssl_verify:
            if self._ca_certs:
                context.verify_mode = ssl.CERT_OPTIONAL
            else:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

        # Client side certificate auth.
        if self._certfile and self._keyfile:
            context.load_cert_chain(self._certfile, keyfile=self._keyfile)

        return context.wrap_socket(s, server_hostname=self._host)
