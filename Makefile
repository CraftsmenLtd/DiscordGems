DOCKER_BUILD_EXTRA_ARGS?=--quiet
DOCKER_ENV:=-e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION -e APP_ID -e GUILD_ID -e COMMAND -e TF_BACKEND_BUCKET_NAME -e TF_BACKEND_BUCKET_KEY -e TF_BACKEND_BUCKET_REGION -e TF_VARS -e INTERACTIONS_ENDPOINT_URL -e DISCORD_BOT_TOKEN
DOCKER_RUN_MOUNT_OPTIONS:=-v ${CURDIR}:/app -w /app
RUNNER_IMAGE_NAME?=runner-image
TF_BACKEND_CONFIG=--backend-config="bucket=$(TF_BACKEND_BUCKET_NAME)" --backend-config="key=$(TF_BACKEND_BUCKET_KEY)" --backend-config="region=$(TF_BACKEND_BUCKET_REGION)"
INTERACTIONS_ENDPOINT_URL?=$(shell terraform -chdir=terraform output interactions_endpoint_url)
DISCORD_BOT_TOKEN?=$(shell terraform -chdir=terraform output discord_bot_token)
MAKEFLAGS+= --no-print-directory

install-dependencies:
	pip install -r requirements.txt
.PHONY: install-dependencies

validate-terraform:
	terraform -chdir=terraform init -input=false $(TF_BACKEND_CONFIG)
	terraform -chdir=terraform validate
.PHONY: validate-terraform

lint-terraform:
	terraform -chdir=terraform fmt
.PHONY: lint-terraform

run-tests:
	pytest -s
.PHONY: run-tests

deploy:
	terraform -chdir=terraform init -input=false $(TF_BACKEND_CONFIG)
	terraform -chdir=terraform plan -input=false -out=tfplan-apply $(TF_VARS)
	terraform -chdir=terraform apply -input=false tfplan-apply
.PHONY: deploy

destroy:
	terraform -chdir=terraform init -input=false $(TF_BACKEND_CONFIG)
	terraform -chdir=terraform plan -input=false -out=tfplan-destroy -destroy $(TF_VARS)
	terraform -chdir=terraform destroy -input=false tfplan-destroy
.PHONY: destroy

.SILENT:
register-bot:
	cd utils && INTERACTIONS_ENDPOINT_URL=$(INTERACTIONS_ENDPOINT_URL) DISCORD_BOT_TOKEN=$(DISCORD_BOT_TOKEN) python setup_bot.py
.PHONY: register-bot

build-runner-image:
	docker build -t $(RUNNER_IMAGE_NAME) $(DOCKER_BUILD_EXTRA_ARGS) .
.PHONY: build-runner-image

run-command-in-container-%:
	docker run $(DOCKER_RUN_MOUNT_OPTIONS) $(DOCKER_ENV) $(RUNNER_IMAGE_NAME) make $*
.PHONY: run-command-in-container-%
