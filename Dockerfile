FROM python:3.11-alpine

WORKDIR /srv

RUN apk update && apk add python3-dev gcc g++ libc-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
