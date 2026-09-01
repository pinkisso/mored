import os
import re
import requests

# ============================================================
# NORMAL M3U8 SOURCES
# ============================================================

playlists = {
    "ulusalkanal.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/ulusalkanal.m3u8",
    "beinsportshaber.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/beinsportshaber.m3u8",
    "cnnturk.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/cnnturk.m3u8",
    "ekoturk.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/ekoturk.m3u8",
    "krttv.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/krttv.m3u8",
    "sozcutelevizyonu.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/sozcutelevizyonu.m3u8",
}


# ============================================================
# PHP REDIRECT SOURCES
# ============================================================

php_sources = {
    "ahaber.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/refs/heads/main/channels/ahaber.php",
    "ulusalkanal.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/channels/ulusalkanal.php",
    "beinsportshaber.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/channels/beinsportshaber.php",
    "cnnturk.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/channels/cnnturk.php",
    "ekoturk.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/channels/ekoturk.php",
    "krttv.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/channels/krttv.php",
    "sozcutelevizyonu.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/channels/sozcutelevizyonu.php",
}


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

output_dir = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# SESSION
# ============================================================

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0"
})


# ============================================================
# PROCESS NORMAL M3U8 FILES - DISABLED
# ============================================================
"""
 for filename, url in playlists.items():

    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()

        lines = response.text.splitlines()

        if len(lines) >= 2:
            lines[1] = "#EXT-X-STREAM-INF:BANDWIDTH=7680000"

        # Remove lines 3 and 4
        if len(lines) >= 4:
            del lines[2:4]

        output_path = os.path.join(output_dir, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        print(f"Created: {filename}")

    except Exception as e:
        print(f"ERROR processing {filename}: {e}")
"""

# ============================================================
# PROCESS PHP REDIRECT FILES
# ============================================================

for filename, url in php_sources.items():

    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()

        php_content = response.text

        # Extract URL from:
        # header("Location: https://....m3u8");

        match = re.search(
            r'header\s*\(\s*["\']Location:\s*(https?://[^"\']+\.m3u8[^"\']*)["\']',
            php_content,
            re.IGNORECASE
        )

        if not match:
            raise ValueError("No M3U8 URL found in PHP file")

        m3u8_url = match.group(1)

        # Remove possible trailing characters
        m3u8_url = m3u8_url.strip()

        # Create M3U8 master playlist
        content = (
            "#EXTM3U\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=7680000\n"
            f"{m3u8_url}\n"
        )

        output_path = os.path.join(output_dir, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Created: {filename}")
        print(f"  URL: {m3u8_url}")

    except Exception as e:
        print(f"ERROR processing {filename}: {e}")
