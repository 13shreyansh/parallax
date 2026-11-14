// Fixed read-only proxy. Neither the caller nor stored article text chooses an upstream URL.
export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');
 if(req.method!=='GET')return res.status(405).json({error:'Only GET is supported.'});
 const allowed=new Set(['health','align','history','asof','probe']);
 const mode=typeof req.query.mode==='string'?req.query.mode:'health';
 if(!allowed.has(mode))return res.status(400).json({error:'Unknown query mode.'});
 const origin=process.env.RADAR_API_ORIGIN;
 if(!origin)return res.status(503).json({error:'Live database is not configured. Saved MariaDB evidence remains available.'});
 try{
  const url=new URL('/'+mode,origin);
  for(const k of ['id','qid','lang','date','mutation'])if(typeof req.query[k]==='string'&&req.query[k].length<=90)url.searchParams.set(k,req.query[k]);
  const r=await fetch(url,{signal:AbortSignal.timeout(12000),headers:{Accept:'application/json'}});
  const j=await r.json();return res.status(r.status).json(j);
 }catch{return res.status(503).json({error:'The live database is offline. Saved MariaDB evidence remains available; retry when the build Mac reconnects.'})}
}
