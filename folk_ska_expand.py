#!/usr/bin/env python3
"""v5.0: 日本のフォークとスカ／スカパンクを独立カテゴリとして拡充する。"""
import json
from pathlib import Path
ROOT=Path(__file__).parent; AP=ROOT/"data/artists.json"; GP=ROOT/"data/genres.json"; LP=ROOT/"data/glossary.json"; AG=ROOT/"data/album_guide.json"
ROWS=r"""
遠藤賢司|person|1969|japanese folk|カレーライス/夜汽車のブルース/満足できるかな/不滅の男
加川良|person|1970|japanese folk|教訓I/下宿屋/ゼニの効用力について/流行歌
友川カズキ|person|1974|japanese folk|生きてるって言ってみろ/サーカス/無残の美/海みたいな空だ
三上寛|person|1970|japanese folk|夢は夜ひらく/負ける時もあるだろう/ひびけ電気釜!!/青森県北津軽郡東京村
なぎら健壱|person|1970|japanese folk|悲惨な戦い/葛飾にバッタを見た/いっぽんでもニンジン/夜風に乾杯
小室等|person|1968|japanese folk|雨が空から降れば/出発の歌/だれかが風の中で/お早うの朝
六文銭|group|1968|japanese folk|雨が空から降れば/面影橋から/キングサーモンのいる島/サーカスゲーム
五つの赤い風船|group|1967|japanese folk|遠い世界に/血まみれの鳩/恋は風に乗って/これがボクらの道なのか
赤い鳥|group|1969|japanese folk|翼をください/竹田の子守唄/赤い花 白い花/河
ガロ|group|1970|japanese folk|学生街の喫茶店/君の誕生日/ロマンス/一枚の楽譜
ふきのとう|group|1972|japanese folk|白い冬/風来坊/春雷/柿の実色した水曜日
NSP|group|1972|japanese folk|夕暮れ時はさびしそう/さようなら/八十八夜/赤い糸の伝説
さだまさし|person|1973|japanese folk|関白宣言/道化師のソネット/案山子/主人公
グレープ|group|1972|japanese folk|精霊流し/無縁坂/縁切寺/朝刊
伊勢正三|person|1970|japanese folk|なごり雪/海岸通/22才の別れ/ほんの短い夏
南こうせつ|person|1970|japanese folk|夢一夜/夏の少女/妹/神田川
山崎ハコ|person|1975|japanese folk|呪い/望郷/織江の唄/白い花
中川五郎|person|1967|japanese folk|受験生ブルース/主婦のブルース/25年目のおっぱい/腰まで泥まみれ
斉藤哲夫|person|1970|japanese folk|悩み多き者よ/いまのキミはピカピカに光って/グッド・タイム・ミュージック/さんま焼けたか
あがた森魚|person|1972|japanese folk|赤色エレジー/最后のダンスステップ/大寒町/春の嵐の夜の手品師
高石ともや|person|1966|japanese folk|受験生ブルース/想い出の赤いヤッケ/街/陽気に行こう
KEMURI|group|1995|ska punk|P.M.A./Ato-Ichinen/Along the Longest Way/Ohichyo
MUTE BEAT|group|1981|ska|Still Echo/Organ's Melody/Dub No.5/Metro
THE SKA FLAMES|group|1985|ska|Tokyo Shot/Christine Keeler/Tokyo Ska Fever/Samurai
DETERMINATIONS|group|1991|ska|Under My Skin/Full of Determination/Bayon/Perfidia
POTSHOT|group|1995|ska punk|Radio/Party/Be Alive/Clear
SCAFULL KING|group|1990|ska punk|YOU AND I, WALK AND SMILE/The Simple Anger/IRISH FARM/Save You Love
RUDE BONES|group|1993|ska punk|Loosen Up/Let's Keep Our Heads Up/Where Are You Now?/Just to Have Fun
GELUGUGU|group|1996|ska punk|100 SKA/CRACKERS!/彼女は/WE ARE GELUGUGU
COOL WISE MEN|group|1993|ska|Cool Wise Man/Run Down/Don't Stop Music/Unforgettable
Oi-SKALL MATES|group|1996|ska|NUTTY SOUND/いかれたBaby/SKINHEAD RUNNIN'/Bring On Nutty Stomper Fun
THE MICETEETH|group|1999|ska|霧の中/レモンの花が咲いていた/ネモ/春のあぶく
DOBERMAN|group|1998|ska|Bella Ciao/消えた狂犬とそれにまつわるウワサ/朱い太陽/車掌は寝転んだまま
SKA SKA CLUB|group|1997|ska punk|Santa Monica/Right Now!/Heartbreak Cafe/Daybreak Turnpike
Yum!Yum!ORANGE|group|1999|ska punk|葛飾ラプソディー/Orange Street/WITH YOU/Precious Days
ムラマサ☆|group|2001|ska punk|サクラ舞い散る夜は/SWAY/夢風鈴/HECTIC!!!!!!!!
ORESKABAND|group|2003|ska|アーモンド/自転車/爪先/ピノキオ
HEY-SMITH|group|2006|ska punk|Endless Sorrow/Be The One/California/Inside Of Me
YOUR SONG IS GOOD|group|1998|ska|SUPER SOUL MEETIN'/A MAN FROM THE NEW TOWN/THE LOVE SONG/あいつによろしく
THE MAN|group|2012|ska|GABBA GABBA HEY/THE MAN STILL STANDING/SHOT THE SHERIFF/Preach
ROLLINGS|group|1996|ska|SAMURAI/BLUE BEAT/ROLLING MAN/CHERRY OH BABY
CHANGE UP|group|1997|ska punk|ONE MORE TIME/NEVER GIVE UP/SMILE/KEEP ON RUNNING
FRUITY|group|1995|ska punk|SUMMER CAMP/ROCKAWAY/SONG FOR YOU/LET'S GO
""".strip().splitlines()

