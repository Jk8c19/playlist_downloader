#!/bin/bash

# send start hc ping
if [ -n "${HC_URL:-}" ]; then
    echo 'Sending HC starting ping'
    /usr/bin/curl -m 10 --retry 5 "$HC_URL/start"
fi

# download latest version of yt-dlp
echo 'Downloading yt-dlp'
/usr/bin/curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/bin/yt-dlp

# check if download has completed without error
if [ ! -f /usr/bin/yt-dlp ]; then
    echo 'Sending HC failure'
    /usr/bin/curl -m 10 --retry 5 "$HC_URL/fail"
    exit 1
fi

# set file as executable
chmod a+rx /usr/bin/yt-dlp

# run python downloader
mkdir -p $WORKDIR/.logs
python /opt/ytpl-dl.py

# send hc ping
if [ -n "${HC_URL:-}" ]; then
    echo 'Sending HC ping'
    /usr/bin/curl -m 10 --retry 5 $HC_URL
fi

echo 'Done!'
