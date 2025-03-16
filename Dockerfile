FROM python:3.10

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn -w 1 -t 60 -b 0.0.0.0:5000 app:app
