# Base image: Node 16 & Debian Buster
FROM mcr.microsoft.com/vscode/devcontainers/javascript-node:16-buster

# Install packages from apt
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends vim python3-pip python3-setuptools
