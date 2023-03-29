locals {
  lambda_options = {
    discord-gems = {
      name             = "discord-gems"
      source_directory = "src/discord_gems"
      policy           = data.aws_iam_policy_document.discord_gems_policy
      handler          = "handler.handler"
      timeout          = 900
      memory_size      = 1024
      env_variables = {
        gems_table_name      = aws_dynamodb_table.gems_table.name
        discord_public_key   = var.discord_public_key
        max_gems_per_day     = var.max_gems_per_day
        gems_discord_channel = var.gems_discord_channel
        monthly_cron_rule    = aws_cloudwatch_event_rule.monthly_cron_rule.arn
        credentials_secretsmanager_name = var.credentials_secretsmanager_name
        discord_bot_token_secret_name = var.discord_bot_token_secret_name
      }
    }
  }
}

data "archive_file" "lambda_files" {
  for_each    = local.lambda_options
  output_path = "${path.module}/lambda_zip/${each.key}.zip"
  source_dir  = "${path.module}/../../${each.value.source_directory}"
  excludes    = ["__pycache__", "*.pyc", "test"]
  type        = "zip"
}

resource "aws_lambda_function" "lambda_functions" {
  for_each         = local.lambda_options
  function_name    = "${var.prefix}-${each.value.name}-lambda"
  filename         = data.archive_file.lambda_files[each.key].output_path
  source_code_hash = data.archive_file.lambda_files[each.key].output_base64sha256
  handler          = each.value.handler
  role             = aws_iam_role.lambda_roles[each.key].arn
  runtime          = var.lambda_python_version
  timeout          = lookup(each.value, "timeout", 120)
  memory_size      = lookup(each.value, "memory_size", 128)
  layers           = [var.lambda_layer_arn]

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
