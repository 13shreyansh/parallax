"""Frozen v2 confirmation article selection from official S, no scoring here."""
import pyarrow.parquet as pq,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
titles=['Great Fire of Turku','Juho Kusti Paasikivi','Urho Kekkonen','Treaty of Fredrikshamn','Finnish famine of 1866–1868']
rows=pq.read_table(root/'work/vector-starter/data/articles-en.parquet').to_pylist()
chosen=[next(r for r in rows if r['title']==t) for t in titles]
json.dump(chosen,open(root/'work/confirmation-articles.json','w'),ensure_ascii=False)
print('Prepared',len(chosen),'frozen confirmation articles')
