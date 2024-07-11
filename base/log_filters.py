import logging
import uuid
from logging import Filter
from threading import local


class ExcludeStatReloaderFilter(Filter):
    def filter(self, record):
        return 'Watching for file changes with StatReloader' not in record.getMessage()


_local = local()


class TraceIDFilter(logging.Filter):
    def filter(self, record):
        trace_id = getattr(_local, 'trace_id', None)
        if not trace_id:
            trace_id = uuid.uuid4().hex
            _local.trace_id = trace_id
        record.trace_id = trace_id
        return True
