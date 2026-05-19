import requests

auth_url = "https://hdfauth.ftven.fr/esi/TA?url=https://live-event.ftven.fr/out/v1/d0d28e140b004cbc94cb54114f438c71/start/1779176686/index_france-domtom.m3u8"

# Get authenticated URL
response = requests.get(auth_url)
base_url = response.text.strip()

# Remove query string (?hdnea=...)
base_url = base_url.split("?")[0]

# Replace master playlist with variant playlists
url_6 = base_url.replace(
    "index_france-domtom.m3u8",
    "index_france-domtom_6.m3u8"
)

url_10 = base_url.replace(
    "index_france-domtom.m3u8",
    "index_france-domtom_10.m3u8"
)

# Build final playlist
playlist = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-INDEPENDENT-SEGMENTS
#EXT-X-STREAM-INF:BANDWIDTH=873774,AVERAGE-BANDWIDTH=652221,RESOLUTION=384x216,FRAME-RATE=25.000,CODECS="avc1.42C01E,mp4a.40.2"
{url_6}
#EXT-X-STREAM-INF:BANDWIDTH=4569747,AVERAGE-BANDWIDTH=2962186,RESOLUTION=1280x720,FRAME-RATE=25.000,CODECS="avc1.640029,mp4a.40.2"
{url_10}
"""

print(playlist)
