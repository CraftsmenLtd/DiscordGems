data "aws_iam_policy_document" "lambda_assume_role_policy" {
  version = "2012-10-17"

  statement {
    sid     = "LambdaAssume"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "cloudwatch_log_policy" {
  version = "2012-10-17"

  statement {
    sid = "LambdaLogPolicy"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogStreams"
    ]

    resources = [
      "arn:aws:logs:*:${data.aws_caller_identity.current.account_id}:*"
    ]
  }
}

data "aws_iam_policy_document" "discord_gems_policy" {
  source_policy_documents = [data.aws_iam_policy_document.cloudwatch_log_policy.json]

  statement {
    sid    = "SecretsmanagerPolicy"
    effect = "Allow"
    actions = [
      "secretsmanager:*"
    ]
    resources = [
      var.discord_bot_token_secret_arn,
      var.discord_public_key_secret_arn,
      "arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "dynamodb:Scan",
      "dynamodb:Query",
      "dynamodb:PutItem",
      "dynamodb:DeleteItem",
      "dynamodb:DescribeTable",
    ]
    resources = [
      aws_dynamodb_table.gems_table.arn
    ]
  }
}
