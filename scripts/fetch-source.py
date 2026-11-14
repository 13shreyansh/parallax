"""Fetch the single curated source example. Do not crawl arbitrary user URLs."""
import requests,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
r=requests.get('https://yle.fi/a/3-5823726',headers={'User-Agent':'NPOVRadar/0.1 source-check research'},timeout=30);r.raise_for_status()
(root/'work/source-yle.html').write_text(r.text)
assert 'February 21, 1808' in r.text,'The cited source changed; inspect it before using the curated example.'
print('Source retrieved; exact excerpt present. Review the source before rerunning update-findings.')
