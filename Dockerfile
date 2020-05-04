FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /mango

COPY requirements.txt /mango/
RUN pip3 install -r requirements.txt

COPY . /mango/