FROM debian:bullseye-slim

RUN apt-get update
RUN apt-get install -y jq make unzip gnupg --no-install-recommends

# install correct python verion

# install correct terraform version
