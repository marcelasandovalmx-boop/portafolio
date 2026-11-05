const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--autoplay-policy=no-user-gesture-required']});const p=await b.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+process.cwd()+'/synthflow-copia.html',{waitUntil:'load',timeout:60000});
const r=await p.evaluate(async()=>{
  const out={};const toB64=async blob=>{const a=new Uint8Array(await blob.arrayBuffer());let s='';for(let i=0;i<a.length;i+=32768)s+=String.fromCharCode.apply(null,a.subarray(i,i+32768));return btoa(s)};
  const cola=[];window.downloadBlob=(blob,name)=>cola.push([name,blob]);
  try{initAudioEngine()}catch(e){}
  selectGenre('lofi');
  const buf=await renderProceduralTrackOffline(206,48000);
  out['musica-lofi.wav']=await toB64(encodeAudioBufferToWAV(buf,16,false,true));
  for(const t of ['whoosh','uiclick']){await downloadSingleSFX(t)}
  for(const [n,bl] of cola) out[n]=await toB64(bl);
  out._seed=String(state.seed);return out});
for(const [n,v] of Object.entries(r)){if(n.startsWith('_')){console.log(n,v);continue}fs.writeFileSync(n,Buffer.from(v,'base64'));console.log('ok',n)}
console.log('errores:',errs.slice(0,5));await b.close()})();
