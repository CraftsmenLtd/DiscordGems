FROM python:3.8-bullseye

RUN apt-get update
RUN apt-get install -y jq make unzip gnupg wget --no-install-recommends

ENV TERRAFORM_VERSION=1.1.2
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -P /tmp/
RUN unzip /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/bin
