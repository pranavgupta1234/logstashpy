from ecs_logging import StdlibFormatter, StructlogFormatter
from ecs_logging._utils import normalize_dict

'''
To potentially override the behaviour of ECS formatter
These ECS Formatters do not return string for logrecord 
but a dict instead
'''

class ECSStdlibFormatter(StdlibFormatter):
    def format(self, record):
        record_dict = self.format_to_ecs(record)
        return record_dict

class ECSStructlogFormatter(StructlogFormatter):

    def __call__(self, _, name, event_dict):
        event_dict = normalize_dict(event_dict)
        event_dict.setdefault("log", {}).setdefault("level", name)
        event_dict = self.format_to_ecs(event_dict)
        return event_dict