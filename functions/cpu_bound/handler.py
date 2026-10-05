import random
from utils import ColdStartDetector, timer, build_response, setup_logger, get_workload_size

logger = setup_logger()

def generate_matrix(size):
    return [[random.random() for _ in range(size)] for _ in range(size)]

def multiply_matrices(A, B, size):
    result = [[0.0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += A[i][k] * B[k][j]
    return result

def lambda_handler(event, context):
    cold_start = ColdStartDetector.is_cold_start()
    workload_size = get_workload_size(event, 100)
    
    try:
        with timer() as get_duration:
            matrix_a = generate_matrix(workload_size)
            matrix_b = generate_matrix(workload_size)
            result = multiply_matrices(matrix_a, matrix_b, workload_size)
            
        duration_ms = get_duration() * 1000
        
        return build_response(
            function_name="cpu_bound",
            duration_ms=duration_ms,
            cold_start=cold_start,
            workload_size=workload_size,
            context=context,
            extra_data={"status": "success"}
        )
    except Exception as e:
        logger.error(f"Error in cpu_bound: {str(e)}")
        raise
