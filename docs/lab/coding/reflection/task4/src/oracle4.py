#!/usr/bin/env python3
"""TASK4 independent oracle — frozen battery fixture generator.

Independent implementation (Python) of each idiom, used ONLY to:
  - choose frozen vectors/queries/programs/ops/probes that are solvable,
  - compute frozen expected values where the done-definition pins them
    (B2 expected outputs, B4 expected key sets, B5 expected states),
  - sanity-check achievability of bars (B3 >=20% reduction with the
    documented pattern set, B1 compression sanity).

It is NOT the learner's code path: the learner's Zag templates are written
independently from the prose idiom descriptions. The oracle never appears
in any knowledge store.
"""
import json, heapq, itertools

# ---------------- B1: reference Huffman ----------------
def huffman_code_lengths(data: bytes):
    from collections import Counter
    freq = Counter(data)
    if not freq:
        return {}
    if len(freq) == 1:
        return {next(iter(freq)): 1}
    # deterministic tie-break: (freq, symbol)
    heap = [(f, s, [(s, "")]) for s, f in freq.items()]
    heapq.heapify(heap)
    nid = 256
    while len(heap) > 1:
        f1, s1, t1 = heapq.heappop(heap)
        f2, s2, t2 = heapq.heappop(heap)
        nt = [(s, "0" + c) for s, c in t1] + [(s, "1" + c) for s, c in t2]
        heapq.heappush(heap, (f1 + f2, min(s1, s2), nt))
        nid += 1
    lens = {s: len(c) for s, c in heap[0][2]}
    return lens

B1_VECTORS = {
    "v1": b"",
    "v2": b"a" * 8,
    "v3": b"the quick brown fox jumps over the lazy dog",
    "v4": bytes(range(256)),
    "v5": b"a" * 100 + b"b" * 50 + b"c" * 25 + b"d" * 12 + b"e" * 6 + b"f" * 3,
    "v6": b"AB" * 64,
}

def b1_check():
    print("== B1 reference ==")
    for vid, data in B1_VECTORS.items():
        lens = huffman_code_lengths(data)
        nbits = sum(lens[b] for b in data)
        ratio = (nbits / (8 * len(data))) if data else 0
        print(f"{vid}: len={len(data)} nbits={nbits} ratio={ratio:.3f}")

# ---------------- B2: reference SQL ----------------
EMP = [
    ("1", "Ana", "1", "60000"), ("2", "Bo", "2", "75000"),
    ("3", "Cy", "1", "52000"), ("4", "Di", "3", "80000"),
    ("5", "Eli", "2", "68000"), ("6", "Fay", "1", "61000"),
    ("7", "Gus", "3", "45000"), ("8", "Hal", "2", "72000"),
]
DEPT = [("1", "Eng"), ("2", "Sales"), ("3", "Ops")]

B2_QUERIES = [
    "SELECT name FROM employees WHERE dept_id = 2",
    "SELECT name,salary FROM employees WHERE salary > 70000 ORDER BY salary",
    "SELECT employees.name,departments.dname FROM employees JOIN departments ON employees.dept_id=departments.id",
    "SELECT * FROM departments WHERE id != 1",
    "SELECT name FROM employees WHERE salary >= 60000 AND dept_id = 1 ORDER BY name",
    "SELECT dname FROM departments JOIN employees ON departments.id=employees.dept_id WHERE salary < 65000",
]

def b2_check():
    print("== B2 reference ==")
    # Q1
    q1 = [r[1] for r in EMP if r[2] == "2"]
    # Q2
    q2 = sorted([(r[1], r[3]) for r in EMP if int(r[3]) > 70000], key=lambda x: int(x[1]))
    # Q3
    dmap = {d[0]: d[1] for d in DEPT}
    q3 = [(r[1], dmap[r[2]]) for r in EMP]
    # Q4
    q4 = [d for d in DEPT if d[0] != "1"]
    # Q5
    q5 = sorted([r[1] for r in EMP if int(r[3]) >= 60000 and r[2] == "1"])
    # Q6: departments outer, employees inner
    q6 = []
    for d in DEPT:
        for r in EMP:
            if r[2] == d[0] and int(r[3]) < 65000:
                q6.append(d[1])
    for i, q in enumerate([q1, q2, q3, q4, q5, q6], 1):
        print(f"Q{i}: {q}")

# ---------------- B3: reference VM + peephole ----------------
def vm_run(prog):
    st = []
    for op in prog:
        k = op[0]
        if k == "PUSH": st.append(op[1])
        elif k == "ADD": b = st.pop(); a = st.pop(); st.append(a + b)
        elif k == "SUB": b = st.pop(); a = st.pop(); st.append(a - b)
        elif k == "MUL": b = st.pop(); a = st.pop(); st.append(a * b)
        elif k == "DIV":
            b = st.pop(); a = st.pop()
            st.append(int(a / b) if b != 0 else 0)
        elif k == "DUP": st.append(st[-1])
        elif k == "SWAP": st[-1], st[-2] = st[-2], st[-1]
        elif k == "POP": st.pop()
        elif k == "NEG": st.append(-st.pop())
    return st

