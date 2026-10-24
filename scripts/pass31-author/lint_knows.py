import re,csv,sys
cols=sys.argv[1:] or ['knows']
order=[]
for n in range(1,6):
    s=open(f'public/part-{n}.html').read()
    order+=re.findall(r'class="diagram-card[^"]*" id="([^"]+)"',s)
pos={f:i for i,f in enumerate(order)}
rows=list(csv.reader(open('docs/pass-31-ledger.tsv'),delimiter='\t')); H=rows[0]
st={r[0]:r[H.index('status')] for r in rows[1:]}
def fid(ref):
    a,b=ref.split('.',1)
    if ref=='18.1.5': return 'fig-18-trace'
    return f'fig-{a.lower()}-{b}'
bad=0
for r in rows[1:]:
    if st[r[0]]=='held' or r[0] not in pos: continue
    for c in cols:
        txt=r[H.index(c)]
        for m in re.finditer(r'Figs? ((?:BR|\d+)\.\d+(?:\.\d+)?)(?: (?:to|and) ((?:BR|\d+)\.\d+))?',txt):
            for ref in [m.group(1)]+([m.group(2)] if m.group(2) else []):
                f=fid(ref)
                why=[]
                if f not in pos: why.append('unknown')
                else:
                    if pos[f]>=pos[r[0]] and f!=r[0]: why.append('later')
                    s=st.get(f,'')
                    if s.startswith('cut'): why.append('cut candidate')
                    if s=='held': why.append('held')
                    mm=re.match(r'merge candidate with (fig-\S+)',s)
                    if mm and pos.get(mm.group(1),-1)>pos[f]: why.append('lower half of a merge with '+mm.group(1))
                    if s.startswith('merged into'): why.append(s)
                if why and f!=r[0]: bad+=1; print(f'{r[0]}\t{c}\tFig {ref}\t{", ".join(why)}')
print('findings',bad)
