# Data licenses and attribution

The MIT license applies to the new project code and its original documentation. It does not relicense Wikipedia text, Wikipedia-derived data, embeddings, or cited-source excerpts.

Wikipedia text, revision text, passage extracts, quotes in snapshot.json, the derived sentence embeddings, and real text in evaluation fixtures are by Wikipedia's contributors and remain under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Derived and redistributed text in this repository is offered under that license. Each passage keeps its language, page ID and revision ID. Attribution links have this form:

`https://LANG.wikipedia.org/w/index.php?oldid=REV_ID`

The deployed application links each displayed passage to its exact revision, whose history identifies the contributors. The data files are not covered by the project MIT grant.

Data sources:

- [MariaDB Foundation Wikipedia datasets](https://github.com/MariaDB/mariadb-wikipedia-datasets), S/M/L October 2026 releases, Robert Silén. The S release derives from FineWiki; M derives from Wikimedia revision dumps. Downloaded M/L files were verified against release SHA256SUMS.
- [MariaDB vector Wikipedia starter](https://github.com/MariaDB/mariadb-vector-wikipedia-rag), used for the supplied S Parquet files and setup documentation. No application code copied.
- [MariaDB system-versioned Wikipedia starter](https://github.com/MariaDB/mariadb-system-versioning-wikipedia), consulted for native SVT import behavior. This application and importer were written during the event.
- Live fi, en and sv Wikipedia APIs, fetched during this build. Original revision times are separate from fetch time.

The model is [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2), whose model card declares Apache-2.0. Model weights are downloaded locally and are not committed. Runtime packages retain their own licenses.

A short quotation from Yle News, "Southern Towns Mark War of Finland Bicentennial", 21 February 2008, appears solely to support the start-date source-check example. Copyright remains with Yle. [Original report](https://yle.fi/a/3-5823726). The HTML page is not redistributed. The source-evidence record retains the retrieval hash and URL. This source is referenced in the English Finnish War article; the displayed check supports only the start date, not every statement in the passage.

The synthetic evaluation mutations are deliberately altered text. They are marked synthetic in every fixture and are never presented as real Wikipedia revisions.

The self-hosted Public Sans font is distributed under the SIL Open Font License in `public/fonts/LICENSE.md`. Its license is separate from project code.
