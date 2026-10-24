import csv,re,sys,json
R={r[0]:r for r in csv.reader(open('docs/pass-31-ledger.tsv'),delimiter='\t')}; I=R['id'].index
P={r[0]:r for r in csv.reader(open('docs/pass-31-prose-readers.tsv'),delimiter='\t')}; PH=P['id']
pages={p:open(f'public/{p}.html').read() for p in ['part-1','part-2','part-3','part-4','part-5']}
HELD=re.compile(r'ch15|ch3-overflow|ch3-defenses|ch9-security|ch10-attacks|ch12-security|ch13-injection|ch14-hashing|ch16-numa-p4|ch8-substrates-p5|ch1-cpu-p(9|10|11)\b|ch2-twos-p1[01]\b')
heldfigs={f for f in R if f!='id' and R[f][I('status')]=='held'}
cut_set=set(sys.argv[2].split(',')) if len(sys.argv)>2 else set()
cuts={f for f in R if f!='id' and R[f][I('status')].startswith('cut candidate')}|cut_set
def container(t,pos):
    # innermost: a diagram card, or the last p/li id before pos within the same element
    cs=[m for m in re.finditer(r'<div class="diagram-card[^"]*" id="([^"]+)"',t[:pos])]
    if cs:
        c=cs[-1]; end=t.find('</details>',c.start())
        nxt=t.find('<div class="diagram-card',c.end())
        close=t.find('</div>\n',t.find('</details>',c.start())) if end>0 else -1
        if end>0 and pos<end+12: return 'card:'+c.group(1)
    ids=re.findall(r'<(?:p|li|div|section|h\d)[^>]*id="([^"]+)"',t[:pos]); return ids[-1] if ids else '?'
def para(w):
    for s in pages.values():
        m=re.search(r'<p id="'+w+r'"[^>]*>([\s\S]*?)</p>',s)
        if m: return re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',m.group(1))).strip()
for f in sys.argv[1].split(','):
    part=[p for p,s in pages.items() if f'id="{f}"' in s][0]; s=pages[part]; i=s.index(f'id="{f}"')
    cap=re.search(r'<p id="([^"]+)" class="diagram-caption"',s[i:]).group(1)
    # paragraph directly before the slot that survives (skip captions of cut cards)
    prev=[m for m in re.finditer(r'<p id="([^"]+)"( class="[^"]*")?',s[:i])]
    surv=None
    for m in reversed(prev):
        pid=m.group(1); inc=container(s,m.start())
        if inc.startswith('card:') and inc[5:] in cuts: continue
        surv=pid; break
    print(f'== {f} ({part}) caption={cap} before-slot(surviving)={surv} [{"caption of "+container(s,prev[-1].start()) if "diagram-caption" in (prev[-1].group(2) or "") else "prose"}]')
    print('   intent:',R[f][I('intent')]); print('   sub:',R[f][I('subtraction')][:500]); print('   PR ask:',P[f][PH.index('reader_must_show')][:240],'| disp:',P[f][PH.index('disposition')][:120])
    num=f[4:].replace('-','.',1)
    for p,t in pages.items():
        for m in re.finditer(r'Fig(?:s|ure)?\.?(?:&nbsp;|\s)(?:[\d.]+(?:,| and| to)\s)*'+re.escape(num)+r'(?![\d.]*\d)',t):
            c=container(t,m.start())
            if c in ('card:'+f,) or c.startswith('svg') or HELD.search(c) or c[5:] in heldfigs: continue
            if re.search(r'id="'+re.escape(f)+'"',t[max(0,m.start()-300):m.start()]): continue
            print('   cited in',p,c,'|',re.sub(r'<[^>]+>','',t[max(0,m.start()-80):m.end()+25]).replace('\n',' '))
    for g,rr in R.items():
        if g not in (f,'id') and rr[I('status')]!='held' and re.search(r'Figs? (?:[\d.]+(?:, | and ))*'+re.escape(num)+r"(?![\d])",rr[I('knows')]+' '+rr[I('subtraction')]): print('   ledger-cited by',g,rr[I('status')])
