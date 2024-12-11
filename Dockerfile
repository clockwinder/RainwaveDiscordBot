FROM python:3.12.5-alpine

WORKDIR /rainwavediscordbot

COPY ./requirements.txt /rainwavediscordbot
RUN pip install -r requirements.txt
RUN apk add ffmpeg
RUN apk add opus

ENV DISCORD_TOKEN=
ENV RAINWAVE_ID=
ENV RAINWAVE_KEY=

COPY . /rainwavediscordbot

CMD [ "python", "./app/rainwavebot.py" ]

#Build command `docker build -t rainwavetest .`