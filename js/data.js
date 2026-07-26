import { LOCALE, ROOT, localeDataFile } from "./i18n.js";
import { S } from "./strings.js";

let cache=null;
export async function loadData(){if(cache)return cache;const [artists,genres,relations]=await Promise.all([fetch(`${ROOT}data/artists.json`).then(r=>r.json()),fetch(`${ROOT}${localeDataFile("data/genres.json")}`).then(r=>r.json()),fetch(`${ROOT}data/relations.json`).then(r=>r.json())]);const tagMap=genres.tag_map||{},categoryById=new Map(genres.categories.map(c=>[c.id,c]));artists.forEach(a=>{const ids=new Set();(a.tags||[]).forEach(t=>(tagMap[t.toLowerCase()]||[]).forEach(id=>ids.add(id)));if(!ids.size)ids.add("other");a.genreIds=[...ids];a.slug=slugify(a.name);});const songs=[];artists.forEach(a=>{const seen=new Set();(a.songs||[]).forEach(title=>{const key=title.toLowerCase();if(!seen.has(key)){seen.add(key);songs.push({title,albumTitle:S.allSongsHeading,year:null,artistName:a.name,artistSlug:a.slug});}});(a.albums||[]).forEach(album=>(album.tracks||[]).forEach(track=>{const key=track.title.toLowerCase();if(!seen.has(key)){seen.add(key);songs.push({...track,albumTitle:album.title,year:album.year,artistName:a.name,artistSlug:a.slug});}}));});return cache={artists,genres,relations,categoryById,songs};}
export const slugify=name=>encodeURIComponent(name.trim().toLowerCase().replace(/\s+/g,"-")); export const findArtistBySlug=(artists,slug)=>artists.find(a=>a.slug===slug); export const decadeOf=year=>year==null?null:Math.floor(year/10)*10;
// ===== お気に入り(localStorage、sync.js経由でデバイス間同期も可能) =====
const FAV_KEY = "j-pop-history:favorites";
const FAV_UPDATED_KEY = "j-pop-history:favorites-updated-at";

export function getFavorites() {
  try {
    return JSON.parse(localStorage.getItem(FAV_KEY) || "[]");
  } catch {
    return [];
  }
}

export function getFavoritesUpdatedAt() {
  return Number(localStorage.getItem(FAV_UPDATED_KEY) || 0);
}

export function isFavorite(mbid) {
  return getFavorites().includes(mbid);
}

export function toggleFavorite(mbid) {
  const favs = new Set(getFavorites());
  if (favs.has(mbid)) favs.delete(mbid);
  else favs.add(mbid);
  const list = [...favs];
  localStorage.setItem(FAV_KEY, JSON.stringify(list));
  localStorage.setItem(FAV_UPDATED_KEY, String(Date.now()));
  notifyFavoritesChanged(false);
  return favs.has(mbid);
}

// sync.jsがサーバーから受け取った内容でローカルを上書きするための関数
export function applyFavoritesFromSync(list, updatedAt) {
  localStorage.setItem(FAV_KEY, JSON.stringify(list));
  localStorage.setItem(FAV_UPDATED_KEY, String(updatedAt));
  notifyFavoritesChanged(true);
}

const favoritesListeners = new Set();

// fromSyncがtrueの場合はサーバーからの反映、falseの場合は端末上での変更
export function onFavoritesChanged(fn) {
  favoritesListeners.add(fn);
  return () => favoritesListeners.delete(fn);
}

function notifyFavoritesChanged(fromSync) {
  const list = getFavorites();
  favoritesListeners.forEach((fn) => fn(list, { fromSync }));
}
export function spotifySearchUrl(q){
  const path=`open.spotify.com/search/${encodeURIComponent(q)}`;
  const web=`https://${path}`;
  const isAndroid=typeof navigator!=="undefined" && /Android/i.test(navigator.userAgent);
  if(!isAndroid)return web;
  return `intent://${path}#Intent;scheme=https;package=com.spotify.music;S.browser_fallback_url=${encodeURIComponent(web)};end`;
}
export const appleMusicSearchUrl=q=>{const storefront=LOCALE==="en"?"us":"jp";return `https://music.apple.com/${storefront}/search?term=${encodeURIComponent(q)}`;}; export const wikipediaUrl=name=>{const domain=LOCALE==="en"?"en.wikipedia.org":"ja.wikipedia.org";return `https://${domain}/wiki/${encodeURIComponent(name)}`;};
