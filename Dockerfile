FROM python:3.12.5-alpine

WORKDIR /rainwavediscordbot

#Copying requirements.txt separately prevents everything from being redownloaded on 
#subsequent builds when requirements have not changed, but other files have.
COPY ./requirements.txt /rainwavediscordbot
RUN pip install -r requirements.txt
RUN apk add ffmpeg
RUN apk add opus

ENV DISCORD_TOKEN=
ENV RAINWAVE_ID=
ENV RAINWAVE_KEY=
ENV LOG_LEVEL="INFO"

COPY . /rainwavediscordbot

CMD [ "python", "./app/rainwavebot.py" ]

#Build command `docker build -t rainwavetest .`
#Build Command when using compose `docker-compose up --build`