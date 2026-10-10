# Four schedulers on one workload, simulated (Fig 4.5). Jobs: (name, arrival, burst).
JOBS = [('A', 0, 8), ('B', 1, 4), ('C', 2, 9), ('D', 3, 5)]
def fcfs():
    t, out = 0, []
    for n, ar, b in sorted(JOBS, key=lambda j: j[1]):
        t = max(t, ar); out.append((n, t, t + b)); t += b
    return out
def sjf():                       # non-preemptive shortest job first
    t, out, left = 0, [], list(JOBS)
    while left:
        ready = [j for j in left if j[1] <= t] or [min(left, key=lambda j: j[1])]
        n, ar, b = min(ready, key=lambda j: (j[2], j[1]))
        t = max(t, ar); out.append((n, t, t + b)); t += b; left.remove((n, ar, b))
    return out
def rr(q=2):                     # arrivals join the queue before a preempted job rejoins
    t, out, rem = 0, [], {n: b for n, _, b in JOBS}
    arr = sorted(JOBS, key=lambda j: j[1]); queue, i = [], 0
    while i < len(arr) and arr[i][1] <= t: queue.append(arr[i][0]); i += 1
    while queue or i < len(arr):
        if not queue: t = arr[i][1]; queue.append(arr[i][0]); i += 1; continue
        n = queue.pop(0); run = min(q, rem[n])
        out.append((n, t, t + run)); t += run; rem[n] -= run
        while i < len(arr) and arr[i][1] <= t: queue.append(arr[i][0]); i += 1
        if rem[n]: queue.append(n)
    return out
def mlfq(quanta=(2, 4, 99)):      # new jobs enter the top queue; using a whole quantum demotes a job
    t, out, rem = 0, [], {n: b for n, _, b in JOBS}
    arr = sorted(JOBS, key=lambda j: j[1]); qs = [[], [], []]; i = 0
    def admit():
        nonlocal i
        while i < len(arr) and arr[i][1] <= t: qs[0].append(arr[i][0]); i += 1
    admit()
    while any(qs) or i < len(arr):
        if not any(qs): t = arr[i][1]; admit(); continue
        lvl = next(k for k in range(3) if qs[k]); n = qs[lvl].pop(0)
        run = min(quanta[lvl], rem[n]); out.append((n, t, t + run, lvl)); t += run; rem[n] -= run
        admit()
        if rem[n]: qs[min(lvl + 1, 2)].append(n)
    return out
def avg_wait(sched):
    fin = {}
    for s in sched: fin[s[0]] = s[2]
    return sum(fin[n] - ar - b for n, ar, b in JOBS) / len(JOBS)
if __name__ == '__main__':
    for f in (fcfs, sjf, rr, mlfq):
        s = f(); print(f.__name__, avg_wait(s), [(x[0], x[1], x[2]) for x in s])
