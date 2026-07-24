#!/usr/bin/env python3
"""日本のブルース／ブルースロック系アーティストとジャンルを追加する。"""
import json
from pathlib import Path
ROOT=Path(__file__).parent; AP=ROOT/"data/artists.json"; GP=ROOT/"data/genres.json"; LP=ROOT/"data/glossary.json"
ROWS=r"""
憂歌団|group|1970|おそうじオバチャン/嫌んなった/胸が痛い/パチンコ〜ランラン・ブルース
木村充揮|person|1970|天王寺/胸が痛い/ケサラ/アイム・ソーリー
内田勘太郎|person|1970|ひきがたり/グッバイ・クロスロード/南部の人/10$の恋
上田正樹|person|1972|悲しい色やね/TAKAKO/大阪ベイブルース/わがまま
上田正樹とサウス・トゥ・サウス|group|1974|むかでの錦三/梅田からナンバまで/大阪へ出て来てから/お前を離さない
ウエスト・ロード・ブルース・バンド|group|1972|Tramp/First Time I Met the Blues/T-Bone Shuffle/It's My Own Fault
永井“ホトケ”隆|person|1972|Night People/Another You/Sunrise Blues/Somebody Have Mercy
塩次伸二|person|1972|Chicago Midnight/Stormy Monday/Going Down/Blues With a Feeling
妹尾隆一郎|person|1960|Blues Harp/Key to the Highway/Help Me/Boogie Thing
ブレイクダウン|group|1976|Jukebox Mama/泣いてばかり/お前のそばに/Blue Monday
近藤房之助|person|1976|夢の尻尾/遠くへ行きたい/Take Me Back/Goodbye Morning
有山じゅんじ|person|1968|ありやまな夜だ/梅田からナンバまで/ぐるぐるぐる/上町筋
吾妻光良 & The Swinging Boppers|group|1979|やっぱり肉を喰おう/最後まで楽しもう/福田さんはカッコいい/On the Sunny Side of the Street
ローラーコースター|group|1974|That's All Right/Every Night Every Day/One More Chance/Blues After Hours
小出斉|person|1974|Chicago Bound/You Belong to Me/Blues Is My Business/Everyday I Have the Blues
入道|person|1973|Shake Your Moneymaker/Blues Power/俺のブルース/Stormy Monday
大木トオル|person|1967|Manhattan Midnight/博多ブルース/Stand By Me/When a Man Loves a Woman
浅川マキ|person|1968|夜が明けたら/かもめ/赤い橋/ちっちゃな時から
金子マリ|person|1972|あるとき/最後の本音/彼女の笑顔/CRY BABY
金子マリ & バックスバニー|group|1974|あるとき/韋駄天BUNNY/最後の本音/気分を出してもう一度
Char|person|1976|Smoky/気絶するほど悩ましい/闘牛士/逆光線
Johnny, Louis & Char|group|1978|Wasted/Head Song/Finger/You're Like a Doll Baby
PINK CLOUD|group|1982|Drive Me Nuts/Everyday Everynight/Pink Cloud/Sugar Baby Game
竹田和夫|person|1969|Spinning Toe-Hold/Dark Eyed Lady/Lonely Night/Blues From The Yellow
ブルース・クリエイション|group|1969|Checkin' Up on My Baby/Spoonful/Smokestack Lightnin'/Baby Please Don't Go
クリエイション|group|1972|Spinning Toe-Hold/Lonely Heart/Dreamin'/New York Woman Serenade
柳ジョージ|person|1975|雨に泣いてる/青い瞳のステラ/酔って候/さらばミシシッピー
柳ジョージ & レイニーウッド|group|1975|雨に泣いてる/微笑の法則/プリズナー/フェンスの向こうのアメリカ
石田長生|person|1969|Happiness/Everybody 毎度! On the Street/Boninの島/ねぇ、神様
BAHO|group|1989|HAPPINESS/アミーゴ/DO IT AGAIN/BLACK SHOES
山岸潤史|person|1972|Really?!/Groovin'/Cat Walk/You'll Never Know
大村憲司|person|1971|Left-Handed Woman/Bamboo Bong/春がいっぱい/Maps
仲井戸麗市|person|1968|ティーンエイジャー/チャンスは今夜/打破/ホームタウン
鮎川誠|person|1966|レモンティー/ユー・メイ・ドリーム/ロックの好きなベイビー抱いて/ビールス カプセル
サンハウス|group|1970|レモンティー/キングスネークブルース/地獄へドライブ/ぬすっと
シーナ&ロケッツ|group|1978|ユー・メイ・ドリーム/レモンティー/涙のハイウェイ/ピンナップ・ベイビー・ブルース
陳信輝|person|1968|You Shook Me/The Train/Mississippi Mountain Blues/I Got My Mojo Working
パワー・ハウス|group|1968|Back in the U.S.S.R./Hoochie Coochie Man/Spoonful/Good Morning Little Schoolgirl
三宅伸治|person|1987|たたえる歌/何にもなかった日/フェニックス・ハネムーン/淋しい人
菊田俊介|person|1986|Rising Shun/Chicago Midnight/Look Out Baby/Funky Blues
静沢真紀|person|1990|Lady Blue/Walkin' the Dog/Hard Drivin' Woman/Blues for You
Nacomi Tanaka|person|2000|Onward and Upward/Bluesy Pop/No More Crying/Have You Seen My Man
原田芳雄|person|1973|横浜ホンキートンク・ブルース/新宿心中/風が吹きます/石榴
宇崎竜童|person|1973|身も心も/サクセス/裏切者の旅/知らず知らずのうちに
ダウン・タウン・ブギウギ・バンド|group|1973|スモーキン・ブギ/港のヨーコ・ヨコハマ・ヨコスカ/カッコマン・ブギ/身も心も
もんた&ブラザーズ|group|1979|ダンシング・オールナイト/赤いアンブレラ/DESIRE/KOBE
桑名正博|person|1971|セクシャルバイオレットNo.1/月のあかり/哀愁トゥナイト/オン・ザ・ハイウェイ
BORO|person|1979|大阪で生まれた女/都会千夜一夜/ネグレスコ・ホテル/見返り美人
""".strip().splitlines()
artists=json.loads(AP.read_text()); names={a["name"].casefold() for a in artists}; added=[]
for i,row in enumerate(ROWS):
 name,kind,year,songs=row.split("|",3)
 if name.casefold() in names: continue
 artists.append({"mbid":f"blues-{i+1:03d}","name":name,"type":kind,"begin_year":int(year),"end_year":None,"area":"日本","tags":["japanese blues","blues rock"],"albums":[{"title":"主要楽曲セレクション","year":int(year),"tracks":[{"title":x} for x in songs.split("/")]}]}); names.add(name.casefold()); added.append(name)
