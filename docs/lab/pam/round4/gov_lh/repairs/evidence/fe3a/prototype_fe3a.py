#!/usr/bin/env python3
"""Frozen Python prototype for FE3a. The Zag output must match this exactly."""
EX = [(97,103,1),(98,104,1),(99,105,1),(97,104,1),(98,105,1),(99,103,1),
      (101,97,0),(102,98,0),(101,98,0),(102,97,0)]
out = []
T = 100
it = 0
while True:
    assert it < 64
    errs = 0
    ri = -1
    rj = 0
    for k, (a, b, lb) in enumerate(EX):
        s = 1 if a >= T else 0
        r = 1 if b >= T else 0
        if s != lb:
            errs += 1
        if ri < 0 and s != r:
            ri, rj = k, r
    if ri < 0:
        out.append(f"it={it} T={T} reversals=0 errs={errs} STOP")
        final_errs = errs
        break
    T_next = T - 1 if rj == 1 else T + 1
    out.append(f"it={it} T={T} reversals=1 first_rev={ri} errs={errs} T_next={T_next}")
    T = T_next
    final_errs = errs
    it += 1
out.append(f"FINAL T={T} errs={final_errs} iters={it+1}")
print("\n".join(out))
