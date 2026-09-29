import requests
import re

JSON_URL = "https://raw.githubusercontent.com/panorea744/stawerlo/main/channels5.json"
M3U8_FILE = "res/26-3/szc1.m3u8"
CHANNEL_ID = 872

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ------------------------------------------------------------
# Get channel 872 stream URL
# ------------------------------------------------------------

r = requests.get(JSON_URL, headers=headers, timeout=15)
r.raise_for_status()

channels = r.json()

channel = next(
    (item for item in channels if item.get("id") == CHANNEL_ID),
    None
)

if not channel:
    raise RuntimeError(f"Channel ID {CHANNEL_ID} not found")

stream_url = channel.get("stream", "")

if not stream_url:
    raise RuntimeError("No stream URL found")

# Extract token
match = re.search(r"[?&]token=([^&]+)", stream_url)

if not match:
    raise RuntimeError("No token found in stream URL")

new_token = match.group(1)

print(f"New token: {new_token}")

# ------------------------------------------------------------
# Update szc1.m3u8
# ------------------------------------------------------------

with open(M3U8_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Replace only the token value
new_content, count = re.subn(
    r"([?&]token=)[^&\r\n]+",
    rf"\g<1>{new_token}",
    content,
    count=1
)

if count == 0:
    raise RuntimeError("No token found in szc1.m3u8")

# Write only if changed
if new_content != content:
    with open(M3U8_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("szc1.m3u8 updated successfully")
else:
    print("Token is already up to date")
