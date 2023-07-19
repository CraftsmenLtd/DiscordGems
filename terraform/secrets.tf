data "aws_secretsmanager_secret" "discord_public_key_secret" {
  arn = var.discord_public_key_secret_arn
}

data "aws_secretsmanager_secret" "discord_bot_token_secret" {
  arn = var.discord_bot_token_secret_arn
}

data "aws_secretsmanager_secret_version" "discord_public_key" {
  secret_id = data.aws_secretsmanager_secret.discord_public_key_secret.id
}

data "aws_secretsmanager_secret_version" "discord_bot_token" {
  secret_id = data.aws_secretsmanager_secret.discord_bot_token_secret.id
}
