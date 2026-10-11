# Fig 13.1 · Codd 1970 to PostgreSQL 18 · two lineages, fifty years (Pass 28, law 3). Strongroom dossier plate.
# Codd's 1970 paper on top; below, the two prototypes and what came of them, one row per line of descent:
# IBM (System R 1974, SQL/DS 1981, DB2 1983) with Oracle (1979) built from IBM's published SQL; Berkeley (Ingres
# 1973, Postgres 1986, PostgreSQL 1996) with Sybase (1984, founded by Ingres people) and Microsoft SQL Server
# (1989, licensed from Sybase). Lock-step motion: the systems stamp in date order, the two lines interleaving.
# t=0 (shift): every system stamped.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

W = 400
NW, NH = 104, 38
CX = (28, 150, 272)                               # node columns
ROWS = {'ibm': 78, 'oracle': 140, 'berk': 214, 'syb': 276}
NODES = [  # key, row, column, name, year, colour
    ('sysr', 'ibm', 0, 'System R', 1974, SEAL), ('sqlds', 'ibm', 1, 'SQL/DS', 1981, SEAL), ('db2', 'ibm', 2, 'DB2', 1983, SEAL),
    ('ora', 'oracle', 1, 'Oracle', 1979, OXBLOOD),
    ('ingres', 'berk', 0, 'Ingres', 1973, BRASS), ('pg', 'berk', 1, 'Postgres', 1986, BRASS), ('pgsql', 'berk', 2, 'PostgreSQL', 1996, BRASS),
    ('syb', 'syb', 1, 'Sybase', 1984, SAGE), ('mssql', 'syb', 2, 'SQL Server', 1989, SAGE)]
POS = {k: (CX[c], ROWS[r]) for k, r, c, *_ in NODES}
D = 12.0
T = Timeline(D, shift=11.4)
ty = lambda yr: 0.8 + (yr - 1970) / 26 * 8.0       # stamp time by year
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
# Codd's paper
a(f'<rect x="28" y="8" width="348" height="34" rx="3" fill="{DCARD}" stroke="{PARCH}" stroke-opacity="0.8"/>')
a(text(202, 30, 'Codd, 1970: the relational model', anchor='middle', size=13, fill=PARCH, ls='0'))
# from the paper: down to System R, and down the margin to Ingres
sx, sy = POS['sysr']; ix, iy = POS['ingres']
a(f'<path d="M{sx + 30},42 V{sy}" fill="none" stroke="{PMUTED}"/>')
a(f'<path d="M36,42 V50 H16 V{iy + NH / 2} H{ix}" fill="none" stroke="{PMUTED}"/>')
a(text(150, ROWS['ibm'] - 10, 'IBM, San Jose', anchor='start', size=13, fill=SEAL, ls='0'))
a(text(150, ROWS['berk'] - 10, 'UC Berkeley', anchor='start', size=13, fill=BRASS, ls='0'))
# chains along each row
for p, c in (('sysr', 'sqlds'), ('sqlds', 'db2'), ('ingres', 'pg'), ('pg', 'pgsql'), ('syb', 'mssql')):
    (x1, y1), (x2, y2) = POS[p], POS[c]
    a(f'<path d="M{x1 + NW},{y1 + NH / 2} H{x2 - 2} m-6,-4 l6,4 l-6,4" fill="none" stroke="{PMUTED}"/>')
# side branches, dashed: Oracle from IBM's published SQL; Sybase from Ingres people
for p, c, lab in (('sysr', 'ora', 'IBM\'s SQL'), ('ingres', 'syb', 'alumni')):
    (x1, y1), (x2, y2) = POS[p], POS[c]
    a(f'<path d="M{x1 + 40},{y1 + NH} V{y2 + NH / 2} H{x2 - 2}" fill="none" stroke="{PMUTED}" stroke-dasharray="4 3"/>')
    a(text(x1 + 46, y2 + 4, lab, anchor='start', size=13, fill=PMUTED, ls='0'))
# the systems, stamped in date order
for k, r, c, name, yr, col in NODES:
    x, y = POS[k]
    body = (f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="3" fill="{DCARD}" stroke="{col}" stroke-width="1.5"/>'
            + text(x + NW / 2, y + 16, name, anchor='middle', size=13, fill=col, ls='0')
            + text(x + NW / 2, y + 32, str(yr), anchor='middle', size=13, fill=PSOFT, ls='0'))
    a(f'<g opacity="0.22">{body}</g><g opacity="0">{win(ty(yr))}{body}</g>')
    a(f'<g class="fx" opacity="0">{stamp(ty(yr))}<rect x="{x - 3}" y="{y - 3}" width="{NW + 6}" height="{NH + 6}" rx="4" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
BY = ROWS['syb'] + NH + 30
a(f'<g opacity="0">{win(ty(1996) + 0.8)}{text(28, BY, "still running: DB2, Oracle,", anchor="start", size=13, fill=PSOFT, ls="0")}'
  f'{text(28, BY + 18, "PostgreSQL 18, SQL Server", anchor="start", size=13, fill=PSOFT, ls="0")}</g>')
H = BY + 28
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-2 svgd-part4-2">')
o.insert(1, '<title id="svgt-part4-2">Fig 13.1 · Codd 1970 to PostgreSQL 18 · two lineages, fifty years</title>')
o.insert(2, '<desc id="svgd-part4-2">Codd\'s 1970 paper on the relational model, and the two prototypes it inspired. At IBM in San Jose, System R in 1974, which IBM shipped as SQL/DS in 1981 and DB2 in 1983; Oracle, in 1979, built its product from the SQL that IBM had published. '
  'At UC Berkeley, Ingres in 1973, which led to Postgres in 1986 and PostgreSQL in 1996; people from Ingres founded Sybase in 1984, which Microsoft licensed for SQL Server in 1989. DB2, Oracle, PostgreSQL 18 and SQL Server are all still running.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Codd\'s 1970 paper inspired two prototypes, System R at IBM and Ingres at Berkeley, and the major relational databases still running descend from one or the other: '
           'DB2 and, through IBM\'s published SQL, Oracle; PostgreSQL and, through Ingres\'s people, Sybase and SQL Server.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The paper.</b> "A Relational Model of Data for Large Shared Data Banks", Communications of the ACM, June 1970: data as tables, and queries that say what to find, not how.</li>
          <li><b>IBM's side.</b> System R produced SQL; IBM shipped it as SQL/DS (1981) and DB2 (1983), after Oracle had shipped its own version, built from IBM's published papers, in 1979.</li>
          <li><b>Berkeley's side.</b> Ingres led to Postgres and PostgreSQL (version 18 in 2025); Ingres alumni founded Sybase, which Microsoft licensed for SQL Server. MySQL and SQLite were written fresh, but speak the same SQL.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-13-1">
      <div class="diagram-label">Fig 13.1 · Codd 1970 to PostgreSQL 18 · two lineages, fifty years</div>
      {svg}
      <p id="ch13-codd-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-4', 'fig-13-1', 'ch13-codd-p7', card)
