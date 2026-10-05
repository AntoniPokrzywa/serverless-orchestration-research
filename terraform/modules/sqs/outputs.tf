output "url" {
  description = "The URL of the SQS queue"
  value       = aws_sqs_queue.this.url
}

output "arn" {
  description = "The ARN of the SQS queue"
  value       = aws_sqs_queue.this.arn
}

output "name" {
  description = "The name of the SQS queue"
  value       = aws_sqs_queue.this.name
}
