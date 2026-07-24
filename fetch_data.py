#!/usr/bin/env python3
"""MusicBrainzから日本のポップ系アーティストとアルバムを収集する。

通常実行: python3 fetch_data.py
小規模確認: python3 fetch_data.py --limit 10
APIの1秒制限を守るため、全件収集には数十分〜数時間かかります。
"""
import argparse, json, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
OUT = DATA / "artists.json"
PROGRESS = DATA / "progress.json"
BASE = "https://musicbrainz.org/ws/2"
HEADERS = {"User-Agent": "j-pop-history/1.0 (contact: example@example.com)", "Accept": "application/json"}
SEEDS = ["美空ひばり","坂本九","はっぴいえんど","松任谷由実","山下達郎","大貫妙子","サザンオールスターズ","Yellow Magic Orchestra","中島みゆき","松田聖子","中森明菜","BOØWY","THE BLUE HEARTS","TM NETWORK","DREAMS COME TRUE","B'z","スピッツ","Mr.Children","安室奈美恵","宇多田ヒカル","椎名林檎","浜崎あゆみ","L'Arc〜en〜Ciel","GLAY","ゆず","aiko","くるり","BUMP OF CHICKEN","Perfume","サカナクション","星野源","AKB48","ONE OK ROCK","米津玄師","Official髭男dism","King Gnu","YOASOBI","藤井風","Ado","Creepy Nuts"]

def request(path, params):
    url = f"{BASE}/{path}?" + urllib.parse.urlencode({**params, "fmt": "json"})
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.load(response)
            time.sleep(1.05)
            return result
        except Exception:
            if attempt == 3: raise
            time.sleep(2 ** attempt)

def find_artist(name):
    data = request("artist", {"query": f'artist:"{name}" AND area:Japan', "limit": 5})
    candidates = data.get("artists", [])
    exact = [a for a in candidates if a.get("name", "").casefold() == name.casefold()]
    return (exact or candidates or [None])[0]

def albums_for(mbid):
    albums, offset = [], 0
    while True:
        data = request("release-group", {"artist": mbid, "type": "album", "limit": 100, "offset": offset})
        groups = data.get("release-groups", [])
        for rg in groups:
            secondary = rg.get("secondary-types", [])
            if secondary: continue
            date = rg.get("first-release-date", "")
            year = int(date[:4]) if len(date) >= 4 and date[:4].isdigit() else None
            albums.append({"title": rg["title"], "year": year, "release_group_mbid": rg["id"], "tracks": []})
        offset += len(groups)
        if not groups or offset >= data.get("release-group-count", 0): break
    return sorted(albums, key=lambda a: (a["year"] or 9999, a["title"]))

def convert(raw):
    life = raw.get("life-span", {})
    year = lambda value: int(value[:4]) if value and value[:4].isdigit() else None
    return {"mbid": raw["id"], "name": raw["name"], "type": "person" if raw.get("type") == "Person" else "group", "begin_year": year(life.get("begin")), "end_year": year(life.get("end")), "area": (raw.get("begin-area") or raw.get("area") or {}).get("name", "日本"), "tags": [t["name"] for t in raw.get("tags", [])], "albums": albums_for(raw["id"])}

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--limit", type=int); args = parser.parse_args()
    DATA.mkdir(exist_ok=True)
    progress = json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {"completed": [], "artists": []}
    completed = set(progress["completed"]); names = SEEDS[:args.limit] if args.limit else SEEDS
    for index, name in enumerate(names, 1):
        if name in completed: continue
        print(f"[{index}/{len(names)}] {name}", flush=True)
        raw = find_artist(name)
        if raw: progress["artists"].append(convert(raw))
        progress["completed"].append(name); completed.add(name)
        PROGRESS.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n")
    OUT.write_text(json.dumps(progress["artists"], ensure_ascii=False, indent=2) + "\n")
    print(f"完了: {len(progress['artists'])}組 → {OUT}")

if __name__ == "__main__": main()
