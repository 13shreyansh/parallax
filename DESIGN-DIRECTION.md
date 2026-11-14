# Parallax: exact screen spec (Fable for Claude, Sat 14 Nov 2026)

For Codex. Build exactly this. Read `/mnt/project-files/Junction/plan/DESIGN-FLOOR.md` as the floor under it. This file supersedes the screen details in `mariadb-design.md` and keeps its product decisions. Where this file and your habit disagree, this file wins. Where a value is missing, ask, do not invent.

Mode: Operate (a review tool an editor works in for an hour). The Method page is Read. Colour strategy: Restrained.

**Placeholder convention.** Every figure, date, quote, title and id written inside `‹ ›` is an example of shape only. It must be replaced by the real value from MariaDB. Nothing inside `‹ ›` may be hard-coded. There is no demo mode, no seeded story and no fake number anywhere.

---

## 0. The product in one line

Parallax is a review desk for Wikipedia editors: for one theme it reads the Finnish, Swedish and English articles claim by claim, checks each claim against the source it cites and against the other languages, shows the exact words that disagree, and hands the editor a ready note for the Talk page. It never edits Wikipedia.

Who: an editor who knows Finnish history, at a desk, on a laptop or monitor, with Wikipedia open in the next tab. Job: "show me where to look first, prove it with quotes, and let me act in one click."

---

## 1. Direction contract

**Thesis.** An editor trusts quotes, not scores. So Parallax never says "this is wrong" in its own voice without putting the two sets of exact words next to each other. The interface is quiet so that the only loud thing on any screen is a few marked words.

**The world.** A proofreader's desk, not a dashboard. White reading surface, cool grey chrome, blue-black ink. Wikipedia's words are set in a serif, Parallax's own words in a sans, so the editor always knows who is speaking. Four small marks (one per check) are the only colour. It should sit next to Wikipedia's own tools (Content Translation, Edit check) and look like it belongs with them, without copying Wikipedia's logo, globe or skin.

**Signature element: the Readings block.** One claim, one row per version (each language, and the cited source), each row holding that version's exact words with a link to where they came from. The words that disagree are marked in the colour of the check, the same way in every row. The same block appears in the article rail, in the home example, in the search answer and in the Method page. In the article columns the same words carry a 2px underline in the same colour. Marked words are the brand.

**What we borrow, by name.**
- Wikipedia Content Translation: language versions as parallel columns, aligned unit by unit, with a dashed placeholder where one side has nothing.
- Grammarly: a coloured underline on the exact words, and one card beside the text for the selected issue. One issue at a time.
- GitHub split diff and Mintlify's diff view (Mobbin): word-level tint inside a quiet row, never a whole red block.
- Plane "Compare versions" and Snowflake "Version history" (Mobbin): history as a control beside the content that re-renders the same layout, not a separate page.
- Linear triage: J / K to move through items, a count "3 of 14", accept or dismiss without leaving the list.
- incident.io alerts table (Mobbin): the home list is a plain table with text columns. No cards.
- Plane's query block above results (Mobbin): the real query shown as a first-class object. This is the "Show the SQL" drawer.
- Wayback Machine: when you look at the past, the whole bar changes colour so you cannot forget it.

**Risk taken.** The primary button is ink black, not blue, and the page has almost no colour. On video that can read as plain. The counterweight is that the marked words and the time bar get all the colour and all the motion, and every wow moment is a pair of quotes that visibly disagree. The second risk is three narrow serif columns (about 40 characters a line): accepted, because aligned sentences are short and the rail repeats the selected one at a comfortable width.

**Never.** No scores without quotes. No "AI", no sparkles, no confidence percentages, no chat. On screen the words are "Checked" and "Double-checked".

---

## 2. Tokens

### 2.1 Fonts (self-hosted, never fall back visibly)

| Role | Face | Package | Why |
|---|---|---|---|
| Interface (Parallax speaking) | **Commissioner** variable, 400 to 700 | `@fontsource-variable/commissioner` | Plain low-contrast humanist sans with full Latin, Cyrillic and Greek (ä, ö, å, ß, Russian). Not on the banned list. |
| Quoted text (Wikipedia and sources speaking) | **Source Serif 4** variable, 400 and 600, roman only | `@fontsource-variable/source-serif-4` | Reads as encyclopedia text, has Cyrillic. Used only for quotes and article sentences. Never italic, never as a heading, never in buttons. |
| SQL only | **JetBrains Mono** variable, 400 | `@fontsource-variable/jetbrains-mono` | Code. Used in the SQL drawer and nowhere else. |

`font-family: "Commissioner Variable", system-ui, sans-serif`. Load the Latin, Latin-ext and Cyrillic subsets of the first two. `font-display: swap` is not allowed on first paint of the top bar and H1: preload the Latin subset of Commissioner.

All numbers (counts, distances, dates, revision ids): `font-variant-numeric: tabular-nums lining-nums`. Check in the browser that Commissioner's tabular figures hold their width in the home table. If they do not, fix the column widths and right-align, do not swap the font.

### 2.2 Type scale (fixed px, no fluid type)

| Token | Size / line | Weight | Face | Used for |
|---|---|---|---|---|
| `t-page` | 28 / 36 | 600 | sans | page H1, article title |
| `t-title` | 20 / 28 | 600 | sans | the finding sentence in the rail, answer sentence in search, Method section headings |
| `t-head` | 16 / 24 | 600 | sans | table and panel headings, values in Readings rows |
| `t-body` | 15 / 24 | 400 | sans | body copy, buttons (600), table cells |
| `t-small` | 13 / 20 | 400 | sans | secondary lines, glosses, meta lines, chips (500) |
| `t-micro` | 12 / 16 | 500 | sans | table column heads, language codes, year labels |
| `q-body` | 16 / 26 | 400 | serif | article sentences in the columns |
| `q-small` | 15 / 24 | 400 | serif | quotes in Readings rows, note preview |
| `code` | 13 / 20 | 400 | mono | SQL |

Letter-spacing `-0.01em` on `t-page` and `t-title`, `0` elsewhere. Sentence case everywhere. No uppercase labels. No label above a heading. Headings `text-wrap: balance`, paragraphs `text-wrap: pretty`. Prose measure max 68ch.

### 2.3 Colour (every colour, with its job)

| Token | Hex | Job |
|---|---|---|
| `surface` | `#FFFFFF` | page background, reading columns, Readings block, top bar |
| `ground` | `#F5F6F8` | the rail, the SQL drawer, table head row, toolbars |
| `sunk` | `#ECEEF2` | input fields, slider track, distance-bar track, skeletons |
| `line` | `#D9DCE3` | 1px borders of panels and inputs |
| `line-soft` | `#E7E9EE` | row and column dividers |
| `ink` | `#15181E` | text, icons, **the primary button**, slider thumb, past-mode bar |
| `ink-2` | `#4A505C` | secondary text |
| `ink-3` | `#5F6878` | tertiary text, placeholders, glosses (4.5:1 or better on `surface` and `ground`) |
| `blue` | `#2450C4` | links, focus ring, selected chip and tab text, current-row state |
| `blue-hover` | `#1B3E9C` | link hover |
| `blue-tint` | `#EEF3FD` | selected row ground, selected chip ground, text selection |
| `src` | `#B42318` | Source check: marker, underline, label text |
| `src-tint` | `#FDE7E3` | Source check: marked words |
| `lang` | `#8A5A00` | Languages check: marker, underline, label text |
| `lang-tint` | `#FBEFC9` | Languages check: marked words |
| `tone` | `#6E3FC0` | Tone check: marker, underline, label text |
| `tone-tint` | `#EEE6FB` | Tone check: marked words |
| `fact` | `#0A6E69` | Wrong fact check: marker, underline, label text |
| `fact-tint` | `#D9F0EE` | Wrong fact check: marked words |
| `ok` | `#1F7A4D` | "Supported", "Copied", "Double-checked" tick only |
| `ok-tint` | `#E3F3EA` | ground of the copied confirmation |
| `err` | `#B42318` | system errors (same red, used with an icon and words, never alone) |
| `on-ink` | `#FFFFFF` | text on `ink` |
| `on-ink-2` | `#B9BFCC` | secondary text on `ink` |

