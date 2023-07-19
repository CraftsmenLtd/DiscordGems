locals {
  lambda_options = {
    discord-gems = {
      name                 = "discord-gems"
      source_directory     = "src"
      policy               = data.aws_iam_policy_document.discord_gems_policy
      handler              = "handler.handler"
      timeout              = 120
      memory_size          = 512
      publish_lambda       = true
      reserved_concurrency = var.lambda_reserved_concurrency
      env_variables = {
        gems_table_name      = aws_dynamodb_table.gems_table.name
        discord_public_key   = data.aws_secretsmanager_secret_version.discord_public_key.secret_string
        max_gems_per_day     = var.max_gems_per_day
        discord_gems_channel = var.discord_gems_channel
        monthly_cron_rule    = aws_cloudwatch_event_rule.monthly_cron_rule.arn
        discord_bot_token    = data.aws_secretsmanager_secret_version.discord_bot_token.secret_string
      }
    }
  }
}

data "archive_file" "lambda_files" {
  for_each    = local.lambda_options
  output_path = "${path.module}/lambda_zip/${each.key}.zip"
  source_dir  = "${path.module}/../${each.value.source_directory}"
  excludes    = ["__pycache__", "*.pyc", "test"]
  type        = "zip"
}

resource "aws_lambda_function" "lambda_functions" {
  for_each                       = local.lambda_options
  function_name                  = "${var.prefix}-${each.value.name}-lambda"
  filename                       = data.archive_file.lambda_files[each.key].output_path
  source_code_hash               = data.archive_file.lambda_files[each.key].output_base64sha256
  handler                        = each.value.handler
  role                           = aws_iam_role.lambda_roles[each.key].arn
  runtime                        = local.lambda_python_version
  timeout                        = lookup(each.value, "timeout", 120)
  memory_size                    = lookup(each.value, "memory_size", 128)
  layers                         = [aws_lambda_layer_version.lambda_layer.arn]
  publish                        = lookup(each.value, "publish_lambda", false)
  reserved_concurrent_executions = lookup(each.value, "reserved_concurrency", -1)
  architectures                  = ["arm64"]
  environment {
    variables = lookup(each.value, "env_variables", {})
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_function_url" "discord_gems_url" {
  function_name      = aws_lambda_function.lambda_functions[local.lambda_options.discord-gems.name].function_name
  authorization_type = "NONE"
}

resource "aws_lambda_function_event_invoke_config" "invoke_config" {
  for_each                     = local.lambda_options
  function_name                = aws_lambda_function.lambda_functions[each.value.name].function_name
  maximum_event_age_in_seconds = var.lambda_maximum_event_age_in_seconds
  maximum_retry_attempts       = 2
}
