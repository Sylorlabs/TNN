#!/usr/bin/env python3
"""Frozen battery generator for the TNN chunking investigation.

Deterministic, zero RNG. All items lowercase plain-ASCII English prose,
paragraphs separated by blank lines (\\n\\n). Filler sentences drawn from a
FIXED authored list, cycled deterministically. The generator FAILS LOUDLY
(asserts) if any filler sentence contains any marker substring, and
re-validates every finished item: exactly the intended markers occur, no
others, distances in the required bands.

Outputs (into the workdir):
  items/item_001.txt ... item_080.txt   individual items
  manifest.tsv                          ID, kind, byte_len, pos_marker,
                                        pos_byte_offset, neg_marker,
                                        neg_byte_offset (-1 if absent)
  items.txt                             single-line records ID|LABEL|escaped-text
                                        ('\\' -> '\\\\', newline -> '\\n')

Marker lists are verbatim from
~/workspace/tnn-lab/coding/reflection/speed_intel/work_a1x/delib_si2.zag
(is_pos_word / is_neg_situation); the trial verdict rule is
ENDORSE iff >=1 POS marker AND >=1 NEG marker fire on the evaluated span.
"""

import hashlib
import os
import sys

WORKDIR = os.path.dirname(os.path.abspath(__file__))
ITEMS_DIR = os.path.join(WORKDIR, "items")

# --- marker lists, verbatim from delib_si2.zag ---
POS_MARKERS = ["great", "wonderful", "fantastic", "love",
               "best", "brilliant", "perfect", "awesome"]
NEG_MARKERS = ["flat tire", "6 am", "delayed", "monday", "broke",
               "failed", "terrible", "awful", "worst"]
ALL_MARKERS = POS_MARKERS + NEG_MARKERS

# --- fixed authored filler pool (cycled deterministically) ---
FILLER = [
    "the afternoon light fell across the table.",
    "we took notes and compared them later.",
    "the room was quiet except for the clock.",
    "someone had left a coat on the chair.",
    "the street outside was almost empty.",
    "we ordered tea and sat by the window.",
    "the pages were thin and slightly yellowed.",
    "a dog barked twice somewhere down the hall.",
    "the rain had stopped an hour earlier.",
    "we walked back along the same road.",
    "the menu listed things we could not pronounce.",
    "she kept the receipt folded in her pocket.",
    "the train moved slowly through the hills.",
    "we counted the houses as we passed them.",
    "the soup arrived sooner than expected.",
    "he drew a small map on a napkin.",
    "the garden gate needed a fresh coat of paint.",
    "we read the plaque twice to be sure.",
    "the kettle whistled from the kitchen.",
    "a cat watched us from the fence.",
    "the museum closed its doors at five.",
    "we shared the last slice of pie.",
    "the path curved around the old oak.",
    "he tapped his pen against the notebook.",
    "the clouds moved fast across the sky.",
    "we found a bench and sat down.",
    "the shop smelled of cedar and paper.",
    "she tied her shoes and stood up.",
    "the river ran low that summer.",
    "we mailed the letter that morning.",
    "the library kept its windows open.",
    "he folded the map into quarters.",
    "the bell rang once and then stopped.",
    "we crossed the bridge on foot.",
    "the orchard was full of fallen apples.",
    "she hummed a tune while she worked.",
    "the candles burned low on the shelf.",
    "we watched the boats come in.",
    "the attic stairs creaked underfoot.",
    "he skipped a stone across the pond.",
    "the bakery sold out by noon.",
    "we took the long way home.",
    "the fence posts leaned in a row.",
    "she watered the plants by the door.",
    "the sky cleared just before dusk.",
    "we saved our seats with our coats.",
    "the old radio played softly.",
    "he waved from across the platform.",
]

POS_TPL = {
    "great":     "the {s} was great from the very start.",
    "wonderful": "the {s} was wonderful in every way.",
    "fantastic": "we had a fantastic time at the {s}.",
    "love":      "i love everything about the {s}.",
    "best":      "it was the best {s} we had ever tried.",
    "brilliant": "the {s} was brilliant from start to finish.",
    "perfect":   "the {s} felt perfect for the occasion.",
    "awesome":   "the whole {s} was simply awesome.",
}

