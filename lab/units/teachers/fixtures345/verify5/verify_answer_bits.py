import struct, sys
tape, gtfile = sys.argv[1], sys.argv[2]
units = []
stim_len = 0
for line in open(gtfile):
    line = line.rstrip("\n")
    if line.startswith("GT1 "): stim_len = int(line[4:])
    elif line.startswith("U "):
        s, e, u = line[2:].split(); units.append((int(s), int(e)))
data = open(tape, "rb").read()
evs = []; off = 0
while off < len(data):
    t = data[off]; (ln,) = struct.unpack_from("<I", data, off+1)
    evs.append((t, data[off+5:off+5+ln])); off += 5+ln
queries = {}
for t, p in evs:
    if t == 10:
        seq, a, b, extra, pred = struct.unpack_from("<QQQQB", p, 0)
        queries[seq] = (a, b, extra, pred)
answers = {}
for t, p in evs:
    if t == 4:
        (seq,) = struct.unpack_from("<Q", p, 0); answers[seq] = p[8]
def expect(a, b, extra, pred):
    if pred == 1:
        if not (a >= 0 and b > a and b <= stim_len): return None
        return 1 if (a, b) in units else 0
    if pred == 2:
        if not (a >= 0 and b > a and b <= stim_len and 0 <= extra < len(units)): return None
        return 1 if units[extra] == (a, b) else 0
    if pred == 3:
        if not (0 <= a <= stim_len): return None
        return 1 if any(s == a or e == a for s, e in units) else 0
    return None
bad = 0
for seq, bit in sorted(answers.items()):
    a, b, extra, pred = queries[seq]
    e = expect(a, b, extra, pred)
    if e is None or e != bit:
        print("BIT_FAIL seq=%d pred=%d a=%d b=%d extra=%d got=%d want=%s" % (seq, pred, a, b, extra, bit, e)); bad += 1
print("BITS_CHECKED,%d,BIT_FAILS,%d" % (len(answers), bad))
sys.exit(1 if bad else 0)
