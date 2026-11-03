
import requests
import re
import os

JSON_URL = "https://raw.githubusercontent.com/kadirsener1/avva1-tulixtv/refs/heads/main/channels5.json"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ------------------------------------------------------------
# Channel configuration
# ------------------------------------------------------------

CHANNELS = [
    {
        "name": "Sozcu TV",
        "id": 872,
        "file": "res/26-3/szc3.m3u8"
    },
    {
        "name": "Koza TV",
        "id": 992,
        "file": "res/26-3/koza3.m3u8"
    },
    {
        "name": "TRT 1",
        "id": 787,
        "file": "res/26-3/trt13.m3u8"
    },
    {
        "name": "TV100",
        "id": 738,
        "file": "res/26-3/tv1003.m3u8"
    },
    {
        "name": "NOW TV",
        "id": 718,
        "file": "res/26-3/nowtv3.m3u8"
    },
    {
        "name": "ATV",
        "id": 816,
        "file": "res/26-3/atv3.m3u8"
    }
]

# ------------------------------------------------------------
# Download channels JSON only once
# ------------------------------------------------------------

r = requests.get(JSON_URL, headers=headers, timeout=15)
r.raise_for_status()

channels = r.json()

# ------------------------------------------------------------
# Update each channel M3U8 file
# ------------------------------------------------------------

for config in CHANNELS:

    channel_id = config["id"]
    m3u8_file = config["file"]
    channel_name = config["name"]

    print(f"\nProcessing {channel_name} (ID: {channel_id})")

    try:
        # Find channel in JSON
        channel = next(
            (item for item in channels if item.get("id") == channel_id),
            None
        )

        if not channel:
            raise RuntimeError(f"Channel ID {channel_id} not found")

        # Get stream URL
        stream_url = channel.get("stream", "")

        if not stream_url:
            raise RuntimeError("No stream URL found")

        # Extract token
        match = re.search(r"[?&]token=([^&]+)", stream_url)

        if not match:
            raise RuntimeError("No token found in stream URL")

        new_token = match.group(1)

        # Check M3U8 file
        if not os.path.isfile(m3u8_file):
            raise FileNotFoundError(f"File not found: {m3u8_file}")

        with open(m3u8_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace only the first token value
        new_content, count = re.subn(
            r"([?&]token=)[^&\r\n]+",
            lambda m: m.group(1) + new_token,
            content,
            count=1
        )

        if count == 0:
            raise RuntimeError("No token found in M3U8 file")

        # Write only if changed
        if new_content != content:

            with open(m3u8_file, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"SUCCESS: {m3u8_file} updated")

        else:
            print(f"UNCHANGED: {m3u8_file} token is already up to date")

    except Exception as e:
        print(f"ERROR: {channel_name}: {e}")

print("\nAll channels processed.")
