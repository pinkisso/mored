import requests

API_URL = "https://xddrts.alwaysdata.net/stream/lire.php"
OUTPUT_FILE = "res/26-3/scz.m3u8"

headers = {
    "User-Agent": "Mozilla/5.0",
}

try:
    r = requests.get(
        API_URL,
        headers=headers,
        timeout=15,
        allow_redirects=False
    )

    print("HTTP status:", r.status_code)
    print("Location:", r.headers.get("Location"))

    stream_url = r.headers.get("Location")

    if not stream_url:
        raise ValueError("No Location header returned by lire.php")

    content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:11
#EXT-X-MEDIA-SEQUENCE:51686
#EXT-X-DISCONTINUITY-SEQUENCE:23
#EXT-X-PROGRAM-DATE-TIME:2026-09-23T16:50:56.038Z
#EXTINF:10.04
{stream_url}
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"{OUTPUT_FILE} updated successfully.")

except Exception as e:
    print(f"Error: {e}")
    raise
