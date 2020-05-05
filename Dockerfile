FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DJANGO_DB_HOST="db" \
    DJANGO_DB_PORT="5432" \
    DJANGO_SUPERUSER_NAME="cat" \
    DJANGO_SUPERUSER_MAIL="cat@mail" \
    DJANGO_SUPERUSER_PASS="meow"

WORKDIR /mango

COPY requirements.txt /mango/
RUN pip3 install -r requirements.txt

COPY . /mango/
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["runserver", "0.0.0.0:8000"]
