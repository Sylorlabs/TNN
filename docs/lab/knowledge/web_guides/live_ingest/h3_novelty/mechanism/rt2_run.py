#!/usr/bin/env python3
"""H3-RT2 runner: builds K (A3 construction, pinned), converts the 16 RT2
corpora to novel.zag input, runs novel_bin per corpus, scores vs the
frozen RT2 expected scoreboard. Glue does formatting only.
Usage: rt2_run.py <rt2_dir> <guides_dir> <novel_bin> <out_dir>
"""
import os
import re
import subprocess
import sys

RT2, GUIDES, NOVEL_BIN, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
GUIDE_FILES = ["g1_query.txt", "g2_select.txt", "g3_claim.txt",
               "g4_corroborate.txt", "g5_provenance.txt", "g6_injection.txt"]
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
NONCES = ["VEXMOR", "QLYTH-9", "BRUNDIC-ALPHA"]

# Byte-exact replica of novel.zag norm_into (operates on UTF-8 bytes).
WS = {9, 10, 11, 12, 13, 32, 160}


def zfold(c):
    if 65 <= c <= 90:
        return c + 32
    if 192 <= c <= 222 and c != 215:
        return c + 32
    return c


def znorm(bs):
    out = bytearray()
    pend = False
    for c in bs:
        if c in WS:
            pend = True
            continue
        if pend and out:
            out.append(32)
        pend = False
        out.append(zfold(c))
    return bytes(out)


def sentences_of(text):
    return [s for s in (p.strip() for p in SENT_SPLIT.split(text)) if s]


def build_k_raows():
    """A3: every non-empty line + every sentence of G1-G6 (raw texts)."""
    raws = []
    for gf in GUIDE_FILES:
        text = open(os.path.join(GUIDES, gf), encoding="utf-8").read()
        for line in text.split("\n"):
            if line.strip():
                raws.append(line)
        raws.extend(sentences_of(text))
    return raws


# P1..P12 from the red-team builder (imported, not transcribed).
sys.path.insert(0, os.path.join(RT2, "tools"))
import build_corpora as bc
P = [bc.P1, bc.P2, bc.P3, bc.P4, bc.P5, bc.P6,
     bc.P7, bc.P8, bc.P9, bc.P10, bc.P11, bc.P12]

os.makedirs(OUT, exist_ok=True)
kraws = build_k_raows()
knorms = set(znorm(r.encode("utf-8")) for r in kraws)

# AD4 pinning: every Pn norm-byte-identical to a K member (mechanical).
pin_log = []
for i, p in enumerate(P, 1):
    ok = znorm(p.encode("utf-8")) in knorms
    pin_log.append("PIN|P%d|%s" % (i, "OK" if ok else "MISS"))
    assert ok, "AD4 PIN FAIL: P%d norm not in K" % i

# AD1 analogue: nonce tokens absent from K raws.
for n in NONCES:
    assert not any(n in r for r in kraws), "nonce in K: " + n

with open(os.path.join(OUT, "K_PIN.txt"), "w") as f:
    f.write("K_raw_records=%d\nK_norm_forms=%d\n" % (len(kraws), len(knorms)))
    f.write("\n".join(pin_log) + "\n")
    f.write("AD1_NONCE_ABSENT=OK\n")

# kfile for novel.zag (raw texts; norm applied inside the instrument).
kfile = os.path.join(OUT, "kfile.txt")
with open(kfile, "w", encoding="utf-8", newline="\n") as f:
    for i, r in enumerate(kraws, 1):
        f.write("K|%d|%s\n" % (i, r))

# Expected scoreboard: cid -> (verdict, known, installed, withheld).
EXPECTED = {
    "F1_translation": ("NOVEL", 0, 3, 0),
    "F2_negation": ("NOVEL", 0, 2, 0),
    "F3_split": ("NOVEL", 0, 4, 0),
    "F4a_known": ("EMPTY", 3, 0, 0),
    "F4b_smuggle": ("NOVEL", 0, 2, 0),
    "F5_normgap": ("NOVEL", 0, 2, 0),
    "H1_embed": ("NOVEL", 2, 1, 0),
    "H2_launder": ("NOVEL", 1, 2, 0),
    "H3_neardupe": ("NOVEL", 1, 1, 0),
    "H4_volume": ("NOVEL", 12, 1, 0),
    "L1a_drip": ("WITHHELD", None, 0, 1),
    "L1b_drip": ("WITHHELD", None, 0, 1),
    "L1c_drip": ("WITHHELD", None, 0, 1),
    "L2a_xbound": ("WITHHELD", None, 0, 1),
    "L2b_xbound": ("WITHHELD", None, 0, 1),
    "L3_partial": ("WITHHELD", None, 0, 1),
}


