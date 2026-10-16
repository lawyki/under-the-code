# el.py <page> <id> [<id>...]: print the source of the element with that id (p, div figure card, etc.)
import sys,re,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[3]
page=sys.argv[1]; s=open(ROOT/'public'/f'{page}.html').read()
for i in sys.argv[2:]:
    m=re.search(r'<(\w+)[^>]*\bid="%s"'%re.escape(i),s)
    if not m: print('NOT FOUND',i); continue
    tag=m.group(1); st=m.start(); depth=0; pos=st
    rx=re.compile(r'<(/?)%s\b[^>]*?(/?)>'%tag)
    for t in rx.finditer(s,st):
        if t.group(1): depth-=1
        elif not t.group(2): depth+=1
        if depth==0: end=t.end(); break
    line=s.count('\n',0,st)+1
    print(f'===== {i} (line {line}, {end-st} chars)'); print(s[st:end])
