#!/bin/bash

# download latest version of yt-dlp
echo 'Downloading yt-dlp'
/usr/bin/curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/bin/yt-dlp

# set file as executable
chmod a+rx /usr/bin/yt-dlp

# run python script
python /opt/app.py
