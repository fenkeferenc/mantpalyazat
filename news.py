import json
import requests

def news():
    f = "https://api.spaceflightnewsapi.net/v3/articles"
    raw = requests.get(f)
    all = json.loads(raw.text)
    last = dict(all[0])
    title = last.get("title")
    summary = last.get("summary")
    url = last.get("url")
    imgurl = last.get("imageUrl")
    return title,summary,url,imgurl

print(news()[0])