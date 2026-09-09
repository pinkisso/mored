import requests
from urllib.parse import urljoin
import os
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept-Encoding": "identity",
})

# ============================================================
# RETRY CONFIGURATION
# ============================================================

retry = Retry(
    total=4,
    connect=4,
    read=4,
    status=4,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)

adapter = HTTPAdapter(max_retries=retry)

session.mount("https://", adapter)
session.mount("http://", adapter)


# ============================================================
# GET VARIANT URL
# ============================================================

def get_variant_url(api_url):

    # --------------------------------------------------------
    # Get secured URL
    # --------------------------------------------------------

    print(f"Getting API: {api_url}")

    r = session.get(
        api_url,
        timeout=(20, 30)
    )

    r.raise_for_status()

    secured_url = r.json()["data"]["secured_url"]

    print("Secured URL:")
    print(secured_url)

    # --------------------------------------------------------
    # Get master m3u8
    # --------------------------------------------------------

    for attempt in range(3):

        try:
            print(f"Getting master playlist (attempt {attempt + 1}/3)...")

            r = session.get(
                secured_url,
                timeout=(20, 45)
            )

            r.raise_for_status()

            break

        except requests.exceptions.RequestException as e:

            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt == 2:
                raise

            wait = 5 * (attempt + 1)

            print(f"Waiting {wait} seconds before retry...")
            time.sleep(wait)

    playlist = r.text

    # --------------------------------------------------------
    # Try to extract 720p stream URL
    # --------------------------------------------------------

    variant_url = None

    for line in playlist.splitlines():

        line = line.strip()

        if "royatv_720p" in line:

            variant_url = urljoin(
                secured_url,
                line
            )

            break

    # --------------------------------------------------------
    # Fallback: first stream URL
    # --------------------------------------------------------

    if variant_url is None:

        for line in playlist.splitlines():

            line = line.strip()

            if line and not line.startswith("#"):

                variant_url = urljoin(
                    secured_url,
                    line
                )

                break

    # --------------------------------------------------------
    # No stream found
    # --------------------------------------------------------

    if variant_url is None:
        raise Exception("No stream URL found")

    print("Variant URL:")
    print(variant_url)

    return variant_url


# ============================================================
# WRITE M3U8
# ============================================================

def write_m3u8(filename, variant_url):

    content = f'''#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=3583979,FRAME-RATE=25,RESOLUTION=1280x720,CODECS="avc1.4d401f,mp4a.40.2"
{variant_url}
'''

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Written: {filename}")


# ============================================================
# API 1 -> roya1.m3u8
# ============================================================

api_url = "https://ticket.roya-tv.com/api/v5/fastchannel/1"

try:

    roya1_url = get_variant_url(api_url)

    write_m3u8(
        "res/26-2/roya1.m3u8",
        roya1_url
    )

except Exception as e:

    print(f"ERROR Roya 1: {e}")


# ============================================================
# API 2 -> roya2.m3u8
# ============================================================

api_url2 = "https://ticket.roya-tv.com/api/v5/fastchannel/21"

try:

    roya2_url = get_variant_url(api_url2)

    write_m3u8(
        "res/26-2/roya2.m3u8",
        roya2_url
    )

except Exception as e:

    print(f"ERROR Roya 2: {e}")


# ============================================================
# API 3 -> roya3.m3u8
# ============================================================

# api_url3 = "https://ticket.roya-tv.com/api/v5/fastchannel/48"

# try:
#     roya3_url = get_variant_url(api_url3)
#     write_m3u8("res/26-2/roya3.m3u8", roya3_url)
#
# except Exception as e:
#     print(f"ERROR Roya 3: {e}")
