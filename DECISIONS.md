# Parallax implementation decisions

## Ask retrieval threshold

The accepted best-claim cosine distance is at most **0.45**. This was chosen from a small development query sample on the live theme, independently measured by gpt-6-astra on release 72f655a. Five relevant fi/sv/en questions had best-claim distances 0.15688–0.25990. Six unrelated queries had distances 0.59555–0.77418. This is a small development calibration, not a held-out accuracy estimate.

The SQL reserves up to 18 claim candidates and 18 source passages before merging them, so source chunks cannot remove every article candidate. German and Russian remain comparison-only. Among nearby claims, a reviewed finding may be selected within 0.12 cosine distance of the closest claim; the original nearest passages remain visible.

Validated Finnish question: “Kuinka monta ruotsalaista vapaaehtoista kuului Svenska Frivilligkåreniin?” It retrieves the real Swedish claim whose own archived source gives a different count. No answer is generated at query time.

## History

Revision dates describe exact wording unless a material boundary has been separately verified against the complete parent revision. The equipment-performance source flag has that additional verification. Similar historical wording is displayed from the actual stored revision; failed alignment is labeled as such, rather than declared absent.

## Hosting

Vercel rejected further builds at its account-wide 100-deployment daily limit. The new Parallax project's promoted routing rule serves its verified frontend and API from the isolated VPS. The served HTML records the actual release commit, separately from the older Vercel build record. Existing projects and Traefik/SSH configuration were not changed.

## Coverage prompt v5 and third held-out run

The v4 run (32/40) and second disjoint run (34/40) remain held out and are never reused as development data. Version5 clarifies that a supplied complete empty article has no coverage, while an absent language key is unknown, and that textual coverage is distinct from supporting-source verification. Development used three Winter War passage pairs and three clean controls only:2/3 omissions caught,0/3 clean flags. The prompt was then frozen before the third run.

The third article families were reserved separately before labeling. A blind gpt-6-astra pass labeled40 source-supported controls before any detector output. Their exact excerpts, literal source passages and real English citation URLs were verified mechanically. The third run caught40/40 planted errors with0/40 false flags. It retains the first two measurements. Its numeric perturbation is double plus7 rather than plus7, because small perturbations can remain compatible with approximate figures; date changes are plus10 years. This changed severity limits comparisons across rounds. Eight dropped passages retain actual Finnish/Swedish counterpart citation text; a supporting-source suggestion is still forbidden without a readable supporting document. Published v4 findings remain independently reviewed; the latest evaluation validates the clarified v5 coverage prompt, not a retroactive v5 rerun of every published finding.
