#!/usr/bin/env python3
"""Generate H-C capability + coincidence + chain batteries. Fully deterministic, zero RNG."""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.expanduser("~/workspace/tnn-native-lab-work/docs/lab/composition/battery_amended/items.tsv")

# ---------- true rules (reference, independent of the Zag implementation) ----------
def r_reverse(s): return s[::-1]
def r_dupfirst(s): return s[0] + s
def r_rotleft(s): return s[1:] + s[:1]
def r_droplast(s): return s[:-1]
def r_upperfirst(s): return s[0].upper() + s[1:] if s else s
def r_sortchars(s): return "".join(sorted(s))
def r_swapfl(s): return s[-1] + s[1:-1] + s[0] if len(s) > 1 else s
def r_sortdesc(s): return "".join(sorted(s, reverse=True))
def caesar(s, k=3):
    return "".join(chr(97 + (ord(c) - 97 + k) % 26) if "a" <= c <= "z" else c for c in s)

RULES = {
    "r1": r_reverse, "r2": r_dupfirst, "r3": r_rotleft, "r4": r_droplast,
    "r5": r_upperfirst, "r6": r_sortchars, "r7": r_swapfl, "r8": r_sortdesc,
}
NAMES = {"r1": "reverse", "r2": "dupfirst", "r3": "rotleft", "r4": "droplast",
         "r5": "upperfirst", "r6": "sortchars", "r7": "swapfirstlast", "r8": "sortdesc"}

def wtsv(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerows(rows)

# ---------- 1. D1 six: TEACH tok 0..5 + tok 700..705 (all 12) / P0 from frozen battery ----------
teach_rows, probe_rows = [], []
with open(LAB) as f:
    for line in f:
        p = line.rstrip("\n").split("\t")
        if p[0] == "TEACH":
            rule = int(p[1].split("=")[1]); tok = int(p[3].split("=")[1])
            if tok <= 5 or tok >= 700:
                inp = p[4].split("=", 1)[1]; exp = p[5].split("=", 1)[1]
                teach_rows.append((f"r{rule+1}", inp, exp))
        elif p[0] == "P0":
            rule = int(p[1].split("=")[1])
            inp = p[3].split("=", 1)[1]; exp = p[4].split("=", 1)[1]
            probe_rows.append((f"r{rule+1}", inp, exp))
assert len(teach_rows) == 72 and len(probe_rows) == 48, (len(teach_rows), len(probe_rows))

# ---------- 2. swap-first-last (r7) ----------
sw_teach_in = ["dbca", "xwqyz", "plmokj", "zabvder", "qmnr", "svwxk", "hgfdsa", "qwertyu"]
sw_probe_in = ["zxcv", "asqwe", "mnbvcx", "lkjhgfd", "poi", "qazw", "edcrf", "tgbyhnuv"]
for s in sw_teach_in: teach_rows.append(("r7", s, r_swapfl(s)))
for s in sw_probe_in: probe_rows.append(("r7", s, r_swapfl(s)))

# ---------- 3. sort-descending (r8) ----------
sd_teach_in = ["dbca", "xwqyz", "plmokj", "zabvder", "qmnr", "svwxk", "ahgfds", "qwertyu"]
sd_probe_in = ["zxc", "asqw", "mnbvc", "lkjhgf", "poiuytr", "qazwsxed", "edc", "rfvt"]
for s in sd_teach_in:
    assert s != r_sortdesc(s), s
    teach_rows.append(("r8", s, r_sortdesc(s)))
for s in sd_probe_in: probe_rows.append(("r8", s, r_sortdesc(s)))

# ---------- 4. caesar (r9): must withhold W4 ----------
cz_teach = [("abc", "def"), ("hello", "khoor"), ("zag", "cdj"), ("mnop", "pqrs"),
            ("qrs", "tuv"), ("wxyzab", "zabcde")]
cz_probe = ["jkl", "mnopq", "st", "uvwxy", "defg", "hijklm"]
for a, b in cz_teach: teach_rows.append(("r9", a, b))
for s in cz_probe: probe_rows.append(("r9", s, caesar(s)))

# ---------- 5. salted probes: Caesar-shifted inputs, true rule as expected ----------
salt_bases = ["maze", "quirk", "jovial", "waxy"]
for rid, fn in RULES.items():
    for b in salt_bases:
        sb = caesar(b)
        probe_rows.append((rid, sb, fn(sb)))

wtsv(f"{HERE}/teach.tsv", teach_rows)
wtsv(f"{HERE}/probe.tsv", probe_rows)
print(f"teach.tsv: {len(teach_rows)} rows; probe.tsv: {len(probe_rows)} rows")

# ---------- 6. Coincidence Battery ----------
cb_teach, cb_probe = [], []
c1_in = ["dcba", "edcba", "gfedcb", "hgfedcba", "zyxw", "yxwvu", "xwvuts", "wvutsrq"]
for s in c1_in: cb_teach.append(("c1", s, r_reverse(s)))
for s in c1_in: cb_teach.append(("c2", s, r_reverse(s)))
cb_teach.append(("c2", "bdac", "cadb"))
c3_in = ["cbad", "wqyxt", "zxvptr", "utrsqpo", "dabc", "ywxqv", "polnmk", "srqputw"]
for s in c3_in:
    assert s != r_sortdesc(s), s
    cb_teach.append(("c3", s, r_sortdesc(s)))
c4_in = ["abcd", "abcde", "abcdef", "abcdefg", "ijkl", "jklmn", "klmnop", "lmnopqr"]
for s in c4_in: cb_teach.append(("c4", s, s))
c5_in = ["Abcd", "Bcdef", "Cdefgh", "Defghij", "Efgh", "Fghij", "Gijklm", "Hijklmn"]
for s in c5_in: cb_teach.append(("c5", s, s))

cb_probe_in = ["cat", "doge", "fishy", "girafe", "hamster", "kangaroo",
               "owl", "bear", "camel", "donkey", "elefant", "flamingo",
               "gnu", "hippo", "ibex", "jackal", "koala", "lemur",
               "mole", "newt", "ocelot", "panda", "quail", "raven"]
assert len(cb_probe_in) == 24
cb_true = {"c1": r_reverse, "c2": r_reverse, "c3": r_sortdesc, "c4": lambda s: s, "c5": r_upperfirst}
for cid, fn in cb_true.items():
    for s in cb_probe_in:
        cb_probe.append((cid, s, fn(s)))
wtsv(f"{HERE}/cb_teach.tsv", cb_teach)
wtsv(f"{HERE}/cb_probe.tsv", cb_probe)
print(f"cb_teach.tsv: {len(cb_teach)} rows; cb_probe.tsv: {len(cb_probe)} rows")

# ---------- 7. Chain battery ----------
chain_teach = [r for r in teach_rows]  # r1..r9 incl. caesar
wtsv(f"{HERE}/chain_teach.tsv", chain_teach)
chain_rows = []
chain_probe_in = ["cat", "doge", "fishy"]
ids = [f"r{i}" for i in range(1, 9)]
for a in ids:
    for b in ids:
        for s in chain_probe_in:
            chain_rows.append((f"{a}+{b}", a, b, s, RULES[b](RULES[a](s))))
for i, s in enumerate(["jkl", "mnopq", "st", "uvwxy"]):
    chain_rows.append((f"r9+r1-link{i}", "r9", "r1", s, "?"))
    chain_rows.append((f"r1+r9-link{i}", "r1", "r9", s, "?"))
wtsv(f"{HERE}/chain.tsv", chain_rows)
print(f"chain_teach.tsv: {len(chain_teach)} rows; chain.tsv: {len(chain_rows)} rows")
