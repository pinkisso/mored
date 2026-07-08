import requests
from urllib.parse import urljoin

api_url = "https://ticket.roya-tv.com/api/v5/fastchannel/1"

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.roya-tv.com/"
})

# Get secured URL
r = session.get(api_url, timeout=10)
r.raise_for_status()

secured_url = r.json()["data"]["secured_url"]

print("Master playlist:")
print(secured_url)

# Get master m3u8
r = session.get(secured_url, timeout=10)
r.raise_for_status()

playlist = r.text

print("\nPlaylist:")
print(playlist)

# Extract first stream URL
for line in playlist.splitlines():
    if line and not line.startswith("#"):
        variant_url = urljoin(secured_url, line)
        break

print("\nVariant URL:")
print(variant_url)

# Test variant playlist
r2 = session.get(
    variant_url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.roya-tv.com/"
    },
    timeout=10
)

print("\nVariant playlist response:")
print(r2.status_code)
print(r2.text[:500])
