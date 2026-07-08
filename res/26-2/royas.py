import requests
from urllib.parse import urljoin

api_url = "https://ticket.roya-tv.com/api/v5/fastchannel/1"

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0",
})

# Get secured URL
r = session.get(api_url, timeout=10)
r.raise_for_status()

secured_url = r.json()["data"]["secured_url"]

# Get master m3u8
r = session.get(secured_url, timeout=10)
r.raise_for_status()

playlist = r.text

# Extract first stream URL
for line in playlist.splitlines():
    if line and not line.startswith("#"):
        variant_url = urljoin(secured_url, line)
        break

print("#EXTM3U")
print("#EXT-X-VERSION:3")
print("#EXT-X-STREAM-INF:BANDWIDTH=3583979,FRAME-RATE=25,RESOLUTION=1280x720,CODECS="avc1.4d401f,mp4a.40.2" ")
print(variant_url)
