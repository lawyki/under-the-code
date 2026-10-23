# Go deeper videos: how to add one cleanly

How to point readers to an outside video without it becoming part of the
book. The component exists (`public/deeper.js`, the "Go deeper" block at the
end of `public/book.css`); adding a video is markup plus checks. The first
one is Veritasium's Enigma video beside `ch1-context-p8` in `part-1.html`.

## What the reader sees

- **Wide screens (1200 px and up):** a quiet note in the right margin beside
  the paragraph. It has a gold "Go deeper" label, a small dark 16:9 picture
  drawn in the figure style, the title in serif and "Creator · 48 min" in mono.
  The text column is untouched.
- **Narrower screens:** a light paper pill ("▶ Go deeper 48 min") at the
  bottom right, shown only while that paragraph is on screen.
- **Click or tap:** a dark viewer like the fullscreen figures (a bottom sheet
  on phones). It holds the play button, the credit, one line on what the
  video shows, the cookie note and "Watch on YouTube". The video plays in the
  viewer, and closing the viewer stops it.
- **No script:** one quiet line under the heading.

The owner approved this look on 2026-10-12 (commit `188a645`). He rejected
the first version, a black tab at the screen edge and a black panel with
eight lines of text in four type styles, as a web widget stuck on a book.
Keep it this calm: never add text to the note, and never put a video into
the text column.

## 1. Check the video

1. **Official upload only.** The creator's own upload on their own channel,
   never a re-upload, mirror, clip channel or compilation:

   ```bash
   curl -s "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json"
   ```

   `author_name` and `author_url` must be the creator's official channel.
2. **Embedding allowed.** The same call answers `401` when the creator has
   switched embedding off. Then the video still gets its note, with
   `data-embed="off"`: the viewer shows only the "Watch on YouTube" link.
3. **Length.** Read it from the watch page and write it as `m:ss` or `h:mm:ss`:

   ```bash
   curl -s -A "Mozilla/5.0" "https://www.youtube.com/watch?v=VIDEO_ID" \
     | grep -o '"lengthSeconds":"[0-9]*"\|"playableInEmbed":[a-z]*\|"ownerChannelName":"[^"]*"' | sort -u
   ```

4. **What it covers.** Take the one-line description only from what the
   video states about itself: its chapter list or description. Never describe
   content you have not seen.
5. **Plain ID.** Use the 11-character id with no start time (`&t=12s` is dropped).

## 2. Add the markup

Put the aside **just before the paragraph it belongs to**. The note lines up
with the top of that paragraph, and the pill shows while that paragraph is on
screen.

```html
    <!-- Go deeper (YYYY-MM-DD): an optional outside video, shown beside the
         text by deeper.js (docs/go-deeper-videos.md). Verified YYYY-MM-DD:
         the creator's own upload on the official channel, embedding allowed. -->
    <aside class="deeper" data-yt="VIDEO_ID" data-art="ART_KEY" data-length="47:41" aria-label="Go deeper: an outside video">
      <div class="deeper-static">
        <span class="deeper-kicker">Go deeper · outside video · 47:41</span>
        <span class="deeper-about">One sentence on what the video shows.</span>
        <span class="deeper-credit">“<a class="deeper-title" href="https://www.youtube.com/watch?v=VIDEO_ID" target="_blank" rel="noopener">Exact Video Title</a>” by <a class="deeper-channel" href="https://www.youtube.com/@channel" target="_blank" rel="noopener">Creator</a></span>
      </div>
    </aside>
```

| Field | What goes in it |
|---|---|
| `data-yt` | The 11-character video id. Required: anything else leaves only the no-script line. |
| `data-length` | `47:41`. The note and pill round it to minutes ("48 min"). |
| `data-art` | Optional picture key (see step 4). Leave it out for a plain dark card. |
| `data-embed="off"` | Only when step 1.2 found embedding switched off. |
| `.deeper-about` | One sentence, from what the video itself states. |
| `.deeper-title` | The exact title as the creator wrote it, linked to the watch URL. |
| `.deeper-channel` | The creator's name, linked to their channel. |

The aside is the single source of the data: the script reads everything from
it. Inside the aside:

- **No `<p>` or `<li>`.** They count as section prose (`scripts/count-prose.mjs`).
- **No `<strong>` or `<em>`.** The glossary tooltips attach to those.
- **No ids** in the markup. `ch…` and `fig-…` ids would join the reading
  anchors (anchor law). Ids the script adds at runtime must start with `utc-`
  (the invariants test checks this).
