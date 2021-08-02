# playlist_downloader
I needed a way to download and keep up to date a collection of youtube music playlist. This container will, with the latest version of yt-dlp download .mp3's into a mounted volume.

Run the container with
```bash
docker run \
  --name=pl_dl \
  --rm \
  -e PLAYLISTS="" \
  -e HC_URL="" \
  -v <path to download folder>:/media \
  jk8c19/playlist_downloader:latest
```

This is a run once container, so using --rm will clean up once it's done its thing.

# Other features

## Health Checks

The container has support to ping a Health Checks instance, simply supply the HTTP url to your check.

## playlists.txt

If you have a *really* large collection of playlists to download you can supply mount a playlists.txt file to `/opt` in the container to read from, if you do this make sure not to specify the PLAYLISTS environment variable!

# Parameters

| Parameter | Function | Req | Default |
|-|-|-|-|
| PLAYLISTS | comma separated list of playlists to be downloaded from | n
| HC_URL | Healthchecks URL to ping | N
| WORKDIR | This is set by the Dockerfile and is where you should mount your download volume too | N | /media |
