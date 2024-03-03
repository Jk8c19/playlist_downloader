FROM python:3.9-slim
ENV DOWNLOAD_DIR=/data
ENV CONFIG_PATH=/opt/yt-dlp.conf
ENV CREATE_AUDIO_PLAYLISTS=False

# Install req'd packages
RUN apt-get update
RUN apt-get -y install bash curl ffmpeg

# Install python packages
COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

COPY run.sh /opt/run.sh
COPY app.py /opt/app.py

CMD bash /opt/run.sh
