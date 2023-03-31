# DiscordGems

## Required Env Variables

| Variable Name | Description | Default Value |
| ------------- | ------------- | ------------- |
| APP_ID | Application Id from Discord | None |
| AWS_ACCESS_KEY_ID | Access Key Id from aws | None |
| AWS_DEFAULT_REGION | Default region to deploy resources in | None |
| AWS_SECRET_ACCESS_KEY | Secret Access Key from aws | None |
| BOT_TOKEN | Bot Token from Discord | None |
| COMMAND | Command in discord to register | None |
| GUILD_ID | Guild/Server Id from Discord | None |
| RUNNER_IMAGE_NAME | Runner image name | runner-image |
| TF_BACKEND_BUCKET_KEY | Key name to store terraform state as | None |
| TF_BACKEND_BUCKET_NAME | Bucket name to store terraform state in | None |
| TF_BACKEND_BUCKET_REGION | Region of the terraform state bucket | None |

## Terraform Specific Variables
| Variable Name | Description | Default Value |
| ------------- | ------------- | ------------- |
| prefix | Application Id from Discord | None |
| discord_public_key_secrets_arn | Access Key Id from aws | None |
| max_gems_per_day | Default region to deploy resources in | None |
| discord_gems_channel | Secret Access Key from aws | None |
| discord_bot_token_secret_arn | Discord bot token arn of secrets manager | None |
### Passing Terraform Variables as Environment
If you are running the terraform code in our provided container you must pass terraform variables as TF_VARS.
Example:
```shell
TF_VARS='-var="prefix=a_prefix" -var="max_gems_per_day=5"' make run-command-in-container-deploy
```
