resource "aws_cloudwatch_event_rule" "monthly_cron_rule" {
  name                = "${var.prefix}-monthly-gem-cron"
  description         = "Gem summary of every month"
  schedule_expression = "cron(0 5 1 * ? *)"
}

resource "aws_lambda_permission" "allow_cloudwatch_cron" {
  statement_id  = "AllowExecutionFromCloudWatchMonthly"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_functions[local.lambda_options.discord-gems.name].function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.monthly_cron_rule.arn
}

resource "aws_cloudwatch_event_target" "event_target_lambda" {
  rule      = aws_cloudwatch_event_rule.monthly_cron_rule.name
  target_id = "MonthlyGemReport"
  arn       = aws_lambda_function.lambda_functions[local.lambda_options.discord-gems.name].arn
}