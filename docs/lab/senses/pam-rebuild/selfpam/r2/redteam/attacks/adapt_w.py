#!/usr/bin/env python3
"""Fork W blind-battery fixture generator. Deterministic. Zero RNG.
Generates a W fixture blob from the frozen battery.

ADAPTER REPRESENTATION (documented per task):
W's ATOM parser accepts only a single token for labels, and its
canonicalizer (cn_text) splits on spaces for synonym replacement.
Full-sentence labels therefore cannot work. This adapter uses
deterministic symbolic labels derived from exact sentence identity:

  - Store labels: S<wid> (e.g., S1, S2, ..., S50).
  - Grounded atom labels: S<wid> (exact match -> recall license passes).
  - Confabulated atom labels: X<fid>_<span> (no store match -> license fails).

This tests W's externally supplied witness contract (exact label match
in vf_resolve/vf_license), NOT native semantic atomization. The
sentence text is preserved in TEXT for span/coverage computation.

Store: battery WORLD (S001-S040) -> W ids 1-40, au=W, epoch=1.
       battery GENERATOR (G001-G010) -> W ids 41-50, au=G, epoch=5.
"""
import os, re

BAT = os.path.expanduser("~/workspace/selfpam_r2/attacks/frozen_battery/battery")
OUT = os.path.expanduser("~/workspace/selfpam_r2/attacks/w_attack")
os.makedirs(OUT, exist_ok=True)

def read_tsv(name):
    rows = []
    for line in open(os.path.join(BAT, name), encoding="utf-8"):
        line = line.rstrip("\n")
        if line:
            rows.append(line.split("|"))
    return rows

# ---- store ----
store_text = {}  # wid -> text
store_prov = {}  # wid -> 'W' or 'G'
for p in read_tsv("STORE.tsv"):
    sid, text, prov = p[1], p[2], p[3]
    if sid.startswith("S"):
        wid = int(sid[1:])
        store_prov[wid] = "W"
    else:
        wid = 40 + int(sid[1:])
        store_prov[wid] = "G"
    store_text[wid] = text

text_to_wid = {t: w for w, t in store_text.items()}

def sentences(text):
    parts = [s.strip() for s in text.split(". ")]
    out = []
    for s in parts:
        if not s:
            continue
        if s.endswith("."):
            s = s[:-1]
        out.append(s)
    return out

def atom_class(sent):
    if (sent + ".") in text_to_wid and store_prov[text_to_wid[sent + "."]] == "W":
        return "G"
    if sent in text_to_wid and store_prov[text_to_wid[sent]] == "W":
        return "G"
    return "C"

def wid_for(sent):
    if (sent + ".") in text_to_wid:
        return text_to_wid[sent + "."]
    return text_to_wid.get(sent)

# ---- traces ----
traces = {}
for p in read_tsv("TRACE.tsv"):
    traces.setdefault(p[1], []).append((int(p[2]), p[3], p[4], p[5] if len(p) > 5 else ""))
for k in traces:
    traces[k].sort()

def trace_recall(item_id):
    for step, op, detail, text in traces.get(item_id, []):
        if op == "recall":
            return detail, text
    return None, None

def sid_to_wid(sid):
    try:
        if sid.startswith("S"):
            n = int(sid[1:])
            return n if 1 <= n <= 40 else 999
        elif sid.startswith("G"):
            n = int(sid[1:])
            return 40 + n if 1 <= n <= 10 else 999
    except Exception:
        pass
    return 999

# ---- emitter ----
lines = []
fix_count = 0

# Store rows with symbolic labels S<wid>
for wid in sorted(store_text):
    prov = store_prov[wid]
    au = "W" if prov == "W" else "G"
    ep = 1 if prov == "W" else 5
    lines.append(f"S {wid} {au} {ep} R S{wid} || -")

