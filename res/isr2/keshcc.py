import requests

headers = {
    "User-Agent": "SmartOsTV",
    "Accept-Encoding": "identity",
}

master = "https://d2249b6f08tjt0.cloudfront.net/k12cc/index.m3u8?b-in-range=0-5000&"
base = "https://d2249b6f08tjt0.cloudfront.net/k12cc/"

ticket_url = (
    "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp"
    "?et=ngt"
    "&lp=/k12cc/index.m3u8?b-in-range=0-5000"
    "&rv=AWS"
)

s = requests.Session()

# Get ticket
ticket = s.get(ticket_url, headers=headers).json()["tickets"][0]["ticket"]

# Build authenticated master URL
master_url = master + ticket

# Download master playlist
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
        content += base + line + "\n"

print(content)

with open("res/isr2/k12cc.m3u8", "w", encoding="utf-8") as f:
    f.write(content)
