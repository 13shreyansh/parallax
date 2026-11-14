"""Stored neutral note templates. No browser-generated findings or live prose."""
import os

NAMES={'fi':'Finnish','sv':'Swedish','en':'English','de':'German','ru':'Russian'}
def fill_note(flag,articles):
    lang=flag['language'];target=flag.get('missing_language',lang)
    article=articles.get(target) or articles.get(lang)
    writing=target if target in ['fi','sv','en'] else 'en'
    v=flag['versions'][lang];quote=v['text'];url=f'https://{lang}.wikipedia.org/w/index.php?oldid={v["rev_id"]}'
    site=os.environ.get('PARALLAX_PUBLIC_ORIGIN','https://parallax-13shreyanshs-projects.vercel.app')
    headings={
        'en':{'src':'Claim and cited source do not match','lang':'A claim differs between language versions','tone':'A suggestion for neutral wording','fact':'A date, number or name differs between versions'},
        'fi':{'src':'Väite ja sen lähde','lang':'Kieliversioiden välinen ero','tone':'Ehdotus neutraaliksi sanamuodoksi','fact':'Kieliversioiden päivämäärä, luku tai nimi eroaa'},
        'sv':{'src':'Påstående och angiven källa','lang':'Skillnad mellan språkversionerna','tone':'Förslag till neutral formulering','fact':'Datum, tal eller namn skiljer sig mellan versionerna'}}
    start={'en':'The article says','fi':'Artikkelissa sanotaan','sv':'I artikeln står'}[writing]
    origin={'en':f'The {NAMES[lang]} article says','fi':f'Kieliversiossa {lang} sanotaan','sv':f'I språkversionen {lang} står'}[writing]
    lines=[f'== {headings[writing][flag["check"]]} ==',f'{origin}: "{quote}" ({url}).']
    if flag.get('source') or flag.get('supporting_source'):
        s=flag.get('source') or flag['supporting_source'];label={'en':'The cited source','fi':'Artikkelin lähde','sv':'Den angivna källan'}[writing]
        lines.append(f'{label}, {s["title"]} ({s["url"]}), {start.lower()}: "{s["passage"]}".')
        if s.get('archive_url'):lines.append(s['archive_url'])
    for other,x in flag['versions'].items():
        if other==lang:continue
        label={'en':'For comparison','fi':'Vertailuksi','sv':'Som jämförelse'}[writing]
        lines.append(f'{label} ({other}): "{x["text"]}" (https://{other}.wikipedia.org/w/index.php?oldid={x["rev_id"]}).')
    if flag.get('suggestion'):
        label={'en':'A possible wording to consider','fi':'Mahdollinen sanamuoto harkittavaksi','sv':'En möjlig formulering att överväga'}[writing]
        lines.append(f'{label}: "{flag["suggestion"]["text"]}".')
    endings={
        'en':f'Could someone familiar with the topic check these passages? I found them with Parallax ({site}), which compares language versions and cited sources. Please read the original quotes and sources before making an edit. ~~~~',
        'fi':f'Voisiko aiheeseen perehtynyt tarkistaa nämä kohdat? Löysin ne Parallax-palvelulla ({site}), joka vertaa kieliversioita ja viitattuja lähteitä. Alkuperäiset kohdat ja lähteet on hyvä lukea ennen muokkausta. ~~~~',
        'sv':f'Kan någon som känner ämnet granska dessa avsnitt? Jag hittade dem med Parallax ({site}), som jämför språkversioner och angivna källor. Läs originalcitaten och källorna innan en ändring görs. ~~~~'}
    lines.append(endings[writing]);flag['note']='\n\n'.join(lines);flag['note_language']=target;flag['note_title']=article['title'] if article else None;return flag
