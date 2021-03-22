FROM python:3.8
LABEL maintainer='Eyob Tariku'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY Pipfile* ./
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y netcat libcairo2 libpango-1.0-0 \
    libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info && \
    pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system
COPY  . .

EXPOSE 8000
