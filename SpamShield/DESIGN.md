---
name: SpamShield
description: A spam checker that issues every verdict like a security-printed bank slip, hard to fake and easy to read.
colors:
  ground: "#eef3ee"
  sheet: "#ffffff"
  paper-wash: "#f7f9f8"
  row-hover: "#f6f9f7"
  rule: "#c5d3ca"
  rule-soft: "#e2e9e4"
  input-stroke: "#8a9a92"
  ink: "#14181b"
  ink-hover: "#2c3337"
  ink-2: "#3c4a44"
  ink-3: "#56645e"
  bank: "#0e3b36"
  bank-2: "#17524b"
  bank-tint: "#dbe8e2"
  on-bank: "#d3e2dc"
  rail-rule: "#2a5a53"
  rail-meta: "#a9c2ba"
  spam: "#c4202f"
  spam-tint: "#fbe9ea"
  spam-ink: "#8e1621"
  warn: "#a86a12"
  warn-tint: "#fbf0dc"
  warn-ink: "#7a4c0a"
  safe: "#1d6b4f"
  safe-tint: "#e2f0e9"
  safe-ink: "#154f3a"
typography:
  display:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "84px"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "-0.03em"
    fontFeature: "\"tnum\" 1"
    fontVariation: "\"wdth\" 82"
  headline:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "30px"
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-0.02em"
    fontFeature: "\"tnum\" 1"
    fontVariation: "\"wdth\" 82"
  stamp-display:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "28px"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "0.07em"
    fontVariation: "\"wdth\" 82"
  title-reading:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "22px"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "-0.01em"
    fontVariation: "\"wdth\" 82"
  title:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.005em"
    fontVariation: "\"wdth\" 82"
  body:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "\"tnum\" 1"
  body-reading:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.65
  body-entry:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 700
    lineHeight: 1.5
  label-caps:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: "0.06em"
  stamp:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 800
    lineHeight: 1.4
    letterSpacing: "0.08em"
  meta:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.5
  serial:
    fontFamily: "Martian Mono, ui-monospace, Consolas, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "-0.01em"
  microprint:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "6.5px"
    fontWeight: 700
    lineHeight: "9px"
    letterSpacing: "0.14em"
rounded:
  hair: "1px"
  sm: "2px"
  md: "3px"
  pill: "50%"
spacing:
  rule: "1px"
  xs: "6px"
  sm: "10px"
  md: "14px"
  gutter: "16px"
  lg: "22px"
  slip: "24px"
  page: "36px"
