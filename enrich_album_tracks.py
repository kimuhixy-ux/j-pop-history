#!/usr/bin/env python3
"""Apple Musicのcollection IDから作品種別とアルバム収録曲を補完する。"""
import json, re, subprocess, time, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT=Path(__file__).parent; FILE=ROOT/"data/artists.json"; PROGRESS=ROOT/"data/album_tracks_progress.json"

def get(url):
    for n in range(5):
        p=subprocess.run(["curl","-fsS","--retry","3","--retry-all-errors","--connect-timeout","15","--max-time","90",url],capture_output=True,text=True)
        if p.returncode==0: return json.loads(p.stdout)
        if n==4: raise RuntimeError(p.stderr.strip())
        time.sleep(2**n)

def release_type(title):
    if re.search(r"(?:^|\s[-–—]\s?)Single$", title, re.I): return "single"
    if re.search(r"(?:^|\s[-–—]\s?)EP$", title, re.I): return "ep"
    if title in {"主要楽曲セレクション","代表楽曲"}: return "selection"
    return "album"

def enrich_artist(artist):
    albums=artist.get("albums",[]); by_id={a.get("apple_collection_id"):a for a in albums if a.get("apple_collection_id")}
    for album in albums: album["release_type"]=release_type(album.get("title", ""))
    ids=list(by_id)
    for start in range(0,len(ids),20):
        batch=ids[start:start+20]
        url="https://itunes.apple.com/lookup?"+urllib.parse.urlencode({"id":",".join(map(str,batch)),"country":"JP","entity":"song"})
        rows=get(url).get("results",[]); grouped={cid:[] for cid in batch}
        for row in rows:
            cid=row.get("collectionId"); title=(row.get("trackName") or "").strip()
            if row.get("wrapperType")=="track" and cid in grouped and title:
                grouped[cid].append({"title":title,"number":row.get("trackNumber")})
        for cid,tracks in grouped.items():
            album=by_id[cid]
            if album["release_type"] != "single":
                seen=set(); unique=[]
                for track in sorted(tracks,key=lambda t:(t.get("number") or 9999,t["title"])):
                    key=track["title"].casefold()
                    if key not in seen: seen.add(key); unique.append({"title":track["title"]})
                album["tracks"]=unique
    return len(ids)

def main():
    artists=json.loads(FILE.read_text()); done=set(json.loads(PROGRESS.read_text()).get("completed",[])) if PROGRESS.exists() else set()
    targets=[a for a in artists if a["name"] not in done]
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures={pool.submit(enrich_artist,a):a for a in targets}
        for i,future in enumerate(as_completed(futures),1):
            artist=futures[future]
            try:
                count=future.result(); done.add(artist["name"])
                if i%10==0 or i==len(targets):
                    FILE.write_text(json.dumps(artists,ensure_ascii=False,indent=2)+"\n")
                    PROGRESS.write_text(json.dumps({"completed":sorted(done)},ensure_ascii=False,indent=2)+"\n")
                print(f"[{i}/{len(targets)}] {artist['name']}: {count}作品",flush=True)
            except Exception as e: print(f"[{i}/{len(targets)}] {artist['name']}: 失敗 {e}",flush=True)
    # 公開JSONには表示に必要な曲名だけを残す。
    for artist in artists:
        for album in artist.get("albums",[]):
            album["tracks"]=[{"title":track["title"]} for track in album.get("tracks",[]) if track.get("title")]
    FILE.write_text(json.dumps(artists,ensure_ascii=False,indent=2)+"\n")

if __name__=="__main__": main()
