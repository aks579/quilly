FROM python:3.6.15-slim-buster

RUN mkdir -p /app
RUN mkdir -p /app/app
RUN mkdir -p /app/data

COPY app /app/app
COPY requirements.txt /app/requirements.txt
COPY run.py /app/entrypoint.py

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

EXPOSE 80

ENTRYPOINT [ "gunicorn" ]
CMD ["--bind", "0.0.0.0:80", "entrypoint:app"]