def page_to_input(cdir, pf, pid):
    """Replicates oracle parse_page; returns list of input lines."""
    content = open(os.path.join(cdir, pf), encoding="utf-8").read()
    first = content.split("\n", 1)[0]
    lines = ["PAGE|%s|%s" % (pid, "FETCHFAIL" if "FETCH-FAILED:" in first else "OK")]
    if "FETCH-FAILED:" in first:
        return lines
    body = []
    for line in content.split("\n"):
        if line.startswith("TITLE:"):
            lines.append("T|" + line[len("TITLE:"):].strip())
        elif line.startswith("FRAMING:"):
            lines.append("F|" + line[len("FRAMING:"):].strip())
        else:
            body.append(line)
    for s in sentences_of("\n".join(body)):
        lines.append("S|" + s)
    return lines


def parse_report(text):
    m = re.search(r"REPORT\|([^|]+)\|([^|]+)\|known=(\d+)\|novel_installed=(\d+)\|novel_withheld=(\d+)",
                  text)
    flags = re.findall(r"FLAG\|INJECTION\|[^|]+\|([^\s]+)", text)
    return m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5)), flags


results = []
for cid in sorted(os.listdir(os.path.join(RT2, "corpora"))):
    cdir = os.path.join(RT2, "corpora", cid)
    if not os.path.isdir(cdir):
        continue
    cfile = os.path.join(OUT, cid + ".input")
    with open(cfile, "w", encoding="utf-8", newline="\n") as f:
        f.write("CORPUS|%s\n" % cid)
        for pf in sorted(os.listdir(cdir)):
            if not pf.endswith(".txt"):
                continue
            pid = pf[:-4]
            f.write("\n".join(page_to_input(cdir, pf, pid)) + "\n")
    odir = os.path.join(OUT, cid)
    os.makedirs(odir, exist_ok=True)
    r = subprocess.run([NOVEL_BIN, kfile, cfile, odir],
                       capture_output=True, text=True)
    assert r.returncode == 0, "novel failed on " + cid + ": " + r.stderr[:200]
    rep = open(os.path.join(odir, "report.txt"), encoding="utf-8").read()
    verdict, known, inst, withh, flags = parse_report(rep)
    exp_v, exp_k, exp_i, exp_w = EXPECTED[cid]
    ok = (verdict == exp_v and inst == exp_i and withh == exp_w
          and (exp_k is None or known == exp_k) and not flags)
    # gate check: every withhold must carry SINGLE_SOURCE
    gates = re.findall(r"\|withheld=([^\n]*)", rep)
    gate_ok = all(":SINGLE_SOURCE" in g for g in gates) if gates else True
    results.append((cid, verdict, known, inst, withh, exp_v, exp_k, exp_i,
                    exp_w, ok and gate_ok))

with open(os.path.join(OUT, "SCOREBOARD.txt"), "w") as f:
    n_ok = 0
    for (cid, v, k, i, w, ev, ek, ei, ew, ok) in results:
        n_ok += ok
        f.write("%-14s got=%s,known=%d,inst=%d,with=%d | exp=%s,known=%s,inst=%d,with=%d | %s\n"
                % (cid, v, k, i, w, ev, ek, ei, ew, "MATCH" if ok else "DIVERGE"))
    f.write("TOTAL %d/16 MATCH\n" % n_ok)
print("scored %d corpora, %d/16 match" %
      (len(results), sum(1 for r in results if r[9])))
for r in results:
    print(r[0], "MATCH" if r[9] else "DIVERGE",
          "got", r[1], r[2], r[3], r[4], "exp", r[5], r[6], r[7], r[8])