components:
  button-ink:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.sheet}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "12px 20px"
  button-ink-hover:
    backgroundColor: "{colors.ink-hover}"
    textColor: "{colors.sheet}"
  button-line:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "12px 20px"
  button-line-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.sheet}"
  button-danger-line:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.spam}"
    rounded: "{rounded.md}"
    padding: "12px 20px"
  button-danger-line-hover:
    backgroundColor: "{colors.spam}"
    textColor: "{colors.sheet}"
  button-sm:
    padding: "8px 12px"
  input:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "11px 13px"
  textarea-message:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    typography: "{typography.body-entry}"
    rounded: "{rounded.md}"
    padding: "11px 13px"
    height: "180px"
  rail:
    backgroundColor: "{colors.bank}"
    textColor: "{colors.on-bank}"
    width: "232px"
    padding: "22px 14px 18px"
  rail-link:
    textColor: "{colors.on-bank}"
    rounded: "{rounded.md}"
    padding: "9px 10px"
  rail-link-hover:
    backgroundColor: "{colors.bank-2}"
    textColor: "{colors.sheet}"
  rail-link-current:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.bank}"
  sheet:
    backgroundColor: "{colors.sheet}"
    rounded: "{rounded.md}"
  module:
    backgroundColor: "{colors.sheet}"
    padding: "20px 22px"
  stat:
    backgroundColor: "{colors.sheet}"
    typography: "{typography.headline}"
    padding: "16px 20px 18px"
  stamp-spam:
    textColor: "{colors.spam}"
    typography: "{typography.stamp}"
    rounded: "{rounded.sm}"
    padding: "2px 8px 1px"
  stamp-suspicious:
    textColor: "{colors.warn-ink}"
    typography: "{typography.stamp}"
    rounded: "{rounded.sm}"
    padding: "2px 8px 1px"
  stamp-safe:
    textColor: "{colors.safe}"
    typography: "{typography.stamp}"
    rounded: "{rounded.sm}"
    padding: "2px 8px 1px"
  slip-band-spam:
    backgroundColor: "{colors.spam-tint}"
    textColor: "{colors.spam}"
    height: "76px"
    padding: "0 24px"
  slip-band-suspicious:
    backgroundColor: "{colors.warn-tint}"
    textColor: "{colors.warn}"
    height: "76px"
    padding: "0 24px"
  slip-band-safe:
    backgroundColor: "{colors.safe-tint}"
    textColor: "{colors.safe}"
    height: "76px"
    padding: "0 24px"
  slip-stamp:
    backgroundColor: "{colors.sheet}"
    typography: "{typography.stamp-display}"
    rounded: "{rounded.md}"
    padding: "3px 14px 1px"
  slip-figure:
    typography: "{typography.display}"
    padding: "12px 24px 10px"
  slip-warning:
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "6px 12px"
  slip-serial:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink-2}"
    typography: "{typography.serial}"
    rounded: "{rounded.sm}"
    padding: "4px 8px"
  word-chip:
    backgroundColor: "{colors.paper-wash}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
  verdict-notes:
    textColor: "{colors.ink-2}"
    typography: "{typography.body}"
    padding: "18px 0 0"
  segmented-current:
    backgroundColor: "{colors.bank}"
    textColor: "{colors.sheet}"
    padding: "8px 14px"
  pager-current:
    backgroundColor: "{colors.bank}"
    textColor: "{colors.sheet}"
    rounded: "{rounded.sm}"
    padding: "6px 10px"
  meter-track:
    backgroundColor: "{colors.rule-soft}"
    rounded: "{rounded.hair}"
    height: "6px"
  notice-danger:
    backgroundColor: "{colors.spam-tint}"
    textColor: "{colors.spam-ink}"
    rounded: "{rounded.md}"
    padding: "12px 16px"
  notice-success:
    backgroundColor: "{colors.safe-tint}"
    textColor: "{colors.safe-ink}"
    rounded: "{rounded.md}"
    padding: "12px 16px"
  notice-warning:
    backgroundColor: "{colors.warn-tint}"
    textColor: "{colors.warn-ink}"
    rounded: "{rounded.md}"
    padding: "12px 16px"
  confirm-dialog:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    width: "420px"
---

# Design System: SpamShield

## Overview

**Creative North Star: "The Security-Printed Slip"**

SpamShield borrows its whole material language from Indian bank cheque and passbook security printing. Every page sits on a pale pantograph-tint ground; information lives on white sheets ruled in hairlines and packed edge to edge, like the boxes of a passbook. A banking-ink green rail carries navigation. Verdicts are not badges or glowing pills: they are inked stamps, struck once, in cancel red, amber or ledger green. The one place the security printing becomes literal is the verdict slip, whose band carries guilloché fine-line and a microprint rule, the marks that make a real cheque hard to forge.

The system is dense, flat and high-contrast on purpose. It is read on a classroom projector in a lit room and on a laptop in daylight, so the ground is light, the ink is near-black, and depth comes from rules, never from shadow or blur. Each screen gets one monumental figure (the spam probability on the slip, or a 30px stat row) and everything else is set small, narrow and tabular. This system replaces a rejected dark navy and cyan glassmorphism look; nothing in it floats, glows or blurs.

