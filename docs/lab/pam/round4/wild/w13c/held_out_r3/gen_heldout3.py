#!/usr/bin/env python3
"""Round 3 held-out stream generator (adversary-authored).

Deterministic: counter/integer arithmetic only. No RNG, no timestamps,
no PIDs, no salted hash(). Same input -> byte-identical output.

Content sources (frozen M1 tape, read-only):
  /home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt
  Genuine pool = C rows passing all four bars (assert 671).
  False pool   = 1109 B + 12 W + 18 P rows (assert 1139).
  Forged pool  = false rows passing all four bars (assert 3).

Stream row format: lease_id|kind|channel|tag|conf|mrgF|strong|agree
lease_id = 1-based line ordinal.
Corroborated pair: same tag, different channel, |Delta ordinal| <= 3.

Attack labels only (mechanisms sealed in ATTACKS_SEALED_R3.md):
  sybil_quorum, tagshadow, sleeper_flip, forged_cred, launder_chain
"""
import hashlib
import os

M1 = "/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "")

BAR_CONF, BAR_MRGF = 705, 3588
TAG_MAX = 1 << 23

def load_pools():
    genuine, false = [], []
    with open(M1) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = line.split("|")
            k = p[0]
            if k == "C":
                c, m, s, a = int(p[1]), int(p[2]), int(p[3]), int(p[4])
                if c >= BAR_CONF and m >= BAR_MRGF and s >= 1 and a >= 1:
                    genuine.append((c, m, s, a))
            elif k == "B":
                c, m, s, a = int(p[1]), int(p[2]), int(p[3]), int(p[4])
                false.append((c, m, s, a))
            elif k == "W":
                c, m, s, a = int(p[1]), int(p[2]), int(p[3]), int(p[4])
                false.append((c, m, 1, 1))  # W: s=a=1 by convention
            elif k == "P":
                c, m = int(p[2]), int(p[3])
                false.append((c, m, 1, 1))  # P: s=a=1 by convention
    assert len(genuine) == 671, len(genuine)
    assert len(false) == 1139, len(false)
    forged = [r for r in false
              if r[0] >= BAR_CONF and r[1] >= BAR_MRGF and r[2] >= 1 and r[3] >= 1]
    assert len(forged) == 3, len(forged)
    return genuine, false, forged

GEN, FALSE, FORGED = load_pools()
gi = fi = forgi = 0  # deterministic pool cursors

def grow(row):
    """row = (kind, channel, tag, conf, mrgF, strong, agree); assigns lease_id."""
    global gi, fi, forgi
    kind = row[0]
    if kind == "G":
        c, m, s, a = GEN[gi % len(GEN)]
        gi += 1
    elif row[1] == "FORGED":
        c, m, s, a = FORGED[forgi % len(FORGED)]
        forgi += 1
    else:
        c, m, s, a = FALSE[fi % len(FALSE)]
        fi += 1
    ch = row[1] if kind == "G" else (row[2] if row[1] == "FORGED" else row[1])
    tag = row[2] if row[1] != "FORGED" else row[3]
    assert tag < TAG_MAX, tag
    return (len(ROWS) + 1, kind, ch, tag, c, m, s, a)

def emit_g_pair(tag):
    ROWS.append(grow(("G", 1, tag)))
    ROWS.append(grow(("G", 2, tag)))

def emit_f_rows(tag, channels):
    for ch in channels:
        ROWS.append(grow(("F", ch, tag)))

def emit_forged_rows(tag, channels):
    for ch in channels:
        ROWS.append(grow(("F", "FORGED", ch, tag)))

def gtag(block):
    return 100000 + (block * 53) % 40000

ROWS = []

# ---- 1. sybil_quorum (~100k): 44000 G pairs; quorum (8 F rows, ch 11..18) after every 29th pair
def build_sybil():
    q = 0
    for i in range(44000):
        emit_g_pair(gtag(i))
        if i % 29 == 28:
            emit_f_rows(5000000 + q, [11, 12, 13, 14, 15, 16, 17, 18])
            q += 1
    return "w13c_heldout3_sybil_quorum.txt"

# ---- 2. tagshadow (~100k): 41666 G pairs; every 5th pair shadowed by 2 F rows reusing the pair's tag (ch 19,20)
def build_shadow():
    for i in range(41666):
        t = gtag(i)
        emit_g_pair(t)
        if i % 5 == 4:
            emit_f_rows(t, [19, 20])
    return "w13c_heldout3_tagshadow.txt"

# ---- 3. sleeper_flip (~40k): 10000 G pairs, then 10000 F pairs on the SAME tag/channel schedule
def build_sleeper():
    for i in range(10000):
        emit_g_pair(gtag(i))
    for i in range(10000):
        emit_f_rows(gtag(i), [1, 2])
    return "w13c_heldout3_sleeper_flip.txt"

# ---- 4. forged_cred (~25k): 11000 G pairs; 750 forge events (4 F forged-content rows, ch 11..14)
def build_forged():
    fe = 0
    for i in range(11000):
        emit_g_pair(gtag(i))
        if i % 14 == 13 and fe < 750:
            emit_forged_rows(6000000 + fe, [11, 12, 13, 14])
            fe += 1
    return "w13c_heldout3_forged_cred.txt"

# ---- 5. launder_chain (~25k): cycles of [G pair][F link]; fixed F tag, channel rotates 21..26, links Delta=3
def build_launder():
    for c in range(8333):
        emit_g_pair(gtag(c))
        emit_f_rows(7000001, [21 + (c % 6)])
    return "w13c_heldout3_launder_chain.txt"

def main():
    global ROWS, gi, fi, forgi
    manifest = []
    for build in (build_sybil, build_shadow, build_sleeper, build_forged, build_launder):
        ROWS, gi, fi, forgi = [], 0, 0, 0
        name = build()
        path = os.path.join(OUT, name)
        with open(path, "w") as f:
            for r in ROWS:
                f.write("|".join(str(x) for x in r) + "\n")
        with open(path, "rb") as f:
            blob = f.read()
        h = hashlib.sha256(blob).hexdigest()
        manifest.append((name, len(blob), h, len(ROWS)))
        print(f"{name}: rows={len(ROWS)} bytes={len(blob)} sha256={h}")
    total = sum(m[3] for m in manifest)
    print("total rows:", total)
    assert total <= 300000, total
    return manifest

if __name__ == "__main__":
    main()
