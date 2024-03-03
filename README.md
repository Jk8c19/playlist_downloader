# playlist_downloader
I needed a way to download and keep up to date a collection of youtube music playlist. This container will, with the latest version of yt-dlp download .mp3's into a mounted volume.

Run the container with
```bash
docker run \
  --name=pl_dl \
  --rm \
  -e HC_URL=" \
  -e "TEMPLATE_PATH=<Path to Jinja2 configuration template file>" \
  -e "DOWNLOAD_DIR=<Directory to download files into>" \
  -e "ARCHIVE_PATH=<Path to the yt-dlp '–download-archive' parameter>" \
  -e "BATCH_PATH=<Path to the yt-dlp '-a' parameter>" \
  -e "CREATE_AUDIO_PLAYLISTS=<True/False>" \
  -v <path to download folder>:/media \
  jk8c19/playlist_downloader:latest
```

This container will exit on completion so using --rm will clean up once it's done its thing.

## Health Checks

Passing a Health Checks HTTP url with the `HC_URL` variable will signal start, success and failure of the container

## Configuration Templates

The container will take in a Jinja2 template file from the `TEMPLATE_PATH` environment variable to be used for generating the config file passed to yt-dlp.
The following variables are mapped to:

| Config Variable | Container Env | yt-dlp Parameter
|-|-|-|
| {{ downloadDir }} | DOWNLOAD_DIR | -o
| {{ archivePath }} | ARCHIVE_PATH | --download-archive
| {{ batchPath }} | BATCH_PATH | -a

Examples have been provided.

## CREATE_AUDIO_PLAYLISTS

This parameter defaults to `False` if not provided. If set to true it will iterate through the folders in the `DOWNLOAD_DIR`, list the audio files and output them into a `.m3u` file.

This allows apps like Navidrome to read the audio files in the folders as playlists.
