DOCKER_BUILD_EXTRA_ARGS?=--quiet
DOCKER_ENV:=-e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION -e APP_ID -e GUILD_ID -e BOT_TOKEN -e COMMAND -e TF_BACKEND_BUCKET_NAME -e TF_BACKEND_BUCKET_KEY -e TF_BACKEND_BUCKET_REGION -e TF_VARS
DOCKER_RUN_MOUNT_OPTIONS:=-v ${CURDIR}:/app -w /app
RUNNER_IMAGE_NAME?=runner-image
TF_BACKEND_CONFIG=--backend-config="bucket=$(TF_BACKEND_BUCKET_NAME)" --backend-config="key=$(TF_BACKEND_BUCKET_KEY)" --backend-config="region=$(TF_BACKEND_BUCKET_REGION)"

MAKEFLAGS+= --no-print-directory

install-dependencies:
	pip install -r requirements.txt
.PHONY: install-dependencies

validate-terraform:
	terraform init -input=false $(TF_BACKEND_CONFIG)
	terraform validate
.PHONY: validate-terraform

deploy:
	terraform init -input=false $(TF_BACKEND_CONFIG)
	terraform plan -input=false -out=tfplan-apply $(TF_VARS)
	terraform apply -input=false tfplan-apply
.PHONY: deploy

destroy:
	terraform init -input=false $(TF_BACKEND_CONFIG)
	terraform plan -input=false -out=tfplan-destroy -destroy $(TF_VARS)
	terraform destroy -input=false tfplan-destroy
.PHONY: destroy

register-bot:
	cd utils && python setup_bot.py

build-runner-image:
	docker build -t $(RUNNER_IMAGE_NAME) $(DOCKER_BUILD_EXTRA_ARGS) .
.PHONY: build-runner-image

run-command-in-container-%:
	docker run $(DOCKER_RUN_MOUNT_OPTIONS) $(DOCKER_ENV) $(RUNNER_IMAGE_NAME) make $*
.PHONY: run-command-in-container-%
