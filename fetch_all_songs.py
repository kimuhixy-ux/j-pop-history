#!/usr/bin/env python3
"""全アーティストのMusicBrainz登録録音をページ送りで取得する。

1組だけ: python3 fetch_all_songs.py --artist サザンオールスターズ
全組:     python3 fetch_all_songs.py --all
処理済みアーティストはスキップされ、各組の完了ごとにartists.jsonへ保存する。
"""
import argparse, json, subprocess, time, unicodedata, urllib.parse
from pathlib import Path

ROOT=Path(__file__).parent; FILE=ROOT/"data/artists.json"; PROGRESS=ROOT/"data/songs_progress.json"
BASE="https://musicbrainz.org/ws/2"; UA="j-pop-history/3.0 (contact: example@example.com)"

def api(path,params):
    url=f"{BASE}/{path}/?"+urllib.parse.urlencode({**params,"fmt":"json"})
    for attempt in range(6):
        p=subprocess.run(["curl","-fsS","--retry","4","--retry-all-errors","--connect-timeout","15","--max-time","90","-A",UA,url],capture_output=True,text=True)
        if p.returncode==0:
            time.sleep(1.05); return json.loads(p.stdout)
        if attempt==5: raise RuntimeError(p.stderr.strip() or f"curl error {p.returncode}")
        time.sleep(2**attempt)

def resolve(artist):
    mbid=artist.get("mbid","")
    if len(mbid)==36 and mbid.count("-")==4: return mbid
    q=f'artist:"{artist["name"]}" AND area:Japan'
    rows=api("artist",{"query":q,"limit":10}).get("artists",[])
    exact=[x for x in rows if x.get("name","").casefold()==artist["name"].casefold()]
    return (exact or rows or [{}])[0].get("id")

def fetch_titles(mbid):
    titles=[]; offset=0; total=None
    while total is None or offset<total:
        result=api("recording",{"query":f"arid:{mbid}","limit":100,"offset":offset})
        rows=result.get("recordings",[]); total=result.get("count",len(rows))
        titles.extend(x.get("title","").strip() for x in rows if x.get("title","").strip())
        offset+=len(rows)
        if not rows: break
    # Unicode表記を揃え、取得順を保って完全重複だけを除く。
    seen=set(); unique=[]
    for title in titles:
        title=unicodedata.normalize("NFC",title); key=title.casefold()
        if key in seen: continue
        seen.add(key); unique.append(title)
    return unique,total

def fetch_itunes(artist_name):
    aliases={"UNICORN":"ユニコーン","L'Arc〜en〜Ciel":"L'Arc-en-Ciel","チューリップ":"TULIP","プリンセス プリンセス":"PRINCESS PRINCESS","フリッパーズ・ギター":"Flipper's Guitar","フィッシュマンズ":"Fishmans","マキシマム ザ ホルモン":"Maximum the Hormone","キリンジ":"KIRINJI"}
    search_name=aliases.get(artist_name,artist_name)
    url="https://itunes.apple.com/search?"+urllib.parse.urlencode({"term":search_name,"country":"JP","media":"music","entity":"song","limit":200})
    p=subprocess.run(["curl","-fsS","--retry","4","--retry-all-errors","--connect-timeout","15","--max-time","60",url],capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr.strip())
    rows=json.loads(p.stdout).get("results",[]); seen=set(); titles=[]
    def norm(v): return unicodedata.normalize("NFKC",v).casefold().replace(" ","").replace("・","")
    wanted=norm(search_name)
    for row in rows:
        credited=norm(row.get("artistName",""))
        # 同名曲を歌う別アーティストやトリビュート盤を除外する。
        if wanted not in credited and credited not in wanted: continue
        title=unicodedata.normalize("NFC",row.get("trackName","").strip()); key=title.casefold()
        if title and key not in seen: seen.add(key); titles.append(title)
    return titles,len(rows)

def get_url(url):
    p=subprocess.run(["curl","-fsS","--retry","4","--retry-all-errors","--connect-timeout","15","--max-time","90",url],capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr.strip())
    return json.loads(p.stdout)

