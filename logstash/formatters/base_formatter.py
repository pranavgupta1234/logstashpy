import traceback
import logging
import socket
import sys
from datetime import datetime
import json


def get_extra_fields(record):
    # The list contains all the attributes listed in
    # http://docs.python.org/library/logging.html#logrecord-attributes
    skip_list = (
        'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
        'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module',
        'msecs', 'message', 'msg', 'name', 'pathname', 'process',
        'processName', 'relativeCreated', 'thread', 'threadName', 'extra',
        'stacklevel', 'password', 'stack_info')

    easy_types = (str, bool, dict, float, int, list, type(None))
    extra_fields = {}

    for key, value in record.__dict__.items():
        if key not in skip_list:
            if isinstance(value, easy_types):
                extra_fields[key] = value
            else:
                extra_fields[key] = repr(value)

    return extra_fields

def get_debug_information(record):
    stack_debug_info = {
        'stack_info': traceback.format_stack(record.stack_info)
    }
    return stack_debug_info

def get_process_info(record):
    process_thread_fields = {
        'thread': record.thread,
        'threadName': record.threadName,
        'process': record.processName,
        'processName': record.processName,
    }
    return process_thread_fields


class DefaultLogstashFormatter(logging.Formatter):

    def __init__(self, message_type='Logstash', tags=None, fqdn=False):
        super().__init__()
        self.message_type = message_type
        self.tags = tags if tags is not None else []
        if fqdn:
            self.host = socket.getfqdn()
        else:
            self.host = socket.gethostname()

    '''
    Instead of return string to be serialized, return the object 
    '''
    def format(self, record: logging.LogRecord) -> dict:
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.stack_info:
            record.stack_info = self.formatStack(record.stack_info)

        # update record with
        record.__dict__.update(get_extra_fields(record))

        record.__dict__.update(get_process_info(record))

        return dict(record.__dict__)