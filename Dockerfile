FROM python:3.10

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

CMD python app.py
