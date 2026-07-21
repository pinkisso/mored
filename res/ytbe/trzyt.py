import os
import requests

playlists = {
    "sqool.m3u8": "https://tvradiozap.eu/tools/cof-m3u8.php/yt/UCaEqMbRYYOmI3WrALMhxuIg.m3u8",
    "tvvendee.m3u8": "https://tvradiozap.eu/tools/cof-m3u8.php/yt/UCEw9gcSDo-LlC0ci60bl-Rg.m3u8",
    "tv7bor.m3u8": "https://tvradiozap.eu/tools/cof-m3u8.php/yt/UCV9yrdAfyd1BdDyd4tDdVxg.m3u8",
    "maurienne.m3u8": "https://tvradiozap.eu/tools/cof-m3u8.php/yt/UCva-htH2wvmKsG6SkcEJ4Vw.m3u8",
    "mozacris.m3u8": "https://tvradiozap.eu/tools/cof-m3u8.php/yt/UCQC0xLG_W0QpqAXQ4-yhwBA.m3u8",
    "lmsarthe.m3u8": "https://tvradiozap.eu/tools/cof-m3u8.php/yt/UCidJ6dBJ7oEfdAVzqaL2nSg.m3u8",
    "lemedia.m3u8" : "https://tvradiozap.eu/tools/cof-m3u8.php/dm/x8dtuir.m3u8",
	"7alimoges.m3u8" : "https://tvradiozap.eu/tools/cof-m3u8.php/dm/x5gv5v0.m3u8",
	"moselle.m3u8" : "https://tvradiozap.eu/tools/cof-m3u8.php/dm/x9lgbik.m3u8",
	#"tv8mb.m3u8" : "https://tvradiozap.eu/tools/cof-m3u8.php/dm/x3wqv8b.m3u8",
	"angers.m3u8" : "https://tvradiozap.eu/tools/cof-m3u8.php/dm/x8r7256.m3u8",
	"lyoncap.m3u8" : "https://tvradiozap.eu/tools/cof-m3u8.php/dm/x7z3zqa.m3u8",
	"szcytbe.m3u8" : "https://tvradiozap.eu/tools/cof-m3u8.php/yt/UCOulx_rep5O4i9y6AyDqVvw.m3u8",
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

output_dir = os.path.dirname(os.path.abspath(__file__))

for filename, url in playlists.items():
    response = requests.get(url, headers=headers, allow_redirects=True, timeout=20)
    response.raise_for_status()

    lines = [
        "#EXTM3U",
        "#EXT-X-VERSION:3",
        "#EXT-X-STREAM-INF:BANDWIDTH=7680000",
        response.url
    ]

    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Created {output_path}")
