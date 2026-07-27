# J-POP History 名盤ガイドPSEO運用手順

精選した日本のポピュラー音楽名盤の日英静的ページを再生成・検証するための手順書です。生成ページは既存アプリを置き換えず、事実情報からアプリ本体へ案内します。

## 対象と日英対応

- 日本語: `data/album_guide.json`
- 英語: `data/album_guide.en.json`
- ジャンル: `data/genres.json` / `data/genres.en.json`
- URL: `/items/<slug>/` と `/en/items/<slug>/`

日英各33件を14カテゴリ内の位置と発表年で対応させる。日本語名と英語名は翻訳により異なるため一致を要求しない。slugは英語のアーティスト名・アルバム名・年からASCIIケバブケースで生成する。

`data/artists.json` 内の約15,564件の取得アルバムは補助データであり、精査が済むまで対象にしない。

## 出力範囲

アルバム名、アーティスト名、発表年、ジャンルだけを出力する。紹介文、画像、曲目、歌詞、音源は本文、メタ情報、OGP、JSON-LD、索引へ複製しない。SpotifyとApple Musicは検索リンクだけを設置する。

## 構造化データと配信

`MusicAlbum`、`Person`／`MusicGroup`、`WebSite`、`WebPage`、`BreadcrumbList`、索引用`CollectionPage`を使用する。アーティスト種別は日本語・英語のMBID対応データから取得し、未一致時は `MusicGroup` とする。データにない値は推測しない。

既存のAdSense読み込みと本番ホスト判定を維持し、canonical、日英相互hreflang、共通OGP画像を設定する。33件×2言語、索引2ページ、既存主要6ページの合計74 URLをsitemapへ収録する。生成ページはService Workerの事前キャッシュに加えない。

## 再生成と検証

```sh
python3 scripts/generate_pages.py
python3 scripts/validate_generated_pages.py
git diff --check
```

生成物は手編集せず、入力データ、テンプレート、生成スクリプトを修正して再生成する。公開前に日英各33詳細ページ、索引2ページ、sitemap 74 URL、全内部リンク、SEO要素、除外項目を確認し、pushはオーナー承認後に行う。
