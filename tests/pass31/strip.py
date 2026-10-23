# Pass 31: lay frames out as one sheet image (a strip of frames, or a contact sheet of figures).
#   python3 tests/pass31/strip.py <out.png> --cols=4 [--labels=a,b,...] [--title=...] [--width=360] <img> [<img> ...]
# Each cell is the image scaled to --width px wide, with an optional small label under it (frame number or figure
# id). The labels are the harness's, drawn in a plain system face outside the picture, never figure text.
import sys
from PIL import Image, ImageDraw, ImageFont

def main(argv):
    opts = {a.split('=', 1)[0][2:]: (a.split('=', 1)[1] if '=' in a else True) for a in argv if a.startswith('--')}
    files = [a for a in argv if not a.startswith('--')]
    out, imgs = files[0], files[1:]
    cols = int(opts.get('cols', 4)); w = int(opts.get('width', 360))
    labels = opts['labels'].split('|') if 'labels' in opts else [None] * len(imgs)
    title = opts.get('title')
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 18)
        tfont = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 24)
    except OSError:
        font = tfont = ImageFont.load_default()
    cells = []
    for f in imgs:
        im = Image.open(f).convert('RGB')
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        cells.append(im)
    lab_h = 28 if any(labels) else 0
    ch = max(c.height for c in cells) + lab_h
    rows = (len(cells) + cols - 1) // cols
    gap, top = 12, (40 if title else 0)
    sheet = Image.new('RGB', (cols * w + (cols + 1) * gap, top + rows * ch + (rows + 1) * gap), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    if title: d.text((gap, 8), title, fill=(230, 230, 230), font=tfont)
    for i, (c, lab) in enumerate(zip(cells, labels)):
        x = gap + (i % cols) * (w + gap); y = top + gap + (i // cols) * (ch + gap)
        sheet.paste(c, (x, y))
        if lab: d.text((x + 4, y + c.height + 4), lab, fill=(230, 230, 230), font=font)
    sheet.save(out)

if __name__ == '__main__':
    main(sys.argv[1:])