AP.write_text(json.dumps(artists,ensure_ascii=False,indent=2)+"\n")
genres=json.loads(GP.read_text()); cats=genres["categories"]
if not any(c["id"]=="japanese-blues" for c in cats): cats.insert(2,{"id":"japanese-blues","label":"ジャパニーズ・ブルース／ブルースロック","period":"1960s–","description":"米国ブルースを日本語、方言、都市の生活感で再解釈し、関西を中心に独自の演奏文化を築いた流れ。"})
for edge in [{"from":"kayokyoku","to":"japanese-blues"},{"from":"japanese-blues","to":"rock"},{"from":"folk-newmusic","to":"japanese-blues"}]:
 if edge not in genres["genealogy"]: genres["genealogy"].append(edge)
genres["tag_map"].update({"japanese blues":["japanese-blues"],"blues":["japanese-blues"],"blues rock":["japanese-blues","rock"],"rhythm and blues":["japanese-blues","dance-rnb"]}); GP.write_text(json.dumps(genres,ensure_ascii=False,indent=2)+"\n")
terms=json.loads(LP.read_text()); existing={x["term"] for x in terms}
for x in [{"term":"関西ブルース","desc":"1970年代の大阪・京都・神戸を中心に、憂歌団、ウエスト・ロード・ブルース・バンド、上田正樹らが育てた日本独自のブルース文化。"},{"term":"ジャパニーズ・ブルース","desc":"米国ブルースの形式を土台に、日本語や方言、都市生活の実感を歌う音楽。歌謡曲、フォーク、ロックとも深く交差する。"}]:
 if x["term"] not in existing: terms.insert(0,x)
LP.write_text(json.dumps(terms,ensure_ascii=False,indent=2)+"\n")
guide_path=ROOT/"data/album_guide.json"; guide=json.loads(guide_path.read_text())
guide["japanese-blues"]=[
 {"artist":"憂歌団","album":"憂歌団","year":1975,"note":"大阪の生活語と木村充揮の声、内田勘太郎のギターが結晶した、日本語ブルースの出発点。"},
 {"artist":"上田正樹とサウス・トゥ・サウス","album":"この熱い魂を伝えたいんや","year":1975,"note":"ソウルとブルースの熱気を関西弁の歌へ変えた、関西ブラックミュージック史の重要作。"},
 {"artist":"ウエスト・ロード・ブルース・バンド","album":"BLUES POWER","year":1975,"note":"シカゴ・ブルースへの敬意と若い演奏の勢いを刻んだ、関西ブルースを代表する一枚。"},
 {"artist":"浅川マキ","album":"浅川マキの世界","year":1970,"note":"ジャズ、ブルース、アングラ文化が交差する暗い手触りと日本語表現が圧倒的。"},
 {"artist":"吾妻光良 & The Swinging Boppers","album":"Squeezin' & Blowin'","year":1991,"note":"ジャンプ・ブルースの快楽と日本語のユーモアを、大編成の鋭い演奏で鳴らす。"}]
guide_path.write_text(json.dumps(guide,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"added":len(added),"total":len(artists),"names":added},ensure_ascii=False))