Rules. Check colours appear only as: the 10px marker, the 2px underline, the tint behind marked words, and the check name in text. Never as a button, a card ground, a border or a side stripe. Text on a tint is always `ink`. Blue is for links, focus and selection only. Light theme only (reason: long reading of quoted prose at a desk; Wikipedia beside it is white). No gradients.

Browser surfaces: `::selection { background:#D5E0FA; color:#15181E }`, `caret-color:#2450C4`, `:focus-visible { outline:2px solid #2450C4; outline-offset:2px }` on every focusable element, link underline offset 3px, `scrollbar-color:#C4C8D1 transparent; scrollbar-width:thin` on the rail, the SQL drawer and the page.

### 2.4 Spacing, radii, elevation

- Spacing steps: 4, 8, 12, 16, 24, 32, 48. Page side padding 24 (16 under 700px).
- Radii: 3 (marked words), 6 (buttons, inputs, chips, segmented controls), 8 (Readings block, panels, dropdowns), 12 (mobile sheet top corners).
- Elevation: everything is flat with 1px lines. Only floating things cast a shadow: dropdowns and the five-language rail overlay `0 8px 24px rgba(21,24,30,.12), 0 1px 2px rgba(21,24,30,.08)`; the SQL drawer `0 -8px 24px rgba(21,24,30,.10)`; the mobile sheet `0 -8px 32px rgba(21,24,30,.16)`.
- Hit targets at least 32 x 32 on desktop, 44 x 44 under 700px.

### 2.5 The four check markers (authored SVG, 10 x 10, filled, one per check)

| Check | Name on screen | Shape | Colour |
|---|---|---|---|
| 1 | Source | circle | `src` |
| 2 | Languages | diamond (square rotated 45°) | `lang` |
| 3 | Tone | triangle, point up | `tone` |
| 4 | Wrong fact | square | `fact` |

Shape and colour always travel together, and the name is always within reach (in the toolbar chips, the rail header, or a tooltip). A flag marked "Not an issue" shows the same shape as a 1.5px `ink-3` outline with no fill. Do not use unicode glyphs for these.

Verdict words (the only ones allowed):

| Check | Flag verdicts | Non-flag results |
|---|---|---|
| Source | "Contradicted", "Not in source" | "Supported", "Source unreachable" |
| Languages | "Versions differ", "Missing in ‹Swedish›" | "Versions agree" |
| Tone | "Loaded wording" | none |
| Wrong fact | "Numbers differ", "Dates differ", "Names differ" | none |

### 2.6 Controls (one vocabulary)

- **Primary button:** height 40, radius 6, `ink` ground, `on-ink` `t-body` 600, padding 0 16. Hover `#2A2F3A`. Pressed `#000000`. Disabled `sunk` ground, `ink-3` text. Loading: label stays, a 14px ring spinner left of it. **At most one on any screen.**
- **Quiet button:** height 32 (40 when it sits beside a primary), `surface` ground, 1px `line`, `ink` `t-small` 500, padding 0 12. Hover: border `ink-3`. Pressed `ground`.
- **Text button:** `blue` `t-small` 500, no ground, underline on hover, 32 high hit area.
- **Link:** `blue`, underlined only on hover inside UI, always underlined inside prose. External links to Wikipedia or a source end with a 12px Lucide `arrow-up-right`.
- **Segmented control:** height 32, 1px `line`, radius 6, segments divided by 1px `line`. Selected segment: `blue-tint` ground, `blue` text 600. Others `ink-2`.
- **Check chip (toggle filter):** height 28, radius 6, 1px `line`, padding 0 10: marker, name `t-small` 500, count in `ink-3` tabular. On: `surface`, text `ink`. Off: `ground`, marker and text `ink-3`, name struck through is not used, the grey is enough. `aria-pressed`.
- **Text field:** height 36, radius 6, `sunk` ground, no border, `t-body`. Focus: `surface` ground, 1px `blue` border plus the focus ring.
- **Tooltip:** `ink` ground, `on-ink` `t-small`, radius 6, padding 6 8, appears after 400ms hover or on focus.
- **Language tag:** `t-micro` 600 `ink-2`, lower case code in a 24 x 18 box, radius 3, `ground` ground: `fi`, `sv`, `en`, `de`, `ru`.
- **Marked words** (`<mark data-check>`): in article columns, `text-decoration: underline 2px` in the check colour, offset 4px, no ground. Hover: check tint at 50%. When its flag is selected, and always inside a Readings block: check tint ground, `ink` text, padding 1px 2px, radius 3, `box-decoration-break: clone`, underline kept. Dismissed flag: 1px dotted `ink-3` underline, no tint.

### 2.7 Icons

Lucide, stroke 1.5, 16px (14px inside chips and meta lines). Used: `search`, `arrow-up-right`, `chevron-up`, `chevron-down`, `chevron-left`, `chevron-right`, `x`, `check`, `copy`, `history`, `database`, `link`, `undo-2`, `triangle-alert`, `circle-slash`, `languages`. Not allowed: `sparkles`, `wand`, `bot`, `brain`, `zap`, `shield`. No emoji.

**Parallax mark:** authored SVG 20 x 20. Two identical rounded bars 12 x 3 (radius 1.5). The first at x=2, y=5 in `ink`. The second at x=6, y=12 in `blue`. One object, seen from two places, 4px apart. Beside it "Parallax" in Commissioner 600, 17px, `ink`. Also used as the favicon. No Wikipedia globe, puzzle piece or "W" anywhere.

### 2.8 Motion

