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
