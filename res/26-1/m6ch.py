import requests

source_url = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/group/netplus.tv/filter/raw.m3u"

# Download M3U source
content = requests.get(source_url).text

target_name = "#EXTINF:-1,M6 HD [FR]"

lines = content.splitlines()

modified_url = None

# Find channel and retrieve next HTTPS link
for i, line in enumerate(lines):
    if target_name in line:
        for j in range(i + 1, len(lines)):
            if lines[j].startswith("https://"):
                modified_url = lines[j].replace(
                    "m6hd.m3u8",
                    "m6hd-avc1_2000000=35-mp4a_130400_fra=3.m3u8"
                )
                break
        break

if modified_url:
    final_playlist = f"""#EXTM3U
#EXT-X-VERSION:8
#EXT-X-STREAM-INF:BANDWIDTH=2487873,AVERAGE-BANDWIDTH=2261704,CODECS="avc1.640020,mp4a.40.2",RESOLUTION=1280x720,FRAME-RATE=25.000
{modified_url}
"""

    print(final_playlist)

else:
    print("M6 HD [FR] stream not found.")
