import json,csv,re,sys
C,W=sys.argv[1],sys.argv[2]
D=json.load(open(f'{C}/data.json'))
rows=list(csv.reader(open(f'{W}/docs/pass-31-ledger.tsv'),delimiter='\t'));H=rows[0];I=H.index
R={r[0]:r for r in rows[1:]}
def num(f): return f[4:].replace('br-','BR.').replace('-','.',1) if f!='fig-18-trace' else '18.1.5'
def chap(f): x=f[4:].split('-')[0]; return 'Bridge' if x=='br' else x
def owner(rec):
    import re as _re
    return _re.split(r' (?:Placement|Merge|Merged|Verdicts|Phase 2 inputs|Two verdicts|Session e2)\b', rec)[0].strip()   # notes for the redraw stay in the ledger
D['cuts']=[{'id':f,'num':num(f),'chap':chap(f),'why':owner(R[f][I('subtraction')])} for f in R if R[f][I('status')].startswith('cut candidate')]
M=[]
for f in R:
    st=R[f][I('status')]; m=re.match(r'merge candidate with (fig-\S+)',st)
    if m and f < m.group(1) or (m and num(f).split('.')[0]==num(m.group(1)).split('.')[0] and int(num(f).split('.')[1])<int(num(m.group(1)).split('.')[1])):
        b=m.group(1); M.append({'a':f,'b':b,'anum':num(f),'bnum':num(b),'chap':chap(f),'why':owner(R[f][I('subtraction')])})
M.append({'a':'fig-13-5','b':'fig-13-6','anum':'13.5','bnum':'13.6','chap':'13','why':'Already merged as the Part IV exemplar (section 3), now numbered Fig 13.6: the failure on top, then the log that prevents it.'})
seen=set(); D['merges']=[x for x in M if not (x['a'] in seen or seen.add(x['a']))]
for k in D['kept']:
    if k['fig']=='BR.3': k['action']="Redraw at concept level in Phase 2 (the Bridge), from the ledger's takeaway: a vector number picks an entry in the kernel's table, and the CPU jumps to that entry's handler."
    if k['fig']=='3.10': k['fixes']="Open: five errors, listed with your Chapter 3 calls in docs/audit/owner-calls.md."
def suffix(svg,suf):
    ids=re.findall(r'\bid="([^"]+)"',svg)
    for i in sorted(set(ids),key=len,reverse=True):
        svg=re.sub(r'(?<=[" #(])'+re.escape(i)+r'(?=[" )])',i+suf,svg)
    return svg
for e in D['exemplars']:
    if e['id']=='fig-13-5':
        e['id']='fig-13-6'; e['num']='13.6'; e['label']='Fig 13.6 · A bank transfer · the failure, and the log that prevents it'
    e['take']=re.sub(r'^(Function|Real thing):\s*','',R[e['id']][I('intent')])
    if e['id'] in ('fig-1-5','fig-4-8','fig-10-3','fig-13-6','fig-17-6'):
        part={'fig-1-5':1,'fig-4-8':2,'fig-10-3':3,'fig-13-6':4,'fig-17-6':5}[e['id']]
        s=open(f'{W}/public/part-{part}.html').read()
        i=s.find(f'id="{e["id"]}"'); a=s.find('<svg',i); b=s.find('</svg>',a)+6
        e['after']=suffix(s[a:b],'-a'+e['num'].replace('.','-'))
json.dump(D,open(f'{C}/data.json','w'),ensure_ascii=False)
print('cuts',len(D['cuts']),'merges',len(D['merges']),[ (m['anum'],m['bnum']) for m in D['merges']])
