# pull official base image
FROM python:3.9.4-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY . .
COPY ./requirements.txt .
RUN pip install --no-cache -r requirements.txt
# copy project
COPY . .