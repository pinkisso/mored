import requests

url = "https://tvradiozap.eu/tools/cof-m3u8.php/yt/UCaEqMbRYYOmI3WrALMhxuIg.m3u8"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, allow_redirects=True)

print("#EXTM3U")
print("#EXT-X-VERSION:3")
print('#EXT-X-STREAM-INF:BANDWIDTH=7680000')
print(response.url)