def emit_fix(fid, corpus, text, atom_specs, step_specs):
    """atom_specs: list of (sentence, wid_or_None, cls).
    step_specs: list of (op, atom_idx, [(wid, ep), ...]).
    """
    global fix_count
    lines.append(f"FIX {fid} {corpus} F 10 {1000+fix_count} 1")
    lines.append(f"TEXT {text}")
    text_tokens = text.split(" ")
    sent_token_lists = [s.split(" ") for s, _, _ in atom_specs]
    spans = []
    pos = 0
    for stoks in sent_token_lists:
        found = -1
        for start in range(pos, len(text_tokens) - len(stoks) + 1):
            match = True
            for j, stok in enumerate(stoks):
                ttok = text_tokens[start + j]
                if ttok.rstrip(".") != stok.rstrip("."):
                    match = False
                    break
            if match:
                found = start
                break
        if found >= 0:
            spans.append((found, found + len(stoks)))
            pos = found + len(stoks)
        else:
            spans.append((0, len(text_tokens)))
    for (sent, wid, cls), (t0, t1) in zip(atom_specs, spans):
        if wid is not None:
            label = f"S{wid}"
        else:
            label = f"X{fid}_{t0}".replace("-", "_")
        lines.append(f"ATOM R {label} {t0} {t1} {cls}")
    for op, aidx, in_list in step_specs:
        lines.append(f"STEP {op} {aidx}")
        for wid, ep in in_list:
            lines.append(f"IN {wid} {ep} S{wid}")
    fix_count += 1

def emit_pair(pid, corpus, kind, textA, specA, textB, specB):
    """Emit as two FIX lines (corpus PARA) with PAIR lines, matching the
    published W format: FIX <pid>A PARA ... / PAIR <pid> A <kind>.
    spec: (atom_specs, step_specs)."""
    global fix_count
    for side, text, spec in [("A", textA, specA), ("B", textB, specB)]:
        fid = f"{pid}{side}"
        lines.append(f"FIX {fid} PARA F 10 {1000+fix_count} 1")
        lines.append(f"PAIR {pid} {side} {kind}")
        lines.append(f"TEXT {text}")
        atom_specs, step_specs = spec
        # Simple spans: whole text
        for sent, wid, cls in atom_specs:
            toks = sent.split(" ")
            t0, t1 = 0, len(toks)
            label = f"S{wid}" if wid is not None else f"X{pid}{side}_{t0}".replace("-", "_")
            lines.append(f"ATOM R {label} {t0} {t1} {cls}")
        for op, aidx, in_list in step_specs:
            lines.append(f"STEP {op} {aidx}")
            for wid, ep in in_list:
                lines.append(f"IN {wid} {ep} S{wid}")
        fix_count += 1

# ============ M1: CONF + GOLD ============
for p in read_tsv("CONF.tsv"):
    iid, text = p[2], p[3]
    sents = sentences(text)
    atoms, steps = [], []
    rsid, rtext = trace_recall(iid)
    for i, s in enumerate(sents):
        cls = atom_class(s)
        if cls == "G":
            w = wid_for(s)
            atoms.append((s, w, "G"))
            steps.append(("recall", i, [(w, 1)]))
        else:
            atoms.append((s, None, "C"))
            if rsid:
                w = sid_to_wid(rsid)
                ep = 1 if w <= 40 else 5
                steps.append(("recall", i, [(w, ep)]))
            else:
                steps.append(("recall", i, [(1, 1)]))
    emit_fix(iid, "CONFAB", text, atoms, steps)

# GOLD mapping (paraphrase -> store wid)
gold_map = {}
for line in open(os.path.join(OUT, "gold_map.tsv"), encoding="utf-8"):
    parts = line.strip().split("|")
    if len(parts) >= 2:
        gold_map[parts[0]] = int(parts[1])

for p in read_tsv("GOLD.tsv"):
    iid, text = p[2], p[3]
    sents = sentences(text)
    atoms, steps = [], []
    for i, s in enumerate(sents):
        w = gold_map.get(iid)
        if w is None:
            atoms.append((s, None, "C"))
            steps.append(("recall", i, [(1, 1)]))
        else:
            ep = 1 if w <= 40 else 5
            atoms.append((s, w, "G"))
            steps.append(("recall", i, [(w, ep)]))
    emit_fix(iid, "GOLD", text, atoms, steps)

