FROM python:3.12.5-alpine

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN apk add ffmpeg
RUN apk add opus

ENV DISCORD_TOKEN=
ENV RAINWAVE_ID=
ENV RAINWAVE_KEY=

COPY . /app

CMD [ "python", "./app/rainwavebot.py" ]