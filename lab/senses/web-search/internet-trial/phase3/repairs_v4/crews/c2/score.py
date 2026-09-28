import subprocess, sys, hashlib
bats = ["g_neg","g_con","g_cau","g_qnt","g_cond","g_hedge","g_tmp","g_cmp","v3proof","mlogic"]
allout = b""
tot_ok = tot_n = 0
for b in bats:
    tsv = "batteries/%s.tsv" % b
    oracle = {}
    for ln in open(tsv, encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        oracle[p[0]] = int(p[3])
    out = subprocess.run(["./logic_bin", tsv], capture_output=True).stdout
    allout += out
    ok = n = 0
    misses = []
    for ln in out.decode().splitlines():
        q = ln.split(" ")
        tag = int(q[1])
        n += 1
        if tag == oracle[q[0]]: ok += 1
        else: misses.append((q[0], tag, oracle[q[0]], q[2] if len(q) > 2 else ""))
    tot_ok += ok; tot_n += n
    flag = "OK " if (ok >= 18 if b in ("g_neg","g_con","g_cau") else ok >= 17) or b in ("v3proof","mlogic") else "MISS-BAR"
    print("%-10s %2d/%2d = %.3f %s %s" % (b, ok, n, ok/n, flag, misses if misses else ""))
print("TOTAL %d/%d = %.4f" % (tot_ok, tot_n, tot_ok/tot_n))
print("COMBINED_SHA256", hashlib.sha256(allout).hexdigest())
