#!/usr/bin/env python3
"""Freeze Task-4 expected outputs (pre-scored-run, oracle-grounded).

Generates expected/ artifacts from the INDEPENDENT oracle + verified
templates, cross-checking template output against oracle-computed values.
"""
import os, sys, subprocess, hashlib

TASK = os.path.expanduser("~/workspace/tnn-lab/coding/reflection/task4")
EXP = os.path.join(TASK, "expected")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
LEARNER = os.path.join(TASK, "work/learner4")
STORES = os.path.join(TASK, "stores")
FIX = os.path.join(TASK, "fixtures")
sys.path.insert(0, os.path.join(TASK, "src"))
import oracle4 as O

os.makedirs(EXP, exist_ok=True)
os.makedirs("/tmp/t4freeze", exist_ok=True)

def build(item, spec):
    src = f"/tmp/t4freeze/{item}.zag"
    binary = f"/tmp/t4freeze/{item}"
    gen = subprocess.run([LEARNER, "gen", f"{STORES}/kb_informed.dat", spec],
                         capture_output=True)
    assert gen.returncode == 0, gen.stderr
    open(src, "wb").write(gen.stdout)
    c = subprocess.run([ZNC, src, "-o", binary, "--no-analyze", "--no-zagd"],
                       capture_output=True, text=True)
    assert c.returncode == 0, c.stderr
    return binary

# ---------- B2 ----------
b2 = build("b2", "B2 sql engine select where join query csv table")
# oracle-computed expected text: header = cols joined by |, rows likewise
def emp_rows():
    return [r for r in O.EMP]
def dept_rows():
    return [r for r in O.DEPT]
exp_q = []
# Q1
q1 = ["name"] + [r[1] for r in O.EMP if r[2] == "2"]
# Q2
q2rows = sorted([(r[1], r[3]) for r in O.EMP if int(r[3]) > 70000], key=lambda x: int(x[1]))
q2 = ["name|salary"] + [f"{a}|{b}" for a, b in q2rows]
# Q3
dmap = {d[0]: d[1] for d in O.DEPT}
q3 = ["employees.name|departments.dname"] + [f"{r[1]}|{dmap[r[2]]}" for r in O.EMP]
# Q4
q4 = ["id|dname"] + [f"{d[0]}|{d[1]}" for d in O.DEPT if d[0] != "1"]
# Q5
q5 = ["name"] + sorted([r[1] for r in O.EMP if int(r[3]) >= 60000 and r[2] == "1"])
# Q6
q6rows = []
for d in O.DEPT:
    for r in O.EMP:
        if r[2] == d[0] and int(r[3]) < 65000:
            q6rows.append(d[1])
q6 = ["dname"] + q6rows
for i, q in enumerate([q1, q2, q3, q4, q5, q6], 1):
    expected_text = "\n".join(q) + "\n"
    p = subprocess.run([b2, f"{FIX}/b2", O.B2_QUERIES[i-1]], capture_output=True)
    got = p.stdout.decode()
    # the template prints a trailing blank line? normalize: compare exact
    assert got == expected_text, f"Q{i} mismatch:\nGOT:{got!r}\nEXP:{expected_text!r}"
    open(f"{EXP}/B2_q{i}.txt", "w").write(expected_text)
    print(f"B2_q{i}: frozen {len(expected_text)} bytes, oracle-match OK")

# ---------- B4 ----------
b4 = build("b4", "B4 btree b-tree split merge insert delete|ORDER=4")
p = subprocess.run([b4, f"{FIX}/b4_ops.txt"], capture_output=True)
assert p.returncode == 0, p.stderr[:500]
out = p.stdout.decode()
open(f"{EXP}/B4.txt", "w").write(out)

def parse_b4_blocks(out):
    blocks = []
    cur = []
    for ln in out.split("\n"):
        s = ln.strip()
        if not s:
            continue
        cur.append(s)
        if s.startswith("ROOT"):
            blocks.append(cur)
            cur = []
    assert not cur, "trailing lines after last ROOT"
    return blocks

