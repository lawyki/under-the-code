#!/usr/bin/env python3
"""Pass 31 takeaway freeze (brief section 7).

The hash the seen-loss re-test proves it ran on: sha256 of the UTF-8 text built from docs/pass-31-ledger.tsv (read by
header), every data row in file order, held rows included, one line per row:

    id <TAB> intent                      (every row)
    id <TAB> intent <TAB> content        (a row whose status starts with "cut candidate")

lines joined by a single newline, with none after the last. Round 6's freeze, at figures-final 2a14001:
60790bc2c1f3904b769065d5786ef2926f725ff7d7235786be38d167695a2b32.

    python3 scripts/pass31-freeze.py [ledger.tsv]
"""
import csv
import hashlib
import sys

path = sys.argv[1] if len(sys.argv) > 1 else 'docs/pass-31-ledger.tsv'
with open(path, encoding='utf-8') as fh:
    rows = list(csv.reader(fh, delimiter='\t'))
col = rows[0].index
lines = []
for r in rows[1:]:
    line = f"{r[0]}\t{r[col('intent')]}"
    if r[col('status')].startswith('cut candidate'):
        line += f"\t{r[col('content')]}"
    lines.append(line)
print(hashlib.sha256('\n'.join(lines).encode('utf-8')).hexdigest())
