FROM python:3.9
LABEL maintainer='Eyob Tariku'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt ./
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y netcat libcairo2 libpango-1.0-0 \
    libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
COPY  . .

EXPOSE 8000
