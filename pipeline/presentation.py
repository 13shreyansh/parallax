"""Exclude extraction syntax from editor-facing claim text; preserve raw records."""
import re

def readable(text):return bool(text and not re.search(r'\||\{\{|\[\[',text))

def readable_groups(groups,valid_ids=None):
 out=[]
 for g in groups:
  g={**g,'versions':{lang:v for lang,v in g['versions'].items() if readable(v.get('text')) and (valid_ids is None or v.get('claim_id',v.get('id')) in valid_ids)}}
  if g['versions']:out.append(g)
 return out
