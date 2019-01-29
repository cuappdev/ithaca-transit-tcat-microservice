FROM python:3.6

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000 

CMD sh start_server.sh
