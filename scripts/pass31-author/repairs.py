import csv,io,subprocess,sys
def load(ref):
    txt=subprocess.run(['git','show',f'{ref}:docs/pass-31-ledger.tsv'],capture_output=True,text=True).stdout if ref!='WORK' else open('docs/pass-31-ledger.tsv').read()
    rows=list(csv.reader(io.StringIO(txt),delimiter='\t')); H=rows[0]
    return {r[0]:dict(zip(H,r)) for r in rows[1:]}
rounds=[('Round 1 (Phase 0 repairs)','fb4c1b9','7876daa'),('Round 2 (with the Phase 1 drafts committed in between)','7876daa','5022e8f'),('Round 3','d76e513','832cb0d'),('Round 4','832cb0d','3d20ca5'),('Round 5','6257b62','929b930'),('Round 6','929b930','2a14001'),('Round 6b, the stop-rule step','647d172','WORK')]
cols=['job','intent','content','knows','subtraction','chosen','status']
out=['# Pass 31 · repairs, cell by cell','','Generated from git: every change each repair round made to the ledger columns job, intent (the takeaway), content, knows, subtraction, chosen and status (`docs/pass-31-ledger.tsv`); the bookkeeping columns date, bin, concepts_tried, gate, failed_criterion and commit are not listed. Held rows never change. The reasons are in `UNDER.md` §4ag and in the verification reports it names.','']
for name,a,b in rounds:
    try: A,B=load(a),load(b)
    except Exception as e: continue
    if not A: continue
    ch=[]
    for f in B:
        if f not in A: ch.append((f,['(new row)'])); continue
        c=[k for k in cols if k in A[f] and k in B[f] and A[f][k]!=B[f][k]]
        if c: ch.append((f,c))
    total=sum(len(c) for _,c in ch)
    out.append(f'## {name}: `{a}` to ' + ('the commit that adds this section' if b=='WORK' else f'`{b}`') + f', {len(ch)} rows, {total} cells')
    out.append('')
    for f,c in ch: out.append(f'- {f}: {", ".join(c)}')
    out.append('')
open('docs/pass-31-repairs.md','w').write('\n'.join(out))
print('\n'.join(l for l in out if l.startswith('##')))
