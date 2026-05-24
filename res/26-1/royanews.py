import requests
import re
import json

# Roya News
base_url = "https://guxaykcuao.erbvr.com/royanews/"
url = "https://ticket.roya-tv.com/api/v5/fastchannel/21"

# Roya
base_url_roya = "https://ochuergrys.erbvr.com/roya/"
url_roya = "https://ticket.roya-tv.com/api/v5/fastchannel/1"

s = requests.Session()

# -------- Roya News --------
resplink = s.get(url)
response_json = json.loads(resplink.text)
mastlnk = response_json["data"]["secured_url"]

content_response = requests.get(mastlnk)
content = content_response.text

lines = content.split("\n")
modified_content = ""

for line in lines:
    if line.startswith("royanews"):
        full_url = base_url + line
        modified_content += full_url + "\n"
    else:
        modified_content += line + "\n"

with open("res/26-1/royanews.m3u8", "w", encoding="utf-8") as f:
    f.write(modified_content)

# -------- Roya --------
resplink_roya = s.get(url_roya)
response_json_roya = json.loads(resplink_roya.text)
mastlnk_roya = response_json_roya["data"]["secured_url"]

content_response_roya = requests.get(mastlnk_roya)
content_roya = content_response_roya.text

lines_roya = content_roya.split("\n")
modified_content_roya = ""

for line in lines_roya:
    if line.startswith("roya"):
        full_url = base_url_roya + line
        modified_content_roya += full_url + "\n"
    else:
        modified_content_roya += line + "\n"

with open("res/26-1/roya.m3u8", "w", encoding="utf-8") as f:
    f.write(modified_content_roya)
