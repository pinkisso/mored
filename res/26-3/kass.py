import requests
from urllib.parse import urljoin, urlsplit, urlunsplit
import os

API_URL = "https://shoofapi.alkass.net/Shoof/liveV3.php"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

session = requests.Session()
session.headers.update(headers)


def get_base_url(m3u8_url):
    """
    Example:

    https://liveeu-gcps.alkassdigital.net/alkass1-p/main.m3u8?hdnts=...

    becomes:

    https://liveeu-gcps.alkassdigital.net/alkass1-p/
    """

    parsed = urlsplit(m3u8_url)

    path = parsed.path

    # Remove main.m3u8 or master.m3u8
    if "/main.m3u8" in path:
        path = path.split("/main.m3u8")[0] + "/"

    elif "/master.m3u8" in path:
        path = path.split("/master.m3u8")[0] + "/"

    else:
        # Fallback
        path = path.rsplit("/", 1)[0] + "/"

    return urlunsplit((
        parsed.scheme,
        parsed.netloc,
        path,
        "",
        ""
    ))


def process_channel(channel):

    title = channel.get("title", "").strip()
    body = channel.get("body", "").strip()

    if not body:
        print(f"SKIP: {title} - no body URL")
        return

    print("\n" + "=" * 80)
    print(f"CHANNEL: {title}")
    print(f"MASTER : {body}")
    print("=" * 80)

    try:
        # Download master playlist
        response = session.get(body, timeout=15)
        response.raise_for_status()

        content = response.text

        # Base URL
        base_url = get_base_url(body)

        print(f"BASE URL: {base_url}")
        print("-" * 80)

        # Process playlist
        output_lines = []

        for line in content.splitlines():

            line = line.strip()

            if not line:
                output_lines.append("")
                continue

            # Keep M3U8 tags unchanged
            if line.startswith("#"):
                output_lines.append(line)
                continue

            # Convert relative URL to absolute URL
            full_url = urljoin(base_url, line)

            output_lines.append(full_url)

            print(full_url)

        # Final M3U8 content
        output = "\n".join(output_lines) + "\n"

        # Filename
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"{title}.m3u8"
        )

        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)

        print("-" * 80)
        print(f"SAVED: {filename}")

    except requests.RequestException as e:
        print(f"ERROR downloading {title}: {e}")

    except Exception as e:
        print(f"ERROR processing {title}: {e}")


def main():

    try:
        response = session.get(API_URL, timeout=15)
        response.raise_for_status()

        channels = response.json()

    except Exception as e:
        print(f"ERROR getting API: {e}")
        return

    for channel in channels:
        process_channel(channel)


if __name__ == "__main__":
    main()