| Token | Value | Used for |
|---|---|---|
| `ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | everything |
| `d-press` | 120ms | pressed states, chip toggles |
| `d-state` | 180ms | row selection, rail content swap (cross-fade), cells changing |
| `d-panel` | 260ms | SQL drawer, mobile sheet, extra columns sliding in |
| `d-travel` | 900ms | the time bar thumb gliding to a date (the one authored moment) |
| `d-arrive` | 700ms | the tint flash on a sentence that has just entered the article |

No page-load choreography, no entrance animation on rows. Dragging the time thumb has no easing: it follows the pointer. With `prefers-reduced-motion: reduce` every animation is an instant state change and the thumb jumps.

---

## 3. Shared shell

### 3.1 Top bar (every page, 56 high, `surface`, 1px `line-soft` bottom border, sticky, z above everything but drawers)

- Left, x=24: the Parallax mark and wordmark. Link to `/`.
- Centre (absolutely centred in the bar): the Ask field, 480 wide, 36 high. Left inside: `search` icon `ink-3`. Placeholder `ink-3`: **"Ask in any language"**. Right inside: a `t-micro` `ink-3` key hint "/" in a 20 x 20 box with 1px `line` (hidden while focused). "/" focuses the field from anywhere. Enter goes to `/ask?q=…`. No button in the field.
- Right, x=24 from the edge: text link **"Method"** (`ink`, 500, underline on hover, `blue` with a 2px `blue` underline offset 6 when on `/method`).
- Nothing else. No theme switch, no login, no language switch (interface is English only).

**Ask field on focus, while empty:** a dropdown under the field, 480 wide, radius 8, shadow, padding 8. One `t-small` `ink-3` line "Ask about anything in these articles. Finnish, Swedish, English, German or Russian." then up to three example questions as rows (36 high, `t-body`, language tag at left). Examples come from a config list `askExamples`. **Each example is shown only if a nightly check confirms it returns an answer with at least two versions.** Ship with these three if they pass, otherwise replace with ones that do: `en` "How many Soviet soldiers died in the Winter War?", `fi` "Kuinka monta ruotsalaista vapaaehtoista taisteli talvisodassa?", `sv` "När slutade vinterkriget?". Arrow keys move, Enter picks, Esc closes.

### 3.2 Routes (all state lives in the URL, so every screen can be reopened exactly)

| Route | Screen |
|---|---|
| `/?theme=<slug>&sort=distance\|issues` | Home |
| `/a/<wikidata id>?flag=<id>&asof=YYYY-MM-DD&langs=5&show=all&checks=src,lang,tone,fact&sql=1` | Article |
| `/ask?q=<text>` | Ask |
| `/method` | Method |

### 3.3 Page footer (Home, Ask, Method; not on Article)

One line, `t-small` `ink-3`, 24 above the bottom, left aligned to the content: "Text from Wikipedia, CC BY-SA 4.0. Parallax is not part of the Wikimedia Foundation. It never edits Wikipedia."

---

## 4. Screen 1: Home `/`

Purpose: a judge with no context understands the product in 5 seconds, an editor sees where to start. The table is the one main element.

**Frame at 1440 x 900.** Content box 1392 wide (24 side padding). Two columns under the top bar: left 944, gap 48, right 400. Everything below fits in 900 high without scrolling when there are 10 rows.

### 4.1 Left column, top to bottom

1. 32 below the top bar. H1 `t-page`: **"The 10 articles that most need an expert"**
2. 8 gap. One paragraph, `t-body` `ink-2`, max 68ch (three lines at this width):
   "Parallax reads the Finnish, Swedish and English Wikipedia articles on one theme, claim by claim. It checks each claim against the source it cites and against the other two languages, and lists where an editor should look first. It never edits Wikipedia."
3. 24 gap. Controls row, 36 high:
   - Left: theme menu, a quiet button 36 high: "Theme: **‹Finland in the Second World War›**" with `chevron-down`. Opens a dropdown of the real themes in the database, each row: name, and `ink-3` "‹24› articles". Default theme: Finland in the Second World War. **If the database holds one theme, render it as plain text "Theme: Finland in the Second World War" with no chevron and no button.**
   - 16 gap. Segmented control with the label "Sort by" (`t-small` `ink-2`) left of it: **"Language distance"** (default) | **"Number of issues"**.
   - Right end: the primary button **"Open the top article"**. It opens row 1 of the current sort.
4. 12 gap. The table. No card around it. Head row 36 high on `ground`, `t-micro` `ink-2`, 1px `line-soft` under it. Body rows 52 high, 1px `line-soft` between rows, no zebra.

| Column | Width | Align | Content |
|---|---|---|---|
| (rank) | 40 | right | "1" to "10", `t-body` `ink-3`, tabular |
| Article | flex (about 330) | left | English title `t-body` 600 `ink`. Under it `t-micro` `ink-3`: "‹Talvisota› · ‹Vinterkriget›". Both lines truncate with an ellipsis. |
| Language distance | 170 | left | The number 0 to 100 (`t-body` 600, tabular, 28 wide, right aligned) then 12 gap then a bar 96 x 4, radius 2, track `sunk`, fill `ink`. |
| Issues | 64 | right | Total open flags, `t-body` 600 tabular. |
| Source | 56 | right | Head: the circle marker and "Source". Cell: count, `t-body` tabular, `ink`. A zero is `ink-3` "0". |
| Languages | 56 | right | same, diamond |
| Tone | 56 | right | same, triangle |
| Wrong fact | 56 | right | same, square (head label wraps to "Wrong fact" on one line at `t-micro`; if it does not fit, the head shows the marker and "Fact") |
| Last changed | 116 | right | "‹3 Nov 2026›" `t-small` `ink-2`: the newest stored revision across the three languages |

   - The head of the column that drives the sort is `ink` 600 with a 12px `chevron-down`. Clicking "Language distance" or "Issues" in the head does the same as the segmented control.
   - Head tooltips: Language distance: "How much of the meaning the three versions do not share. 0 is the same story, 100 is three different stories." Issues: "Open flags that passed the second check."
   - The whole row is one link (`<a>` stretched over the row). Hover: `ground` row. Focus ring on the row. Pressed: `blue-tint`.
   - Changing sort or theme reorders in place with no animation. The URL updates.
5. 16 gap. One line, `t-small` `ink-3`, split left and right:
   - Left: "Distance is how much meaning the three versions do not share. " then the link "How it is measured".
   - Right (tabular): "‹184› articles · ‹41,220› claims · ‹9,870› sources read · ‹612,400› revisions". Live from MariaDB on every load.

### 4.2 Right column: one real finding (starts level with the H1)

This is what makes the first screen explain itself: a real pair of quotes that disagree.

- `t-head`: "What a finding looks like"
- 12 gap. A Readings block (section 5.4) with two rows, from one real flag.
- 12 gap. The flag's stored summary sentence, `t-body` `ink`. Example of shape: "‹The English article says 25,904 Finnish soldiers died. The source it cites says 22,830.›"
- 8 gap. `t-small` `ink-2`: the marker, the check name and verdict, then " · Double-checked". Example: "Source: contradicted · Double-checked".
- 12 gap. Text button: "Open this claim in ‹Winter War›" with `chevron-right`. Goes to `/a/<id>?flag=<id>`.

**Which flag is shown (a rule, not a choice):** within the current theme, among open double-checked flags whose source text was read, where every quote is 220 characters or shorter: take Source "Contradicted" first, then Wrong fact, then Languages. Within that, the article with the highest rank in the table, then the earliest claim in the article. If no flag qualifies, the right column is not rendered and the left column is centred at 1120 max.

### 4.3 States

- **Loading:** head row real, 10 skeleton rows (52 high: a `sunk` bar 60% wide in the Article column, short bars in the number columns, opacity pulse 1.2s). Right column: three `sunk` blocks. The H1, paragraph and controls are static text and render at once.
- **Fewer than 10 articles in a theme:** the H1 becomes "The ‹7› articles in this theme, ranked" and the table shows what exists.
- **Theme has no open flags:** table still shows by distance. Issues columns show "0". Right column not rendered.
- **Database unreachable:** in place of the table, left aligned, 48 above: `triangle-alert` 20px `err`, `t-head` "The database did not answer.", `t-body` `ink-2` "Nothing is shown from memory. Try again in a moment.", quiet button "Try again". The footer counts show "counts unavailable".

---

## 5. Screen 2: Article `/a/<wikidata id>`

Purpose: read the three versions side by side, see the marked words, act on one flag at a time.

### 5.1 Frame at 1440 x 900

From the top: top bar 56 (sticky). Article header 88 (scrolls away). Time bar 48 (sticky at top 56, full width). Below it two regions side by side:
- **Left, 1008 wide** (24 left padding, 16 right padding, 968 of content): toolbar 44 (sticky at 104), column heads 32 (sticky at 148), then claim rows. Content grid: gutter 40, then three columns of equal width (about 309 each).
- **Right, 432 wide: the rail** (`ground`, 1px `line-soft` left border, sticky at top 104, height `calc(100vh - 104px)`, its own scroll, actions pinned to its bottom).

The page scrolls. The rail does not move.

### 5.2 Article header (88 high, padding 20 24 16)

- Line 1: English title, `t-page`. Right end of the same line, `t-small`: "On Wikipedia:" then three external links "Finnish", "Swedish", "English" (each to the exact stored revision, `oldid=`), 16 apart.
- Line 2, 4 below, `t-small` `ink-2`: "‹Talvisota› · ‹Vinterkriget› · Language distance ‹62› · ‹14› open issues · in " then the link "‹Finland in the Second World War›" (back to Home with that theme).

### 5.3 Time bar (48 high, full width, 1px `line-soft` bottom border)

**Present state** (`surface`):
- Left at x=24: `history` icon, `t-small` `ink-2` "As of", then a quiet button with the date "‹14 Nov 2026›" (opens the native date picker, limited to the stored range).
- Middle, flex, 24 side margins: the track. 4 high, radius 2, `sunk`. It spans from the date of the earliest stored revision of this article to today, linear in time. Under the track, `t-micro` `ink-3` year labels at each 1 January (if the range is over 12 years, every second year). Above the track at y=-10: one check marker (8px) at the date each currently visible flag entered the article. Markers may overlap. The selected flag's marker is 10px with a 2px `surface` ring and a `t-micro` `ink` label above it: "entered ‹14 Mar 2019›". Thumb: 16px circle, `ink`, 2px `surface` ring, hit area 32. At "today" the thumb sits at the right end.
- Right: two 32 x 32 icon buttons `chevron-left` / `chevron-right` with tooltips "Previous change to this claim" / "Next change to this claim" (they jump the date to the previous or next stored revision in which the selected claim's text changed in any language; with no claim selected, the previous or next revision of the article). Then `t-small` `ink-3` tabular: "‹3,204› revisions stored".

**Past state** (any date before today): the whole bar turns `ink`. Text `on-ink`, secondary `on-ink-2`, track `#3A404D`, thumb `surface` with a 2px `ink` ring, markers keep their colours. The left group reads: "As of **‹13 Mar 2019›**" and a text button in `on-ink` underlined: "Back to today". The bar change is instant (no fade), so it reads as a mode.

