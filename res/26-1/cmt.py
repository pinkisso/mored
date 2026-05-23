import requests

url = "https://tvradiozap.eu/tools/m3u-m3u8.php/para/TMC.m3u8"

# Follow redirects automatically
response = requests.get(url, allow_redirects=True)
response.raise_for_status()

# Print only the content of the redirected .m3u8 file
print(response.text)