A=json.loads(AP.read_text()); names={a["name"].casefold() for a in A}; added=[]
for i,row in enumerate(ROWS):
 name,kind,year,tag,songs=row.split("|",4)
 if name.casefold() in names: continue
 A.append({"mbid":f"v5-{i+1:03d}","name":name,"type":kind,"begin_year":int(year),"end_year":None,"area":"日本","tags":[tag],"albums":[{"title":"主要楽曲セレクション","year":int(year),"tracks":[{"title":x} for x in songs.split("/")]}]}); names.add(name.casefold()); added.append(name)
# 既存の代表的フォーク／スカ系も新カテゴリへ明示的に分類する。
folk={"井上陽水","吉田拓郎","岡林信康","高田渡","泉谷しげる","かぐや姫","海援隊","森山良子","中島みゆき","長渕剛","ハナレグミ","折坂悠太","カネコアヤノ"}
ska={"東京スカパラダイスオーケストラ"}
for a in A:
 if a["name"] in folk and "japanese folk" not in a["tags"]: a["tags"].append("japanese folk")
 if a["name"] in ska and "ska" not in a["tags"]: a["tags"].append("ska")
AP.write_text(json.dumps(A,ensure_ascii=False,indent=2)+"\n")

G=json.loads(GP.read_text()); cats=G["categories"]
new=[{"id":"japanese-folk","label":"日本のフォーク","period":"1960s–","description":"社会への問い、日常の言葉、個人の物語を自作自演で歌い、日本語の歌を変えた流れ。"},{"id":"ska","label":"スカ／スカパンク","period":"1980s–","description":"ジャマイカのスカを基礎に、ホーン、ダブ、パンクを交差させた日本独自のダンス音楽。"}]
for c in reversed(new):
 if not any(x["id"]==c["id"] for x in cats): cats.insert(2,c)
for edge in [{"from":"kayokyoku","to":"japanese-folk"},{"from":"japanese-folk","to":"folk-newmusic"},{"from":"japanese-folk","to":"rock"},{"from":"japanese-blues","to":"ska"},{"from":"ska","to":"rock"}]:
 if edge not in G["genealogy"]: G["genealogy"].append(edge)
G["tag_map"].update({"japanese folk":["japanese-folk"],"folk":["japanese-folk"],"folk rock":["japanese-folk","rock"],"singer-songwriter":["japanese-folk","folk-newmusic"],"ska":["ska"],"japanese ska":["ska"],"ska punk":["ska","rock"],"2 tone":["ska"]}); GP.write_text(json.dumps(G,ensure_ascii=False,indent=2)+"\n")

L=json.loads(LP.read_text()); existing={x["term"] for x in L}
for x in [{"term":"関西フォーク","desc":"1960年代後半、関西の若者が社会や日常を自分の言葉で歌った運動。岡林信康、高石ともや、中川五郎らが重要。"},{"term":"フォーク・クルセダーズ以後","desc":"日本語の創作フォークが全国へ広がり、吉田拓郎や井上陽水らのシンガーソングライター文化へ接続した流れ。"},{"term":"スカ","desc":"ジャマイカで生まれた裏拍のリズムを特徴とする音楽。日本ではMUTE BEAT、スカパラ、KEMURIらがダブやパンクと結びつけた。"},{"term":"P.M.A.","desc":"KEMURIが掲げるPositive Mental Attitudeの略。日本のスカパンクを象徴する理念として広く知られる。"}]:
 if x["term"] not in existing: L.insert(0,x)
LP.write_text(json.dumps(L,ensure_ascii=False,indent=2)+"\n")

guide=json.loads(AG.read_text())
guide["japanese-folk"]=[{"artist":"岡林信康","album":"わたしを断罪せよ","year":1969,"note":"社会への鋭い視線を日本語のフォークへ刻んだ初期の重要作。"},{"artist":"吉田拓郎","album":"元気です。","year":1972,"note":"個人の言葉とメロディを大衆へ届け、シンガーソングライター時代を切り開いた。"},{"artist":"井上陽水","album":"氷の世界","year":1973,"note":"言葉の曖昧さと鮮やかなサウンドで、フォークからニューミュージックへの扉を開いた。"},{"artist":"友川カズキ","album":"やっと一枚目","year":1975,"note":"張りつめた声と詩が、フォークの表現を極限まで押し広げる。"},{"artist":"山崎ハコ","album":"飛・び・ま・す","year":1975,"note":"孤独と故郷を深い声で描き、70年代フォークの陰影を伝える。"}]
guide["ska"]=[{"artist":"MUTE BEAT","album":"STILL ECHO","year":1987,"note":"ダブの空間とスカのリズムを研ぎ澄まし、世界に先駆けた日本の重要作。"},{"artist":"東京スカパラダイスオーケストラ","album":"スカパラ登場","year":1990,"note":"祝祭性と高い演奏力で、日本のスカを広い観客へ開いたデビュー作。"},{"artist":"KEMURI","album":"Little Playmate","year":1997,"note":"P.M.A.の精神と高速スカパンクを結び、日本と米国のシーンをつないだ。"},{"artist":"DETERMINATIONS","album":"Full of Determination","year":1997,"note":"ルーツへの深い理解と大阪の熱気が共存するジャパニーズ・スカの名盤。"},{"artist":"YOUR SONG IS GOOD","album":"YOUR SONG IS GOOD","year":2004,"note":"スカ、カリプソ、ソウルを現代のインストゥルメンタル・ダンス音楽へ更新した。"}]
AG.write_text(json.dumps(guide,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"added":len(added),"total":len(A),"names":added},ensure_ascii=False))