- **No em dashes** (law 1). Use curly quotes around the title, as above.

## 3. Load the script on that page

Only pages with a video load `deeper.js` (today only `part-1.html`). On a new
page, add this line directly after the `book.js` script tag, with the same
`?v=` value `part-1.html` uses:

```html
<script src="deeper.js?v=20261015"></script>
```

## 4. Optional: a picture (`data-art`)

Never use the video's thumbnail: loading it from `i.ytimg.com` would contact
Google before the reader chooses to, and the thumbnail is the creator's
artwork. Draw a small picture instead, in the `art(kind)` function in
`deeper.js`:

- Add one branch for the new key, next to `enigma`.
- `viewBox 0 0 320 180`, line art in the figure style. Use the same colours
  as `enigma`: lines `rgba(236,230,218,0.42)`, faint `rgba(236,230,218,0.16)`,
  gold `#d4a853`.
- No text and no ids. Few shapes: it is shown 216 px wide in the note.
- At most one part moves on hover (as the first rotor steps on the Enigma
  card), and only if that motion is the mechanism. Reduced motion is already
  handled in the CSS.

## 5. If you change `deeper.js` or `book.css`

Browsers keep both files for 4 hours, so a change is invisible until the URL
changes. Bump the `?v=` value on every page that loads the file:
`book.css?v=…` on all five parts, `deeper.js?v=…` on every page with a
video. Without the bump the owner sees the old version (this happened once,
on 2026-10-12).

## 6. Check before it ships

```bash
npm run check:dashes                                     # law 1
node scripts/count-prose.mjs --part=part-N               # same numbers as:
node scripts/count-prose.mjs --part=part-N --rev=HEAD
npm run build:glossary && git diff --stat public/glossary.json   # only the "generated" stamp may change
cd tests/pass25 && ./run-all.sh                          # invariants know the note and pill as tab stops
```

Check that the reading anchors are byte-identical to HEAD:

```bash
node -e "
const fs=require('fs'),{execFileSync}=require('child_process'),P='public/part-N.html';
const ids=s=>[...s.matchAll(/\sid=\"([^\"]+)\"/g)].map(m=>m[1]).filter(i=>/^(ch[0-9B][^ ]*|fig-[0-9]+-[0-9]+[a-z]?)$/.test(i));
console.log(JSON.stringify(ids(execFileSync('git',['show','HEAD:'+P],{encoding:'utf8',maxBuffer:1<<26})))===JSON.stringify(ids(fs.readFileSync(P,'utf8'))));"
```

Then look at it in a browser (`tests/pass25/serve.mjs` serves `public/` on
:8123), at 1440 px and at 375 px:

- [ ] The note sits in the margin beside the paragraph and covers no text. On
      the phone, the pill appears at that paragraph and leaves after it.
- [ ] **Before play, the page has made zero requests** to `youtube`, `ytimg`,
      `google`, `gstatic` or `ggpht` hosts (record the requests with Playwright).
- [ ] After play, the player's `src` is
      `https://www.youtube-nocookie.com/embed/VIDEO_ID?autoplay=1&rel=0`.
- [ ] The credit, the cookie note and "Watch on YouTube" show. Closing the
      viewer stops the video.
- [ ] No console errors from the book. Errors from inside YouTube's player
      (its own stats calls) are not ours.

Pushing `main` deploys the site, so push only on the owner's word.

## Already in place: do not redo

- **Privacy:** the notice at `/account#privacy` has a paragraph covering
  every embed (nothing loads before play; then YouTube's privacy-enhanced
  mode, run by Google, and what Google receives from then on). Its wording
  says "Passages can offer", so a new video needs no change there.
- **Licence:** `README.md` and `LICENSE` say that embedded and linked
  third-party videos belong to their creators and are not covered by
  CC BY-NC 4.0.
- **CSP:** the pages set none. If one is ever added, it must include
  `frame-src https://www.youtube-nocookie.com`.

## Never

- Never embed a re-upload or mirror, and never download, re-host, crop or
  edit a video, its thumbnail or its audio.
- Never let anything contact Google before the click: no thumbnail, no
  iframe, no preconnect, no loading on hover.
- Never imply the creator endorses or works with the book. Introduce every
  video as an outside resource.
- Never let a video carry something the book needs: the reader must
  understand everything without leaving the page.
