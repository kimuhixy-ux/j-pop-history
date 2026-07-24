# J-POP History

昭和歌謡から現代までをたどる、ビルド不要の静的PWAです。v5.2では15,564作品をアルバム／EP／シングルに分類し、アルバムとEPは作品ごとに収録曲を表示します。全330組・83,907件のユニーク曲名を収録し、年表、検索と絞り込み、作品・全楽曲、ジャンル系統図、D3.js相関図、名盤ガイド、用語集、お気に入り、統計を利用できます。

## ローカルで見る

ターミナルで次の2行を実行します。

```bash
cd /Users/user/j-pop-history
python3 -m http.server 8080
```

Safariなどで `http://localhost:8080` を開いてください。終了するときはターミナルで `control + C` を押します。HTMLを直接ダブルクリックすると、ブラウザの制限でJSONを読めないため、必ずローカルサーバーを使います。

## データを再収集する

まず10組で確認できます。

```bash
python3 fetch_data.py --limit 10
```

問題なければ `python3 fetch_data.py` でシード全件を取得します。MusicBrainzの利用制限に合わせて1リクエストごとに約1秒待つため、アルバム数によって数十分以上かかります。進捗は `data/progress.json` に保存され、中断後も同じコマンドで再開できます。再収集すると同梱の編集済み `artists.json` を置き換える点に注意してください。

### 数百組・数千曲へ拡張する

編集済みデータを残したままMusicBrainzのアーティスト、アルバム、楽曲を追加します。

```bash
python3 expand_data.py --target 300
```

API制限を守るため、300組では約10〜20分が目安です。処理ごとに保存され、途中で止めても同じコマンドで再開できます。

## GitHub Pagesへ公開する

```bash
cd /Users/user/j-pop-history
git init
git add .
git commit -m "Create J-POP History PWA"
git branch -M main
git remote add origin https://github.com/あなたのユーザー名/j-pop-history.git
git push -u origin main
```

GitHubのリポジトリで **Settings → Pages → Deploy from a branch** を選び、`main` / `root` を保存します。数分後に表示されるURLから開けます。

## データについて

代表的な330組を選び、Apple Music掲載作品、検索結果、編集済み代表曲から83,907件のユニーク曲名を収録しています。アルバム／EP 8,485作品には合計101,963件の収録曲情報があり、利用可能な作品にはApple Music提供のアートワークを表示します。再発盤、ライブ版、リミックスなど表題が異なる録音も含みます。配信されていない作品まで保証する網羅的データベースではありません。MusicBrainz由来データは [CC0](https://musicbrainz.org/doc/About/Data_License)、D3.jsはISCライセンスです。
