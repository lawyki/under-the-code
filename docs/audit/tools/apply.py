# apply.py: helper — apply(path, [(old,new),...]) with exact-once assertion
def apply(p, R):
    s = open(p).read()
    for a, b in R:
        n = s.count(a)
        assert n == 1, (p, a[:80], n)
        s = s.replace(a, b)
    open(p, 'w').write(s)
