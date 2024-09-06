FROM python:3.12.5-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN apk add ffmpeg
RUN apk add opus

CMD [ "python", "./app/rainwavebot.py" ]