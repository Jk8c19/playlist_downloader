import os
import requests
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def send_hc_ping(state):
    if os.environ.get('HC_URL') is not None:
        hcUrl = os.environ.get('HC_URL')
        try:
            requests.get(f"{hcUrl}/{state}", timeout=10)
        except requests.RequestException as e:
            print("HC Ping failed: %s" % e)
            return False
        return True
    else:
        return False

def test_env(environmentVariable):
    if os.environ.get(environmentVariable) is None:
        print(f"Env '{environmentVariable}' not present")
        send_hc_ping("fail")
        exit(1)
    else:
        return True

send_hc_ping("start")

# make sure all the env's we need are present
environtVariables = ['TEMPLATE_PATH', 'CONFIG_PATH', 'DOWNLOAD_DIR', 'ARCHIVE_PATH', 'BATCH_PATH']
for variable in environtVariables:
    test_env(variable)

templateDir = os.path.split(os.environ.get('TEMPLATE_PATH'))[0]
env = Environment(
    loader=FileSystemLoader(templateDir)
)

templateFile = os.path.split(os.environ.get('TEMPLATE_PATH'))[1]
template = env.get_template(templateFile)

templateProperties = {
    'downloadDir': os.environ.get('DOWNLOAD_DIR'),
    'archivePath': os.environ.get('ARCHIVE_PATH'),
    'batchPath': os.environ.get('BATCH_PATH')
}

configData = template.render(templateProperties)
configPath = os.environ.get('CONFIG_PATH')

with open(configPath, mode="w", encoding="utf-8") as configFile:
    configFile.write(configData)

# run yt-dlp
os.system(f"/usr/bin/yt-dlp --config-location {configPath}")
print("Finished downloading!")

if os.environ.get('CREATE_AUDIO_PLAYLISTS') == False:
    send_hc_ping("")
    exit(0) # Nothing left to do

print("Updating playlist files")

downloadDir = os.environ.get('DOWNLOAD_DIR')
dirlist = [ item for item in os.listdir(downloadDir) if os.path.isdir(os.path.join(downloadDir, item)) ]

filetypes = ("*.mp3", "*.m4a", "*.flac")

for folder in dirlist:
    audiofiles = []
    print(f"Scanning for media in {folder}")

    for filetype in filetypes:
        audiofiles.extend(list(Path(os.path.join(downloadDir, folder)).rglob(filetype)))

    if len(audiofiles) > 0:
        print(f"Found {len(audiofiles)} files to add to playlist")
        with open(os.path.join(downloadDir, folder, f"{folder}.m3u"), 'w', encoding="utf-8") as plf:
            for file in audiofiles:
                filepath = os.path.join(downloadDir, file)
                filename = os.path.basename(filepath)
                plf.write(f"{filename}\n")
        print(f"Saved to {folder}.m3u")

print("Playlists updated")
send_hc_ping("")
exit(0)
