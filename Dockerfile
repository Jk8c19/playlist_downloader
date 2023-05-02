FROM python:3.9-slim
ENV WORKDIR=/media
ENV DLTYPE=mp3

# Install req'd packages
RUN apt-get update
RUN apt-get -y install bash curl ffmpeg

COPY download.sh /opt/download.sh
COPY ytpl-dl.py /opt/ytpl-dl.py

CMD "/opt/download.sh"