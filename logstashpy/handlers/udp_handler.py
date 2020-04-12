from logging.handlers import DatagramHandler
from logstashpy.handlers.tcp_handler import TCPLogstashHandler

class UDPLogstashHandler(TCPLogstashHandler, DatagramHandler):
    pass