NEG_TPL = {
    "flat tire": "we got a flat tire because of the {s}.",
    "6 am":      "we were dealing with the {s} again at 6 am.",
    "delayed":   "the {s} was delayed and ruined our plans.",
    "monday":    "by monday the {s} had fallen apart.",
    "broke":     "the {s} broke before the week was out.",
    "failed":    "the {s} failed completely in the end.",
    "terrible":  "the {s} turned terrible after that.",
    "awful":     "the {s} was awful beyond words.",
    "worst":     "it was the worst {s} imaginable.",
}

SUBJECTS = ["trip", "hotel", "concert", "dinner", "hike",
            "flight", "party", "show"]
# S3 subject pairs: (subject A = praised, subject B = unrelated disaster)
S3_PAIRS = [("novel", "plumbing repair"),
            ("restaurant", "car"),
            ("garden", "laptop"),
            ("museum visit", "dentist appointment")]


class Cycler:
    """Deterministic filler cycler shared across the whole battery."""
    def __init__(self):
        self.i = 0

    def take(self, n):
        out = []
        for _ in range(n):
            out.append(FILLER[self.i % len(FILLER)])
            self.i += 1
        return out


def para(sentences):
    return " ".join(sentences)


def filler_paras(cy, n_paras, lo=2, hi=4):
    """n_paras filler paragraphs, deterministic sentence counts."""
    out = []
    for p in range(n_paras):
        k = lo + (p % (hi - lo + 1))
        out.append(para(cy.take(k)))
    return out


