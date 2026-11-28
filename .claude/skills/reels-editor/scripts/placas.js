const fs=require('fs');const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
for(const f of fs.readdirSync('placasN').filter(x=>x.endsWith('.html'))){
  await p.goto('file://'+process.cwd()+'/placasN/'+f,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
  await p.screenshot({path:'placasN/'+f.replace('.html','.png'),omitBackground:true});}
await b.close();})();