**Key Characteristics:**
- Light pantograph-tint ground, white ruled sheets, 1px hairline modules packed with no gutters.
- Banking-ink green reserved for the rail, the current selection and interaction affordances.
- Three verdict inks (cancel red, amber, ledger green), each with a tint and a darker ink for text on that tint.
- Archivo for everything, narrowed to 82% width for display text; tabular numerals globally.
- Martian Mono only for serial numbers, timestamps and IDs.
- Guilloché fine-line and microprint appear only on the verdict slip.
- Flat: no elevation shadows on surfaces; a single struck-stamp motion as the signature.

## Colors

A cool paper-and-ink palette: green-grey neutrals, one deep banking green, and three verdict inks that each come as a full set of stroke, tint and text ink.

### Primary
- **Banking Ink** (`bank`): the rail background, the current page in navigation, the current segment in a filter, the current page in the pager, links, the focus outline, the text caret and text selection. It is the colour of "where you are" and "what you can act on".
- **Banking Ink Lifted** (`bank-2`): hover state of rail links and link hover; never used at rest.
- **Banking Tint** (`bank-tint`): the 3px focus halo around inputs and the hover wash on filter segments.
- **Rail Paper** (`on-bank`): body text on the rail (9.2:1 on Banking Ink). **Rail Rule** (`rail-rule`) and **Rail Meta** (`rail-meta`) are the rail footer's divider and caption.

### Secondary: verdict inks
- **Cancel Red** (`spam`): spam stamps, spam figures, meter fills, chart series, "Found" in the checks table, field errors and the destructive line button. **Cancel Tint** (`spam-tint`) is the spam slip band, danger notice and matrix miss cells. **Cancel Ink** (`spam-ink`) is text set on the tint and the score on word chips.
- **Caution Amber** (`warn`): the struck Suspicious stamp on the slip, the suspicious band strokes and microprint, meter and stat fills, and warning borders. **Amber Tint** (`warn-tint`) is the suspicious band and warning notice. **Amber Ink** (`warn-ink`) is all small amber text: the inline Suspicious stamp, the near-limit character count and text on the tint.
- **Ledger Green** (`safe`): safe stamps, safe figures, "Not found" in the checks table, safe chart series. **Ledger Tint** (`safe-tint`) and **Ledger Ink** (`safe-ink`) follow the same pattern.

### Neutral
- **Pantograph Tint** (`ground`): the page ground behind every sheet, and the fill of the current rail link.
- **Sheet White** (`sheet`): every module, table and slip body; also the paper patch behind the slip stamp and serial.
- **Paper Wash** (`paper-wash`): word chips, keyboard keys, the formula box and the dialog action bar. **Row Hover** (`row-hover`) is the ledger row hover.
- **Hairline** (`rule`): borders between modules (shown through the 1px grid gap), sheet borders, dashed empty-slip frame.
- **Soft Rule** (`rule-soft`): rows inside a module, meter and bar tracks, chart grid lines.
- **Input Stroke** (`input-stroke`): resting 1.5px border of inputs; darkens to Secondary Ink on hover.
- **Ink** (`ink`): text, primary buttons, the 1.5px rule under ledger headers, chart axis lines, tooltips. **Ink Hover** (`ink-hover`) is the primary button hover.
- **Secondary Ink** (`ink-2`): descriptions, explanations, reading copy.
- **Meta Ink** (`ink-3`): labels, captions, table headers, timestamps (6.2:1 on white, 5.5:1 on the ground).

### Named Rules
**The Banking Ink Rule.** Banking green marks navigation, the current selection and interaction affordances (links, focus, caret). It never carries a verdict, a data value or a chart series. Safe is Ledger Green, a separate and lighter ink, so "safe" can never be confused with "selected".

**The Three Inks Rule.** Every verdict colour ships as a triple: the stroke colour for stamps, figures and fills; the tint for bands and notices; the darker ink for text set on the tint. Never set verdict-coloured text directly on its own tint at body size; use the ink.

**The Amber Legibility Rule.** Caution Amber (4.43:1 on white) is a stroke, fill and large-figure colour only. Any amber text below display size is set in Amber Ink, as the inline Suspicious stamp and the near-limit character count are.

## Typography

