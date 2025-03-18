FROM python:3
WORKDIR /app
COPY . .
RUN apt-get update
RUN pip install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:5000 wsgi:app