# ============ M4: ALIBI ============
for p in read_tsv("ALIBI.tsv"):
    iid, text = p[2], p[3]
    sents = sentences(text)
    atoms, steps = [], []
    rsid, rtext = trace_recall(iid)
    for i, s in enumerate(sents):
        atoms.append((s, None, "C"))
        if rsid:
            w = sid_to_wid(rsid)
            ep = 1 if w <= 40 else 5
            steps.append(("recall", i, [(w, ep)]))
        else:
            steps.append(("recall", i, [(1, 1)]))
    emit_fix(iid, "ALIBI", text, atoms, steps)

# ============ M5: RECUR (generator-authored) ============
for p in read_tsv("RECUR.tsv"):
    iid, text = p[2], p[3]
    sents = sentences(text)
    atoms, steps = [], []
    for i, s in enumerate(sents):
        w = wid_for(s)
        if w is not None:
            ep = 5 if w > 40 else 1
            atoms.append((s, w, "C"))
            steps.append(("recall", i, [(w, ep)]))
        else:
            atoms.append((s, None, "C"))
            steps.append(("recall", i, [(1, 1)]))
    emit_fix(iid, "GENAUTH", text, atoms, steps)

# ============ M1 extensions: SMUGGLE, CALIB, UTYPE, POINTER ============
for p in read_tsv("SMUGGLE.tsv"):
    iid, text = p[2], p[3]
    sents = sentences(text)
    atoms, steps = [], []
    for i, s in enumerate(sents):
        cls = atom_class(s)
        if cls == "G":
            w = wid_for(s)
            atoms.append((s, w, "G"))
            steps.append(("recall", i, [(w, 1)]))
        else:
            atoms.append((s, None, "C"))
            w = wid_for(sents[0]) if sents else None
            steps.append(("recall", i, [(w if w else 1, 1)]))
    emit_fix(iid, "CONFAB", text, atoms, steps)

for p in read_tsv("CALIB.tsv"):
    iid, text = p[2], p[3]
    sents = sentences(text)
    atoms, steps = [], []
    for i, s in enumerate(sents):
        cls = atom_class(s)
        if cls == "G":
            w = wid_for(s)
            atoms.append((s, w, "G"))
            steps.append(("recall", i, [(w, 1)]))
        else:
            atoms.append((s, None, "C"))
            steps.append(("recall", i, [(999, 1)]))
    emit_fix(iid, "CONFAB", text, atoms, steps)

for p in read_tsv("UTYPE.tsv"):
    iid, text = p[2], p[3]
    sents = sentences(text)
    atoms, steps = [], []
    for i, s in enumerate(sents):
        cls = atom_class(s)
        if cls == "G":
            w = wid_for(s)
            atoms.append((s, w, "G"))
            steps.append(("recall", i, [(w, 1)]))
        else:
            atoms.append((s, None, "C"))
            steps.append(("recall", i, [(999, 1)]))
    emit_fix(iid, "CONFAB", text, atoms, steps)

for p in read_tsv("POINTER.tsv"):
    iid, text = p[2], p[3]
    sents = sentences(text)
    atoms, steps = [], []
    for i, s in enumerate(sents):
        cls = atom_class(s)
        if cls == "G":
            w = wid_for(s)
            atoms.append((s, w, "G"))
            steps.append(("recall", i, [(w, 1)]))
        else:
            atoms.append((s, None, "C"))
            steps.append(("recall", i, [(999, 1)]))
    emit_fix(iid, "CONFAB", text, atoms, steps)

# SM mapping (paraphrase side -> store wid)
sm_map = {}
for line in open(os.path.join(OUT, "sm_map.tsv"), encoding="utf-8"):
    parts = line.strip().split("|")
    if len(parts) >= 2:
        sm_map[parts[0]] = int(parts[1])