**Display Font:** Archivo (variable, wdth 62–125, wght 100–900), with Segoe UI and system-ui fallback
**Body Font:** Archivo, same file
**Label/Mono Font:** Martian Mono (variable, wght 100–800), with ui-monospace and Consolas fallback

**Character:** One grotesque does all the work, the way a cheque uses one face in several widths. Display text is narrowed to 82% width and set heavy, like the condensed amount line on a printed slip; body text stays at normal width. Numerals are tabular everywhere (`font-variant-numeric: tabular-nums` on the body) so columns of probabilities line up.

### Hierarchy
- **Display** (800, 84px, line-height 0.95, -0.03em, 82% width): the monumental spam probability on the verdict slip. One per screen. Drops to 60px under 640px.
- **Headline** (800, 30px, line-height 1.15, -0.02em, 82% width): page titles and stat strip values. Page titles drop to 25px and stat values to 24px under 640px.
- **Stamp Display** (800, 28px, +0.07em, uppercase, 82% width): the struck stamp on the slip band. 22px under 640px.
- **Title, reading** (800, 22px, -0.01em, 82% width): section heads on the About page and the error sheet (28px there); also inline fact figures and rail accuracy (22px).
- **Title** (700, 16px, -0.005em, 82% width): module heads. The slip caption (800, 20px) and dialog title (800, 19px) sit between Title and Headline.
- **Body** (400, 15px, line-height 1.5): all interface text, tables and checks.
- **Body, reading** (400, 16px, line-height 1.65, max 70ch): About page prose.
- **Body, entry** (400, 17px, line-height 1.55): the message textarea, so pasted text is easy to proof.
- **Label** (700, 13px): field labels. **Meta** (400 to 500, 13px): stat labels, captions, footers, notes.
- **Label caps** (700, 12px to 13px, +0.06em, uppercase): ledger table headers, matrix headers and slip section heads.
- **Stamp** (800, 12px, +0.08em, uppercase): the inline verdict stamp in tables.
- **Serial** (Martian Mono 400, 12px to 13px, -0.01em): record numbers, the slip serial and date, error codes.
- **Microprint** (700, 6.5px on a 9px line, +0.14em, uppercase): the repeated line under the slip band; decorative and hidden from assistive tech.

### Named Rules
**The Narrow Display Rule.** Anything set as a display figure or heading (page title, module head, stat value, stamps, slip figure, reading heads, matrix and legend figures) uses `font-stretch: 82%`. Body, labels and table cells stay at 100% width.

**The Serial Face Rule.** Martian Mono is for serial numbers, timestamps and IDs, and nothing else. It is never used for headings, labels, numbers that are values (probabilities, counts), or body text.

## Layout

The shell is a fixed 232px banking-green rail on the left and a main column capped at 1320px, padded 28px top and 36px at the sides. Every page opens with a page head: title and one-line description on the left, a meta line (model accuracy, record count) right-aligned at the bottom, closed by a hairline.

Content is built from **ledger grids**: CSS grids with a 1px gap over a Hairline background, so modules butt edge to edge and the rule shows between them. Column presets are 2, 3, 4 and main-plus-side (1.65fr / 1fr); the Detect sheet splits composer and slip at 1fr / 1.15fr. Stacked groups of sheets are separated by 22px. A stat strip can be fused to the sheet above it (the sheet drops its bottom radius, the strip drops its top border and top radius), so the two read as one form; Detect always fuses its four-cell strip under the composer-and-slip sheet. The composer column is not sticky; it scrolls with the page.

Spacing rhythm is small and steady: 6px and 10px inside rows, 14px between head and content, 20px to 24px module and slip padding, 22px between sheets, 36px page sides, 16px gutter on phones.