**Behaviour.**
- Drag: the date button text follows the pointer live (day resolution). The columns re-query 150ms after the pointer stops moving or on release (`FOR SYSTEM_TIME AS OF`). While a query is pending for more than 250ms the row text drops to 60% opacity, no spinner. Result arrives: text swaps with a `d-state` cross-fade.
- Keyboard on the thumb: Left / Right one day, Shift+arrow 30 days, Page Up / Down one year, Home earliest, End today. `role="slider"` with `aria-valuetext` "13 March 2019".
- In the past, each cell shows that language's text of the same claim as it was on that date. If the claim did not exist yet in a language: the dashed cell "Not in the ‹English› article on ‹13 Mar 2019›". Marked words are drawn only for flags whose claim text already existed in its flagged form. Rows where no language had the claim yet are hidden, and the toolbar count updates ("‹9› of ‹14› flagged claims existed").
- **Glide (the authored moment):** when the date is set by a button ("Show the day before it entered", the chevrons, a date in the rail's history list, "Back to today"), the thumb travels in `d-travel` with `ease-out`, the date text counts through the days with it, and the columns swap once at the end. If the swap makes a sentence appear in a cell that was empty (stepping forward onto the day a claim entered), that sentence's ground flashes the check tint and fades to none in `d-arrive`.

### 5.4 The Readings block (the signature component, used on four screens)

A `surface` panel, 1px `line`, radius 8. One row per version, rows divided by 1px `line-soft`. Order: fi, sv, en, (de, ru on Winter War), then the cited source last when the check is Source.

Each row, padding 12 16:
- **Meta line** (`t-small`, 20 high): the language tag, then `ink-2` "‹English› Wikipedia", then an external link "revision ‹1254417890›" (`oldid` permalink). For a source row: no tag, a 14px `link` icon, `ink-2` "Cited source", then the external link with the source's domain "‹mannerheim.fi›", and if the text came from the Internet Archive, `ink-3` " · archived copy". Right end of the meta line, when the check has an extractable value (number, date, name): the value in `t-head` tabular, on the check tint with padding 0 6 and radius 3 if it differs from another row, plain `ink` if it agrees with all rows.
- 4 gap. **The quote**, `q-small`, with the disagreeing words as marked words in the check colour. Whole sentence, never truncated mid-sentence. If the sentence is over 320 characters, show the clause around the marked words with "…" at the cut ends and a text button "Whole sentence".
- For rows not in English: 4 gap, the English gloss in `t-small` `ink-3` (sans, so it is clearly Parallax speaking, not Wikipedia).
- For a language row whose own citation was read: 4 gap, `t-small`: `check` 14px `ok` "Supported by its source" or `circle-slash` 14px `src` "Not in its source" or `ink-3` "Its source could not be read". This is how the editor sees which language is better sourced.
- A version that lacks the claim: the row holds only the meta line and `t-small` `ink-3` "Not in the ‹Swedish› article." No quote.

### 5.5 Toolbar (44 high, `surface`, 1px `line-soft` bottom border, padding 0 16 0 24)

Left to right:
1. Segmented control: **"Flagged claims ‹14›"** (default) | **"All claims ‹212›"**.
2. 16 gap. The four check chips with counts: Source ‹6›, Languages ‹4›, Tone ‹3›, Wrong fact ‹1›. All on by default. They filter rows and also serve as the legend for the markers. A chip with count 0 is disabled (`ink-3`, not clickable).
3. Right end: quiet button **"+2 languages"** (only on an article that has German and Russian stored; today that is Winter War; otherwise not rendered). Tooltip "Add German and Russian". When on, the label is "5 languages" with a `check` icon and `blue-tint` ground.
4. 8 gap. Quiet button with `database` icon: **"Show the SQL"**. When the drawer is open the label is "Hide the SQL".

### 5.6 Column heads (32 high, `ground`, 1px `line-soft` bottom border)

Gutter cell empty. Each column head, padding 0 16: language tag, `t-small` 600 `ink` "Finnish", then right aligned an external link `t-small` "rev ‹2334455›". In the past state the link shows the revision that was current on that date.

### 5.7 Claim rows

One row is one claim, aligned across languages by vector distance. Row order follows the English article. A claim missing from English sits after its nearest aligned neighbour. Rows are grouped under **section rows**: 32 high, `surface`, padding 0 16 0 64 (aligned with the first column's text), `t-small` 600 `ink-2`, the English article's section heading, for example "‹Soviet invasion›". A section with no visible rows is not shown.

Row anatomy:
- **Gutter (40 wide):** the row's flag markers stacked vertically, 6 apart, starting level with the first text line (top padding 20). Each marker sits in a 24 x 24 button. Tooltip: "Source: contradicted". Clicking a marker selects that flag. This gutter replaces the coloured left rule: the mark is a small shape in a margin column, never a border.
- **Three cells**, padding 14 16, divided by 1px `line-soft` vertical lines. In a cell: the sentence in `q-body` `ink`, with marked words underlined in the check colour (2.6). For `fi` and `sv` (and `de`, `ru`): 6 below, the English gloss in `t-small` `ink-3`. No marks in the gloss.
- **Missing cell:** inside the cell padding, a box with 1px dashed `line`, radius 6, padding 10 12, `t-small` `ink-3`: "Not in the ‹Swedish› article". Top aligned.
- Rows are divided by 1px `line-soft`. No zebra.

Row states:
- Hover: `#FAFBFC` ground, pointer cursor. Clicking anywhere in a row selects its first flag (or the claim itself if it has none).
- **Selected:** `blue-tint` ground on the whole row including the gutter. The selected flag's marked words switch from underline to tint. Its gutter marker gets a 2px `blue` ring at 3px offset. The row scrolls into view with 96 of margin if needed.
- Dismissed flag ("Not an issue"): hollow marker, dotted underline. If all flags of a row are dismissed the row stays visible in "Flagged claims" until reload, then moves to "All claims" only.
- Unflagged row (only in "All claims"): empty gutter.

**On load:** the first open flag in row order is selected, unless `?flag=` names one. The rail is never empty on a page that has flags.

**Citations that could not be read** never appear as flags. They are collected in one collapsed row at the very end of the list: `t-small` `ink-2`, `chevron-right`, "‹9› cited sources could not be read (paywall, dead link or book)". Expanding lists them as plain rows: language tag, the claim's first 80 characters, the source link, the reason. No marker, no rail action. This keeps the review path, and the video, on claims whose source text we actually hold.

### 5.8 The rail (432 wide, `ground`, padding 16 16 0)

Top to bottom for a selected flag:

1. **Header row, 32 high.** Left: the marker, then `t-head` in the check colour: the check name, then `t-head` `ink`: the verdict. Example: "Source" "Contradicted". Right: `t-small` `ink-2` tabular "‹3› of ‹14›" and two 32 x 32 icon buttons `chevron-up` / `chevron-down` (previous / next flag in row order; keys K / J).
   - If the claim has more than one flag: under the header a row of tabs (segmented control, full width), one per flag: marker and check name. The selected tab is the selected flag.
2. 12 gap. **The finding sentence**, `t-title` `ink`: the flag's stored `summary`. One or two plain sentences, at most 160 characters, written at pre-compute time to one of these patterns and never generated in the browser:
   - Source, contradicted: "The ‹English› article says ‹25,904 Finnish soldiers died›. The source it cites says ‹22,830›."
   - Source, not in source: "The ‹English› article cites ‹Trotter 1991› for this. The source does not mention it."
   - Languages, differ: "The ‹Swedish› article describes this differently from the ‹Finnish› and ‹English› articles."
   - Languages, missing: "The ‹Finnish› and ‹English› articles say this. The ‹Swedish› article does not."
   - Tone: "The ‹English› article uses loaded wording here: ‹"single-handedly"›."
   - Wrong fact: "The three articles give ‹three› different ‹figures› for ‹Soviet dead›."
3. 16 gap. **The Readings block** (5.4) for this claim. Source flags: the flagged language row, then the source row. Languages and Wrong fact flags: all language rows. Tone flags: the flagged language row only, then item 5 shows the rewording.
4. 12 gap. **Status line**, `t-small` `ink-2`: `check` 14px `ok`, "Double-checked", then " · source read ‹12 Nov 2026›" (Source flags) or " · versions compared ‹12 Nov 2026›". Tooltip on "Double-checked": "Two separate passes agreed on this flag. See Method."
5. 16 gap. **Suggestion** (only when one exists). `t-head` "Suggested fix", then `t-body`:
   - Better-sourced language: "The ‹Swedish› article states this with a source that supports it: " then the external link "‹Sandström 1991, p. 112›". "It could be used here."
   - Source gives a value: "The cited source gives ‹22,830›."
   - Tone: the neutral rewording as a quote in `q-small` inside a `surface` box (1px `line`, radius 8, padding 12 16), written in the article's language, with the gloss under it if not English. Above the box `t-small` `ink-2`: "A neutral wording".
   - Never phrased as an order, and never "the correct version is".
6. 16 gap. **History.** `t-head` "When this got in". Then `t-body`:
   - Sentence 1: "Entered the ‹English› article on ‹14 Mar 2019›, in " then external link "revision ‹887654321›" (the diff on Wikipedia) "."
   - Sentence 2, one of: "It has never matched its source." / "It matched its source until ‹2 Jun 2021›, when ‹25,904 replaced 22,830›." / "It had no source until ‹9 Jan 2020›." / for Languages and Tone flags: "The other languages have said ‹this› since ‹2012›."
   - A list of up to 4 dated changes to this claim, each a 32-high button row: date `t-small` tabular `ink` (88 wide), then `t-small` `ink-2` what changed ("added", "figure changed", "source added", "source removed", "wording changed") and, for Source flags, the verdict at that time. Clicking a row glides the time bar to that date.
   - Quiet button with `history` icon: **"Show the day before it entered"**. Glides the time bar to the day before the entry date. In the past state the button reads "Back to today".
   - If history is not available for the claim: one line `t-small` `ink-3` "No stored history reaches back to when this entered."
7. **Action area**, pinned to the bottom of the rail, `ground`, 1px `line-soft` top border, padding 16:
   - **Primary button, full width: "Copy note for editors"** with `copy` icon. Key: C.
   - 8 below, one line `t-small` `ink-3`: "A neutral note for the ‹English› Talk page, with both quotes and links. Written in ‹English›."
   - 8 below, a disclosure text button: "Read the note first" (`chevron-down`). It expands a `surface` box (1px `line`, radius 8, padding 12 16, max height 240, scroll) holding the exact text that will be copied, `t-small` `ink`, wiki markup shown as plain text.
   - 12 below, a row: left, text button **"Not an issue"**. Right, nothing. (The SQL button lives in the toolbar.)

**After "Copy note for editors":** the note goes to the clipboard. The button turns to `ok-tint` ground with `ok` text and `check` icon, label **"Copied. Paste it on the Talk page"**, for 4 seconds, then returns. Under it, replacing the helper line until another flag is selected: an external link "Open the ‹English› Talk page, new section" (`https://‹en›.wikipedia.org/wiki/Talk:‹Title›?action=edit&section=new`). The flag gains a stored count: the status line adds " · note copied ‹2› times". Copy failure (no clipboard permission): the note box opens with all text selected and the helper line reads `err` "Could not copy. The note is selected, press Ctrl or Cmd + C."

**The note** (template, filled from the flag; languages fi, sv, en; the language is that of the article that needs fixing):
```
== Claim and cited source do not match ==
The article says: "‹sentence›" (‹permalink to revision›).
The cited source, ‹source title› (‹url›, archived ‹url›), says: "‹passage›".
‹summary sentence›
For comparison, the ‹Swedish› article says: "‹sentence›" and cites ‹source›.
Could someone with access to the source check this? I found it with Parallax (‹site url›), which compares language versions and cited sources. I read both quotes before posting. ~~~~
```
One template per check (Source, Languages, Tone, Wrong fact), same shape: what the article says, what the other side says, the summary, the comparison if any, the request. No accusation, no "wrong", no "AI".

**After "Not an issue":** the action area swaps in place (`d-state`) to: `t-head` "Why is this not an issue?", three radio rows (40 high): "A fair difference for this audience" (preselected), "The check misread the article or the source", "Already fixed on Wikipedia". Then a quiet button "Save" and a text button "Cancel". Saving writes to MariaDB (`editor_reviews`) and returns the action area to a settled state: `t-body` `ink`: "Marked not an issue on ‹14 Nov 2026, 22:10›." `t-small` `ink-2`: "Reason: ‹A fair difference for this audience›. Everyone who opens this article sees this." Text button with `undo-2`: "Reopen". The primary button is not shown for a dismissed flag. The marker goes hollow, counts drop by one everywhere (toolbar, Home). Save failure: the form stays, `err` `t-small` "Could not save. Nothing was changed. Try again."

**Rail for an unflagged claim** (selected in "All claims"): header "Checked" in `ink` with `check` `ok`. Sentence `t-title`: "No issues found in this claim." The Readings block with all language rows. No suggestion. History with sentence 1 only. Action area: a quiet full-width button "Next flagged claim" (key J). No primary button.

**Rail in the past state:** unchanged, plus one line under the header, `t-small` `ink` on a `sunk` strip (padding 8 12, radius 6): "You are reading ‹13 Mar 2019›. The flag describes the article as it is today."

### 5.9 Five languages ("+2 languages", Winter War only)

Turning it on:
- The rail slides out to the right and the left region grows to the full 1440 in `d-panel`. The grid becomes gutter 40 and five equal columns (about 270 each) in the order fi, sv, en, de, ru. The two new columns slide in from the right with the grid. Column heads: "German", "Russian". Russian sentences are set in Source Serif 4 Cyrillic with the English gloss under them.
- The toolbar count becomes "Flagged claims ‹19›" (flags found in de and ru are included).
- Selecting a row or marker opens the same rail as an overlay from the right (432 wide, full height below the time bar, shadow, no scrim, `x` button top right, Esc closes). It covers the two rightmost columns while open. Its Readings block shows all five rows, so nothing is lost. Closing it returns to the five columns with the row still tinted.
- Notes for flags on the German or Russian article: the helper line reads "Written in English. No German note template yet."
- Turning it off restores three columns and the docked rail.

### 5.10 "Show the SQL" drawer

A drawer from the bottom of the window, 380 high, full width, `ground`, 1px `line` top border, drawer shadow, no scrim, the page stays usable above it. Opens in `d-panel`. Esc or the `x` closes it. `?sql=1` opens it on load.

- Header row 44: `database` icon, `t-head` "The queries behind this view", then `t-small` `ink-2` "MariaDB ‹11.8›, run just now". Right: `x`.
- Tabs (segmented control) under it, each the real query that produced what is on screen, with the bound values filled in:
  1. "Aligned claims": the vector join that pairs sentences across languages (`VEC_DISTANCE_COSINE`).
  2. "Closest source passage": the vector search over the cited source's stored chunks for the selected claim (`VEC_DISTANCE_COSINE … ORDER BY … LIMIT`).
  3. "As of ‹13 Mar 2019›": the history query (`FOR SYSTEM_TIME AS OF`). Present state: the tab reads "As of today" and shows the same query with the current timestamp.
- Body: the SQL in `code` on `surface` (1px `line`, radius 8, padding 16), wrapped, scrolls. Syntax colour: keywords `ink` 600, the two MariaDB features (`VEC_DISTANCE_COSINE`, `FOR SYSTEM_TIME AS OF`) on `blue-tint` with `blue` text, everything else `ink-2`. No other colours.
- Under the code, `t-small` `ink-2` tabular: "‹14› rows · ‹38› ms" (real timing from that request) and a quiet button "Copy query".
- The queries shown must be the strings the server actually executed for this response. Never a prepared sample.

### 5.11 States

- **Loading the article:** header, time bar, toolbar and column heads render as frames with `sunk` bars for text. 6 skeleton rows (three `sunk` lines per cell). Rail: `sunk` blocks for sentence, block and button. No spinner.
- **No open flags on this article:** "Flagged claims 0" selected. In place of rows, at the first column's left edge, 48 down: `t-head` "No open flags on this article." `t-body` `ink-2` "Every claim was checked against its source and the other two languages. " then text button "Show all ‹212› claims". Rail: "Nothing selected" state.
- **Filters hide everything:** "No flagged claims match these checks." and a text button "Turn all four on".
- **Nothing selected** (rail): `t-head` "Select a marked claim", `t-body` `ink-2` "Coloured underlines are words that do not match their source or the other languages. Click one to see both sides." Under it the four markers with their names and one line each: "Source: the cited source does not say this." "Languages: the versions do not say the same thing." "Tone: emotional or heroic wording." "Wrong fact: a date, number or name differs." This is the teaching empty state.
- **Article exists in fewer than three languages:** the missing column shows its head and one dashed box at the top spanning the column: "No ‹Swedish› article for this topic." Rows show two cells.
- **Unknown id:** page body: `t-page` "This article is not in the database." `t-body` `ink-2` "Parallax holds ‹184› articles on ‹2› themes." Quiet button "Back to the list".
- **As-of query fails:** the date snaps back to the last good date, and a line appears in the time bar's right group for 6s, `err` on present bar or `#FFB4A8` on the ink bar: "Could not load that date."
- **Database unreachable:** same pattern as Home 4.3.
- **Source text for the selected flag was removed after pre-compute:** cannot happen for open flags (a flag is only shown while its source text is stored). Keep this invariant in the query.

### 5.12 Keyboard

`J` / `K` next / previous flag. `C` copy note. `N` not an issue. `[` / `]` previous / next change to this claim. `T` back to today. `S` toggle SQL. `/` Ask field. `Esc` closes the drawer, the overlay rail or a dropdown. Shortcuts are off while a text field is focused. A `?` key opens a small popover listing them (anchored bottom left, not a modal).

---

## 6. Screen 3: Ask `/ask?q=…`

Purpose: a question in any language, answered with the versions side by side, disagreement kept visible.

How it works (so the design is honest): the question is embedded once, MariaDB returns the closest sentences across all languages and source texts (`VEC_DISTANCE_COSINE`), the top hits are grouped by aligned claim, and the screen shows the best claim's Readings. The headline sentence is chosen by rule from stored data. No prose is generated at query time.

**Frame.** One column, 760 wide, left edge at x=24 + ((1392 − 1160) / 2) so that the column and a 352 side column (gap 48) are centred as a 1160 pair. The top-bar field holds the question (it is the input for this page; there is no second field).

### 6.1 Main column

1. 32 below the top bar. H1 `t-page`: the question exactly as typed. Under it `t-small` `ink-3`: "Asked in ‹Finnish› · closest of ‹41,220› claims and ‹9,870› source texts · ‹64› ms".
2. 24 gap. **The answer sentence**, `t-title`, chosen by rule from the best-matching claim:
   - it has an open Wrong fact or Languages flag: "The versions do not agree." then, when values exist, a second sentence: "‹Three› versions, ‹three› different ‹figures›."
   - it has an open Source flag: "Wikipedia and its source do not agree."
   - no open flags and two or more languages have it: "The versions agree."
   - only one language has it: "Only the ‹Finnish› article covers this."
3. 16 gap. **The Readings block** for that claim: every language that has it, each with its value on the meta line when one exists, its quote with the differing words marked, its gloss, and its "Supported by its source / Not in its source" line. For a Source flag the source row is included. This is the "three numbers, three versions, each with its source" view.
4. 16 gap. One row: the **primary button "Open this claim in ‹Winter War›"** (goes to `/a/<id>?flag=<id>` or to the claim with `show=all`), and a text button "Show the SQL" (opens the same drawer with one tab: "Closest claims and source texts").
5. 40 gap. `t-head` "Other close passages". A plain list, up to 8 rows, 1px `line-soft` between, each row padding 12 0: meta line (language tag or `link` icon, article title as a link, section name `ink-3`, and right aligned `t-small` `ink-3` tabular "distance ‹0.21›"), then the sentence in `q-small`, then the gloss. Rows from source texts say "Cited source · ‹domain›" in the meta line. Rows of the same claim as the answer are left out.

### 6.2 Side column (352, starts level with the answer sentence)

`t-head` "How this was found". Three short lines, `t-small` `ink-2`, each with a 14px icon: `languages` "Your question was matched by meaning, not by words, so the language does not matter." `database` "One MariaDB vector search over every stored sentence and source passage." `check` "The quotes are exact. Nothing on this page was written by a model."

### 6.3 States

- **Loading:** H1 real at once. Answer sentence, Readings and list as skeletons (`sunk` bars, pulse). The meta line reads "Searching…".
- **Nothing close enough** (best distance above the threshold set in config): `t-title` "Nothing in these articles is close to that." `t-body` `ink-2` "Parallax holds ‹184› articles on ‹Finland in the Second World War›. Try a person, a place, a date or a number." Then the passing `askExamples` as text buttons. No primary button on this state.
- **Empty `q`:** redirect to `/` with the Ask field focused.
- **Embedding or database failure:** `triangle-alert`, `t-head` "The search did not run.", `t-body` `ink-2` "Your question was not saved. Try again.", quiet button "Try again".
- **Question over 300 characters:** the field stops accepting input at 300 and a `t-micro` `ink-3` counter "300 / 300" appears at its right.

---

## 7. Screen 4: Method `/method`

Purpose: prove it is real, measured and honest. Read mode: one column 680 wide, left edge at x=24 + ((1392 − 680) / 2 − 140) with a sticky section list (200 wide, `t-small`, links, current one `ink` 600) in the left margin. Body `t-body` 15 / 26 `ink`, max 68ch. Section headings `t-title`, 48 above, 12 below.

1. H1 `t-page`: "How Parallax checks Wikipedia". Under it `t-body` `ink-2`: "What is stored, how each check works, how often it is right, and where it fails."
2. **"In the database now"**: a two-column definition table (label left `ink-2`, value right `ink` 600 tabular, rows 36 high, 1px `line-soft`), live on every load, with the time of the newest row under it ("Last updated ‹14 Nov 2026, 21:40›"):
   - Articles "‹184›" · Language versions "‹552›" · Claims "‹41,220›" · Cited sources found "‹14,310›" · Sources read "‹9,870› (‹69›%)" · Revisions stored "‹612,400›" · Open flags "‹1,206›" · Marked not an issue by editors "‹17›" · Notes copied "‹43›"
   - No big-number tiles. It is a table.
3. **"The four checks"**: four entries in a list (not cards), each: marker and name as `t-head`, one paragraph, and one real Readings block as the example (picked by the same rule as Home 4.2, one per check; if a check has no qualifying flag, the example is omitted).
   - Source: "For every claim with a citation, Parallax fetches the cited page (or its Internet Archive copy), stores the text in MariaDB as vectors, and retrieves the passages closest to the claim. The claim is then judged against those passages: Supported, Contradicted, Not in source. If the page cannot be read, the claim is not flagged."
   - Languages: "Sentences in the three versions are paired by meaning with a MariaDB vector search. A claim is flagged when one version says something the others do not, or lacks it. When one language has the claim with a source that supports it, Parallax suggests that version."
   - Tone: "Wording that praises, blames or dramatises is flagged, with a neutral wording in the same language."
   - Wrong fact: "Dates, numbers and names are extracted from each paired claim and compared across languages and with the source."
4. **"Checked, then double-checked"**: "Every claim is read once by a fast model (Gemini ‹model name›). Every flag it raises is read again, separately, by a stronger model (Gemini ‹model name›). Only flags both agree on are shown. All of this happens before you open the page. Nothing is generated while you read." This is the one place the models are named.
5. **"History"**: "Every revision is loaded into MariaDB system-versioned tables. The time bar asks the database for the article `AS OF` a date. That is how Parallax knows when a claim entered and whether it ever matched its source."
6. **"How often it is right"**: a table. Head row on `ground`. Columns: Check · Planted errors caught "‹46› of ‹50›" · False flags on clean claims "‹3› of ‹50›" · Held-out set "‹38› of ‹40›". One row per check and a total row (600). Under it `t-small` `ink-2`: how the test was made, in two sentences, and a link to the eval file. All values read from the eval files at request time. If an eval has not been run, the cell reads "not measured" in `ink-3`. Never a guess.
7. **"Where it fails"**: a plain list, each a sentence:
   - "‹31›% of cited sources could not be read (books, paywalls, dead links). Those claims are not checked against their source."
   - "A difference between languages can be fair: each version writes for readers who know different things. That is why a person decides, and why 'Not an issue' exists."
   - "Pairing sentences by meaning sometimes pairs the wrong ones. A flag can rest on a bad pair."
   - "'Not an issue' needs no login, so anyone can dismiss or reopen a flag."
   - "English glosses are machine translations. Read the original before acting."
   - "Only ‹2› themes and ‹184› articles are loaded."
8. **"What Parallax never does"**: "It does not edit Wikipedia. It does not post to Talk pages. It does not decide which version is right."
9. End of page: the primary button **"See it on ‹Winter War›"** (the top article of the default theme by distance, first flag selected).

States: counts loading as `sunk` bars 64 wide in the value cells. Database unreachable: values read "unavailable", prose stays.

---

## 8. Phone (390 wide; everything under 700px)

- **Top bar** 56: mark and wordmark left; right: a 44 x 44 `search` icon button (opens the Ask field as a full-width bar over the top bar, with `x`), then "Method".
- **Home:** H1 24 / 30. Paragraph. Controls stack: theme menu full width, segmented control full width, primary button full width. The table becomes a list of rows (72 high, padding 12 16): line 1 rank and English title (600) with the distance number right aligned; line 2 `t-small`: the four markers each followed by its count, then the date right aligned. Tap opens the article. The finding example sits below the list. The live counts wrap to two lines. No horizontal scroll.
- **Article:** header: title 22 / 28, meta line wraps to two lines, Wikipedia links on a third. Time bar 48: "As of ‹14 Nov 2026›" as a full-width button that opens a bottom sheet (220 high) holding the track at full width, the two change buttons, the date picker button and "Back to today". Past state: the 48 bar is `ink`. Toolbar: the segmented control full width, then the four chips in one horizontally scrollable row (the only horizontal scroll allowed, with the right edge fading by a 24px mask), then "+2 languages" and "Show the SQL" as two half-width quiet buttons.
- **Columns become tabs:** a sticky segmented control fi | sv | en (| de | ru) under the toolbar. One language shown at a time, each row one cell with its gutter. A row whose flag is in another language shows, under the sentence, a `t-small` text button with that flag's marker: "Flag is in the ‹Swedish› version".
- **Rail becomes a bottom sheet:** tapping a row opens it at 88% height, `ground`, top radius 12, grabber 36 x 4 `line`, scrim `rgba(21,24,30,.4)`, drag down or `x` to close. Same content, the action area pinned at the bottom with safe-area padding. Previous / next arrows stay in the header.
- **SQL drawer:** full screen sheet. Code wraps, 12 / 18.
- **Ask:** one column, side column moves below the list. **Method:** one column, no section list.

---

## 9. The 2:00 video (every beat is a real click on the live site, 1440 x 900)

Before recording, pick the three flags from the real Winter War data by this checklist, and write their ids in the shot list. If no flag meets a row, change the beat, do not fake the data.
- **Flag A (Source, Contradicted):** source text read, both quotes under 220 characters, a number or date in both, entry date known and at least one later change.
- **Flag B (Wrong fact or Languages):** all three languages have the claim, at least two different values, German and Russian versions also aligned.
- **Question Q:** a Finnish or Swedish question whose best claim is Flag B or another claim with two or more different values.

| Time | Screen | Action | What the viewer learns |
|---|---|---|---|
| 0:00–0:10 | Home | Page loads on the default theme. Pointer rests on the H1, then on the finding example at right. Click "Number of issues", then back to "Language distance". | What it is, who it is for, and the sponsor's exact ask: the 10 articles with the biggest distance. |
| 0:10–0:16 | Home → Article | Click the Winter War row. The three columns appear with underlined words, the first flag selected. | Three languages side by side, problems marked on exact words. |
| 0:16–0:40 | Article, Flag A | Click Flag A's marker. The rail shows the sentence and the two quotes with the same words tinted. Click the source link (new tab shows the real page, close it). Click "Read the note first", then **"Copy note for editors"** → "Copied. Paste it on the Talk page". | **Wow 1: the source says otherwise.** And the editor's action is one click. |
| 0:40–0:58 | Article, Flag A | Click "Show the day before it entered". The bar turns black, the thumb glides back, the English cell becomes "Not in the English article on ‹date›". Press `]`: the thumb steps forward and the sentence arrives with a tint flash. Click "Back to today". | **Wow 2: when did this get in.** MariaDB system-versioned tables, live. |
| 0:58–1:18 | Article, Flag B | Press J to Flag B (or click it). The rail lists fi, sv, en with three values on the right of each row. Click "+2 languages": the German and Russian columns slide in. Click the row: the overlay rail shows five rows. Close it, click "5 languages" off. | **Wow 3: three languages, one claim** (then five). |
| 1:18–1:30 | Article | Click "Show the SQL". Click the tabs "Closest source passage" and "As of today". Close. Then on a Tone flag click "Not an issue", keep the first reason, "Save". | It is real MariaDB (vectors and history). Editors stay in charge, and the decision is saved for everyone. |
| 1:30–1:46 | Ask | Press "/". Type Question Q in Finnish. Enter. The answer: "The versions do not agree." with the values and sources. Click "Show the SQL", close. | **Wow 4: ask in any language**, and the answer shows the disagreement instead of hiding it. |
| 1:46–1:56 | Method | Click "Method". Scroll: "In the database now", "How often it is right", "Where it fails". | Live counts, measured accuracy, honest limits. |
| 1:56–2:00 | Home | Click the wordmark. Title added in the edit: "Parallax. See where Wikipedia's languages tell a different story." | |

Recording rules: no cut may hide a loading state longer than 1s (pre-warm the routes). The path never opens the "could not be read" group. Every number on screen during recording is the live value.

---

## 10. Data the screens need (so no copy is invented in the browser)

Per flag, stored at pre-compute time: `id`, `check`, `verdict`, `status` (open / dismissed), `summary` (the finding sentence, 160 characters max, pattern from 5.8), `article`, `claim`, `language` (the article that needs fixing), per version: `quote`, `marked_spans` (character offsets), `gloss`, `revision id`, `value` (when extractable), `own_source_verdict`; for Source flags: `source title`, `url`, `archive url`, `passage`, `passage marked_spans`, `read at`; `suggestion` (type and text); history: `entered at`, `entered revision`, `ever supported` and up to 4 dated changes; `note` text in the article's language; `copied count`. Per article: titles in each language, distance 0 to 100, counts per check, last changed, stored revision range. If a field is missing the element that needs it is not rendered. Never a blank label, never "undefined", never "N/A".

Dates on screen: "14 Nov 2026", with time "14 Nov 2026, 22:10". Numbers: thin thousands comma "41,220" in Parallax's own text. Numbers inside quotes are left exactly as the article wrote them.

---

## 11. Do not

- No "AI", "AI-detected", "LLM", "model", "confidence", "score" or percentages of certainty on Home, Article or Ask. "Checked" and "Double-checked" only. Models are named once, on Method.
- No demo mode, seeded example, canned answer, autoplay, tour, or "next step" key. No hard-coded figure, quote, title or date.
- No verdict in Parallax's voice without both quotes on the same screen. No "wrong", "false", "biased" as labels.
- No coloured left or right border on rows, cards or callouts. No coloured card grounds. Check colours only in the marker, the underline, the tint behind words and the check name.
- No cards on Home, no hero-metric tiles, no charts, no sparklines, no progress rings, no badges besides counts.
- No label above a heading, no uppercase tracked labels, no section numbers.
- No gradients, glass, glow, or shadows on anything that is not floating.
- No modal dialogs. The SQL is a drawer, "Not an issue" is inline, the note preview is a disclosure.
- No serif in headings, buttons or labels. No italic. No mono outside the SQL drawer. No font other than the three named.
- No chat bubbles, typing dots, streamed text or assistant avatar on Ask.
- No Wikipedia logo, globe, puzzle piece, "W" mark or Wikipedia skin. No claim of affiliation.
- No button that edits or posts to Wikipedia. Parallax only copies text and opens links.
- No second primary button on any screen. No dead buttons, placeholder pages or "coming soon".
- No truncating a quote in the middle of a sentence without "…" and a way to see the whole.
- No horizontal page scroll at 390 or 1440. No text overflow with real Finnish compound words (set `overflow-wrap: anywhere` on quotes and `hyphens: auto` with the right `lang` attribute on every quoted element).
- Every quoted element carries its `lang` attribute (`fi`, `sv`, `en`, `de`, `ru`) for hyphenation and screen readers.

---

## 12. Acceptance: screenshots Codex must produce and check

Save to `screenshots/parallax/` as PNG from the deployed site with real data. Desktop is a 1440 x 900 viewport, phone is 390 x 844.

1. `01-home-distance-desktop.png`: Home, default theme, sorted by language distance, all 10 rows and the live counts visible without scrolling, the finding example at right.
2. `02-home-issues-desktop.png`: sorted by number of issues.
3. `03-home-loading-desktop.png`: skeleton state.
4. `04-article-default-desktop.png`: Winter War, flagged claims, first flag selected, rail filled.
5. `05-article-source-contradicted-desktop.png`: a Source "Contradicted" flag selected, both quotes with the same words tinted.
6. `06-article-note-open-desktop.png`: "Read the note first" expanded.
7. `07-article-copied-desktop.png`: the button in its "Copied" state with the Talk page link.
8. `08-article-languages-desktop.png`: a Languages or Wrong fact flag with three rows and values.
9. `09-article-tone-desktop.png`: a Tone flag with the neutral wording.
10. `10-article-past-desktop.png`: the time bar in the past state (ink bar), at least one "Not in the … article on …" cell.
11. `11-article-five-languages-desktop.png`: five columns, no rail.
12. `12-article-five-overlay-desktop.png`: five columns with the overlay rail and five Readings rows.
13. `13-article-sql-desktop.png`: SQL drawer on the "Closest source passage" tab with timing.
14. `14-article-not-an-issue-form-desktop.png` and `15-article-dismissed-desktop.png`: the reason form, then the settled state with a hollow marker.
15. `16-article-all-claims-desktop.png`: "All claims" with an unflagged row selected.
16. `17-article-empty-rail-desktop.png`: the "Select a marked claim" state.
17. `18-ask-disagree-desktop.png`: a Finnish question, "The versions do not agree.", values and sources.
18. `19-ask-nothing-desktop.png`: the nothing-close-enough state.
19. `20-method-desktop.png` (top) and `21-method-accuracy-desktop.png` (accuracy and limits).
20. `22-home-phone.png`, `23-article-phone.png` (tabs), `24-article-sheet-phone.png` (rail sheet), `25-ask-phone.png`.

Checks to run and report with the screenshots:
- **5-second test:** on screenshot 01, the words "Wikipedia", "Finnish, Swedish and English", "source", "editor" and "never edits" are all visible above the fold, with one pair of disagreeing quotes.
- **One primary:** count the `ink` filled buttons on each of the four screens in every screenshot. The answer is 1 (0 on a dismissed flag, an unflagged claim, and the Ask empty state).
- **Real data:** no `‹` or `›` character anywhere in the rendered site. Every count on Home, Article and Method equals a direct SQL count run at the same moment (attach the queries and results).
- **Quotes are exact:** for 10 random open flags, the quote on screen is a substring of the stored revision text, and the source passage is a substring of the stored source text.
- **Source path is safe:** no open flag has an unread source. Clicking J through every flag on Winter War never shows an empty Readings row.
- **SQL is real:** the text in the drawer equals the server's query log for that request, and contains `VEC_DISTANCE_COSINE` on tabs 1 and 2 and `FOR SYSTEM_TIME AS OF` on tab 3.
- **Time bar:** dragging to five dates returns text that matches the Wikipedia revision current on each date. The as-of query answers in under 300ms warm.
- **Not an issue persists:** dismiss a flag, open the page in a second browser with no cookies, the flag is hollow and the reason is shown. Reopen restores it.
- **Clipboard:** the copied text equals the note preview, and is in the language of the flagged article.
- **Keyboard only:** open the top article from Home, move through three flags with J, copy a note with C, travel in time with `[` `]` and T, open and close the SQL with S, ask a question with `/`.
- **Marks without colour:** in a greyscale screenshot of 04, the four checks are still told apart by shape, and the marked words are still visible by underline.
- **Contrast:** every text pair 4.5:1 or better (check `ink-3` on `ground`, each check colour on `surface` and on `blue-tint`, `on-ink-2` on `ink`). Every marker 3:1 or better.
- **Fonts:** computed font of a Russian sentence is Source Serif 4, of a Finnish UI string Commissioner. No fallback font renders any glyph on the Winter War page in five languages.
- **Reduced motion:** with `prefers-reduced-motion`, the time travel, the columns sliding in and the drawer all reach their end states instantly.
- **No overflow:** at 390 and 1440, no horizontal page scroll and no clipped text, with the longest real Finnish title in the theme.

---

## 13. Chief decisions on the open questions (Sat 23:50, binding)
1. Note for editors: generated at pre-compute time by Gemini in the language of the article that needs fixing (fi, sv, en, de, ru), from one fixed English template, then stored. No live generation.
2. German and Russian are comparison-only (no flags, not counted in rankings); they appear only in the Winter War "+2 languages" view.
3. Old revisions: store the entry revision and check the claim's text at entry against its source once. If that check exists, show "It matched its source until <date>"; otherwise drop the line (never guess).
4. Time bar: if the warm as-of query exceeds 300 ms, snap the thumb to stored revision dates; same visuals.
5. Ask threshold and example questions: Codex sets the distance threshold on the dev split and records it in DECISIONS.md; example questions must be validated against real data or replaced.
6. Drop "note copied N times".
All of Fable's other choices (unreachable sources never flags, Show the SQL in the toolbar, "Not an issue" reasons, "Open the top article", real revision range, Method only names Gemini, theme menu) are approved.
