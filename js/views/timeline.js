import { loadData, decadeOf } from "../data.js"; import { artistCardHtml } from "../components/artist-card.js";
const DECADES=[
{year:1940,label:"1940〜50年代",desc:"戦後の復興とともにラジオ、映画、レコードが流行歌を全国へ届けた。ジャズやラテンなど海外音楽を吸収した歌謡曲が、スター歌手と作家の分業によって磨かれ、後のJ-POPを支える大衆音楽の基盤が生まれた。"},
{year:1960,label:"1960年代",desc:"テレビの普及、青春歌謡、グループ・サウンズとともに、関西フォークが登場。岡林信康、高石ともやらは社会や日常を自分の言葉で歌った。洋楽のコピーから出発した若者たちは日本語で歌う方法を探り、後のシンガーソングライター文化を育てた。"},
{year:1970,label:"1970年代",desc:"吉田拓郎、井上陽水らがフォークを個人の言葉と大衆的なポップスへ広げ、シンガーソングライターの時代が到来。大阪・京都では憂歌団、上田正樹、ウエスト・ロードらがブルースを日本語と生活の音楽へ変えた。ソウルや電子音楽も交差し、シティポップとテクノポップの芽が開いた。"},
{year:1980,label:"1980年代",desc:"アイドル黄金期とバンドブームがテレビを彩り、CDへの移行が音楽産業を拡大した。YMO以後の電子音、BOØWYらのロック、松田聖子らの精緻なポップスが共存し、「J-POP」という呼び名も生まれた。"},
{year:1990,label:"1990年代",desc:"CD市場が頂点へ向かい、ドラマやCMとのタイアップから巨大ヒットが続出。小室サウンド、渋谷系、ヴィジュアル系、R&B、ヒップホップが次々と主流に接続し、J-POPの輪郭が最も大きく広がった。"},
{year:2000,label:"2000年代",desc:"CDから着うた・配信へ聴取環境が変化。ロックフェスとライブハウスから多様なバンドが育つ一方、動画投稿サイトとボーカロイドが、レーベルを経由しない新しい創作と発見の回路を作った。"},
{year:2010,label:"2010年代",desc:"ストリーミングとSNSが定着し、アイドル、バンド、ネット発の制作者が同じチャートで交差。シティポップの世界的再評価も進み、過去の音源と新曲を同時に聴く、世代や国境を越えた環境が整った。"},
{year:2020,label:"2020年代〜",desc:"ショート動画やアニメを通じて一曲が瞬時に世界へ届く時代。ネット文化と高い作家性を両立する表現者が増え、J-POPは国内ジャンルという枠を越えて更新され続けている。"}];
export async function renderTimeline(view){view.innerHTML='<div class="loading">読み込み中…</div>';const{artists}=await loadData();const by=new Map(DECADES.map(d=>[d.year,[]]));artists.forEach(a=>{let dec=decadeOf(a.begin_year);if(dec<1940)dec=1940;if(dec>2020)dec=2020;if(by.has(dec))by.get(dec).push(a);});view.innerHTML=`<section class="hero"><p class="eyebrow">A STORY OF JAPANESE POPULAR MUSIC</p><h1 class="page-title">日本のポップミュージックを<br>時代と音でたどる。</h1><p class="page-lead">歌謡曲からシティポップ、バンドブーム、ネット発の音楽まで。${artists.length}組の入り口からJ-POPの変化を見渡せます。</p></section>${DECADES.map(d=>{const list=by.get(d.year).sort((a,b)=>a.begin_year-b.begin_year||a.name.localeCompare(b.name,"ja"));return `<section class="decade-block"><div class="decade-header"><span class="decade-year">${d.label}</span><span class="chip">${list.length}組</span></div><p class="decade-desc">${d.desc}</p><div class="artist-grid">${list.map(artistCardHtml).join("")}</div></section>`;}).join("")}`;}
