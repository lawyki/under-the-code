import json,sys,html
C=sys.argv[1]
D=json.load(open(f'{C}/data.json'))
esc=html.escape
# exemplar SVGs live in the markup; everything else renders from JSON
ex_html=[]
for e in D['exemplars']:
    befores=''.join(f'<figure class="plate" style="--plate:{e["plate"]}"><figcaption>Now · {esc(b["label"])}</figcaption>{b["svg"]}</figure>' for b in e['before'])
    ex_html.append(f'''<article class="exemplar" id="ex-{e["id"]}">
  <header><p class="eyebrow">{esc(e["part"])}</p><h3>{esc(e["label"])}</h3>
  <p class="take">{esc(e["take"][0].upper()+e["take"][1:])}</p></header>
  <div class="pair"><div class="col">{befores}</div>
  <div class="col"><figure class="plate" style="--plate:{e["plate"]}"><figcaption>Proposed</figcaption>{e["after"]}</figure></div></div>
  <p class="why">{esc(e["chosen"])}</p>
  <div class="choice" role="group" aria-label="Your verdict on {esc(e["num"])}" data-key="exemplar-{e["id"]}">
    <button type="button" data-v="yes">Yes, this direction</button><button type="button" data-v="no">No, try again</button>
  </div>
  <label class="note"><span>Anything to say about it (optional)</span><textarea id="note-{e["id"]}" data-key="exemplar-{e["id"]}" rows="2"></textarea></label>
</article>''')
data=json.dumps({k:v for k,v in D.items() if k!='exemplars'}).replace('</','<\\/')
page=open(f'{C}/page.tpl.html').read().replace('%%EXEMPLARS%%','\n'.join(ex_html)).replace('%%DATA%%',data)
open(f'{C}/index.html','w').write(page)
print(len(page)//1000,'KB')
