# Run one figure script against a chosen public/ tree (Pass 31 gate builder).
#
#   python3 scripts/figs/build_into.py <public dir> <script.py> [<script.py> ...]
#
# Many figure scripts (and figlib.splice) read and write the main checkout's public/ by its absolute path.
# This runner redirects every open() under that path to <public dir>, so a script can be built into a
# worktree or a scratch copy without touching the main checkout. Each script runs in its own process,
# because scripts set module state (figlib.FONT) that must not leak into the next one.
import builtins, io, os, runpy, subprocess, sys

MAIN = '/Users/yki/Documents/github/atheric/under-the-code/public/'
HERE = os.path.dirname(os.path.abspath(__file__))

def run_one(tree, script):
    tree = os.path.abspath(tree).rstrip('/') + '/'
    real_open = builtins.open
    def redirected(file, *a, **k):
        if isinstance(file, str) and file.startswith(MAIN):
            file = tree + file[len(MAIN):]
        return real_open(file, *a, **k)
    builtins.open = redirected
    io.open = redirected
    script = os.path.abspath(script)
    # figlib and the shared models come from this folder unless the script's own folder has them
    sys.path[:0] = [os.path.dirname(script), HERE]
    os.chdir(os.path.dirname(script))
    runpy.run_path(script, run_name='__main__')

if __name__ == '__main__':
    if len(sys.argv) >= 4 and sys.argv[1] == '--one':
        run_one(sys.argv[2], sys.argv[3]); sys.exit(0)
    if len(sys.argv) < 3:
        sys.exit(__doc__ or 'usage: build_into.py <public dir> <script.py> ...')
    tree, scripts = sys.argv[1], sys.argv[2:]
    if not os.path.isdir(tree):
        sys.exit(f'no such public dir: {tree}')
    bad = 0
    for sc in scripts:
        r = subprocess.run([sys.executable, os.path.abspath(__file__), '--one', tree, sc], capture_output=True, text=True)
        if r.returncode:
            bad += 1
            sys.stderr.write(f'FAIL {sc}\n{r.stderr[-2000:]}\n')
    sys.exit(1 if bad else 0)
