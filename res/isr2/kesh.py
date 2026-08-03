import os
import requests

headers = {
    "User-Agent": "SmartOsTV",
    "Accept-Encoding": "identity",
}

channels = {
    "k12": {
        "master": "https://mako-streaming.akamaized.net/stream/hls/live/2033791/k12/index.m3u8",
        "base": "https://mako-streaming.akamaized.net/stream/hls/live/2033791/k12/",
    },
    "k12wad": {
        "master": "https://mako-streaming.akamaized.net/stream/hls/live/2033791/k12n12wad/index.m3u8",
        "base": "https://mako-streaming.akamaized.net/stream/hls/live/2033791/k12n12wad/",
    },
    "n12rh": {
        "master": "https://mako-streaming.akamaized.net/n12/hls/live/20000821/k12rh/index.m3u8",
        "base": "https://mako-streaming.akamaized.net/n12/hls/live/20000821/k12rh/",
    },
    "t24": {
        "master": "https://mako-streaming.akamaized.net/direct/hls/live/2035340/ch24live/index.m3u8",
        "base": "https://mako-streaming.akamaized.net/direct/hls/live/2035340/ch24live/",
    },
}

os.makedirs("res/isr2", exist_ok=True)

s = requests.Session()

toki = s.get(
    "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp"
    "?et=ngt&lp=/stream/hls/live/2033791/k12/index.m3u8?as=1&rv=AKAMAI",
    headers=headers,
).json()["tickets"][0]["ticket"]

for name, info in channels.items():

    master_url = f"{info['master']}?{toki}"

    response = s.get(master_url, headers=headers)
    response.raise_for_status()

    content = ""

    for line in response.text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            content += line + "\n"
        else:
            content += info["base"] + line + "\n"

    with open(f"res/isr2/{name}.m3u8", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created res/isr2/{name}.m3u8")
