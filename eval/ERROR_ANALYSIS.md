# Agent inspection of 36 real alignments

Reviewed the saved sample in `agent-inspection-sample.json`, four spaced passages from each of the nine topics. These are agent observations of excerpts, not human gold labels. No semantic accuracy percentage is derived from this inspection.

What the traces showed:

- Related text is often a good match. The Mannerheim examples about school expulsion and buying horses are close in content at cosine similarities around 0.92. Calling these "different emphasis" would overstate what the classifier knows. The UI now calls this category "Related passages".
- A low score is not an omission. The Häyhä example `fi-24889-69` and its English match both discuss avoiding groups, yet similarity is only 0.37. The UI now says "Weak alignment" and preserves the alternatives, rather than asserting a coverage gap.
- Other low-scoring matches do appear off topic at passage level, such as a shooting-verification sentence matched to later NATO-related interest. These are retrieval failures or possible coverage differences, which the current evidence cannot separate.
- Dates anchor some good matches: the Winter War introduction, Continuation War introduction, Mannerheim birth/death dates and Moscow Peace Treaty start-date passage. Matching dates verify only those extracted dates.
- Scope can diverge even when the topic is similar. A percentage of Reds among total deaths and a percentage of civilians in a different casualty group produced a numerical false lead in development. The numeric similarity threshold was raised; that observation does not establish general numeric precision.
- Date expressions such as a span of days, dates without years, and relative dates are not comprehensively normalized. Some relevant passages have no usable full date and therefore never enter the weak date-overlap retrieval benchmark.

Decision: keep date/unit warnings conservative, keep source checks scoped, show the exact passage and alternatives, and leave the human-label sheet blank until an editor/historian labels it. More automatic verdict labels would hide the failures already visible in these traces.
