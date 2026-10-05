variable "name" {
  description = "Name of the Step Functions state machine"
  type        = string
}

variable "definition" {
  description = "Amazon States Language (ASL) JSON definition"
  type        = string
}

variable "type" {
  description = "Type of state machine: STANDARD or EXPRESS"
  type        = string
  default     = "STANDARD"
}
