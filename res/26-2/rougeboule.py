import os
import requests

playlist_url = "https://raw.githubusercontent.com/Paradise-91/ParaTV/main/playlists/paratv/main/filter/raw.m3u"
output_file = "res/26-2/rougeboule.m3u8"

# Download playlist
response = requests.get(playlist_url)
response.raise_for_status()

lines = response.text.splitlines()

stream_url = None

for i, line in enumerate(lines):
    if line.strip() == "#EXTINF:-1,RED BULL TV":
        if i + 1 < len(lines):
            stream_url = lines[i + 1].strip()
        break

if not stream_url:
    raise Exception("RED BULL TV not found in playlist")

# Download the referenced m3u8
stream_response = requests.get(stream_url, headers=headers, timeout=20)
stream_response.raise_for_status()

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(stream_response.text)

print(f"Saved to {output_file}")
