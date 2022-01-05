FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-20.04

# Install Node 16
ENV NODE_VERSION=16
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash \
    && bash -c ". $HOME/.nvm/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && npm install -g typescript yarn"

# Install packages from apt
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends vim python3-pip python3-setuptools
