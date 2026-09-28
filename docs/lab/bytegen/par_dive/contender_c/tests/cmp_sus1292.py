import struct, re

def rd(p):
    d = open(p, 'rb').read()
    n = len(d) // 4
    fmt = '<' + str(n) + 'i'
    return struct.unpack(fmt, d[:n*4])

a = rd('results/c_clean.mix')
b = rd('results/c_sus1292.mix')
print("lens:", len(a), len(b))
# 1292 flat blocks = ceil(1323000/1024): the whole fixture is the corrupted span
span = min(1292 * 1024, len(a))
print("corrupted span samples:", span, "of", len(a))
diffs_in = sum(1 for i in range(span) if a[i] != b[i])
diffs_out = sum(1 for i in range(span, len(a)) if a[i] != b[i])
print("diffs inside corrupted span:", diffs_in)
print("diffs OUTSIDE (tail):", diffs_out)

def gains(trace):
    g = {}
    for line in open(trace):
        m = re.match(r'C rg=(\d+) rb=(\d+) g=(\d+)', line)
        if m:
            g[(int(m.group(1)), int(m.group(2)))] = int(m.group(3))
    return g

gc = gains('results/c_clean2.trace')
gs = gains('results/c_sus1292_trace.txt')
common = set(gc) & set(gs)
ndiff = sum(1 for k in common if gc[k] != gs[k])
print("gain trajectory: %d common blocks, %d differ from clean" % (len(common), ndiff))
gv = list(gs.values())
print("gain range under attack: %.4f..%.4f" % (min(gv)/65536, max(gv)/65536))
print("vetoes (from trace):", open('results/c_sus1292_trace.txt').read().count('veto=1'))
