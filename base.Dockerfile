FROM python:3.8.2-slim-buster
RUN apt-get update && apt-get install -y --no-install-recommends --yes vim netcat

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
