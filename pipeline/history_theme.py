"""Cache genuine fi/sv/en history for every article in the active theme."""
import concurrent.futures
from .common import db
from .history import cache_api_history,load_history,onset

def main():
 c=db();cur=c.cursor();cur.execute("SELECT a.* FROM article a JOIN topic_theme t ON t.qid=a.qid WHERE t.theme='finland-second-world-war' AND a.lang IN ('fi','sv','en') ORDER BY a.qid<>'Q134949',a.qid,a.lang");articles=cur.fetchall();c.close()
 def work(a):
  try:cache_api_history(a);load_history(a)
  except Exception as e:print('History retry needed',a['qid'],a['lang'],type(e).__name__,flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(work,articles))
 for qid in dict.fromkeys(a['qid'] for a in articles):
  try:onset(qid);print('Onset complete',qid,flush=True)
  except Exception as e:print('Onset retry needed',qid,type(e).__name__,flush=True)
if __name__=='__main__':main()
