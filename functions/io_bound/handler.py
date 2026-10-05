import os
import boto3
import uuid
import string
import random
from utils import ColdStartDetector, timer, build_response, setup_logger, get_workload_size

logger = setup_logger()
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    cold_start = ColdStartDetector.is_cold_start()
    workload_size = get_workload_size(event, 100) # Size in KB
    
    bucket_name = os.environ.get('BENCHMARK_BUCKET')
    if not bucket_name:
        raise ValueError("BENCHMARK_BUCKET environment variable is required")
        
    try:
        with timer() as get_duration:
            # Generate random payload
            payload_size_bytes = workload_size * 1024
            # A simple way to generate random string data
            chars = string.ascii_letters + string.digits
            payload = ''.join(random.choices(chars, k=min(payload_size_bytes, 1000)))
            if payload_size_bytes > 1000:
                payload = payload * (payload_size_bytes // 1000) + payload[:payload_size_bytes % 1000]
                
            object_key = f"io_bound_test_{context.aws_request_id if hasattr(context, 'aws_request_id') else uuid.uuid4()}.txt"
            
            # Write to S3
            s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=payload.encode('utf-8'))
            
            # Read back from S3
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            read_payload = response['Body'].read()
            
            # Delete from S3
            s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            
        duration_ms = get_duration() * 1000
        
        return build_response(
            function_name="io_bound",
            duration_ms=duration_ms,
            cold_start=cold_start,
            workload_size=workload_size,
            context=context,
            extra_data={"status": "success", "bytes_transferred": payload_size_bytes * 2}
        )
    except Exception as e:
        logger.error(f"Error in io_bound: {str(e)}")
        raise
