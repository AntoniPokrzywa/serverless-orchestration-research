variable "queue_name" {
  description = "Name of the SQS queue"
  type        = string
}

variable "visibility_timeout_seconds" {
  description = "The visibility timeout for the queue in seconds"
  type        = number
  default     = 30
}

variable "message_retention_seconds" {
  description = "The number of seconds Amazon SQS retains a message"
  type        = number
  default     = 3600 # 1 hour
}

variable "max_message_size" {
  description = "The limit of how many bytes a message can contain"
  type        = number
  default     = 262144 # 256 KB
}

variable "dead_letter_target_arn" {
  description = "ARN of the dead-letter queue to receive messages after max_receive_count is exceeded"
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags to assign to the queue"
  type        = map(string)
  default     = {}
}
