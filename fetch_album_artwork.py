#!/usr/bin/env python3
"""Apple Music公開検索からアルバム情報とアートワークを追加する。"""
import json, subprocess, time, unicodedata, urllib.parse
from pathlib import Path

ROOT=Path(__file__).parent; FILE=ROOT/"data/artists.json"; PROGRESS=ROOT/"data/artwork_progress.json"
ALIASES={"荒井由実／松任谷由実":"松任谷由実","UNICORN":"ユニコーン","L'Arc〜en〜Ciel":"L'Arc-en-Ciel","チューリップ":"TULIP","プリンセス プリンセス":"PRINCESS PRINCESS","フリッパーズ・ギター":"Flipper's Guitar","フィッシュマンズ":"Fishmans","マキシマム ザ ホルモン":"マキシマムザホルモン","キリンジ":"KIRINJI","サザンオールスターズ":"Southern All Stars"}

def get(url):
    for n in range(5):
        p=subprocess.run(["curl","-fsS","--retry","3","--retry-all-errors","--connect-timeout","15","--max-time","60",url],capture_output=True,text=True)
        if p.returncode==0: return json.loads(p.stdout)
        if n==4: raise RuntimeError(p.stderr.strip())
        time.sleep(2**n)

def norm(v): return unicodedata.normalize("NFKC",v).casefold().replace(" ","").replace("・","").replace("ザ","")

def catalog(name):
    query=ALIASES.get(name,name); params={"term":query,"country":"JP","media":"music","entity":"musicArtist","limit":10}
    rows=get("https://itunes.apple.com/search?"+urllib.parse.urlencode(params)).get("results",[])
    if not rows: return []
    exact=[x for x in rows if norm(x.get("artistName",""))==norm(query)]; artist=(exact or rows)[0]
    params={"id":artist["artistId"],"country":"JP","entity":"album","limit":200}
    albums=[]; seen=set()
    for row in get("https://itunes.apple.com/lookup?"+urllib.parse.urlencode(params)).get("results",[]):
        title=row.get("collectionName","").strip(); key=norm(title)
        if not title or not row.get("collectionId") or key in seen: continue
        seen.add(key); date=row.get("releaseDate",""); artwork=row.get("artworkUrl100","")
        if artwork: artwork=artwork.replace("100x100bb","600x600bb")
        albums.append({"title":title,"year":int(date[:4]) if date[:4].isdigit() else None,"artwork":artwork,"apple_collection_id":row["collectionId"],"tracks":[]})
    return sorted(albums,key=lambda x:(x["year"] or 9999,x["title"]))

def main():
    data=json.loads(FILE.read_text()); done=set(json.loads(PROGRESS.read_text()).get("completed",[])) if PROGRESS.exists() else set()
    for i,a in enumerate(data,1):
        if a["name"] in done: continue
        print(f"[{i}/{len(data)}] {a['name']}",flush=True)
        try:
            incoming=catalog(a["name"]); existing={norm(x["title"]):x for x in a.get("albums",[])}
            for album in incoming:
                old=existing.get(norm(album["title"]))
                if old:
                    if album["artwork"]: old["artwork"]=album["artwork"]
                    old.setdefault("apple_collection_id",album["apple_collection_id"])
                else: a.setdefault("albums",[]).append(album)
            a["albums"].sort(key=lambda x:(x.get("year") or 9999,x["title"])); done.add(a["name"])
            FILE.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n"); PROGRESS.write_text(json.dumps({"completed":sorted(done)},ensure_ascii=False,indent=2)+"\n")
            print(f"  {len(incoming)}作品",flush=True)
        except Exception as e: print(f"  失敗: {e}",flush=True)
    print(f"完了: アートワーク {sum(1 for a in data for x in a.get('albums',[]) if x.get('artwork'))}件",flush=True)
if __name__=="__main__": main()
