import re,sys,csv
pages={p:open(f'public/{p}.html').read() for p in ['part-1','part-2','part-3','part-4','part-5']}
R={r[0]:r for r in csv.reader(open('docs/pass-31-ledger.tsv'),delimiter='\t')}; I=R['id'].index
held={f for f in R if f!='id' and R[f][I('status')]=='held'}
HELDSEC=re.compile(r'^(ch15|ch3-overflow|ch3-defenses|ch9-security|ch10-attacks|ch12-security|ch13-injection|ch14-hashing)|^(ch16-numa-p4|ch8-substrates-p5|ch1-cpu-p9|ch1-cpu-p10|ch1-cpu-p11|ch2-twos-p10|ch2-twos-p11)$')
def where(t,pos):
    cards=list(re.finditer(r'<div class="diagram-card[^"]*" id="([^"]+)"',t[:pos]))
    if cards:
        c=cards[-1]; 
        if t.rfind('</details>',c.start(),pos)<0 and t.rfind('</svg>',c.start(),pos)>=0 or (t.rfind('</details>',c.start(),pos)<0):
            # still inside card if no closing details between card start and pos
            return 'card:'+c.group(1)
    ids=re.findall(r'<(?:p|li|h[1-6]|section|div)\b[^>]*\bid="([^"]+)"',t[:pos]); return ids[-1] if ids else '?'
nums=sys.argv[1].split(',')
for num in nums:
    fid='fig-'+num.replace('.','-')
    for p,t in pages.items():
        for m in re.finditer(r'Fig(?:s|ure)?\.?(?:&nbsp;|&#160;|\s)+(?:\d+\.\d+(?:,|\s+and|\s+to|&#8211;|–)\s*)*'+re.escape(num)+r'(?![.\d]*\d)',t):
            w=where(t,m.start())
            sec=[x.group(1) for x in re.finditer(r'<section[^>]*id="([^"]+)"',t[:m.start()])]
            if w=='card:'+fid: continue
            if w.startswith('card:') and w[5:] in held: continue
            if HELDSEC.search(w) or (sec and HELDSEC.search(sec[-1])): continue
            print(num,'|',p,'|',w,'|',re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',t[max(0,m.start()-60):m.end()+25])))
