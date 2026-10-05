from utils import ColdStartDetector, timer, build_response, setup_logger, get_workload_size

logger = setup_logger()

def lambda_handler(event, context):
    cold_start = ColdStartDetector.is_cold_start()
    workload_size = get_workload_size(event, 0)
    
    with timer() as get_duration:
        # No-op does nothing
        pass
        
    duration_ms = get_duration() * 1000
    
    return build_response(
        function_name="noop",
        duration_ms=duration_ms,
        cold_start=cold_start,
        workload_size=workload_size,
        context=context
    )