**Responsive behaviour:**
- **Under 1200px:** the Detect sheet and main-plus-side grids go to one column. Once a verdict exists, the slip is ordered first and the composer folds into a two-line quoted summary of the checked message with an Edit message button (which unfolds the form); the verdict notes stay below it. Three-column grids go to two.
- **Under 992px:** the rail becomes an off-canvas drawer (slides in over a green-black scrim) opened from a sticky banking-green top bar; page padding becomes 20px 16px; two- and four-column grids are two columns.
- **Under 768px:** the evaluation split on Analytics stacks.
- **Under 640px:** the page head stacks, all grids except the four-cell stat strip become one column, slip padding tightens to 16px, the ledger hides its No., probability and date columns and shows them as one meta line under the message instead (the serial and timestamp spans never wrap internally), and the pager stacks.

### Named Rules
**The Packed Module Rule.** Modules inside a sheet touch. Separate them with the 1px rule showing through a grid gap, never with whitespace gutters or separate floating cards.

**The Fixed Furniture Rule.** Every record row carries the same furniture in the same order: serial No., verdict stamp, spam probability, time. On phones the furniture collapses into one meta line but keeps its order.

## Elevation & Depth

The system is flat. Sheets, modules, slips and tables carry no shadow; depth is conveyed by the tint ground behind white sheets and by hairline rules (1px Hairline between modules, 1px Soft Rule between rows, 1.5px Ink under table headers). Two box-shadows exist, both functional: the 3px Banking Tint focus halo on inputs (Cancel Tint when invalid), and the soft shadow cast by the rail when it is open as a drawer on small screens. The modal dialog separates itself with a green-black backdrop, not a shadow.

### Shadow Vocabulary
- **Focus halo** (`box-shadow: 0 0 0 3px var(--bank-tint)`): inputs and the textarea on focus.
- **Drawer cast** (`box-shadow: 8px 0 30px rgba(0, 0, 0, .18)`): the rail only while it is an off-canvas drawer.

### Named Rules
**The Ruled, Not Raised Rule.** Separation comes from rules and tint, never from shadow, blur or glass. If a surface needs to stand apart, give it a border or a tint.

## Shapes

Corners are nearly square: 3px on sheets, buttons, inputs, notices, the dialog and the slip stamp; 2px on inline stamps, word chips, pager cells, the split bar and tooltips; 1px on meter and bar tracks. The only round shapes are the step counters on the empty slip. Borders are part of the vocabulary: 1px for structure, 1.5px for interactive outlines (buttons, inputs, segmented filter, notices), 2px for inline stamps and 3px for the struck slip stamp. The slip stamp is rotated -3deg; nothing else is rotated. The empty slip uses a 1.5px dashed Hairline frame, like a blank form box.

## Components

### Buttons
Inked and plain, like the action line of a bank form.
- **Shape:** near-square (3px), 1.5px border, 700 weight, 15px text, 12px 20px padding; small size is 8px 12px at 14px.
- **Primary (Ink):** Ink fill, white text. Used for the one main action per screen (Analyze message, Check a message). Hover lifts to Ink Hover; busy state drops to 70% opacity with a progress cursor and the label changes to "Analyzing…".
- **Line:** white with an Ink border; hover fills with Ink and turns the text white.
- **Danger line:** white with a Cancel Red border and text; hover fills red. Used for Clear history, the dialog's confirm and delete actions.
- **Icon:** line button with 7px padding and a 16px single-weight stroke icon (trash).
- **Focus:** 2px Banking Ink outline offset 2px, everywhere.

### Inputs / Fields
- **Style:** white, 1.5px Input Stroke border, 3px radius, 11px 13px padding; placeholder in a muted green-grey.
- **Hover / Focus:** border darkens to Secondary Ink on hover; on focus it turns Banking Ink with the 3px Banking Tint halo.
- **Error:** border Cancel Red with a Cancel Tint halo, plus a 600-weight red message below.
- **Message textarea:** 180px minimum height, 17px entry type, vertical resize, with a character count (turns Amber Ink and 600 weight past 90% of the limit) and the primary button at its foot.

