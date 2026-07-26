// artist-detail.js: アーティスト詳細ページ

import { loadData, findArtistBySlug, isFavorite, toggleFavorite, spotifySearchUrl, appleMusicSearchUrl, wikipediaUrl } from "../data.js";
import { escapeHtml } from "../router.js";
import { S } from "../strings.js";

export async function renderArtistDetail(view, slug) {
  view.innerHTML = `<div class="loading">${S.loading}</div>`;
  const { artists, genres, categoryById } = await loadData();
  const artist = findArtistBySlug(artists, slug);

  if (!artist) {
    view.innerHTML = `<div class="empty-state">${S.artistNotFound}<br><a href="#/artists">${S.backToList}</a></div>`;
    return;
  }

  const typeLabel = artist.type === "person" ? S.person : S.group;
  const period = `${artist.begin_year ?? S.yearUnknownShort} ${S.periodSeparator} ${artist.end_year ?? S.present}`;
  const genreLabels = artist.genreIds.map((id) => categoryById.get(id)?.label).filter(Boolean);
  const albums = artist.albums.filter((item) => ["album", "ep"].includes(releaseType(item)));
  const singles = artist.albums.filter((item) => releaseType(item) === "single");
  const selections = artist.albums.filter((item) => releaseType(item) === "selection");

  view.innerHTML = `
    <p><a href="#/artists">${S.backToArtists}</a></p>
    <div class="detail-header">
      <h1>${escapeHtml(artist.name)}</h1>
      <div class="detail-meta">
        <span class="chip">${typeLabel}</span>
        <span class="chip">${period}</span>
        ${artist.area ? `<span class="chip">${escapeHtml(artist.area)}</span>` : ""}
        ${genreLabels.map((g) => `<span class="chip">${escapeHtml(g)}</span>`).join("")}
      </div>
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button class="btn fav ${isFavorite(artist.mbid) ? "is-active" : ""}" id="favBtn">
          ${isFavorite(artist.mbid) ? S.favRemove : S.favAdd}
        </button>
        <a class="btn" href="${wikipediaUrl(artist.name)}" target="_blank" rel="noopener">${S.wikipediaLabel}</a>
        <a class="btn" href="${spotifySearchUrl(artist.name)}">${S.spotifySearch}</a>
        <a class="btn" href="${appleMusicSearchUrl(artist.name)}" target="_blank" rel="noopener">${S.appleMusicSearch}</a>
      </div>
    </div>

    <h2 style="margin-top:28px; font-size:16px;">${S.albumsHeading(albums.length)}</h2>
    <div class="discography">
      ${albums.length ? albums.map((al) => albumRowHtml(artist, al, true)).join("") : `<p class="empty-hint">${S.noAlbums}</p>`}
    </div>
    ${singles.length ? `<h2 class="release-section-title">${S.singlesHeading(singles.length)}</h2><div class="discography">${singles.map((al) => albumRowHtml(artist, al, false)).join("")}</div>` : ""}
    ${selections.length ? `<h2 class="release-section-title">${S.selectionsHeading}</h2><div class="discography">${selections.map((al) => albumRowHtml(artist, al, false)).join("")}</div>` : ""}
    ${allSongsHtml(artist)}
  `;

  view.querySelector("#favBtn").addEventListener("click", (e) => {
    const active = toggleFavorite(artist.mbid);
    e.target.classList.toggle("is-active", active);
    e.target.textContent = active ? S.favRemove : S.favAdd;
  });
  const songInput = view.querySelector("#artistSongSearch");
  if (songInput) songInput.addEventListener("input", () => {
    const q = songInput.value.trim().toLocaleLowerCase("ja");
    view.querySelectorAll(".all-song-item").forEach(li => li.hidden = q && !li.dataset.title.includes(q));
    const visible = [...view.querySelectorAll(".all-song-item")].filter(li => !li.hidden).length;
    view.querySelector("#artistSongCount").textContent = S.allSongsCount(visible);
  });
}

function allSongsHtml(artist) {
  const seen = new Set();
  const titles = [...(artist.songs || []), ...(artist.albums || []).flatMap(a => (a.tracks || []).map(t => t.title))]
    .filter(title => { const key = title.toLocaleLowerCase("ja"); if (seen.has(key)) return false; seen.add(key); return true; });
  if (!titles.length) return `<section class="all-songs"><h2>${S.allSongsHeading}</h2><p class="empty-hint">${S.allSongsEmpty}</p></section>`;
  return `<section class="all-songs"><div class="all-songs-head"><h2>${S.allSongsHeading} <span id="artistSongCount">${S.allSongsCount(titles.length)}</span></h2><input id="artistSongSearch" type="search" placeholder="${S.allSongsSearchPlaceholder}"></div><ol class="all-songs-grid">${titles.map(title => `<li class="all-song-item" data-title="${escapeHtml(title.toLocaleLowerCase("ja"))}"><a href="${spotifySearchUrl(`${artist.name} ${title}`)}">${escapeHtml(title)}</a></li>`).join("")}</ol></section>`;
}

function releaseType(album) {
  if (album.release_type) return album.release_type;
  if (/\s[-–—]\s?single$/i.test(album.title)) return "single";
  if (/\s[-–—]\s?ep$/i.test(album.title)) return "ep";
  if (["主要楽曲セレクション", "代表楽曲"].includes(album.title)) return "selection";
  return "album";
}

function albumRowHtml(artist, album, showTracks) {
  const query = `${artist.name} ${album.title}`;
  const artwork = album.artwork
    ? `<img class="album-artwork" src="${escapeHtml(album.artwork)}" alt="" loading="lazy" onerror="this.replaceWith(Object.assign(document.createElement('div'), {className: 'album-artwork album-artwork-placeholder'}))">`
    : `<div class="album-artwork album-artwork-placeholder"></div>`;
  return `
    <div class="album-row">
      ${artwork}
      <div class="album-info">
        <span class="album-title">${escapeHtml(album.title)}</span>
        <span class="album-year">${album.year ?? S.yearUnknown}</span>
        ${album.personnel
          ? `<div class="personnel" style="margin-top:4px; font-size:0.85em; color:var(--text-dim);">${S.personnelPrefix}${escapeHtml(album.personnel)}</div>`
          : album.lineup
          ? `<div class="personnel" style="margin-top:4px; font-size:0.85em; color:var(--text-dim);">${S.lineupPrefix}${escapeHtml(album.lineup)}</div>`
          : ""}
        ${showTracks ? tracklistHtml(album) : ""}
      </div>
      <div class="album-links">
        <a href="${spotifySearchUrl(query)}">Spotify</a>
        <a href="${appleMusicSearchUrl(query)}" target="_blank" rel="noopener">Apple Music</a>
      </div>
    </div>
  `;
}

function tracklistHtml(album) {
  if (!album.tracks || !album.tracks.length) return "";
  const items = album.tracks
    .map((t) => `<li>${escapeHtml(t.title)}${t.length ? ` <span class="track-length">${escapeHtml(t.length)}</span>` : ""}</li>`)
    .join("");
  return `
    <details class="tracklist">
      <summary>${S.tracklistSummary(album.tracks.length)}</summary>
      <ol>${items}</ol>
    </details>
  `;
}