def fetch_itunes_catalog(artist_name):
    aliases={"荒井由実／松任谷由実":"松任谷由実","UNICORN":"ユニコーン","L'Arc〜en〜Ciel":"L'Arc-en-Ciel","チューリップ":"TULIP","プリンセス プリンセス":"PRINCESS PRINCESS","フリッパーズ・ギター":"Flipper's Guitar","フィッシュマンズ":"Fishmans","マキシマム ザ ホルモン":"マキシマムザホルモン","キリンジ":"KIRINJI","サザンオールスターズ":"Southern All Stars"}
    query=aliases.get(artist_name,artist_name); params={"term":query,"country":"JP","media":"music","entity":"musicArtist","limit":10}
    candidates=get_url("https://itunes.apple.com/search?"+urllib.parse.urlencode(params)).get("results",[])
    if not candidates: return [],0
    def norm(v): return unicodedata.normalize("NFKC",v).casefold().replace(" ","").replace("・","").replace("ザ","")
    exact=[x for x in candidates if norm(x.get("artistName",""))==norm(query)]
    chosen=(exact or candidates)[0]; artist_id=chosen["artistId"]
    albums_url="https://itunes.apple.com/lookup?"+urllib.parse.urlencode({"id":artist_id,"country":"JP","entity":"album","limit":200})
    album_rows=get_url(albums_url).get("results",[]); ids=[]
    for row in album_rows:
        cid=row.get("collectionId")
        if cid and cid not in ids: ids.append(cid)
    titles=[]; seen=set()
    for start in range(0,len(ids),20):
        batch=",".join(map(str,ids[start:start+20])); url="https://itunes.apple.com/lookup?"+urllib.parse.urlencode({"id":batch,"country":"JP","entity":"song"})
        for row in get_url(url).get("results",[]):
            title=row.get("trackName","").strip(); key=unicodedata.normalize("NFC",title).casefold()
            if row.get("wrapperType")=="track" and title and key not in seen: seen.add(key); titles.append(unicodedata.normalize("NFC",title))
        time.sleep(.15)
    return titles,len(ids)

def save(data,done):
    FILE.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    PROGRESS.write_text(json.dumps({"completed":sorted(done)},ensure_ascii=False,indent=2)+"\n")

def main():
    p=argparse.ArgumentParser(); g=p.add_mutually_exclusive_group(required=True); g.add_argument("--artist"); g.add_argument("--all",action="store_true"); p.add_argument("--source",choices=["musicbrainz","itunes","itunes-catalog"],default="musicbrainz"); args=p.parse_args()
    data=json.loads(FILE.read_text()); done=set(json.loads(PROGRESS.read_text()).get("completed",[])) if PROGRESS.exists() else set()
    targets=data if args.all else [a for a in data if a["name"]==args.artist]
    if not targets: raise SystemExit("指定したアーティストが見つかりません")
    for i,a in enumerate(targets,1):
        done_key=f"{args.source}:{a['name']}"
        if args.all and done_key in done: continue
        print(f"[{i}/{len(targets)}] {a['name']}",flush=True)
        try:
            if args.source=="itunes": titles,total=fetch_itunes(a["name"])
            elif args.source=="itunes-catalog": titles,total=fetch_itunes_catalog(a["name"])
            else:
                mbid=resolve(a)
                if not mbid: print("  MusicBrainz未検出",flush=True); done.add(done_key); save(data,done); continue
                titles,total=fetch_titles(mbid); a["musicbrainz_mbid"]=mbid
            # 複数ソースを実行しても曲名を失わず、完全重複だけを除く。
            merged=[]; seen=set()
            for title in [*a.get("songs",[]),*titles]:
                key=unicodedata.normalize("NFC",title).casefold()
                if key not in seen: seen.add(key); merged.append(title)
            a["songs"]=merged; done.add(done_key); save(data,done); print(f"  {len(titles)}曲取得 / 合計{len(merged)}曲",flush=True)
        except Exception as e: print(f"  失敗: {e}",flush=True)
    print(f"保存完了: 全曲一覧 {sum(len(a.get('songs',[])) for a in data)}曲",flush=True)
if __name__=="__main__": main()
