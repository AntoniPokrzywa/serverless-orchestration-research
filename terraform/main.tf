terraform {
  required_version = ">= 1.5.0"
}

locals {
  lambda_role_arn = "arn:aws:iam::123456789012:role/${var.project_name}-placeholder"
  lambda_runtime  = "python3.12"
  lambda_handler  = "handler.lambda_handler"
}

module "basic_lambda" {
  source      = "./modules/lambda"
  function_name = "${var.project_name}-basic"
  role_arn    = local.lambda_role_arn
  source_dir  = "../functions/basic"
  handler     = local.lambda_handler
  runtime     = local.lambda_runtime
  memory_size = 128
  timeout     = 30
}

module "cpu_bound_lambda" {
  source      = "./modules/lambda"
  function_name = "${var.project_name}-cpu-bound"
  role_arn    = local.lambda_role_arn
  source_dir  = "../functions/cpu_bound"
  handler     = local.lambda_handler
  runtime     = local.lambda_runtime
  memory_size = 256
  timeout     = 30
}

module "io_bound_lambda" {
  source      = "./modules/lambda"
  function_name = "${var.project_name}-io-bound"
  role_arn    = local.lambda_role_arn
  source_dir  = "../functions/io_bound"
  handler     = local.lambda_handler
  runtime     = local.lambda_runtime
  memory_size = 256
  timeout     = 30
  environment_variables = {
    BENCHMARK_BUCKET = "${var.project_name}-benchmark-bucket"
  }
}

module "sequential_step_functions" {
  source  = "./modules/step-functions"
  name    = "${var.project_name}-sequential"
  type    = "STANDARD"
  definition = templatefile("${path.module}/state-machines/sequential.asl.json", {
    basic_arn     = module.basic_lambda.arn
    cpu_bound_arn = module.cpu_bound_lambda.arn
    io_bound_arn   = module.io_bound_lambda.arn
  })
}

module "async_sqs_queue" {
  source    = "./modules/sqs"
  queue_name = "${var.project_name}-async-sqs"
}
