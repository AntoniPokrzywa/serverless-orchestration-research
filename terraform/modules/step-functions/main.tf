resource "aws_sfn_state_machine" "this" {
  name       = var.name
  type       = var.type
  definition = var.definition
}