def parse_b4_block(lines):
    nodes = {}
    root = None
    for ln in lines:
        if ln.startswith("ROOT"):
            root = int(ln.split()[1])
            continue
        # N<id> leaf=<l> n=<n> keys=<ks> children=<cs>
        assert ln.startswith("N"), ln
        rest = ln[1:]
        nid_s, rest = rest.split(" ", 1)
        nid = int(nid_s)
        parts = dict(kv.split("=", 1) for kv in rest.split(" "))
        keys = [int(x) for x in parts["keys"].split(",")] if parts["keys"] else []
        children = [int(x) for x in parts["children"].split(",")] if parts["children"] else []
        nodes[nid] = {"leaf": int(parts["leaf"]), "n": int(parts["n"]),
                      "keys": keys, "children": children}
    return nodes, root

def inorder_of(nodes, root):
    res = []
    def walk(nid):
        nd = nodes[nid]
        if nd["leaf"] == 1:
            res.extend(nd["keys"])
        else:
            for i, k in enumerate(nd["keys"]):
                walk(nd["children"][i])
                res.append(k)
            walk(nd["children"][len(nd["keys"])])
    walk(root)
    return res

blocks = parse_b4_blocks(out)
assert len(blocks) == 3, f"expected 3 print blocks, got {len(blocks)}"
exp_sets = [
    [5,6,7,10,12,17,20,30],
    [4,5,7,10,11,12,17,25,30,40,50],
    [1,2,4,7,9,11,12,15,17,25,30,40,50],
]
for i, (lines, eset) in enumerate(zip(blocks, exp_sets), 1):
    nodes, root = parse_b4_block(lines)
    ino = inorder_of(nodes, root)
    assert ino == eset, f"print {i} inorder {ino} != {eset}"
    print(f"B4 print {i}: inorder OK ({len(ino)} keys), root={root}, nodes={len(nodes)}")
print(f"B4: frozen {len(out)} bytes")

# ---------- B1 vectors (params recorded in battery.json by driver) ----------
# sanity: run huff on all vectors, confirm oracle nbits
huff = build("b1", "B1 huffman codec compress decompress prefix tree encode decode bitstream|ALPHABET=256")
vecs = [
    ("v1", b""),
    ("v2", b"a"*8),
    ("v3", b"the quick brown fox jumps over the lazy dog"),
    ("v4", bytes(range(256))),
    ("v5", b"a"*100 + b"b"*50 + b"c"*25 + b"d"*12 + b"e"*6 + b"f"*3),
    ("v6", b"AB"*64),
]
for name, data in vecs:
    p = subprocess.run([huff, "rt", data.hex()], capture_output=True)
    lines = p.stdout.decode().split("\n")
    nbits = int(lines[0]) if lines[0] else 0
    dec = bytes.fromhex(lines[2]) if len(lines) > 2 and lines[2] else b""
    assert dec == data, f"{name} roundtrip failed"
    print(f"B1 {name}: nbits={nbits} roundtrip OK")

# ---------- B5 probes ----------
snake = build("b5", "B5 snake game grid moves food collision|W=10|H=8")
for pid, moves, foods in O.B5_PROBES:
    foodarg = ";".join(f"{x},{y}" for x, y in foods)
    p = subprocess.run([snake, moves, foodarg], capture_output=True)
    r = O.snake_run(moves, foods)
    exp_food = f"{r['food'][0]},{r['food'][1]}" if r['food'] else "-1,-1"
    exp = (f"BOARD 10 8\nSNAKE {r['len']} " +
           " ".join(f"{x},{y}" for x, y in r['body']) +
           f"\nFOOD {exp_food}\nSCORE {r['score']}\nSTATUS {r['status']}\n")
    got = p.stdout.decode()
    assert got == exp, f"{pid} mismatch:\nGOT:{got!r}\nEXP:{exp!r}"
    print(f"B5 {pid}: oracle-match OK")

print("ALL EXPECTED ARTIFACTS FROZEN")