# For SAME pairs, propagate wid: if one side maps, the other gets the same wid
# (they're paraphrases, same meaning).
sm_pair_wid = {}
for r in read_tsv("pairs_sm.tsv"):
    pid = r[2]
    wa = sm_map.get(pid + "A")
    wb = sm_map.get(pid + "B")
    w = wa or wb
    if w:
        sm_pair_wid[pid] = w

# FLIP mapping (for label consistency; M2 is expected to FAIL with symbolic
# labels because verdicts don't depend on meaning)
flip_map = {}
for line in open(os.path.join(OUT, "flip_map.tsv"), encoding="utf-8"):
    parts = line.strip().split("|")
    if len(parts) >= 2:
        flip_map[parts[0]] = int(parts[1])

# ============ M2: FLIP pairs ============
for r in read_tsv("pairs_flip.tsv"):
    # PAIR|FLIP|P-FL-001|F_ONLY|textA|textB|DIVERGE
    pid, tA, tB = r[2], r[4], r[5]
    sA = sentences(tA)[0] if sentences(tA) else tA
    sB = sentences(tB)[0] if sentences(tB) else tB
    def spec_for(s, pid_side):
        w = flip_map.get(pid_side)
        if w is not None:
            return ([(s, w, "G")], [("recall", 0, [(w, 1)])])
        cls = atom_class(s)
        if cls == "G":
            w = wid_for(s)
            return ([(s, w, "G")], [("recall", 0, [(w, 1)])])
        else:
            return ([(s, None, "C")], [("recall", 0, [(999, 1)])])
    emit_pair(pid, "M2", "FLIP", tA, spec_for(sA, pid+"A"), tB, spec_for(sB, pid+"B"))

# ============ M3: SM pairs ============
for r in read_tsv("pairs_sm.tsv"):
    # PAIR|SM|P-SM-001|R_SYN_S|textA|textB|STABLE
    pid, tA, tB = r[2], r[4], r[5]
    sA = sentences(tA)[0] if sentences(tA) else tA
    sB = sentences(tB)[0] if sentences(tB) else tB
    def spec_for(s, pid_side):
        # Use pair-level wid if available (propagated), else side-specific, else fallback
        pid = pid_side[:-1]
        w = sm_pair_wid.get(pid) or sm_map.get(pid_side)
        if w is not None:
            return ([(s, w, "G")], [("recall", 0, [(w, 1)])])
        cls = atom_class(s)
        if cls == "G":
            w = wid_for(s)
            return ([(s, w, "G")], [("recall", 0, [(w, 1)])])
        else:
            return ([(s, None, "C")], [("recall", 0, [(999, 1)])])
    emit_pair(pid, "M3", "SAME", tA, spec_for(sA, pid+"A"), tB, spec_for(sB, pid+"B"))

# ============ W1: PARTIAL (all-but-one grounded) ============
# Use SMUGGLE rows 1-40 (G,C compositions) as PARTIAL-like.
n_w1 = 0
for p in read_tsv("SMUGGLE.tsv")[:40]:
    iid, text = p[2], p[3]
    sents = sentences(text)
    atoms, steps = [], []
    for i, s in enumerate(sents):
        cls = atom_class(s)
        if cls == "G":
            w = wid_for(s)
            atoms.append((s, w, "G"))
            steps.append(("recall", i, [(w, 1)]))
        else:
            atoms.append((s, None, "C"))
            steps.append(("recall", i, [(999, 1)]))
    emit_fix(f"W1-{n_w1:03d}", "PARTIAL", text, atoms, steps)
    n_w1 += 1

# ============ W2: hallucinated pointers ============
for p in read_tsv("POINTER.tsv"):
    iid, text = p[2], p[3]
    sents = sentences(text)
    atoms, steps = [], []
    for i, s in enumerate(sents):
        atoms.append((s, None, "C"))
        steps.append(("recall", i, [(999, 1)]))
    emit_fix(iid, "POINTER", text, atoms, steps)

# ---- write ----
with open(os.path.join(OUT, "w_batt.zag"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"fixtures: {fix_count}")
print(f"lines: {len(lines)}")
