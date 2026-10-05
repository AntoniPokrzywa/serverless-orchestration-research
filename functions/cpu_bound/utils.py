import os
import time
import logging
import json
from contextlib import contextmanager

# Global flag to track cold starts
# It gets setted up as AWS provisions Firecracker microVM
_is_cold_start = True

class ColdStartDetector:
    @staticmethod
    def is_cold_start():
        global _is_cold_start
        if _is_cold_start:
            _is_cold_start = False
            return True
        return False

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger

@contextmanager
def timer():
    start = time.perf_counter()
    yield lambda: time.perf_counter() - start

def build_response(function_name, duration_ms, cold_start, workload_size, context, extra_data=None):
    # Context provides memory limit and request ID
    memory_limit = getattr(context, 'memory_limit_in_mb', 128)
    request_id = getattr(context, 'aws_request_id', 'local-test-id')
    
    response = {
        "function_name": function_name,
        "execution_duration_ms": duration_ms,
        "cold_start": cold_start,
        "memory_allocated": int(memory_limit),
        "memory_used": None, # Lambda doesn't expose this directly in the execution context easily
        "workload_size": workload_size,
        "timestamp": time.time(),
        "request_id": request_id
    }
    
    if extra_data:
        response.update(extra_data)
        
    return response

def get_workload_size(event, default):
    try:
        if 'workload_size' in event:
            return int(event['workload_size'])
        if 'body' in event and isinstance(event['body'], str):
            body = json.loads(event['body'])
            if 'workload_size' in body:
                return int(body['workload_size'])
    except Exception:
        pass
    return default
