import requests

api_url = "https://ticket.roya-tv.com/api/v5/fastchannel/1"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

try:
    # Get secured_url from API
    response = requests.get(api_url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    secured_url = data["data"]["secured_url"]

    print("Secured URL:")
    print(secured_url)
    print("\nPlaylist content:\n")

    # Get m3u8 content
    playlist_response = requests.get(
        secured_url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": "identity"
        },
        timeout=10
    )
    playlist_response.raise_for_status()

    print(playlist_response.text)

except requests.RequestException as e:
    print("Request error:", e)

except KeyError:
    print("secured_url not found in API response")
