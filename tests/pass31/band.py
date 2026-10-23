# Pass 31: the tallest empty band in a still (brief section 7: "t=0 with no empty band taller than a quarter of the
# plate"). A row is empty when nothing is drawn across it: every pixel within TOL of the row's median colour per
# channel (a smooth plate gradient stays empty, any stroke, mark or glyph breaks the row). Bands at the top and bottom
# edges count too: an empty half of a plate is still empty.
#   python3 tests/pass31/band.py <png> [<png> ...]   ->  one JSON line per file: {"file", "h", "band", "frac", "at"}
import json, sys
from PIL import Image

TOL = 20
def band(path):
    im = Image.open(path).convert('RGB'); w, h = im.size; px = im.load()
    step = max(1, w // 300)
    best = run = 0; best_at = start = 0
    for y in range(h):
        row = [px[x, y] for x in range(0, w, step)]
        med = [sorted(c[i] for c in row)[len(row) // 2] for i in range(3)]
        empty = all(abs(c[i] - med[i]) <= TOL for c in row for i in range(3))
        if empty:
            if run == 0: start = y
            run += 1
            if run > best: best, best_at = run, start
        else:
            run = 0
    return {'file': path, 'h': h, 'band': best, 'frac': round(best / h, 3), 'at': best_at}

for f in sys.argv[1:]:
    print(json.dumps(band(f)))
