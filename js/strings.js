// strings.js: 日本語/英語のUI文言辞書。LOCALEに応じてSオブジェクトの値が決まる。
import { LOCALE } from "./i18n.js";

const en = LOCALE === "en";

export const S = {
  // ===== 共通 =====
  loading: en ? "Loading…" : "読み込み中…",
  notFound: en ? "Page not found" : "ページが見つかりません",
  loadError: (msg) => (en ? `An error occurred while loading: ${msg}` : `読み込みエラーが発生しました: ${msg}`),
  person: en ? "Solo" : "個人",
  group: en ? "Group" : "グループ",
  periodUnknown: en ? "Period unknown" : "活動時期不明",
  yearUnknown: en ? "Year unknown" : "年不明",
  yearUnknownShort: en ? "unknown" : "不明",
  present: en ? "present" : "現在",
  periodSeparator: en ? "–" : "〜",
  decadeLabel: (y) => (en ? `${y}s` : `${y}年代`),
  artistsCount: (n) => (en ? `${n} artists` : `${n}組`),

  // ===== timeline.js =====
  timelineEyebrow: en ? "A STORY OF JAPANESE POPULAR MUSIC" : "A STORY OF JAPANESE POPULAR MUSIC",
  timelineTitle: en
    ? `Tracing Japanese pop music<br>through eras and sound.`
    : `日本のポップミュージックを<br>時代と音でたどる。`,
  timelineLead: (n) => (en
    ? `From kayokyoku to city pop, the band boom, and internet-born music — explore ${n} artists to see how J-POP has changed.`
    : `歌謡曲からシティポップ、バンドブーム、ネット発の音楽まで。${n}組の入り口からJ-POPの変化を見渡せます。`),

  // ===== views/timeline.js: 8つの年代の見出しと解説 =====
  DECADES: en
    ? [
        {
          year: 1940,
          label: "1940s–50s",
          desc: `As postwar recovery took hold, radio, film, and records carried popular songs across the country. Kayokyoku absorbed overseas music like jazz and Latin, refined through a division of labor between star singers and songwriters, laying the popular-music foundation that would later support J-POP.`,
        },
        {
          year: 1960,
          label: "1960s",
          desc: `Alongside the spread of television, teen-idol kayokyoku, and Group Sounds, Kansai folk emerged. Artists like Nobuyasu Okabayashi sang about society and everyday life in their own words. Young musicians who started out covering Western songs searched for ways to sing in Japanese, nurturing the singer-songwriter culture that followed.`,
        },
        {
          year: 1970,
          label: "1970s",
          desc: `Takuro Yoshida and Yosui Inoue expanded folk into personal lyricism and popular song, ushering in the singer-songwriter era. In Osaka and Kyoto, acts like Yuka Dan, Masaki Ueda, and West Road turned blues into music sung in Japanese about everyday life. Soul and electronic music intersected too, and the seeds of city pop and technopop began to sprout.`,
        },
        {
          year: 1980,
          label: "1980s",
          desc: `The golden age of idols and the band boom filled television screens, and the shift to CDs expanded the music industry. Electronic sound after YMO, rock from bands like BOØWY, and the polished pop of artists like Seiko Matsuda all coexisted — and the term "J-POP" itself was born.`,
        },
        {
          year: 1990,
          label: "1990s",
          desc: `The CD market climbed toward its peak, and tie-ins with TV dramas and commercials produced one massive hit after another. The Komuro sound, Shibuya-kei, visual kei, R&B, and hip hop connected to the mainstream in quick succession, and J-POP's scope expanded more than ever before.`,
        },
        {
          year: 2000,
          label: "2000s",
          desc: `Listening habits shifted from CDs to ringtone downloads and streaming. While rock festivals and live houses nurtured a diverse range of bands, video-sharing sites and Vocaloid created new circuits for creation and discovery that bypassed record labels entirely.`,
        },
        {
          year: 2010,
          label: "2010s",
          desc: `Streaming and social media took hold, and idols, bands, and internet-born creators began crossing paths on the same charts. City pop saw a major reassessment worldwide, and an environment took shape where listeners could enjoy old recordings and new songs side by side, across generations and borders.`,
        },
        {
          year: 2020,
          label: "2020s–",
          desc: `In an era when a single song can reach the world instantly through short-form video and anime, more artists are balancing internet culture with strong individual artistry. J-POP continues to evolve beyond the boundaries of a purely domestic genre.`,
        },
      ]
    : [
        { year: 1940, label: "1940〜50年代", desc: "戦後の復興とともにラジオ、映画、レコードが流行歌を全国へ届けた。ジャズやラテンなど海外音楽を吸収した歌謡曲が、スター歌手と作家の分業によって磨かれ、後のJ-POPを支える大衆音楽の基盤が生まれた。" },
        { year: 1960, label: "1960年代", desc: "テレビの普及、青春歌謡、グループ・サウンズとともに、関西フォークが登場。岡林信康、高石ともやらは社会や日常を自分の言葉で歌った。洋楽のコピーから出発した若者たちは日本語で歌う方法を探り、後のシンガーソングライター文化を育てた。" },
        { year: 1970, label: "1970年代", desc: "吉田拓郎、井上陽水らがフォークを個人の言葉と大衆的なポップスへ広げ、シンガーソングライターの時代が到来。大阪・京都では憂歌団、上田正樹、ウエスト・ロードらがブルースを日本語と生活の音楽へ変えた。ソウルや電子音楽も交差し、シティポップとテクノポップの芽が開いた。" },
        { year: 1980, label: "1980年代", desc: "アイドル黄金期とバンドブームがテレビを彩り、CDへの移行が音楽産業を拡大した。YMO以後の電子音、BOØWYらのロック、松田聖子らの精緻なポップスが共存し、「J-POP」という呼び名も生まれた。" },
        { year: 1990, label: "1990年代", desc: "CD市場が頂点へ向かい、ドラマやCMとのタイアップから巨大ヒットが続出。小室サウンド、渋谷系、ヴィジュアル系、R&B、ヒップホップが次々と主流に接続し、J-POPの輪郭が最も大きく広がった。" },
        { year: 2000, label: "2000年代", desc: "CDから着うた・配信へ聴取環境が変化。ロックフェスとライブハウスから多様なバンドが育つ一方、動画投稿サイトとボーカロイドが、レーベルを経由しない新しい創作と発見の回路を作った。" },
        { year: 2010, label: "2010年代", desc: "ストリーミングとSNSが定着し、アイドル、バンド、ネット発の制作者が同じチャートで交差。シティポップの世界的再評価も進み、過去の音源と新曲を同時に聴く、世代や国境を越えた環境が整った。" },
        { year: 2020, label: "2020年代〜", desc: "ショート動画やアニメを通じて一曲が瞬時に世界へ届く時代。ネット文化と高い作家性を両立する表現者が増え、J-POPは国内ジャンルという枠を越えて更新され続けている。" },
      ],

  // ===== artists.js =====
  artistsTitle: en ? "Artists" : "アーティスト一覧",
  artistsLead: (n) => (en ? `Search and filter all ${n} J-POP artists.` : `全${n}組のJ-POPアーティストを検索・絞り込みできます。`),
  searchPlaceholder: en ? "Search by artist name…" : "アーティスト名で検索…",
  sortName: en ? "Name" : "名前順",
  sortBegin: en ? "Debut year" : "活動開始年順",
  sortAlbums: en ? "Album count" : "アルバム数順",
  typeAll: en ? "All" : "すべて",
  decadeAll: en ? "All eras" : "すべての年代",
  genreAll: en ? "All genres" : "すべてのジャンル",
  hitsCount: (n) => (en ? `${n} results` : `${n}件ヒット`),
  personnelHeading: (n) => (en ? `As featured personnel (${n} albums)` : `参加ミュージシャンとして(${n}件のアルバム)`),
  personnelHint: en
    ? "These albums matched your search in the personnel credits, not the artist name."
    : "アーティスト名ではなく、アルバムの参加ミュージシャンのクレジットが検索語と一致しています。",
  noResults: en ? "No matching artists found." : "該当するアーティストが見つかりませんでした。",
  featuredBadge: en ? "Featured" : "参加",

  // ===== artist-detail.js =====
  artistNotFound: en ? "Artist not found." : "アーティストが見つかりませんでした。",
  backToList: en ? "Back to list" : "一覧に戻る",
  backToArtists: en ? "← Back to artist list" : "← アーティスト一覧に戻る",
  favRemove: en ? "★ Remove from favorites" : "★ お気に入り解除",
  favAdd: en ? "☆ Add to favorites" : "☆ お気に入りに追加",
  wikipediaLabel: en ? "Wikipedia" : "Wikipedia(日本語版)",
  spotifySearch: en ? "Search on Spotify" : "Spotifyで検索",
  appleMusicSearch: en ? "Search on Apple Music" : "Apple Musicで検索",
  albumsHeading: (n) => (en ? `Albums (${n})` : `アルバム作品 (${n}件)`),
  noAlbums: en ? "No albums on record." : "登録されているアルバムがありません。",
  singlesHeading: (n) => (en ? `Singles (${n})` : `シングル (${n}件)`),
  selectionsHeading: en ? "Selected Songs" : "主要楽曲",
  personnelPrefix: en ? "Personnel: " : "参加ミュージシャン: ",
  lineupPrefix: en ? "Estimated lineup (based on tenure at release): " : "推定メンバー(発売年の在籍期間より): ",
  tracklistSummary: (n) => (en ? `Tracklist (${n} tracks)` : `収録曲(${n}曲)`),
  allSongsHeading: en ? "All Songs" : "全楽曲",
  allSongsCount: (n) => (en ? `${n} songs` : `${n}曲`),
  allSongsEmpty: en ? "Full track data is still being collected." : "全曲データは収集中です。",
  allSongsSearchPlaceholder: en ? "Search this artist's song titles…" : "このアーティストの曲名を検索…",

  // ===== songs.js =====
  songsTitle: en ? "Song Search" : "楽曲検索",
  songsLead: (n) => (en ? `Search track titles across all ${n.toLocaleString()} songs.` : `全${n.toLocaleString()}曲の収録曲タイトルから検索できます。`),
  songSearchPlaceholder: en ? "Search by song title…" : "曲名で検索…",
  songSearchEmpty: en ? "Enter a song title to see results." : "曲名を入力すると検索結果が表示されます。",
  songNoResults: en ? "No matching songs found." : "該当する曲が見つかりませんでした。",
  songHitsCount: (n) => (en ? `${n} results` : `${n}件ヒット`),
  songHitsCountLimited: (n, limit) => (en
    ? `${n} results (showing the first ${limit}; try narrowing your search)`
    : `${n}件ヒット(先頭${limit}件のみ表示。絞り込みを追加してください)`),

  // ===== favorites.js =====
  favoritesTitle: en ? "Favorites" : "お気に入り",
  favoritesLead: en
    ? 'Artists you add via "☆ Add to favorites" on their detail page will appear here.'
    : "アーティスト詳細ページの「☆ お気に入りに追加」で登録したアーティストがここに表示されます。",
  favoritesEmpty: en
    ? 'You haven\'t added any favorites yet. Add some from the <a href="#/artists">artist list</a>.'
    : `まだお気に入りが登録されていません。<a href="#/artists">アーティスト一覧</a>から追加してみましょう。`,
  syncFailed: en
    ? "Sync failed. Please check your connection and try again."
    : "同期に失敗しました。通信環境を確認してもう一度お試しください。",
  syncPanelTitle: en ? "Sync Across Devices" : "デバイス間の同期",
  syncPanelLeadWithCode: en
    ? "Enter this sync code on your other devices to share your favorites."
    : "この同期コードを他の自分の端末に入力すると、お気に入りが共有されます。",
  syncNow: en ? "Sync now" : "今すぐ同期",
  syncReset: en ? "Turn off sync" : "同期を解除",
  syncPanelLeadNoCode: en
    ? "Generate a sync code to share your favorites with your other devices."
    : "同期コードを発行すると、他の自分の端末とお気に入りを共有できます。",
  syncGenerate: en ? "Generate sync code" : "同期コードを発行する",
  syncJoinLabel: en ? "Have a code from another device? Enter it here" : "他の端末で発行したコードをお持ちの場合はこちら",
  syncCodePlaceholder: en ? "e.g. AB3XQK7M" : "例: AB3XQK7M",
  syncJoinSubmit: en ? "Sync with this code" : "このコードで同期",
  syncResetConfirm: en
    ? "Turn off sync on this device? Your favorites will remain on this device."
    : "この端末での同期を解除しますか?お気に入り自体は端末に残ります。",

  // ===== genres.js =====
  genresTitle: en ? "Genre Family Tree" : "ジャンル系統図",
  genresLead: en
    ? "How the major currents that shaped J-POP relate to one another. Tap a genre to see its artists."
    : "J-POPを形づくった主な流れの関係です。ジャンルをタップすると該当アーティストへ移動します。",

  // ===== glossary.js =====
  glossaryTitle: en ? "Glossary" : "用語集",
  glossaryLead: en
    ? "Key scene terms for understanding the history of J-POP."
    : "J-POPの歴史を読み解くためのシーン用語をまとめました。",

  // ===== guide.js =====
  guideTitle: en ? "Essential Albums" : "名盤ガイド",
  guideLead: en
    ? "Essential albums picked for each genre — a great place to start listening."
    : "ジャンルごとに選んだ代表的な名盤です。まずここから聴き始めてみてください。",
  findOnAmazon: en ? "Find on Amazon" : "CD/レコードを探す",

  // ===== relations.js =====
  relationsTitle: en ? "Member Connections" : "メンバー相関図",
  relationsLead: en
    ? "J-POP connections through band members, production, and collaborations. Drag nodes to move them; tap an artist in the data to open their detail page."
    : "メンバー、プロデュース、共演から見るJ-POPのつながりです。ノードはドラッグでき、収録アーティストはタップで詳細へ移動します。",

  // ===== stats.js =====
  statsTitle: en ? "Statistics" : "統計",
  statsLead: (n) => (en ? `A look at the breadth of J-POP through the data on all ${n} artists.` : `収録データ(全${n}組)からJ-POPの広がりを眺めます。`),
  basicInfo: en ? "Overview" : "基本情報",
  albumsByDecadeHeading: en ? "Albums Released by Decade" : "年代別アルバムリリース数",
  artistsByGenreHeading: en ? "Artists by Genre" : "ジャンル別アーティスト数",

  // ===== donate.js =====
  kofiSupport: en ? "☕ Support on Ko-fi" : "☕ Ko-fiで応援する",
};
