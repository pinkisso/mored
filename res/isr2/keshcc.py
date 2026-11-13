import requests

headers = {
    "User-Agent": "SmartOsTV",
    "Accept-Encoding": "identity",
}

session = requests.Session()

channels = {
    "k12cc": {
        "base": "https://d2249b6f08tjt0.cloudfront.net/k12cc/",
        "output": "res/isr2/k12cc.m3u8",
    },
    "k12dvr": {
        "base": "https://d2249b6f08tjt0.cloudfront.net/k12dvr/",
        "output": "res/isr2/k12dvr.m3u8",
    },
}

for name, config in channels.items():

    print(f"Processing {name}...")

    base = config["base"]

    master = base + "index.m3u8?b-in-range=0-5000&"

    ticket_url = (
        "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp"
        "?et=ngt"
        f"&lp=/{name}/index.m3u8?b-in-range=0-5000"
        "&rv=AWS"
    )

    try:
        # Get ticket
        ticket_response = session.get(
            ticket_url,
            headers=headers,
            timeout=20
        )
        ticket_response.raise_for_status()

        ticket = ticket_response.json()["tickets"][0]["ticket"]

        # Build authenticated master URL
        master_url = master + ticket

        # Download master playlist
        response = session.get(
            master_url,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        content = []

        for line in response.text.splitlines():
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                content.append(line)
            else:
                content.append(base + line)

        final_content = "\n".join(content) + "\n"

        # Save playlist
        with open(config["output"], "w", encoding="utf-8") as f:
            f.write(final_content)

        print(f"SUCCESS: {config['output']} updated")

    except Exception as e:
        print(f"ERROR processing {name}: {e}")
