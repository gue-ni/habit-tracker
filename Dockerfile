FROM python:3.11-alpine

WORKDIR /srv

RUN apk update && apk add python3-dev gcc g++ libc-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

VOLUME /srv/db

EXPOSE 5000

ENV FLASK_APP=app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--capture-output", "--log-level", "debug", "app:create_app()"]