### Navigation (the rail)
- **Style:** fixed 232px Banking Ink column; white logo and 800-weight wordmark at the top; five links with 18px single-weight stroke icons; a footer under a Rail Rule showing the algorithm and test accuracy (22px, 800, 82% width).
- **States:** links rest in Rail Paper at 500 weight; hover fills Banking Ink Lifted with white text; the current page fills with Pantograph Tint, Banking Ink text and 700 weight, so it reads as a tab cut through to the page. Focus outline is white on the rail.
- **Mobile:** under 992px a sticky Banking Ink top bar with a 40px menu button opens the rail as a drawer; Escape and the scrim close it.

### Page head
Title (Headline, 82% width) with a one-line description in Secondary Ink capped at 62ch; a right-aligned Meta line; 16px below, a Hairline closes it.

### Sheets and ruled ledger grids
White sheets with a Hairline border and 3px radius. Ledger grids pack modules edge to edge with the 1px rule showing through. Modules pad 20px 22px and open with a module head (Title on the left, a 600-weight link or Meta note on the right).

### Stat strip
A ledger grid of four stat cells (16px 20px 18px padding): Meta label, Headline value at 82% width, optional Meta sub-line. Values may take a verdict colour (spam, safe, suspicious) when the number is that verdict's count. On Detect the strip is fused to the bottom of the composer-and-slip sheet.

### Stamps
Inline verdict labels: transparent fill, 2px border in the text colour, 2px radius, 12px 800 uppercase at +0.08em. Three variants only: Spam (Cancel Red), Suspicious (Amber Ink, for legibility at 12px), Safe (Ledger Green). They never get a filled background.

### Probability meter
A right-aligned 700-weight percentage (minimum 54px wide) beside a 6px Soft Rule track filled in the verdict colour. Paired with a stamp in record rows.

### Ledger table
Full-width, collapsed borders. Headers are Label caps in Meta Ink above a 1.5px Ink rule; rows pad 12px 14px with Soft Rule dividers and a Row Hover wash; first and last columns are flush with the module edge. Serial column in Martian Mono 13px Meta Ink; time column in Meta Ink 14px; numbers right-aligned. Long messages clamp to two lines and expand on click.

