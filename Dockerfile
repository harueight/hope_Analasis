FROM jupyter/base-notebook:latest
# FROM python:3.12-slim

WORKDIR /home/jovyan/work

# rootユーザーとして実行
USER root

# 使用するパッケージはここで入れる
RUN apt update && apt install -y build-essential && apt install -y git && rm -rf /var/lib/apt/lists/*

COPY . .

USER jovyan

RUN pip install --upgrade pip && pip install -r requirements.txt