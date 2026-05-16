import requests

auth_url = "https://hdfauth.ftven.fr/esi/TA?url=https://live-event.ftven.fr/out/v1/64bfbfd7f96c40b3989b029663be3e6d/index_france-domtom.m3u8"

# Get authenticated URL
response = requests.get(auth_url)
base_url = response.text.strip()

# Remove query string (?hdnea=...)
base_url = base_url.split("?")[0]

# Replace master playlist with variant playlists
url_5 = base_url.replace(
    "index_france-domtom.m3u8",
    "index_france-domtom_5.m3u8"
)

url_11 = base_url.replace(
    "index_france-domtom.m3u8",
    "index_france-domtom_11.m3u8"
)

# Build final playlist
playlist = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-INDEPENDENT-SEGMENTS
#EXT-X-STREAM-INF:BANDWIDTH=4486068,AVERAGE-BANDWIDTH=2857587,RESOLUTION=1280x720,FRAME-RATE=25.000,CODECS="avc1.64001F,mp4a.40.2"
{url_5}
#EXT-X-STREAM-INF:BANDWIDTH=348788,AVERAGE-BANDWIDTH=306185,RESOLUTION=256x144,FRAME-RATE=25.000,CODECS="avc1.42C01E,mp4a.40.2"
{url_11}
"""

print(playlist)
