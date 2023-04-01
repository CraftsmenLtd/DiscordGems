output "interactions_endpoint_url" {
  value = aws_lambda_function_url.discord_gems_url.function_url
}
