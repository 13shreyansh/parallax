# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Delegated by the autonomous build brief. React and Vite on Vercel; Python ingestion and a small read-only API; MariaDB native vector search and system-versioned tables. These are implementation choices inferred from the authorized scope.

## Users

Wikipedia editors who know Finnish history and want a prioritized list of passages to examine across Finnish, Swedish and English.

## Product purpose

Show exact language-version evidence and explain why a passage deserves attention. Help a human make a source-grounded editorial decision.

## Capabilities and constraints

Align real passages with multilingual vectors queried in MariaDB. Keep revision IDs and original timestamps. Show known coverage differences without calling them factual errors. Expose source checks as cannot verify unless an accessible quotation supports a verdict. Never edit Wikipedia. Show synthetic evaluation cases separately from Wikipedia.

## Evidence on hand

Sponsor's S dataset includes three languages and linked Wikidata IDs. M includes Finnish revision history; L includes current Finnish text. No human annotations available. Evaluation limits must be visible. All code is new for Junction 2026; code is MIT and Wikipedia text remains CC BY-SA 4.0.

## Product principles

Evidence before verdict. Audience emphasis is valid. Unknown is a useful result. Humans decide and edit.
