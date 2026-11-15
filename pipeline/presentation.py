"""Exclude extraction syntax from editor-facing claim text; preserve raw records."""
import re

def readable(text):return bool(text and not re.search(r'\||\{\{|\[\[',text))

def readable_groups(groups):
 out=[]
 for g in groups:
  g={**g,'versions':{lang:v for lang,v in g['versions'].items() if readable(v.get('text'))}}
  if g['versions']:out.append(g)
 return out
