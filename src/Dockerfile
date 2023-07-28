#
FROM python:3.9

#
WORKDIR /src

#
COPY ../requirements.txt /src/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

#
COPY ./app /src/app
COPY ./migrations /src/migrations
COPY ./alembic.ini /src/alembic.ini

COPY start.sh /start.sh
RUN chmod +x /start.sh
ENTRYPOINT "/start.sh"
