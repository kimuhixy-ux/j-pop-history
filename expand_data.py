#!/usr/bin/env python3
"""MusicBrainzから数百組・数千曲を追加する。既存データを保ち、途中再開できる。"""
import argparse, json, subprocess, time, urllib.parse
from pathlib import Path

ROOT=Path(__file__).parent; ARTISTS=ROOT/"data/artists.json"; PROGRESS=ROOT/"data/expand_progress.json"
BASE="https://musicbrainz.org/ws/2"; HEADERS={"User-Agent":"j-pop-history/2.0 (contact: example@example.com)","Accept":"application/json"}
QUERIES=["tag:j-pop AND area:Japan","tag:japanese AND tag:pop AND area:Japan","tag:j-rock AND area:Japan","tag:city-pop AND area:Japan","tag:japanese-idol AND area:Japan","tag:japanese AND tag:rock AND area:Japan"]

def api(path,params):
    url=f"{BASE}/{path}?"+urllib.parse.urlencode({**params,"fmt":"json"})
    for n in range(5):
        try:
            raw=subprocess.run(["curl","-fsS","--retry","3","--max-time","45","-A",HEADERS["User-Agent"],url],check=True,capture_output=True,text=True).stdout
            data=json.loads(raw)
            time.sleep(1.05); return data
        except Exception as e:
            if n==4: raise
            print(f"  再試行: {e}",flush=True); time.sleep(2**n)

def discover(target):
    found={}
    for query in QUERIES:
        for offset in range(0,500,100):
            rows=api("artist",{"query":query,"limit":100,"offset":offset}).get("artists",[])
            for row in rows:
                if row.get("id") and row.get("name") and row.get("score",0)>=70: found[row["id"]]=row
            if len(rows)<100 or len(found)>=target*2: break
        if len(found)>=target*2: break
    return sorted(found.values(),key=lambda x:(-x.get("score",0),x["name"]))[:target]

def yr(v): return int(v[:4]) if v and len(v)>=4 and v[:4].isdigit() else None

def albums(mbid):
    rows=api("release-group",{"artist":mbid,"type":"album","limit":100}).get("release-groups",[])
    out=[{"title":x["title"],"year":yr(x.get("first-release-date")),"release_group_mbid":x["id"],"tracks":[]} for x in rows if not x.get("secondary-types")]
    return sorted(out,key=lambda x:(x["year"] or 9999,x["title"]))[:40]

def tracks(mbid):
    rows=api("recording",{"query":f"arid:{mbid}","limit":100}).get("recordings",[]); seen=set(); out=[]
    for row in rows:
        title=row.get("title","").strip(); key=title.casefold()
        if not title or key in seen: continue
        seen.add(key); out.append({"title":title})
        if len(out)>=35: break
    return out

def make(raw,al,tr):
    life=raw.get("life-span",{}); tags=[t["name"] for t in raw.get("tags",[])] or ["j-pop"]
    if al: al[0]["tracks"]=tr
    elif tr: al=[{"title":"代表楽曲","year":None,"tracks":tr}]
    return {"mbid":raw["id"],"name":raw["name"],"type":"person" if raw.get("type")=="Person" else "group","begin_year":yr(life.get("begin")),"end_year":yr(life.get("end")),"area":(raw.get("begin-area") or raw.get("area") or {}).get("name","日本"),"tags":tags,"albums":al}

def save(data,done):
    ARTISTS.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n"); PROGRESS.write_text(json.dumps({"completed":sorted(done)},indent=2)+"\n")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--target",type=int,default=300); args=p.parse_args()
    data=json.loads(ARTISTS.read_text()); done=set(json.loads(PROGRESS.read_text()).get("completed",[])) if PROGRESS.exists() else set(); candidates=discover(args.target)
    print(f"候補{len(candidates)}組、既存{len(data)}組から開始",flush=True)
    for i,raw in enumerate(candidates,1):
        if raw["id"] in done: continue
        print(f"[{i}/{len(candidates)}] {raw['name']}",flush=True)
        try:
            al,tr=albums(raw["id"]),tracks(raw["id"]); item=make(raw,al,tr); same=next((a for a in data if a["name"].casefold()==item["name"].casefold()),None)
            if same:
                same["mbid"]=raw["id"]; titles={x.get("title","").casefold() for x in same.get("albums",[])}; same["albums"].extend(x for x in al if x["title"].casefold() not in titles)
                if same["albums"]:
                    known={t["title"].casefold() for a in same["albums"] for t in a.get("tracks",[])}; same["albums"][0].setdefault("tracks",[]).extend(t for t in tr if t["title"].casefold() not in known)
            else: data.append(item)
            done.add(raw["id"]); save(data,done)
        except Exception as e: print(f"  スキップ: {e}",flush=True)
    songs=sum(len(x.get("tracks",[])) for a in data for x in a.get("albums",[])); print(f"完了: {len(data)}組 / {songs}曲",flush=True)
if __name__=="__main__": main()
