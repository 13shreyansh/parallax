https://parallax-gamma-red.vercel.app
Parallax compares Wikipedia claims with their own cited sources and other language versions.
Scope: 22 Finland in the Second World War topics, fi/sv/en; Winter War de/ru comparison only.
Acceptance: real stored findings, exact quotes, readable evidence and revision boundaries.
Hosting: isolated VPS MariaDB 11.8 and API, TLS, private SQL socket; new Vercel project.
Validation: deployed desktop/mobile flow, frozen held-out evaluation and independent blind review.

ENTRY: Parallax / Job 05 in progress / 4fe4330182bdb453b06141b668985c98f9649dce / https://parallax-gamma-red.vercel.app
DONE:
- VPS MariaDB 11.8.9 and API are running; HTTPS health verified. All active vectors, source passages and 14,726 revisions imported.
- Read-only container import and Unix-socket authentication bugs fixed and regression checked.
- Home and Winter War are live. Ask, Method and time travel are hidden until verified.
NUMBERS: measured held-out 32/40 planted errors caught (80%), 0/40 false flags; dropped sentences 0/8. Blind gpt-6-astra review confirmed 53/60 (88.3% precision); six false and one uncertain were hidden, including mirrored counterparts. Previous baseline measured 5/36. The theme now has publication-ready flags with generated editor notes; exact live counts are queried from the hosted database. The first hosted snapshot had 12, then was refreshed to 77 before review.
SCREENSHOTS: artifacts/e2e/core-home-1440.png; artifacts/e2e/core-home-390.png; artifacts/e2e/core-source-390.png
REVIEW: blind evidence precision measured 53/60; separate spec and build passes pending.
NEXT: release core screens, then verify each remaining feature and redeploy.
NEEDS DECISION: none
BLOCKED: none

## Hosting used
Hostinger VPS 72.61.22.106, isolated parallax-db and parallax-api containers. API HTTPS origin: https://parallax.72.61.22.106.sslip.io. MariaDB has networking disabled and uses a private Unix socket; no SQL port is published. API filesystem is read-only, with runtime writes only in /tmp. TLS is terminated by the existing Traefik Docker provider; its configuration and the other projects were not modified. Reader has SELECT only; writer is restricted to review and note-copy tables. Vercel proxies the API with a server-side token. No tunnel is used.

## Spec gaps I filled
- One Home theme and Ask restricted to it, authorized by Job 03.
- Initial release hides Ask, Method and time travel, authorized by Job 05; they return after verification.
- Revision entry dates establish the first stored appearance of exact wording, not necessarily the first appearance of an idea. Historical source support remains unknown.

## Source recovery
Measured Winter War before: 67 Read, 61 Source unreachable, 8 Book, not checked (136 total). After: 110 Read, 20 Source unreachable, 8 Book, not checked (138 total; two extra URLs from citation reconciliation). Archive closest-snapshot retry ran first, then Context.dev. Context usage measured 134 credits, below the 3,000 cap.

## REAL FINDINGS, Job 03 milestone 2026-11-14T22:39:31Z
Measured: 16 shown Winter War flags. Argon confirmed these against stored evidence; blind precision has not been measured yet. Entries below establish exact wording, not conceptual first appearance.

