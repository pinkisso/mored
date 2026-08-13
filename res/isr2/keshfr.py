import os
import requests

headers = {
    "User-Agent": "SmartOsTV",
    "Accept-Encoding": "identity",
}

# Master T24
master_url = "https://mako-streaming.akamaized.net/direct/hls/live/2035340/ch24live/index.m3u8"

# Bases supplémentaires
channels = {
    "comedy": "https://mako-streaming.akamaized.net/evrideo/hls/live/20001278/free_comedy/",
    "drama": "https://mako-streaming.akamaized.net/evrideo/hls/live/20001278/free_drama/",
    "music": "https://mako-streaming.akamaized.net/evrideo/hls/live/20001278/free_music/",
    "food": "https://mako-streaming.akamaized.net/evrideo/hls/live/20001278/free_food/",
    "erets": "https://mako-streaming.akamaized.net/evrideo/hls/live/20001278/erets/",
    "savri": "https://mako-streaming.akamaized.net/evrideo/hls/live/20001278/savri/",
    "ch24live": "https://mako-streaming.akamaized.net/evrideo/hls/live/20001278/ch24live/",
}

os.makedirs("res/isr2", exist_ok=True)

s = requests.Session()

# Récupération du ticket
toki = s.get(
    "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp"
    "?et=ngt&lp=/stream/hls/live/2033791/k12/index.m3u8?as=1&rv=AKAMAI",
    headers=headers,
).json()["tickets"][0]["ticket"]

# Récupération du master T24 une seule fois
master_url_with_ticket = f"{master_url}?{toki}"

response = s.get(master_url_with_ticket, headers=headers)
response.raise_for_status()

master_content = response.text

# Génération des différents fichiers
for name, base in channels.items():

    content = ""

    for line in master_content.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            content += line + "\n"
        else:
            content += base + line + "\n"

    output_file = f"res/isr2/{name}.m3u8"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created {output_file}")
