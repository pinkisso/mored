import os
import requests

playlists = {
    "ulusalkanal.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/ulusalkanal.m3u8",
    "beinsportshaber.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/beinsportshaber.m3u8",
    "cnnturk.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/cnnturk.m3u8",
    "ekoturk.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/ekoturk.m3u8",
    "krttv.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/krttv.m3u8",
    "ahaber.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/refs/heads/main/streams/ahaber.m3u8",
    "sozcutelevizyonu.m3u8": "https://raw.githubusercontent.com/tecotv2025/youtube-canli/main/streams/sozcutelevizyonu.m3u8",
}

output_dir = os.path.dirname(os.path.abspath(__file__))

for filename, url in playlists.items():
    response = requests.get(url)
    response.raise_for_status()

    lines = response.text.splitlines()

    if len(lines) >= 2:
        lines[1] = "#EXT-X-STREAM-INF:BANDWIDTH=7680000"

    # Remove lines 3 and 4 (indices 2 and 3)
    if len(lines) >= 4:
        del lines[2:4]

    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Created {output_path}")
