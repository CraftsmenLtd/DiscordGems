variable "prefix" {
  type        = string
  description = "AWS Resources name prefix"
}

variable "discord_public_key_secrets_arn" {
  type        = string
  description = "Discord bot public key in general information page"
  sensitive   = true
}

variable "max_gems_per_day" {
  type        = number
  description = "Max gems for an user per day"
  default     = 5
}

variable "lambda_max_concurrency" {
  type        = number
  description = "Max number of lambda that can run at a given time"
  default     = 5
}

variable "discord_gems_channel" {
  type        = string
  description = "Allowed discord channel to provide gem"
  sensitive   = true
}

variable "discord_bot_token_secret_arn" {
  type        = string
  description = "Discord bot token arn of ssm"
  sensitive   = true
}

variable "secrets_manager_cache_lambda_layer_account_id" {
  type        = string
  description = "The secrets manager caching layer arn for your region. Default set to ap-south-1. More https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html#ps-integration-lambda-extensions-add"
  default     = "176022468876"
}

variable "secrets_manager_cache_lambda_layer_version" {
  type        = number
  description = "The secrets manager caching layer version for your region. Default set to 4. More https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html#ps-integration-lambda-extensions-add"
  default     = 4
}
