import os

# pwd of the running script
script_dir = os.path.dirname(os.path.realpath(__file__))

# working directory required for storing downloaded content
if os.environ.get('WORKDIR') is None:
    print("No WORKDIR env found, quitting...")
    exit(1)
else:
    WORKDIR = os.environ['WORKDIR']

# detect method of passing playlists to script
if os.environ.get('PLAYLISTS') is None:
    print("No PLAYLISTS env found, checking playlists.txt")
    playlist_file = os.path.join(script_dir, "playlists.txt")
    if os.path.isfile(playlist_file):
        PLAYLISTS = [line.rstrip('\n') for line in open(playlist_file, "r").readlines()]
    else:
        print("No playlists.txt file found, this cannot continue...")
        exit(1)
else:
    print("Found PLAYLISTS env, splitting out")
    PLAYLISTS = os.environ['PLAYLISTS'].split(",")

print("Found playlists to download:")
print(*PLAYLISTS, sep=", ")

for pl in PLAYLISTS:
    print(f"Downloading from {pl} playlist")
    os.system(f"/usr/bin/yt-dlp --download-archive '{WORKDIR}/.logs/{pl}.log' --no-post-overwrites -ciwx --audio-format mp3 --add-metadata --embed-thumbnail -o '{WORKDIR}/%(playlist)s/%(title)s.%(ext)s' {pl}")

print("Finished downloading from all playlists!")
exit(0)
