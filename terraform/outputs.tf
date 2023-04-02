output "interactions_endpoint_url" {
  value = aws_lambda_function_url.discord_gems_url.function_url
  sensitive = true
}

output "discord_bot_token" {
  value = data.aws_secretsmanager_secret_version.discord_bot_token.secret_string
  sensitive = true
}