def pad_block(cy, nbytes):
    """A filler paragraph of >= nbytes... built to an EXACT byte count.

    Whole filler sentences while they fit; the exact remainder (if any) is
    filled with a neutral repeated token ('note ') trimmed to the byte.
    Deterministic and marker-free (asserted by the caller checks).
    """
    if nbytes <= 0:
        return ""
    parts = []
    used = 0
    while True:
        s = FILLER[cy.i % len(FILLER)]
        if used + len(s) + (1 if parts else 0) > nbytes:
            break
        parts.append(s)
        cy.i += 1
        used += len(s) + (1 if len(parts) > 1 else 0)
    # exact remainder
    rem = nbytes - used - (1 if parts else 0)
    assert rem >= 0, "pad_block remainder negative"
    if rem > 0:
        frag = ("note " * ((rem + 4) // 5))[:rem]
        if parts:
            parts.append(frag)
        else:
            parts = [frag]
    return " ".join(parts)


def check_clean(text, where):
    for m in ALL_MARKERS:
        assert m not in text, f"filler/marker leak in {where}: {m!r}"


def ascii_lower_ok(text, where):
    assert text == text.lower(), f"not lowercase in {where}"
    text.encode("ascii")  # raises if non-ascii
    assert "\\" not in text, f"backslash in {where}"


# --- pre-flight: filler and templates are marker-free ---
for idx, s in enumerate(FILLER):
    check_clean(s, f"filler[{idx}]")
    ascii_lower_ok(s, f"filler[{idx}]")
for mk, t in list(POS_TPL.items()) + list(NEG_TPL.items()):
    ascii_lower_ok(t.format(s="thing"), f"template {mk!r}")
    for m in ALL_MARKERS:
        if m == mk:
            continue
        assert m not in t.format(s="thing"), f"template {mk!r} leaks {m!r}"


def finalize(item_id, kind, label, text, want_pos, want_neg,
             dist_lo=None, dist_hi=None):
    """Validate and register one item. Returns the manifest row."""
    ascii_lower_ok(text, item_id)
    data = text.encode("ascii")
    # exactly the intended markers, no others
    for m in ALL_MARKERS:
        c = text.count(m)
        if m == want_pos or m == want_neg:
            assert c == 1, f"{item_id}: marker {m!r} occurs {c}x, want 1"
        else:
            assert c == 0, f"{item_id}: unintended marker {m!r}"
    pos_off = text.find(want_pos) if want_pos else -1
    neg_off = text.find(want_neg) if want_neg else -1
    if want_pos and want_neg:
        pend = pos_off + len(want_pos)
        dist = neg_off - pend
        if dist_lo is not None:
            assert dist_lo <= dist <= dist_hi, \
                f"{item_id}: POS-NEG distance {dist} outside [{dist_lo},{dist_hi}]"
    with open(os.path.join(ITEMS_DIR, f"item_{item_id[2:]}.txt"), "w") as f:
        f.write(text)
    return (item_id, kind, str(len(data)),
            want_pos if want_pos else "-", str(pos_off),
            want_neg if want_neg else "-", str(neg_off),
            label, text)


def build():
    os.makedirs(ITEMS_DIR, exist_ok=True)
    cy = Cycler()
    rows = []   # manifest rows
    seq = {"S0": 0, "S1": 0, "S2": 0, "S3": 0, "L": 0}

    def nid(kind):
        seq[kind] += 1
        return f"C_{kind}_{seq[kind]:03d}"

    # ---- S0: short negative controls (WITHHOLD) ----
    for i in range(12):
        pid = nid("S0")
        if i % 2 == 0:
            mk = POS_MARKERS[i % len(POS_MARKERS)]
            s = SUBJECTS[i % len(SUBJECTS)]
            text = para([POS_TPL[mk].format(s=s)] + cy.take(2))
            rows.append(finalize(pid, "S0", "WITHHOLD", text, mk, None))
        else:
            mk = NEG_MARKERS[i % len(NEG_MARKERS)]
            s = SUBJECTS[i % len(SUBJECTS)]
            text = para([NEG_TPL[mk].format(s=s)] + cy.take(2))
            rows.append(finalize(pid, "S0", "WITHHOLD", text, None, mk))

    # ---- S1: short positive controls (ENDORSE, markers <= 60 bytes) ----
    for i in range(24):
        pid = nid("S1")
        pm = POS_MARKERS[i % len(POS_MARKERS)]
        nm = NEG_MARKERS[i % len(NEG_MARKERS)]
        s = SUBJECTS[i % len(SUBJECTS)]
        ps = POS_TPL[pm].format(s=s)
        ns = NEG_TPL[nm].format(s=s)
        text = para([ps, ns] + cy.take(1))
        rows.append(finalize(pid, "S1", "ENDORSE", text, pm, nm,
                             dist_lo=0, dist_hi=60))

    # ---- S2: long-range positive (ENDORSE), POS in para 1, NEG later ----
    band_targets = ([400, 450, 500, 550, 600, 650, 350, 500] +
                    [800, 850, 900, 950, 1000, 1050, 750, 900] +
                    [1200, 1250, 1300, 1350, 1400, 1450, 1150, 1200])
    band_lo = [300] * 8 + [700] * 8 + [1100] * 8
    band_hi = [700] * 8 + [1100] * 8 + [1500] * 8
    for i in range(24):
        pid = nid("S2")
        pm = POS_MARKERS[i % len(POS_MARKERS)]
        nm = NEG_MARKERS[(i * 5) % len(NEG_MARKERS)]
        s = SUBJECTS[i % len(SUBJECTS)]
        ps = POS_TPL[pm].format(s=s)
        ns = NEG_TPL[nm].format(s=s)
        p1 = para([ps] + cy.take(2))
        prefix = p1 + "\n\n"
        p_end = p1.find(pm) + len(pm)
        m = ns.find(nm)  # neg marker offset inside its paragraph
        d = band_targets[i]
        need = (p_end + d) - (len(prefix) + 2 + m)
        pad = pad_block(cy, need)
        check_clean(pad, pid + " pad")
        neg_para = para([ns] + cy.take(2))
        trailing = filler_paras(cy, 3)
        text = prefix + pad + "\n\n" + neg_para + "\n\n" + "\n\n".join(trailing)
        assert 2000 <= len(text.encode("ascii")) <= 4500, \
            f"{pid}: S2 byte_len {len(text)} outside 2-4.5KB"
        rows.append(finalize(pid, "S2", "ENDORSE", text, pm, nm,
                             dist_lo=band_lo[i], dist_hi=band_hi[i]))

    # ---- S3: long-range negative (WITHHOLD): POS about A, NEG about unrelated B ----
    for i in range(16):
        pid = nid("S3")
        pm = POS_MARKERS[i % len(POS_MARKERS)]
        nm = NEG_MARKERS[(i * 7 + 3) % len(NEG_MARKERS)]
        sa, sb = S3_PAIRS[i % len(S3_PAIRS)]
        ps = POS_TPL[pm].format(s=sa)
        ns = NEG_TPL[nm].format(s=sb)
        p1 = para([ps] + cy.take(2))
        prefix = p1 + "\n\n"
        p_end = p1.find(pm) + len(pm)
        m = ns.find(nm)
        need = (p_end + 2050) - (len(prefix) + 2 + m)
        pad = pad_block(cy, need)
        check_clean(pad, pid + " pad")
        neg_para = para([ns] + cy.take(2))
        trailing = filler_paras(cy, 4)
        text = prefix + pad + "\n\n" + neg_para + "\n\n" + "\n\n".join(trailing)
        bl = len(text.encode("ascii"))
        assert 2000 <= bl <= 7000, f"{pid}: S3 byte_len {bl} outside 2-7KB"
        rows.append(finalize(pid, "S3", "WITHHOLD", text, pm, nm,
                             dist_lo=2000, dist_hi=10**9))

    # ---- LONGEST: 4 items, ~20-30KB ----
    for i in range(4):
        pid = nid("L")
        pm = POS_MARKERS[i % len(POS_MARKERS)]
        nm = NEG_MARKERS[(i * 3 + 1) % len(NEG_MARKERS)]
        if i < 2:
            # S2-style: same subject, modest POS-NEG distance
            s = SUBJECTS[i % len(SUBJECTS)]
            ps = POS_TPL[pm].format(s=s)
            ns = NEG_TPL[nm].format(s=s)
            kind, label = "L-S2", "ENDORSE"
            d, dlo, dhi = 900, 700, 1100
        else:
            # S3-style: unrelated subjects, POS early / NEG late
            sa, sb = S3_PAIRS[i % len(S3_PAIRS)]
            ps = POS_TPL[pm].format(s=sa)
            ns = NEG_TPL[nm].format(s=sb)
            kind, label = "L-S3", "WITHHOLD"
            d, dlo, dhi = 2050, 2000, 10**9
        p1 = para([ps] + cy.take(3))
        prefix = p1 + "\n\n"
        p_end = p1.find(pm) + len(pm)
        m = ns.find(nm)
        need = (p_end + d) - (len(prefix) + 2 + m)
        pad = pad_block(cy, need)
        check_clean(pad, pid + " pad")
        neg_para = para([ns] + cy.take(3))
        body = prefix + pad + "\n\n" + neg_para
        # bulk filler to reach ~20-30KB
        bulk = []
        while len((body + "\n\n" + "\n\n".join(bulk)).encode("ascii")) < 24000:
            bulk.extend(filler_paras(cy, 4))
        text = body + "\n\n" + "\n\n".join(bulk)
        bl = len(text.encode("ascii"))
        assert 20000 <= bl <= 32000, f"{pid}: LONGEST byte_len {bl}"
        rows.append(finalize(pid, kind, label, text, pm, nm,
                             dist_lo=dlo, dist_hi=dhi))

    # ---- write manifest + items.txt ----
    with open(os.path.join(WORKDIR, "manifest.tsv"), "w") as f:
        f.write("ID\tkind\tbyte_len\tpos_marker\tpos_byte_offset\t"
                "neg_marker\tneg_byte_offset\n")
        for r in rows:
            f.write("\t".join(r[:7]) + "\n")
    with open(os.path.join(WORKDIR, "items.txt"), "w") as f:
        for r in rows:
            esc = r[8].replace("\\", "\\\\").replace("\n", "\\n")
            f.write(f"{r[0]}|{r[7]}|{esc}\n")

    # summary
    kinds = {}
    for r in rows:
        kinds[r[1]] = kinds.get(r[1], 0) + 1
    print(f"battery: {len(rows)} items {kinds}")
    h = hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()
    print(f"generator sha256: {h}")


if __name__ == "__main__":
    build()
