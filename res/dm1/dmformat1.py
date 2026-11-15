import requests
import re
import sys

source_url = "https://tvradiozap.eu/tools/cof-m3u8.php/dm/x8dtuir.m3u8"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    # Follow redirects and retrieve the final URL
    response = requests.get(
        source_url,
        headers=headers,
        allow_redirects=True,
        timeout=20
    )
    response.raise_for_status()

    video_url = response.url

    # Extract the Dailymotion video URL
    if "live-h264-" not in video_url:
        raise ValueError(f"Unexpected video URL: {video_url}")

    # Generate corresponding audio URL
    audio_url = re.sub(
        r"live-h264-([^/?]+)\.m3u8",
        "live-aac-128.m3u8",
        video_url
    )

    # Generate master playlist
    playlist = f"""#EXTM3U
#EXT-X-VERSION:7
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="group_A2",NAME="fre",DEFAULT=YES,CHANNELS="2",URI="{audio_url}"
#EXT-X-STREAM-INF:BANDWIDTH=1667072,RESOLUTION=848x477,CODECS="avc1.64001f,mp4a.40.2",NAME="480",AUDIO="group_A2"
{video_url}"""

    print(playlist)

except requests.RequestException as e:
    print(f"HTTP error: {e}", file=sys.stderr)

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