### 1. Not in source
- Claim (fi, revision 24373824): Puna-armeijan mekanisoitu kalusto oli osin soveltumatonta metsäsodankäyntiin, toimi vain aukeilla ja teillä eikä useinkaan kestänyt kovia pakkasia.
- Finding: The cited 2020 thesis on pre-war military press does not establish how Red Army mechanized equipment performed in forest warfare or severe frost.
- Source passage: Käsitys suomalaisen maaston epäedullisuudesta
panssarivaunuille oli puolustuslaitoksessa yleinen aina 1930-luvun puoleenväliin saakka. Vasta
vuonna 1934 Karjalankannaksella toteutetut uudet panssarivaunujen ajokokeet osoittivat
käsityksen vääräksi. (https://erepo.uef.fi/bitstream/handle/123456789/23681/urn_nbn_fi_uef-20201456.pdf?sequence=1&isAllowed=y)
- Entry edit: https://fi.wikipedia.org/w/index.php?diff=12389576, 2012-11-28 18:04:48Z. Historical source support: not established.

### 2. Loaded wording
- Claim (sv, revision 59855895): Ytterligare en märklig omständighet är att de cirka 5 000 sovjetiska krigsfångarna vilka togs av den finländska armén och efter kriget återbördades till Sovjet, är spårlöst försvunna (enligt ryska och finska källor.)
- Finding: Swedish uses editorializing wording ('en märklig omständighet') in narrator voice when introducing the fate of returned Soviet POWs.
- Other version (en, revision 1384334162): Of these, 450 were released, 4,354 were sentenced to imprisonment in labour camps ranging from 3 to 10 years and 414 were exposed to be "active in traitorous activities while in captivity", with 334 criminal cases being transferred to the Supreme Court of the Soviet Union; 232 of those cases ended in a death penalty.
- Source passage: no independently supporting source passage stored for this language/tone comparison yet; no source contradiction is claimed for it.
- Entry edit: https://sv.wikipedia.org/w/index.php?diff=27568032, 2014-09-17T06:32:49Z. Historical source support: not established.

### 3. Missing in Finnish
- Claim (en, revision 1384334162): The ranks of RNA were to be filled by prisoners-of-war, but it would be commanded by White émigrés instead of captured Soviet Army officers, who were deemed unreliable.
- Finding: English and Russian cover the formation of the anti-Soviet 'Russian People's Army' (RNA) from Soviet POWs under White émigré officers; this is absent in Finnish.
- Source passage: Erittäin salaisen operaation puitteissa Feodor Schulgin alkoi koota joukko-osastoja, jotka koostuisivat noin 200 värvätystä sotavangista. Operaatio oli Päämajan tiedusteluosaston alainen. Olen löytänyt arkistoista asiakirjoja, jotka todistavat tämän. Niistä käy muun muassa ilmi, että sotavankeja värväsivät Suomen ROVS:n jäsenet. Muodollisesti he toimivat tiedusteluososton erikoiskuulustelijoina. Leireillä olleita Puna-armeijan upseereita pidettiin epäluotettavina. Tästä syystä päätettiin, että joukko-osaston päällystö muodostetaan Suomen ROVS-osaston upseereista. (https://yle.fi/uutiset/3-11254603)
- Entry edit: https://en.wikipedia.org/w/index.php?diff=1092157805, 2022-06-08T14:23:55Z. Historical source support: not established.

### 4. Missing in Finnish
- Claim (en, revision 1384334162): Further contributing to the legend of Kollaa was the sniper Simo Häyhä, dubbed "the White Death" in Finnish media, credited with over 500 kills in the war.
- Finding: English and Swedish mention sniper Simo Häyhä ("the White Death") and his over 500 kills, whereas he is not mentioned in the Finnish article.
- Source passage: Sotasankari Simo Häyhän ennennäkemätön päiväkirja löytyi - "Tässä on minun syntilistani"
Legendaarinen tarkka-ampuja kirjoittaa ampuneensa yli 500 neuvostosotilasta. (https://www.iltalehti.fi/kotimaa/a/201707172200270836)
- Entry edit: https://en.wikipedia.org/w/index.php?diff=1299597741, 2025-07-09T09:39:55Z. Historical source support: not established.

### 5. Missing in Swedish
- Claim (en, revision 1384334162): When he signed the document, the tormented president uttered the well-known words: "Let the hand wither that signs this monstrous treaty!" Ironically, his right arm was paralysed the following summer, and he was forced to switch his writing hand.
- Finding: English mentions President Kallio's famous curse upon signing the peace mandate and his subsequent arm paralysis; this is absent in Swedish.
- Source passage: Ei ihme, että presidentti Kyösti Kallio oli synkissä tunnelmissa antaessaan valtuutuksen rauhasta neuvotelleelle, Risto Rytin johtamalle valtuuskunnalle.
– Kuivukoon käteni, joka on pakotettu tällaisen paperin allekirjoittamaan, Kallio totesi.
Rauhanteon jälkeen Kallio murtui ruumiillisesti ja henkisesti. Puoli vuotta myöhemmin hänen kätensä halvaantui. (https://www.is.fi/kotimaa/art-2000009449470.html)
- Entry edit: https://en.wikipedia.org/w/index.php?diff=1343076156, 2026-03-12T03:12:36Z. Historical source support: not established.

### 6. Missing in Swedish
- Claim (en, revision 1384334162): After 15 months of Interim Peace, in June 1941, Germany commenced Operation Barbarossa, and the Continuation War between Finland and the Soviets began.
- Finding: English and Finnish state that the Interim Peace was followed by the Continuation War in June/summer 1941; the Swedish article does not state this consequence.
- Other version (fi, revision 24373824): Sotaa seurasi välirauha, jonka aikana Suomi lähentyi Saksan kanssa, ja jota kesällä 1941 seurasi jatkosota.
- Source passage: no independently supporting source passage stored for this language/tone comparison yet; no source contradiction is claimed for it.
- Entry edit: https://en.wikipedia.org/w/index.php?diff=1077761055, 2022-03-18T02:11:44Z. Historical source support: not established.

### 7. Missing in Swedish
- Claim (en, revision 1384334162): The 7th Army, comprising nine divisions, a tank corps and three tank brigades, was located on the Karelian Isthmus.
- Finding: English and Finnish detail the initial strength and deployment of the Soviet 7th Army on the Karelian Isthmus; this is absent in Swedish.
- Other version (fi, revision 24373824): 7. armeijaan kuului yhdeksän jalkaväkidivisioonaa, panssariarmeijakunta ja kolme panssariprikaatia.
- Source passage: no independently supporting source passage stored for this language/tone comparison yet; no source contradiction is claimed for it.
- Entry edit: https://en.wikipedia.org/w/index.php?diff=556795759, 2013-05-25T23:50:24Z. Historical source support: not established.

### 8. Missing in English
- Claim (fi, revision 24373824): Suomalaisten merkittävä vahvuus oli myös radiotiedustelu eli vihollisen radioliikenteen sieppaus, paikantaminen ja salakirjoitussanomien avaaminen.
- Finding: The Finnish article highlights radio intelligence and codebreaking as a significant Finnish strength, which is absent from the English article.
- Source passage: Suomalaisten merkittävä vahvuus oli myös radiotiedustelu eli vihollisen radioliikenteen sieppaus, paikantaminen ja salakirjoitussanomien avaaminen. (https://www.oruk.fi/2020/03/14/talven-soturit/)
- Entry edit: https://fi.wikipedia.org/w/index.php?diff=704318, 2006-01-15 17:29:43Z. Historical source support: not established.

### 9. Missing in Swedish
- Claim (en, revision 1384334162): From there, the 7th Army was to continue towards Lappeenranta, then turn west towards Lahti, before the final push to the capital Helsinki.
- Finding: English and Finnish state the Soviet objective on the Karelian Isthmus was to advance via Viipuri to Helsinki; this planned advance route is missing in Swedish.
- Source passage: no independently supporting source passage stored for this language/tone comparison yet; no source contradiction is claimed for it.
- Entry edit: https://en.wikipedia.org/w/index.php?diff=1188277158, 2023-12-04T10:54:44Z. Historical source support: not established.

### 10. Missing in English
- Claim (fi, revision 24373824): Panssarintorjuntatykkejä oli vain kolmannes suunnitellusta määrästä.
- Finding: The Finnish article states that Finland had only one-third of the planned number of anti-tank guns; this numerical detail is absent in English.
- Source passage: no independently supporting source passage stored for this language/tone comparison yet; no source contradiction is claimed for it.
- Entry edit: https://fi.wikipedia.org/w/index.php?diff=704318, 2006-01-15 17:29:43Z. Historical source support: not established.

## Job 05 live milestone, 01:22 Helsinki
Core release 4fe4330 verified public at https://parallax-gamma-red.vercel.app. VPS HTTPS health reports that exact commit. Deployed Chromium core flow passed at 1440x900 and 390px with zero console errors and no horizontal overflow. Phone evidence-sheet screenshots now wait for the animation to finish. Source-backed language fixes and Gemini-generated editor notes are stored. The next release applies independent review exclusions and fixes a slow temporal lookup (qid scanned all historical bodies; versioned primary-key branches seek each language page).

## Job 05 expanded release, 01:56 Helsinki
Expanded release 72f655a428eb80dcd37d5b541c091910325aebc4 passed the deployed read flow on the VPS and the staged Vercel routing alias at 1440x900 and 390px, with zero console errors and no page overflow. The Vercel project route was promoted to proxy its verified VPS frontend and API; the original Vercel build remains aa7c19e because the account hit its 100-deploy daily limit. No purchase or other project configuration was changed. Public propagation and a repeat on the public URL are being checked.

Fresh independently labeled, disjoint article-family controlled test: measured 34/40 errors caught (85%), 0/40 false flags, including 2/8 dropped sentences. First held-out remains 32/40 (80%), 0/40 false flags. Neither result reaches the 90% recall target. Prompts were frozen before each measurement; the results are not relabeled as development performance.

Source-recovery counts above concern cited URL records: 67 Read / 61 unreachable / 8 book-preview URLs before, 110 Read / 20 unreachable / 8 book-preview URLs after. A separate current count finds 550 offline book reference records on Winter War; these remain Book, not checked.
