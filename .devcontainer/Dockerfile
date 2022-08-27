# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.245.0/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version (use ubuntu-22.04 or ubuntu-18.04 on local arm64/Apple Silicon): ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="jammy"

FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential git \
    python3-pip python3-dev python3-virtualenv \
    poppler-utils sox attr ffmpeg \
    libsm-dev libxrender-dev libxext-dev libxss-dev libgtk-3-dev \
    ghostscript tesseract-ocr && \
    apt-get install -y libreoffice && \
    apt-get clean


RUN git clone --depth=1 https://gitlab.com/sorcero/community/ingestum /workspaces/ingestum-workshop/src/ingestum && \
    pip install /workspaces/ingestum-workshop/src/ingestum
