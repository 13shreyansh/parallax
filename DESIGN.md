# Design system

The application is an editorial comparison desk, with a ranked queue on the left and source-bearing evidence on the right. The main use is reading and comparing, so the desk uses a light background suited to a bright work area.

UI type is self-hosted Public Sans. Evidence quotations use Georgia to distinguish article text from interface language. Monospace is reserved for SQL and measured values. Source passages wrap without truncation; the alternatives are expandable.

Color tokens in src/style.css:

- Background #f4f7f8, paper #ffffff, ink #183446.
- Secondary text #526976, selection/action blue #1c5e9a, rules #d7e1e6.
- Review lead amber #835516, matching-date green #326d53.

A 12px radius belongs to the outer desk; 4–6px radii belong to inputs and controls. Borders separate related documents. No decorative shadows or illustrations are used. The compact top navigation switches between the worklist and method/evaluation view.

At desktop widths the article queue occupies 300px and the passage queue 165px. The three language columns share the remaining width. Below 900px the passage list becomes a horizontal selector and quotes stack. Below 620px the article list also becomes a horizontal selector. Controls retain keyboard focus rings. Selection, scrollbars, inputs, loading, empty and offline/error states use the same colors.

The source-support label is scoped to the date it actually verifies. The synthetic test uses an explicit label and a separate tinted copy. Live connection and saved-results states are distinct. Review status is local to the device.

The sole entrance accent is a one-time live-connection pulse. It respects reduced motion. The direction contract is in .impeccable/worklist-brief.md. Final visual verification is pending Chief IAB screenshots; this document records implemented tokens, not a completed visual sign-off.