def peep(prog):
    prog = [tuple(o) for o in prog]
    changed = True
    while changed:
        changed = False
        out = []
        i = 0
        while i < len(prog):
            def at(j):
                return prog[j] if j < len(prog) else None
            a, b = at(i), at(i + 1)
            rep = None
            if a and b and a[0] == "PUSH" and b[0] == "PUSH" and at(i + 2):
                c = at(i + 2)
                if c[0] in ("ADD", "SUB", "MUL", "DIV"):
                    if c[0] == "DIV" and b[1] == 0:
                        pass
                    else:
                        if c[0] == "ADD":
                            v = a[1] + b[1]
                        elif c[0] == "SUB":
                            v = a[1] - b[1]
                        elif c[0] == "MUL":
                            v = a[1] * b[1]
                        else:
                            v = int(a[1] / b[1])
                        rep = [("PUSH", v)]; i += 3; changed = True
            if rep is None and a == ("PUSH", 0) and b and b[0] == "ADD":
                rep = []; i += 2; changed = True
            if rep is None and a == ("PUSH", 0) and b and b[0] == "SUB":
                rep = []; i += 2; changed = True
            if rep is None and a == ("PUSH", 1) and b and b[0] == "MUL":
                rep = []; i += 2; changed = True
            if rep is None and a == ("PUSH", 0) and b and b[0] == "MUL":
                rep = [("POP",), ("PUSH", 0)]; i += 2; changed = True
            if rep is None and a and a[0] == "DUP" and b and b[0] == "POP":
                rep = []; i += 2; changed = True
            if rep is None and a and a[0] == "PUSH" and b and b[0] == "POP":
                rep = []; i += 2; changed = True
            if rep is None and a and a[0] == "SWAP" and b and b[0] == "SWAP":
                rep = []; i += 2; changed = True
            if rep is None and a and a[0] == "NEG" and b and b[0] == "NEG":
                rep = []; i += 2; changed = True
            if rep is None:
                out.append(a); i += 1
            else:
                out.extend(rep)
        prog = out
    return prog

B3_PROGS = {
    "p1": [("PUSH", 2), ("PUSH", 3), ("ADD",), ("PUSH", 4), ("MUL",),
           ("PUSH", 10), ("PUSH", 2), ("DIV",), ("ADD",)],
    "p2": [("PUSH", 7), ("PUSH", 0), ("ADD",), ("PUSH", 1), ("MUL",),
           ("DUP",), ("POP",), ("PUSH", 5), ("PUSH", 0), ("SUB",), ("ADD",)],
    "p3": [("PUSH", 3), ("DUP",), ("MUL",), ("PUSH", 2), ("PUSH", 2),
           ("MUL",), ("ADD",)],
    "p4": [("PUSH", 9), ("PUSH", 4), ("SWAP",), ("SWAP",), ("SUB",),
           ("NEG",), ("NEG",), ("PUSH", 0), ("MUL",)],
}

def b3_check():
    print("== B3 reference ==")
    for pid, prog in B3_PROGS.items():
        opt = peep(prog)
        r0, r1 = vm_run(prog), vm_run(opt)
        red = 1 - len(opt) / len(prog)
        print(f"{pid}: orig={len(prog)} opt={len(opt)} red={red:.3f} "
              f"stack_eq={r0 == r1} result={r0}")

