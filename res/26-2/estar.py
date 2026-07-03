import requests
import re

eurostar_base = "https://dogusdyg-eurostar.lg.mncdn.com/dogusdyg_eurostar/"
star_base = "https://dogusdyg-star.lg.mncdn.com/dogusdyg_star/"

url = "https://www.eurostartv.com.tr/canli-izle"
response = requests.get(url)

if response.status_code == 200:
    site_content = response.text
    match = re.search(r"liveUrl = '(.*?)'", site_content)

    if match:
        baglanti = match.group(1)
        content_response = requests.get(baglanti)

        if content_response.status_code == 200:
            content = content_response.text
            lines = content.split("\n")

            eurostar_content = ""
            star_content = ""

            for line in lines:
                if line.startswith("live_"):
                    eurostar_content += eurostar_base + line + "\n"
                    star_content += star_base + line + "\n"
                else:
                    eurostar_content += line + "\n"
                    star_content += line + "\n"

            with open("res/26-2/estar.m3u8", "w", encoding="utf-8") as f:
                f.write(eurostar_content)

            with open("res/26-2/star1.m3u8", "w", encoding="utf-8") as f:
                f.write(star_content)

            print("Files generated.")

        else:
            print("Failed to fetch content.")
    else:
        print("Live URL not found in the content.")
else:
    print("Failed to fetch website content.")
