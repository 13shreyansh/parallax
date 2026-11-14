---
name: NPOV Radar
description: An editorial evidence desk for comparing Wikipedia passages.
colors:
  ink: "#183446"
  muted: "#526976"
  background: "#f4f7f8"
  paper: "#ffffff"
  primary: "#1c5e9a"
  navy: "#143649"
  rule: "#d7e1e6"
  review: "#835516"
  matching-date: "#326d53"
typography:
  headline:
    fontFamily: "Public Sans, -apple-system, sans-serif"
    fontSize: "28px"
    fontWeight: 600
    lineHeight: 1.18
    letterSpacing: "-0.035em"
  evidence:
    fontFamily: "Georgia, Times New Roman, serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.75
  explanation:
    fontFamily: "Public Sans, -apple-system, sans-serif"
    fontSize: "11px"
    lineHeight: 1.65
  revision-action:
    fontFamily: "Public Sans, -apple-system, sans-serif"
    fontSize: "12px"
rounded:
  control: "5px"
  field: "6px"
  tag: "4px"
  desk: "12px"
spacing:
  small: "8px"
  medium: "16px"
  large: "24px"
  page: "3.4%"
components:
  button-primary:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.paper}"
    rounded: "{rounded.control}"
    padding: "10px 13px"
  revision-action:
    textColor: "{colors.primary}"
    height: "32px"
---

# NPOV Radar design system

## Overview

The evidence desk keeps a ranked queue beside an open comparison document. Cool paper surfaces and restrained UI type let the quotations carry the reading. This is an operational editor tool, with visible provenance and cautious status language.

## Colors

Ink, muted text and thin rules define the document structure. Blue marks navigation and selected content. Amber identifies a review lead, while green means extracted dates match. Neither color is a general truth or confidence verdict.

## Typography

Public Sans is self-hosted as a variable WOFF2. Georgia distinguishes source evidence from UI language. The headline is 28px on desktop and 25px on mobile. Evidence quotations are 15px at the normal desktop breakpoint, 14px on compact desktop, 16px when columns stack, and 17px on phones. Monospace is reserved for SQL and measured data.

Exact revision links are primary actions, 12px with a 32px click height on desktop and 13px with a 44px height on mobile. Other secondary metadata is smaller; its smallest existing values are not a pattern for primary actions.

## Layout

The header is 66px. Desktop outer margins are 3.4%. The desk has a 300px article queue and a 165px passage queue. The ranked article list is bounded to 320px and scrolls the current selection into view without changing rank. Passage entries include real English previews so repeated section names remain distinguishable.

Below 900px, the passage selector becomes horizontal and quotations stack. Below 620px, the article queue is also horizontal, and the current selected card remains visible. Workspace chrome is compact so the first desktop viewport contains meaningful text in all three language columns. Status sits beside the section heading.

## Elevation & Depth

The application uses tonal surfaces and thin borders, with no decorative shadows. White evidence documents sit on a cool near-white page; selected rows use a pale blue field.

## Shapes

The outer desk uses a 12px radius. Controls use 4–6px radii. Quotations are document columns separated by rules, rather than nested cards. Icons use a consistent Lucide stroke; the radar brand mark is simple geometric linework.

## Components

Primary buttons use navy with white text and a 5px radius. Secondary buttons use a white field and thin rule. Inputs use a white field, subtle stroke and visible keyboard outline. Navigation uses an underline for the active view.

The article queue preserves rank through search. The passage queue shows section, excerpt and restrained status. Revision provenance links to the exact stored revision. Review marks are local to the device; review-note copying happens only on a user click.

The source-support label is scoped to the claim actually checked. Synthetic tests are visibly separate from real article evidence. Live connectivity and saved-result states remain distinct. The single connection pulse respects reduced motion.

## Do's and Don'ts

- Do preserve exact quotations, revision links and clear uncertainty.
- Do keep the selected queue position visible and passage entries distinguishable.
- Do keep actionable revision text at the measured sizes above.
- Don't turn cosine similarity into a confidence or neutrality score.
- Don't place a status tag as an eyebrow above a heading.
- Don't add decorative imagery, texture or shadows to the evidence columns.

Post-build review: the independent reviewer scored all five requested UI fixes resolved on current desktop/mobile IAB captures, with disposition `ship` for those fixes. This is not a broader full-site accessibility certification. The older supplemental history capture was excluded from the typography verdict; history functionality was separately verified through IAB.
