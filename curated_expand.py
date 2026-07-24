#!/usr/bin/env python3
"""代表的なJ-POPアーティストと主要曲を初期データへ安全に追加する。"""
import json
from pathlib import Path

P=Path(__file__).parent/"data/artists.json"
# 名前|種別|開始年|タグ|主要曲（/区切り）。既存名は自動的にスキップする。
ROWS=r"""
石原裕次郎|person|1956|kayokyoku|嵐を呼ぶ男/銀座の恋の物語/赤いハンカチ/夜霧よ今夜も有難う
ザ・ピーナッツ|group|1959|kayokyoku|恋のバカンス/恋のフーガ/モスラの歌/ウナ・セラ・ディ東京
加山雄三|person|1961|kayokyoku|君といつまでも/お嫁においで/蒼い星くず/海 その愛
吉永小百合|person|1962|kayokyoku|寒い朝/いつでも夢を/若い東京の屋根の下/勇気あるもの
橋幸夫|person|1960|kayokyoku|潮来笠/いつでも夢を/恋のメキシカン・ロック/霧氷
舟木一夫|person|1963|kayokyoku|高校三年生/学園広場/絶唱/銭形平次
西郷輝彦|person|1964|kayokyoku|君だけを/星のフラメンコ/青年おはら節/願い星叶い星
ザ・スパイダース|group|1961|rock|フリフリ/夕陽が泣いている/あの時君は若かった/バン・バン・バン
ザ・タイガース|group|1967|rock|僕のマリー/シーサイド・バウンド/君だけに愛を/花の首飾り
ザ・テンプターズ|group|1967|rock|忘れ得ぬ君/神様お願い!/エメラルドの伝説/おかあさん
ジャッキー吉川とブルー・コメッツ|group|1957|rock|青い瞳/青い渚/ブルー・シャトウ/草原の輝き
森山良子|person|1967|folk|この広い野原いっぱい/禁じられた恋/さとうきび畑/涙そうそう
岡林信康|person|1968|folk|山谷ブルース/友よ/チューリップのアップリケ/私たちの望むものは
高田渡|person|1968|folk|自衛隊に入ろう/生活の柄/値上げ/コーヒーブルース
吉田拓郎|person|1970|folk|結婚しようよ/旅の宿/落陽/人生を語らず
井上陽水|person|1969|new music|傘がない/夢の中へ/氷の世界/少年時代
泉谷しげる|person|1971|folk|春夏秋冬/黒いカバン/眠れない夜/翼なき野郎ども
かぐや姫|group|1970|folk|神田川/赤ちょうちん/妹/22才の別れ
チューリップ|group|1971|new music|魔法の黄色い靴/心の旅/青春の影/サボテンの花
アリス|group|1971|new music|冬の稲妻/涙の誓い/チャンピオン/遠くで汽笛を聞きながら
海援隊|group|1971|folk|母に捧げるバラード/思えば遠くへ来たもんだ/贈る言葉/人として
オノ・ヨーコ|person|1961|alternative|Why/Walking on Thin Ice/Kiss Kiss Kiss/Warzone
矢沢永吉|person|1972|rock|アイ・ラヴ・ユー、OK/時間よ止まれ/YES MY LOVE/止まらないHa〜Ha
キャロル|group|1972|rock|ファンキー・モンキー・ベイビー/ルイジアンナ/涙のテディ・ボーイ/憎いあの娘
ゴダイゴ|group|1975|rock|ガンダーラ/モンキー・マジック/ビューティフル・ネーム/銀河鉄道999
ピンク・レディー|group|1976|idol pop|ペッパー警部/S・O・S/渚のシンドバッド/UFO
キャンディーズ|group|1973|idol pop|年下の男の子/ハートのエースが出てこない/春一番/微笑がえし
山口百恵|person|1973|idol pop|ひと夏の経験/横須賀ストーリー/秋桜/いい日旅立ち
岩崎宏美|person|1975|idol pop|ロマンス/センチメンタル/シンデレラ・ハネムーン/聖母たちのララバイ
郷ひろみ|person|1972|idol pop|男の子女の子/よろしく哀愁/2億4千万の瞳/GOLDFINGER '99
西城秀樹|person|1972|idol pop|情熱の嵐/傷だらけのローラ/YOUNG MAN/ギャランドゥ
野口五郎|person|1971|idol pop|青いリンゴ/甘い生活/私鉄沿線/グッド・ラック
沢田研二|person|1967|kayokyoku|勝手にしやがれ/時の過ぎゆくままに/TOKIO/危険なふたり
布施明|person|1965|kayokyoku|霧の摩周湖/シクラメンのかほり/君は薔薇より美しい/マイ・ウェイ
八神純子|person|1974|city pop|思い出は美しすぎて/みずいろの雨/パープルタウン/Mr.ブルー
竹内まりや|person|1978|city pop|September/不思議なピーチパイ/元気を出して/プラスティック・ラブ
杏里|person|1978|city pop|オリビアを聴きながら/CAT'S EYE/悲しみがとまらない/Remember Summer Days
角松敏生|person|1981|city pop|YOKOHAMA Twilight Time/If You…/Sea Line/初恋
杉山清貴&オメガトライブ|group|1983|city pop|SUMMER SUSPICION/君のハートはマリンブルー/ふたりの夏物語/サイレンスがいっぱい
稲垣潤一|person|1982|city pop|ドラマティック・レイン/夏のクラクション/クリスマスキャロルの頃には/ロング・バージョン
寺尾聰|person|1964|city pop|SHADOW CITY/出航 SASURAI/ルビーの指環/HABANA EXPRESS
南佳孝|person|1973|city pop|モンロー・ウォーク/スローなブギにしてくれ/スタンダード・ナンバー/憧れのラジオ・ガール
吉田美奈子|person|1969|city pop|夢で逢えたら/愛は彼方/TOWN/恋は流星
亜蘭知子|person|1981|city pop|Midnight Pretenders/I'm in Love/ひと夏のタペストリー/More Relax
安全地帯|group|1973|rock|ワインレッドの心/恋の予感/悲しみにさよなら/じれったい
玉置浩二|person|1982|j-pop|田園/メロディー/しあわせのランプ/MR.LONELY
CHAGE and ASKA|group|1979|new music|万里の河/SAY YES/YAH YAH YAH/僕はこの瞳で嘘をつく
大滝詠一|person|1970|city pop|君は天然色/恋するカレン/A面で恋をして/幸せな結末
細野晴臣|person|1969|electronic|恋は桃色/終りの季節/Sports Men/薔薇と野獣
坂本龍一|person|1978|electronic|千のナイフ/Merry Christmas Mr. Lawrence/energy flow/andata
高橋幸宏|person|1972|technopop|音楽殺人/Drip Dry Eyes/前兆/Disposable Love
佐野元春|person|1980|rock|アンジェリーナ/SOMEDAY/ガラスのジェネレーション/YOUNG BLOODS
大江千里|person|1983|j-pop|十人十色/格好悪いふられ方/ありがとう/塩屋
渡辺美里|person|1985|j-pop|My Revolution/悲しいね/サマータイム ブルース/10 years
尾崎豊|person|1983|rock|15の夜/十七歳の地図/I LOVE YOU/卒業
浜田省吾|person|1975|rock|路地裏の少年/悲しみは雪のように/J.BOY/もうひとつの土曜日
長渕剛|person|1978|folk|巡恋歌/順子/乾杯/とんぼ
THE ALFEE|group|1974|rock|メリーアン/星空のディスタンス/恋人達のペイヴメント/Promised Love
チェッカーズ|group|1983|j-pop|ギザギザハートの子守唄/涙のリクエスト/ジュリアに傷心/星屑のステージ
米米CLUB|group|1982|j-pop|浪漫飛行/FUNK FUJIYAMA/君がいるだけで/Shake Hip!
プリンセス プリンセス|group|1983|rock|世界でいちばん熱い夏/19 GROWING UP/Diamonds/M
PERSONZ|group|1984|rock|DEAR FRIENDS/7 COLORS/Mighty Boys/BE HAPPY
LINDBERG|group|1988|rock|今すぐKiss Me/BELIEVE IN LOVE/恋をしようよ Yeah! Yeah!/GAMBAらなくちゃね
JUN SKY WALKER(S)|group|1980|rock|歩いていこう/START/すてきな夜空/白いクリスマス
THE BOOM|group|1986|rock|島唄/星のラブレター/風になりたい/中央線
電気グルーヴ|group|1989|electronic|N.O./Shangri-La/虹/富士山
ピチカート・ファイヴ|group|1984|alternative|スウィート・ソウル・レヴュー/東京は夜の七時/大都会交響楽/ベイビィ・ポータブル・ロック
フリッパーズ・ギター|group|1987|alternative|恋とマシンガン/カメラ! カメラ! カメラ!/グルーヴ・チューブ/星の彼方へ
小沢健二|person|1989|alternative|今夜はブギー・バック/ラブリー/強い気持ち・強い愛/ぼくらが旅に出る理由
Original Love|group|1986|city pop|接吻/朝日のあたる道/プライマル/夜をぶっとばせ
Cornelius|person|1989|alternative|STAR FRUITS SURF RIDER/POINT OF VIEW POINT/Drop/あなたがいるなら
フィッシュマンズ|group|1987|alternative|いかれたBaby/ナイトクルージング/頼りない天使/新しい人
UA|person|1995|alternative|情熱/リズム/悲しみジョニー/ミルクティー
CHARA|person|1991|alternative|Heaven/やさしい気持ち/Swallowtail Butterfly/タイムマシーン
MISIA|person|1998|r&b|つつみ込むように…/BELIEVE/Everything/アイノカタチ
久保田利伸|person|1986|r&b|流星のサドル/Missing/LA・LA・LA LOVE SONG/Love Reborn
平井堅|person|1995|r&b|楽園/even if/瞳をとじて/POP STAR
CHEMISTRY|group|2001|r&b|PIECES OF A DREAM/Point of No Return/You Go Your Way/My Gift to You
SPEED|group|1996|dance pop|Body & Soul/STEADY/White Love/ALL MY TRUE LOVE
globe|group|1995|dance pop|Feel Like dance/DEPARTURES/Can't Stop Fallin' in Love/FACES PLACES
TRF|group|1992|dance pop|EZ DO DANCE/survival dAnce/BOY MEETS GIRL/CRAZY GONNA CRAZY
華原朋美|person|1995|dance pop|keep yourself alive/I'm proud/I BELIEVE/Hate tell a lie
Every Little Thing|group|1996|j-pop|Feel My Heart/Time goes by/For the moment/fragile
My Little Lover|group|1995|j-pop|Man & Woman/Hello, Again 〜昔からある場所〜/ALICE/DESTINY
JUDY AND MARY|group|1992|rock|BLUE TEARS/Over Drive/そばかす/くじら12号
THE YELLOW MONKEY|group|1988|rock|JAM/LOVE LOVE SHOW/楽園/バラ色の日々
X JAPAN|group|1982|visual kei|紅/ENDLESS RAIN/Silent Jealousy/Forever Love
LUNA SEA|group|1989|visual kei|ROSIER/TRUE BLUE/END OF SORROW/I for You
BUCK-TICK|group|1983|visual kei|JUST ONE MORE KISS/悪の華/ドレス/蜉蝣
hide|person|1987|visual kei|EYES LOVE YOU/DICE/ROCKET DIVE/ピンク スパイダー
黒夢|group|1991|visual kei|BEAMS/少年/Like @ Angel/MARIA
SOPHIA|group|1994|rock|街/黒いブーツ/ゴキゲン鳥/Believe
Dragon Ash|group|1996|alternative|陽はまたのぼりくりかえす/Let yourself go, Let myself go/Grateful Days/Fantasista
RIP SLYME|group|1994|hip hop|STEPPER'S DELIGHT/楽園ベイベー/One/JOINT
m-flo|group|1998|hip hop|been so long/Come Again/miss you/let go
KICK THE CAN CREW|group|1997|hip hop|スーパーオリジナル/マルシェ/クリスマス・イブRap/アンバランス
RHYMESTER|group|1989|hip hop|B-BOYイズム/ウワサの真相/肉体関係 part 2/梯子酒
スチャダラパー|group|1988|hip hop|ゲームボーイズ/今夜はブギー・バック/サマージャム'95/ついてる男
ZEEBRA|person|1995|hip hop|真っ昼間/Street Dreams/Mr. Dynamite/Neva Enuff
ケツメイシ|group|1993|hip hop|トモダチ/夏の思い出/さくら/君にBUMP
ポルノグラフィティ|group|1994|rock|アポロ/サウダージ/アゲハ蝶/メリッサ
東京スカパラダイスオーケストラ|group|1985|rock|MONSTER ROCK/火の玉ジャイヴ/美しく燃える森/銀河と迷路
BRAHMAN|group|1995|rock|SEE OFF/DEEP/ARRIVAL TIME/A WHITE DEEP MORNING
Hi-STANDARD|group|1991|punk rock|GROWING UP/STAY GOLD/BRAND NEW SUNSET/DEAR MY FRIEND
ELLEGARDEN|group|1998|rock|ジターバグ/風の日/Make A Wish/Salamander
10-FEET|group|1997|rock|RIVER/第ゼロ感/その向こうへ/ヒトリセカイ
MONGOL800|group|1998|rock|小さな恋のうた/あなたに/琉球愛歌/Don't worry be happy
HY|group|2000|rock|AM11:00/366日/Song for…/NAO
ORANGE RANGE|group|2001|rock|上海ハニー/ロコローション/花/イケナイ太陽
レミオロメン|group|2000|rock|3月9日/粉雪/南風/蒼の世界
フジファブリック|group|2000|alternative|桜の季節/若者のすべて/銀河/茜色の夕日
ストレイテナー|group|1998|alternative|KILLER TUNE/シーグラス/REMINDER/Melodic Storm
ACIDMAN|group|1997|alternative|赤橙/ある証明/造花が笑う/ALMA
RADWIMPS|group|2001|alternative|有心論/ふたりごと/前前前世/スパークル
マキシマム ザ ホルモン|group|1998|rock|恋のメガラバ/爪爪爪/What's up, people?!/予襲復讐
Superfly|person|2004|rock|ハロー・ハロー/愛をこめて花束を/タマシイレボリューション/Beautiful
いきものがかり|group|1999|j-pop|SAKURA/ブルーバード/YELL/ありがとう
コブクロ|group|1998|j-pop|YELL〜エール〜/桜/蕾/流星
秦基博|person|2006|j-pop|シンクロ/鱗/アイ/ひまわりの約束
絢香|person|2006|j-pop|I believe/三日月/みんな空の下/にじいろ
中島美嘉|person|2001|j-pop|STARS/WILL/雪の華/GLAMOROUS SKY
倖田來未|person|2000|dance pop|real Emotion/キューティーハニー/Butterfly/愛のうた
BoA|person|2000|dance pop|LISTEN TO MY HEART/VALENTI/メリクリ/永遠
大塚愛|person|2003|j-pop|さくらんぼ/金魚花火/プラネタリウム/恋愛写真
YUI|person|2004|j-pop|feel my soul/Good-bye days/CHE.R.RY/again
木村カエラ|person|2004|j-pop|リルラ リルハ/Butterfly/You/マスタッシュ
AI|person|2000|r&b|Story/ハピネス/みんながみんな英雄/アルデバラン
EXILE|group|2001|dance pop|Choo Choo TRAIN/ただ…逢いたくて/Lovers Again/道
三代目 J SOUL BROTHERS|group|2010|dance pop|Best Friend's Girl/花火/R.Y.U.S.E.I./Summer Madness
嵐|group|1999|idol pop|A・RA・SHI/One Love/Love so sweet/Happiness
SMAP|group|1988|idol pop|夜空ノムコウ/らいおんハート/世界に一つだけの花/オレンジ
KinKi Kids|group|1997|idol pop|硝子の少年/愛されるより 愛したい/フラワー/Anniversary
モーニング娘。|group|1997|idol pop|モーニングコーヒー/LOVEマシーン/恋愛レボリューション21/ザ☆ピ〜ス!
乃木坂46|group|2011|idol pop|ぐるぐるカーテン/制服のマネキン/インフルエンサー/シンクロニシティ
欅坂46|group|2015|idol pop|サイレントマジョリティー/二人セゾン/不協和音/風に吹かれても
BABYMETAL|group|2010|rock|ギミチョコ!!/メギツネ/KARATE/PA PA YA!!
BiSH|group|2015|idol pop|BiSH-星が瞬く夜に-/プロミスザスター/オーケストラ/beautifulさ
SEKAI NO OWARI|group|2007|j-pop|幻の命/RPG/スターライトパレード/Dragon Night
ゲスの極み乙女|group|2012|alternative|キラーボール/猟奇的なキスを私にして/私以外私じゃないの/ロマンスがありあまる
クリープハイプ|group|2001|alternative|左耳/社会の窓/栞/イト
back number|group|2004|j-pop|花束/高嶺の花子さん/クリスマスソング/水平線
Mrs. GREEN APPLE|group|2013|j-pop|StaRt/青と夏/僕のこと/ダンスホール
あいみょん|person|2014|j-pop|生きていたんだよな/君はロックを聴かない/マリーゴールド/裸の心
Vaundy|person|2019|j-pop|東京フラッシュ/不可幸力/怪獣の花唄/踊り子
ずっと真夜中でいいのに。|group|2018|internet music|秒針を噛む/脳裏上のクラッカー/正しくなれない/残機
ヨルシカ|group|2017|internet music|言って。/ただ君に晴れ/だから僕は音楽を辞めた/花に亡霊
Eve|person|2009|internet music|ドラマツルギー/ナンセンス文学/廻廻奇譚/心予報
優里|person|2019|j-pop|ドライフラワー/かくれんぼ/ベテルギウス/ビリミリオン
緑黄色社会|group|2012|j-pop|Mela!/Shout Baby/キャラクター/花になって
羊文学|group|2012|alternative|光るとき/1999/あいまいでいいよ/more than words
マカロニえんぴつ|group|2012|rock|ブルーベリー・ナイツ/恋人ごっこ/なんでもないよ、/リンジュー・ラヴ
Saucy Dog|group|2013|rock|いつか/シンデレラボーイ/結/魔法にかけられて
新しい学校のリーダーズ|group|2015|j-pop|毒花/オトナブルー/Pineapple Kryptonite/Tokyo Calling
Number_i|group|2023|hip hop|GOAT/Blow Your Cover/BON/INZM
ano|person|2013|j-pop|ちゅ、多様性。/普変/スマイルあげない/絶絶絶絶対聖域
ちゃんみな|person|2016|hip hop|FXXKER/Never Grow Up/美人/ハレンチ
Awich|person|2006|hip hop|Remember/GILA GILA/Queendom/Bad Bitch 美学
Nujabes|person|1995|hip hop|Luv(sic) Part 3/Feather/Aruarian Dance/Reflection Eternal
宇多丸|person|1989|hip hop|The Choice Is Yours/After 6 Junction/人間交差点/予定は未定で。
折坂悠太|person|2013|folk|平成/朝顔/さびしさ/トーチ
藤原さくら|person|2013|j-pop|Soup/かわいい/春の歌/Waver
iri|person|2014|r&b|Watashi/Rhythm/Wonderland/会いたいわ
STUTS|person|2013|hip hop|Mirrors/Changes/Presence I/夜を使いはたして
Tempalay|group|2014|alternative|革命前夜/そなちね/あびばのんのん/大東京万博
WONK|group|2013|soul|savior/Signal/Orange Mug/Blue Moon
Lucky Kilimanjaro|group|2014|electronic|Burning Friday Night/太陽/エモめの夏/踊りの合図
水曜日のカンパネラ|group|2012|electronic|桃太郎/一休さん/エジソン/招き猫
DAOKO|person|2012|hip hop|水星/かけてあげる/打上花火/御伽の街
Reol|person|2012|internet music|No title/ギミアブレスタッナウ/第六感/煽げや尊し
LiSA|person|2010|j-pop|crossing field/Rising Hope/紅蓮華/炎
Aimer|person|2011|j-pop|RE:I AM/蝶々結び/カタオモイ/残響散歌
米米CLUB|group|1982|j-pop|浪漫飛行/君がいるだけで/Shake Hip!/FUNK FUJIYAMA
MAN WITH A MISSION|group|2010|rock|FLY AGAIN/Emotions/Raise your flag/絆ノ奇跡
UVERworld|group|2000|rock|D-tecnoLife/SHAMROCK/儚くも永久のカナシ/CORE PRIDE
Alexandros|group|2001|rock|ワタリドリ/Adventure/明日、また/閃光
SiM|group|2004|rock|KiLLiNG ME/Blah Blah Blah/The Rumbling/EXiSTENCE
Fear, and Loathing in Las Vegas|group|2008|rock|Love at First Sight/Just Awake/Let Me Hear/Party Boys
女王蜂|group|2009|rock|デスコ/火炎/メフィスト/01
打首獄門同好会|group|2004|rock|日本の米は世界一/布団の中から出たくない/はたらきたくない/筋肉マイフレンド
キリンジ|group|1996|city pop|風を撃て/エイリアンズ/Drifter/千年紀末に降る雪は
ハナレグミ|person|1997|folk|家族の風景/明日天気になれ/光と影/深呼吸
クラムボン|group|1995|alternative|はなれ ばなれ/シカゴ/サラウンド/Re-ある鼓動
サニーデイ・サービス|group|1992|alternative|青春狂走曲/恋におちたら/サマー・ソルジャー/若者たち
カネコアヤノ|person|2012|folk|祝日/光の方へ/さよーならあなた/抱擁
never young beach|group|2014|city pop|あまり行かない喫茶店で/明るい未来/なんかさ/お別れの歌
Suchmos|group|2013|city pop|STAY TUNE/MINT/YMM/808
Awesome City Club|group|2013|city pop|勿忘/アウトサイダー/今夜だけ間違いじゃないことにしてあげる/Don't Think, Feel
TENDRE|person|2017|soul|DOCUMENT/RAINBOW/HOPE/NOT IN ALMIGHTY
imase|person|2021|j-pop|Have a nice day/NIGHT DANCER/ユートピア/Nagisa
tuki.|person|2023|j-pop|晩餐歌/サクラキミワタシ/地獄恋文/ひゅるりらぱっぱ
こっちのけんと|person|2022|j-pop|死ぬな!/どんぐりGAME/はいよろこんで/もういいよ
ILLIT|group|2024|idol pop|Magnetic/Lucky Girl Syndrome/Cherish/IYKYK
XG|group|2022|hip hop|Tippy Toes/SHOOTING STAR/LEFT RIGHT/WOKE UP
""".strip().splitlines()

data=json.loads(P.read_text()); names={a["name"].casefold() for a in data}; added=0
for i,line in enumerate(ROWS):
    name,kind,begin,tag,songs=line.split("|",4)
    if name.casefold() in names: continue
    tracks=[{"title":s} for s in songs.split("/")]
    data.append({"mbid":f"curated-{i+1:03d}","name":name,"type":kind,"begin_year":int(begin),"end_year":None,"area":"日本","tags":[tag],"albums":[{"title":"主要楽曲セレクション","year":int(begin),"tracks":tracks}]})
    names.add(name.casefold()); added+=1
P.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
print(f"追加 {added}組 / 合計 {len(data)}組 / {sum(len(x.get('tracks',[])) for a in data for x in a.get('albums',[]))}曲")
