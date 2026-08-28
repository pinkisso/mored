import requests

# ============================================================
# SOURCE PLAYLISTS
# ============================================================

sources = [
    (
        "karsilasmalar",
        "https://raw.githubusercontent.com/mehmetey03/METV/refs/heads/main/karsilasmalar.m3u"
    ),
    (
        "karsilasmalar2",
        "https://raw.githubusercontent.com/mehmetey03/METV/refs/heads/main/karsilasmalar2.m3u"
    ),
    (
        "karsilasmalar3",
        "https://raw.githubusercontent.com/mehmetey03/METV/refs/heads/main/karsilasmalar3.m3u"
    ),
    (
        "karsilasmalar4",
        "https://raw.githubusercontent.com/mehmetey03/METV/refs/heads/main/karsilasmalar4.m3u"
    ),
    (
        "karsilasmalar5",
        "https://raw.githubusercontent.com/mehmetey03/METV/refs/heads/main/karsilasmalar5.m3u"
    ),
    (
        "atom_mac",
        "https://raw.githubusercontent.com/mehmetey03/METV/refs/heads/main/atom_mac.m3u"
    ),
    (
        "liste",
        "https://raw.githubusercontent.com/mehmetey03/METV/refs/heads/main/liste.m3u"
    ),
    (
        "sabit",
        "https://raw.githubusercontent.com/pinkisso/mored/refs/heads/main/res/isr/sabit.m3u"
    ),
]

output_file = "sn.m3u"

headers = {
    "User-Agent": "Mozilla/5.0"
}


# ============================================================
# PARSE PLAYLIST
# ============================================================

def parse_playlist(content, group_title):

    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    result = []

    current_extinf = None
    user_agent = None
    referer = None

    for line in lines:

        # ----------------------------------------------------
        # EXTINF
        # ----------------------------------------------------
        if line.startswith("#EXTINF:"):

            channel_name = line.split(",", 1)[1].strip()

            current_extinf = channel_name
            user_agent = None
            referer = None

        # ----------------------------------------------------
        # USER-AGENT
        # ----------------------------------------------------
        elif line.startswith("#EXTVLCOPT:http-user-agent="):

            user_agent = line.split("=", 1)[1].strip()

        # ----------------------------------------------------
        # REFERRER
        # ----------------------------------------------------
        elif line.startswith("#EXTVLCOPT:http-referrer="):

            referer = line.split("=", 1)[1].strip()

        # ----------------------------------------------------
        # STREAM URL
        # ----------------------------------------------------
        elif line.startswith(("http://", "https://")):

            if current_extinf is not None:

                result.append(
                    (
                        group_title,
                        user_agent,
                        referer,
                        current_extinf,
                        line
                    )
                )

                current_extinf = None
                user_agent = None
                referer = None

    return result


# ============================================================
# DOWNLOAD AND PARSE
# ============================================================

all_channels = []

for group_title, url in sources:

    print(f"Downloading: {group_title}")

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        # Parse the playlist
        channels = parse_playlist(
            response.text,
            group_title
        )

        print(f"  Found {len(channels)} channels")

        all_channels.extend(channels)

    except requests.RequestException as e:

        print(f"  ERROR downloading {group_title}: {e}")
        continue


# ============================================================
# BUILD OUTPUT
# ============================================================

output_lines = ["#EXTM3U"]

for (
    group_title,
    user_agent,
    referer,
    channel_name,
    stream_url
) in all_channels:

    extinf = (
        f'#EXTINF:-1 '
        f'group-title="{group_title}" '
        f'user-agent="{user_agent}" '
        f'referer="{referer}",'
        f'{channel_name}'
    )

    output_lines.append(extinf)
    output_lines.append(stream_url)


# ============================================================
# WRITE sn.m3u
# ============================================================

with open(
    output_file,
    "w",
    encoding="utf-8",
    newline="\n"
) as f:

    f.write("\n".join(output_lines) + "\n")


# ============================================================
# SUMMARY
# ============================================================

print()
print(f"Created: {output_file}")
print(f"Total channels: {len(all_channels)}")
