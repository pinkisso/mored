#! /usr/bin/python3

import requests
import json

print('#EXTM3U')
print('#EXT-X-VERSION:6')
print('#EXT-X-INDEPENDENT-SEGMENTS')
print('#EXT-X-STREAM-INF:BANDWIDTH=3082389,AVERAGE-BANDWIDTH=2802174,CODECS="avc1.4d401f,mp4a.40.2",RESOLUTION=1280x720,FRAME-RATE=25.000,AUDIO="audio-AACL-141"')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
s = requests.Session()
resplink = s.get('https://mediainfo.tf1.fr/mediainfocombo/L_LCI?context=ONEINFO&format=hls')
response_json = json.loads(resplink.text)
mastlnk = response_json["delivery"]["url"]
new_string = mastlnk.replace("LCI", "LCI-avc1_2499968=10002.m3u8")
print(new_string)
new3_string = mastlnk.replace("LCI", "LCI-mp4a_140800_fra=20000.m3u8")
print('#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-AACL-141",CHANNELS="2",LANGUAGE="fr",NAME="Français",DEFAULT=YES,AUTOSELECT=YES,URI="{}"'.format(new3_string), end='')
