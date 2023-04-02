data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_secretsmanager_secret_version" "discord_bot_token" {
  secret_id = var.discord_bot_token_secret_arn
}
