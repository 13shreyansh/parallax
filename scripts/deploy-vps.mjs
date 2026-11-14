// Secrets are generated and transmitted in memory, never written to artifacts or stdout.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import { spawn } from 'node:child_process';
const project='prj_snWccxKPuKjCWZR1J7LA6ADSZo0k',team='team_SjINqXczvI3i0JpBv7JRMqQN';
const auth=JSON.parse(await fs.readFile(`${process.env.HOME}/Library/Application Support/com.vercel.cli/auth.json`,'utf8'));
const bridge=crypto.randomBytes(36).toString('base64url');
async function env(key,value,type='sensitive'){
 const r=await fetch(`https://api.vercel.com/v10/projects/${project}/env?teamId=${team}&upsert=true`,{method:'POST',headers:{Authorization:`Bearer ${auth.token}`,'Content-Type':'application/json'},body:JSON.stringify({key,value,type,target:['production','preview']})});
 if(!r.ok)throw new Error(`Environment configuration failed (${r.status})`);
 console.log(JSON.stringify({configured:key}));
}
await env('PARALLAX_BRIDGE_TOKEN',bridge);
await env('PARALLAX_API_ORIGIN','https://parallax.72.61.22.106.sslip.io','plain');
const sha=(await fs.readFile('work/parallax/deploy-commit.txt','utf8')).trim();
const child=spawn('ssh',['-o','BatchMode=yes','-o','ConnectTimeout=10','root@72.61.22.106','python3','/opt/parallax/source/deploy/bootstrap_remote.py'],{stdio:['pipe','pipe','pipe']});
child.stdin.end(JSON.stringify({bridge_token:bridge,commit:sha}));
let output='';child.stdout.on('data',b=>{output+=b;});child.stderr.on('data',b=>{output+=b;});
const code=await new Promise(resolve=>child.on('exit',resolve));
console.log(output.replaceAll(bridge,'[redacted]'));
if(code)process.exit(Number(code));
for(let i=0;i<36;i++){
 try{const r=await fetch('https://parallax.72.61.22.106.sslip.io/health',{headers:{'X-Parallax-Token':bridge}});if(r.ok){console.log(JSON.stringify({https_verified:true,...await r.json()}));break;}}catch{}
 await new Promise(resolve=>setTimeout(resolve,5000));
}
