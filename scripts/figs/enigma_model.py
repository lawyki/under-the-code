# Six-contact Enigma model for fig 1.2 (Pass 28). The rotor steps, then the current runs.
N = 6
L = 'ABCDEF'
FAST = [3, 4, 1, 5, 2, 0]   # wiring of the fast rotor (contact -> contact)
MID  = [3, 0, 4, 1, 5, 2]
SLOW = [1, 5, 3, 0, 2, 4]
REFL = {0: 4, 4: 0, 1: 3, 3: 1, 2: 5, 5: 2}   # pairs, no contact maps to itself
def thru(perm, k, i):  return (perm[(i + k) % N] - k) % N
def back(perm, k, o):  return (perm.index((o + k) % N) - k) % N
def press(key, k):
    a = thru(FAST, k, key); b = thru(MID, 0, a); c = thru(SLOW, 0, b)
    r = REFL[c]
    d = back(SLOW, 0, r); e = back(MID, 0, d); f = back(FAST, k, e)
    return [key, a, b, c], [r, d, e, f]
if __name__ == '__main__':
    for k in (1, 2, 3):
        fw, bk = press(0, k); print(k, 'A ->', L[bk[-1]], fw, bk)
