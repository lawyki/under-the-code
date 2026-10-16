# agg.py <journal> <outdir>: per chapter/part, the judged findings (confirmed and owner) from the audit workflow journal
import json,sys,os,collections
J,OUT=sys.argv[1],sys.argv[2]; os.makedirs(OUT,exist_ok=True)
rows=[json.loads(l) for l in open(J)]
lab={r['key']:r['label'] for r in rows if r['type']=='started'}
res={}
IDX=json.load(open('/private/tmp/claude-501/-Users-yki-Documents-github-atheric-under-the-code/a997133e-b1b0-40ce-96fa-d9b7a2e8f1ee/scratchpad/p30/audit-index.json'))
ORDER={c['chapter']:[x['id'] for x in c['sections']] for c in IDX['chapters']}
for r in rows:
    if r['type']=='result': res[lab.get(r.get('key'),'?')]=r.get('result')
# reconstruct finder items per lens/chapter, then attach verdicts by number
def finder_items(where, lens):
    if lens=='newcomer':
        items=[]
        for sec in ORDER.get(where,[]):
            v=res.get('newcomer:'+sec)
            if v:
                for p in v.get('search_points',[]): items.append({'id':p['id'],'kind':'search-'+p['kind'],'severity':'M','quote':p['quote'],'problem':p['missing'],'fix':p['close_with'],'section':v['section']})
        return items
    if lens=='facts':
        v=res.get(f'facts:{where}') or {'findings':[]}
        items=list(v['findings'])
        for sec in ORDER.get(where,[]):
            vv=res.get('newcomer:'+sec)
            if vv:
                for d in vv.get('fact_doubts',[]): items.append({'id':vv['section'],'kind':'fact-doubt','severity':'M','quote':'','problem':d,'fix':''})
        return items
    v=res.get(f'{lens}:{where}') or {'findings':[]}
    return list(v['findings'])
if res.get('index'): ORDER={c['chapter']:c['sections'] for c in res['index']['chapters']}   # the order the workflow (and so its judges) used
summary=collections.Counter(); per={}
for l,v in res.items():
    if not l.startswith('judge:') or not v: continue
    _,lens,where=l.split(':',2)
    verdicts=v.get('verdicts',[])
    # the judge saw items numbered 1..N in finder order; newcomer order depends on section completion order, so match by n only when counts agree
    items=finder_items(where,lens)
    out=per.setdefault(where,[])
    for vd in verdicts:
        n=vd['n']; it=items[n-1] if 0<n<=len(items) else {}
        summary[(lens,vd['verdict'])]+=1
        if vd['verdict']!='rejected': out.append({'lens':lens,'verdict':vd['verdict'],**it,'reason':vd['reason'],'judge_fix':vd['fix']})
for where,items in per.items():
    json.dump(items,open(f'{OUT}/{where}.json','w'),indent=1)
print(dict(summary)); print({w:len(v) for w,v in per.items()})
