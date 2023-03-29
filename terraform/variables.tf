variable "prefix" {
  type        = string
  description = "AWS Resources name prefix"
}

variable "lambda_layer_arn" {
  type        = string
  description = "lambda layer arn"
}

variable "lambda_python_version" {
  type        = string
  description = "aws lambda python version"
}

variable "discord_public_key" {
  type        = string
  description = "Discord bot public key in general information page"
}

variable "max_gems_per_day" {
  type        = number
  description = "Max gems for an user per day"
}

variable "gems_discord_channel" {
  type        = string
  description = "Allowed discord channel to provide gem"
}

variable "credentials_secretsmanager_name" {
  type        = string
  description = "Secretsmanager name for all kind of credentials"
}

variable "discord_bot_token_secret_name" {
  type        = string
  description = "Discord bot token arn of ssm"
  default     = "discord_bot_token"
}