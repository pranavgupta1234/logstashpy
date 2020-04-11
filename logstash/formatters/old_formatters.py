from logstash.formatters.base_formatter import LogstashFormatterBase
from logstash.formatters.base_formatter import (get_extra_fields,
                                                get_process_info,
                                                get_debug_information)
from logstash.formatters.base_formatter import (format_source,
                                                format_timestamp,
                                                format_exception)
import json

class LogstashFormatterVersion0(LogstashFormatterBase):
    version = 0

    def format(self, record):
        # Create message dict
        message = {
            '@timestamp': format_timestamp(record.created),
            '@message': record.getMessage(),
            '@source': format_source(self.message_type, self.host,
                                          record.pathname),
            '@source_host': self.host,
            '@source_path': record.pathname,
            '@tags': self.tags,
            '@type': self.message_type,
            '@fields': {
                'levelname': record.levelname,
                'logger': record.name,
            },
        }

        # Add extra fields
        message['@fields'].update(get_extra_fields(record))
        # Add process, thread info
        message['@fields'].update(get_process_info(record))
        # If exception, add debug info
        if record.exc_info:
            message['@fields'].update(get_debug_information(record))

        return json.dumps(message)


class LogstashFormatterVersion1(LogstashFormatterBase):

    def format(self, record):
        # Create message dict
        message = {
            '@timestamp': format_timestamp(record.created),
            '@version': '1',
            'message': record.getMessage(),
            'host': self.host,
            'path': record.pathname,
            'tags': self.tags,
            'type': self.message_type,

            # Extra Fields
            'level': record.levelname,
            'logger_name': record.name,
        }

        # Add extra fields
        message['@fields'].update(get_extra_fields(record))
        # Add process, thread info
        message['@fields'].update(get_process_info(record))
        # If exception, add debug info
        if record.exc_info:
            message['@fields'].update(get_debug_information(record))

        return json.dumps(message)