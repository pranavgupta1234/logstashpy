from logging.handlers import DatagramHandler
from logstash.handlers.tcp_handler import TCPLogstashHandler

class UDPLogstashHandler(TCPLogstashHandler, DatagramHandler):
    pass
