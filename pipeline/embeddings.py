import os
from .common import ROOT

MODEL='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
def encoder(device='mps'):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL,cache_folder=os.environ.get('PARALLAX_MODEL_CACHE',str(ROOT/'work/models')),device=device,local_files_only=os.environ.get('HF_HUB_OFFLINE')=='1')
