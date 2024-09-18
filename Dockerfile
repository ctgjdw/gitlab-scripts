ARG DOCKER_IMAGE
FROM ${DOCKER_IMAGE}

WORKDIR /ansible

ARG PRIVATE_KEY_PATH="key.pem"

COPY . /ansible/

RUN chmod 400 ${PRIVATE_KEY_PATH} && \
    ansible-galaxy collection install ansible-collections/*
