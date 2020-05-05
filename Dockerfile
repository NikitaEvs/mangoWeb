FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DJANGO_DB_HOST="db" \
    DJANGO_DB_PORT="5432" \
    DJANGO_SUPERUSER_NAME="cat" \
    DJANGO_SUPERUSER_MAIL="cat@mail" \
    DJANGO_SUPERUSER_PASS="meow"

RUN mkdir mango
WORKDIR /mango

COPY requirements.txt /mango/
RUN pip3 install -r requirements.txt

COPY . /mango/
RUN chmod +x /mango/docker-entrypoint.sh

ENTRYPOINT ["/mango/docker-entrypoint.sh"]
CMD ["runserver", "0.0.0.0:8000"]
