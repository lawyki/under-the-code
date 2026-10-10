import { chromium } from 'playwright';
const B='http://localhost:8798', T='tokenEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE';
let pass=0, fail=0; const ok=(c,n,d='')=>{ if(c){pass++;console.log('PASS',n);} else {fail++;console.log('FAIL',n,d);} };
const b = await chromium.launch();
async function device(vp){ const ctx = await b.newContext({ viewport: vp });
  await ctx.addCookies([{name:'__Host-under_session',value:T,domain:'localhost',path:'/',secure:true,httpOnly:true,sameSite:'Lax'},{name:'under_signedin',value:'1',domain:'localhost',path:'/',secure:true,sameSite:'Lax'}]);
  const errs=[]; ctx.on('page', p=>{p.on('pageerror',e=>errs.push(e.message));}); return {ctx, errs}; }
const db = (q) => fetch(B+q,{headers:{Cookie:'__Host-under_session='+T}}).then(r=>r.json());
// Device A
const A = await device({width:1440,height:900});
const pa = await A.ctx.newPage();
await pa.goto(B+'/part-1?utc-debug#ch1-kernel-p3'); await pa.waitForTimeout(2500);
await pa.click('.place-btn'); await pa.waitForTimeout(300);
await pa.click('.pb-set'); await pa.waitForTimeout(1500);
let pos = await db('/api/position');
ok(pos.position && pos.position.src==='set' && pos.position.cid && pos.position.seq>=1, 'A: set place stored on server with src/cid/seq', JSON.stringify(pos.position));
let sA = await pa.evaluate(()=>__utcPlace.snapshot());
ok(sA.state==='PINNED' && sA.sync==='synced', 'A: PINNED and synced (solid)', sA.state+' '+sA.sync);
ok(await pa.evaluate(()=>document.querySelector('.cue-mark').classList.contains('is-synced')), 'A: mark drawn solid');
await pa.keyboard.press('Escape');
await pa.evaluate(()=>{document.querySelector('#ch1-kernel .section-number').scrollIntoView({block:'center',behavior:'instant'});}); await pa.waitForTimeout(300); await pa.evaluate(()=>document.querySelector('#ch1-kernel .mark-dot').click()); await pa.waitForTimeout(250);
await pa.click('#utc-markmenu .mm-item[data-c="3"]'); await pa.waitForTimeout(1800);
let mk = await db('/api/marks?since=0');
ok(mk.rows.some(r=>r.part==='part-1'&&r.a==='ch1-kernel'&&r.c===3&&!r.x), 'A: mark synced to server', JSON.stringify(mk.rows));
let lsA = await pa.evaluate(()=>JSON.parse(localStorage.getItem('under-the-code:marks')));
ok(lsA.m['part-1|ch1-kernel'] && lsA.m['part-1|ch1-kernel'].s===1 && lsA.owner===mk.owner, 'A: local mark acked (s=1, owner set)', JSON.stringify(lsA));
// Device B (phone)
const Bd = await device({width:375,height:667});
const pb = await Bd.ctx.newPage();
await pb.goto(B+'/part-1?utc-debug'); await pb.waitForTimeout(3500);
let sB = await pb.evaluate(()=>__utcPlace.snapshot());
ok(sB.C && sB.C.anchor===pos.position.anchor && sB.C.src==='set', 'B: adopted the remote place incl. pin', JSON.stringify(sB.C));
ok(sB.state==='PINNED', 'B: adopted pin enters PINNED (M20)', sB.state);
ok(await pb.evaluate(()=>!!document.querySelector('.sync-chip:not(.place-toast)')), 'B: other-device chip offered');
ok(await pb.evaluate(()=>{const d=document.querySelector('#ch1-kernel .mark-dot'); return d.classList.contains('is-marked') && d.dataset.c==='3';}), 'B: mark pulled and painted');
// account page lists it
const pacc = await Bd.ctx.newPage(); await pacc.goto(B+'/account'); await pacc.waitForTimeout(2000);
const items = await pacc.$$eval('#acct-marks-list li', ls=>ls.map(l=>l.textContent));
ok(items.length===1 && /Part I/.test(items[0]) && /Smalt/.test(items[0]), 'B: account lists Your marks', JSON.stringify(items));
// B removes the mark
await pb.evaluate(()=>{document.querySelector('#ch1-kernel .section-number').scrollIntoView({block:'center',behavior:'instant'});}); await pb.waitForTimeout(500); await pb.evaluate(()=>document.querySelector('#ch1-kernel .mark-dot').click()); await pb.waitForTimeout(300);
await pb.click('#utc-markmenu .mm-item[data-c="0"]'); await pb.waitForTimeout(1800);
mk = await db('/api/marks?since=0');
ok(mk.rows.some(r=>r.a==='ch1-kernel'&&r.x===1), 'B: removal is a server tombstone', JSON.stringify(mk.rows));
await pa.reload(); await pa.waitForTimeout(3000);
ok(await pa.evaluate(()=>!document.querySelector('#ch1-kernel .mark-dot').classList.contains('is-marked')), 'A: removal propagates after reload');
// B signs out from account page -> forgets account data
await pacc.reload(); await pacc.waitForTimeout(1500);
await pacc.click('#acct-signout'); await pacc.waitForTimeout(1500);
const after = await pacc.evaluate(()=>({p: localStorage.getItem('under-the-code:progress'), m: JSON.parse(localStorage.getItem('under-the-code:marks')||'{}')}));
ok(!after.p && Object.keys(after.m.m||{}).length===0, 'B: sign-out clears synced place and owned marks (H12)', JSON.stringify(after));
ok(A.errs.length===0 && Bd.errs.length===0, 'no page errors', A.errs.concat(Bd.errs).join(' | '));
console.log('E2E', pass, 'pass', fail, 'fail');
await b.close();
