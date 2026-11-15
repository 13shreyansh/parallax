export function instant(value){
 if(value===null||value===undefined||value==='')return new Date(NaN);
 if(typeof value==='string'&&/^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}/.test(value)){
  value=value.replace(' ','T');if(!/(?:Z|[+-]\d\d:\d\d)$/.test(value))value+='Z';
 }
 return new Date(value);
}
export function date(value){const d=instant(value);return Number.isNaN(d.getTime())?'':d.toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric',timeZone:'UTC'});}
export function dateTime(value){const d=instant(value);return Number.isNaN(d.getTime())?'':d.toLocaleString('en-GB',{day:'numeric',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit',timeZone:'UTC'})+' UTC';}
export function day(value){const d=instant(value);return Number.isNaN(d.getTime())?'':d.toISOString().slice(0,10);}
export const today=()=>day(new Date());
