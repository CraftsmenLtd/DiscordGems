variable "prefix" {
  type        = string
  description = "AWS Resources name prefix"
}

variable "discord_public_key_secrets_arn" {
  type        = string
  description = "Discord bot public key in general information page"
}

variable "max_gems_per_day" {
  type        = number
  description = "Max gems for an user per day"
  default = 5
}

variable "discord_gems_channel" {
  type        = string
  description = "Allowed discord channel to provide gem"
}

variable "discord_bot_token_secret_arn" {
  type        = string
  description = "Discord bot token arn of ssm"
  sensitive = true
}