### Verdict slip (signature component)
The result of an analysis, printed as a security slip.
- **Order:** band, microprint rule, figure with caption, warning (spam and suspicious only), checks, raised words. The explanation and the follow-up actions do not live on the slip; they sit in the composer column as verdict notes.
- **Band:** 76px minimum height, 24px side padding, filled with the verdict tint and tiled horizontally with a guilloché SVG (24 phase-shifted sine strokes at 0.45 to 0.55px in the verdict colour, 35 to 55% opacity, 112px tall). The stamp sits left on a white patch; the serial ("No." plus serial and date in Martian Mono 12px) sits right on a white patch.
- **Microprint rule:** directly under the band, a line of 6.5px uppercase text repeating "SpamShield verified analysis · No. …" between a 1.5px and a 1px rule in the verdict colour, at 85% opacity, unselectable and hidden from assistive tech.
- **Struck stamp:** 28px 800 uppercase at 82% width, 3px verdict-coloured border, rotated -3deg.
- **Figure:** the spam probability at Display size, padded 12px 24px 10px, followed by its caption: the 20px 800 verdict title (the slip's heading) over a 15px Secondary Ink line, max 30ch.
- **Warning:** for spam and suspicious only, a one-line 14px box (6px 12px padding, 1.5px verdict border, verdict tint) with its lead phrase in the verdict ink.
- **Sections:** Label caps heads ("Checks · n of m found", "Words that raised the spam score") over the checks table and the word chips; the last section closes with 24px bottom padding.
- **Motion:** on a fresh result, the band prints in with a left-to-right clip wipe (700ms), then the stamp strikes once (520ms, starting 260ms in) from -9deg at 1.6x scale to its resting -3deg at 1x. Disabled under reduced motion.
- **Empty state:** a dashed blank box ("The verdict prints here") and a five-step numbered list with 24px round Banking Ink counters.

### Checks table
Borderless, compact two-column table with Soft Rule row dividers and 4px row padding. The check name on the left (Secondary Ink when clear) with its evidence inline after the title in 13px Meta Ink; the result right-aligned: "Found" in 700 Cancel Red or "Not found" in 600 Ledger Green.

### Word chips
Paper Wash chips with a 1px Hairline border, 2px radius, 2px 8px padding, 14px 600-weight word, followed 5px later by its score in 12px Cancel Ink.

### Verdict notes
In the composer column under the form, once a verdict exists: a 1.5px Ink rule, then a Label caps head ("Why this verdict"), the model's explanation in Secondary Ink (max 60ch) and two line buttons (Check another message, Open history) with 10px between them.

### Segmented filter
A 1.5px Ink-bordered group of links divided by 1.5px Ink rules, 8px 14px padding, 14px 600 text with a 500-weight count. Hover washes Banking Tint; the current segment fills Banking Ink with white text.

### Pager
A Meta "Page n of m" line on the left; on the right, 34px-minimum cells with 1px Hairline borders and 2px radius. Hover darkens the border to Ink; the current page fills Banking Ink; gaps are borderless ellipses; disabled Previous / Next fade and ignore pointer events.

### Notices
Flash messages above page content: 1.5px border and tint in the matching verdict triple (danger, success, warning), text in the verdict ink, 3px radius, 12px 16px padding, with a 24px dismiss button carrying the authored 14px close icon (two 2px strokes from the icon sprite).

### Confirm dialog
A native modal dialog, at most 420px wide: white body (22px 24px) with a 19px 800 title and Secondary Ink text, and an action bar on Paper Wash under a Soft Rule holding a small line Cancel and a small danger-line confirm. Backdrop is green-black at 45%. Cancel takes focus first.

### Charts
Chart.js in the same inks: Cancel Red for spam and Ledger Green for safe series, Ink for the total line, a dashed (5/4) Cancel Red line for spam rate. Axis lines Ink, grid lines Soft Rule, ticks in Meta Ink at 13px Archivo, legend top-right with 12px square keys, tooltips Ink with a 2px radius, pie slices separated by 2px white. Lines are straight (no tension); bars max 36px thick (28px on the confidence chart). The split bar (28px, 2px radius) and horizontal bar rows (10px Soft Rule track, Cancel Red fill) use the same inks without Chart.js. The confusion matrix uses 1px Hairline cells, Ledger Tint for correct and Cancel Tint for misses, with 26px 800 figures at 82% width.

## Do's and Don'ts

### Do:
- **Do** pack modules edge to edge in a ledger grid with the 1px Hairline showing through the gap.
- **Do** set every display figure and heading at `font-stretch: 82%` and heavy weight (700 to 800), with tabular numerals.
- **Do** give each screen one monumental figure (84px on the slip, 30px stat values elsewhere) and keep everything else small.
- **Do** use the verdict triple together: stroke colour for stamps and figures, tint for bands and notices, ink for text on the tint.
- **Do** keep the record row furniture fixed: serial No., stamp, probability, time.
- **Do** use the 2px Banking Ink outline, offset 2px, as the focus state on every interactive element (white on the rail).
- **Do** draw icons from the authored single-stroke sprite (24px grid, 1.6 to 2px strokes, currentColor); never use text glyphs as icons.
- **Do** gate every animation behind `prefers-reduced-motion: no-preference`.

### Don't:
- **Don't** use banking green for a verdict, a data value or a chart series; it means navigation, current selection and interaction only.
- **Don't** use Martian Mono for anything other than serial numbers, timestamps and IDs.
- **Don't** add shadows, blur, glass, glow or gradients to sheets and modules; this system replaced a dark navy and cyan glassmorphism look.
- **Don't** use guilloché or microprint as a surface pattern anywhere except the verdict slip (the logo's three wave lines are part of the mark, not a pattern).
- **Don't** fill inline stamps; a stamp is an outlined, inked mark.
- **Don't** separate modules inside a sheet with whitespace gutters or turn them into floating cards.
- **Don't** add slip motion beyond the band's single print wipe and the stamp's single strike.