# ---------------- B4: reference B-tree (order 4) ----------------
class BNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self):
        self.root = BNode()

    def _split(self, p, i):
        y = p.children[i]
        z = BNode(leaf=y.leaf)
        mid = y.keys[1]
        z.keys = y.keys[2:]
        if not y.leaf:
            z.children = y.children[2:]
            y.children = y.children[:2]
        y.keys = y.keys[:1]
        p.children.insert(i + 1, z)
        p.keys.insert(i, mid)

    def insert(self, k):
        r = self.root
        if len(r.keys) == 3:
            s = BNode(leaf=False)
            s.children = [r]
            self._split(s, 0)
            self.root = s
        self._ins(self.root, k)

    def _ins(self, n, k):
        i = len(n.keys) - 1
        if n.leaf:
            n.keys.append(0)
            while i >= 0 and k < n.keys[i]:
                n.keys[i + 1] = n.keys[i]
                i -= 1
            n.keys[i + 1] = k
        else:
            while i >= 0 and k < n.keys[i]:
                i -= 1
            i += 1
            if len(n.children[i].keys) == 3:
                self._split(n, i)
                if k > n.keys[i]:
                    i += 1
            self._ins(n.children[i], k)

    def delete(self, k):
        self._del(self.root, k)
        if not self.root.leaf and len(self.root.keys) == 0:
            self.root = self.root.children[0]

    def _del(self, n, k):
        i = 0
        while i < len(n.keys) and n.keys[i] < k:
            i += 1
        if i < len(n.keys) and n.keys[i] == k:
            if n.leaf:
                n.keys.pop(i)
            else:
                if len(n.children[i].keys) >= 2:
                    pred = n.children[i].keys[-1]
                    n.keys[i] = pred
                    self._del(n.children[i], pred)
                elif len(n.children[i + 1].keys) >= 2:
                    succ = n.children[i + 1].keys[0]
                    n.keys[i] = succ
                    self._del(n.children[i + 1], succ)
                else:
                    self._merge(n, i)
                    self._del(n.children[i], k)
        else:
            if n.leaf:
                return
            if len(n.children[i].keys) < 2:
                self._fill(n, i)
                # after fill, child index may shift; recompute
                i = 0
                while i < len(n.keys) and n.keys[i] < k:
                    i += 1
            self._del(n.children[i], k)

    def _merge(self, n, i):
        c = n.children[i]
        s = n.children[i + 1]
        c.keys.append(n.keys[i])
        c.keys.extend(s.keys)
        if not c.leaf:
            c.children.extend(s.children)
        n.keys.pop(i)
        n.children.pop(i + 1)

    def _fill(self, n, i):
        c = n.children[i]
        if i > 0 and len(n.children[i - 1].keys) >= 2:
            sib = n.children[i - 1]
            c.keys.insert(0, n.keys[i - 1])
            n.keys[i - 1] = sib.keys.pop()
            if not c.leaf:
                c.children.insert(0, sib.children.pop())
        elif i < len(n.children) - 1 and len(n.children[i + 1].keys) >= 2:
            sib = n.children[i + 1]
            c.keys.append(n.keys[i])
            n.keys[i] = sib.keys.pop(0)
            if not c.leaf:
                c.children.append(sib.children.pop(0))
        else:
            if i < len(n.children) - 1:
                self._merge(n, i)
            else:
                self._merge(n, i - 1)

B4_OPS = """i 10
i 20
i 5
i 6
i 12
i 30
i 7
i 17
p
i 25
i 40
i 50
d 6
d 13
i 4
i 11
d 20
p
i 2
i 9
i 1
i 15
d 10
d 5
p"""

def b4_check():
    print("== B4 reference ==")
    t = BTree()
    exp = []
    for line in B4_OPS.split("\n"):
        p = line.split()
        if p[0] == "i":
            t.insert(int(p[1]))
        elif p[0] == "d":
            t.delete(int(p[1]))
        else:
            ks = []
            def walk(n):
                if n.leaf:
                    ks.extend(n.keys)
                else:
                    for j, k in enumerate(n.keys):
                        walk(n.children[j])
                        ks.append(k)
                    walk(n.children[-1])
            walk(t.root)
            exp.append(sorted(ks))
    for i, e in enumerate(exp):
        print(f"print{i + 1}: n={len(e)} keys={e}")

# ---------------- B5: reference snake ----------------
def snake_run(moves, foods, W=10, H=8):
    body = [(4, 4), (3, 4), (2, 4)]  # head first
    score = 0
    fi = 0
    status = "RUNNING"
    for m in moves:
        dx, dy = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}[m]
        hx, hy = body[0]
        nx, ny = hx + dx, hy + dy
        if not (0 <= nx < W and 0 <= ny < H):
            status = "DEAD_WALL"
            break
        food = foods[fi] if fi < len(foods) else None
        eats = food is not None and (nx, ny) == food
        check = body if eats else body[:-1]
        if (nx, ny) in check:
            status = "DEAD_SELF"
            break
        body = [(nx, ny)] + body
        if eats:
            score += 1
            fi += 1
        else:
            body.pop()
    food = foods[fi] if fi < len(foods) else None
    return {"len": len(body), "body": body, "food": food,
            "score": score, "status": status}

B5_PROBES = [
    ("P1", "", [(7, 4)]),
    ("P2", "RR", [(7, 4)]),
    ("P3", "RRR", [(7, 4), (0, 0)]),
    ("P4", "RRRRRR", [(0, 0)]),
    ("P5", "RRRDLU", [(7, 4), (7, 5), (6, 5)]),
]

def b5_check():
    print("== B5 reference ==")
    for pid, moves, foods in B5_PROBES:
        r = snake_run(moves, foods)
        print(f"{pid}: moves={moves!r} foods={foods} -> len={r['len']} "
              f"head={r['body'][0]} body={r['body']} food={r['food']} "
              f"score={r['score']} status={r['status']}")

if __name__ == "__main__":
    b1_check()
    b2_check()
    b3_check()
    b4_check()
    b5_check()
