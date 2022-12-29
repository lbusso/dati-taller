#Base image
FROM python:3.10

#Envirment variables
ENV PYTHONDONTWHRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#wORK DIRETORY
WORKDIR /code

#Install Dependencies
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

#Copy project
COPY . /code/