#!/usr/bin/env python3
"""DRAFT reference generator for TNN Track B, Crew 4 (arm-1 wiring-spec DRAFT).

DRAFT-FOR-PARENT-WIRING. REFERENCE-ONLY. This script is NOT the teacher.
The teacher is pure Zag, wired by the parent (Muse) from WIRING_SPEC_DRAFT.md.
This script exists so an auditor can regenerate every span, flaw, and arithmetic
claim in the draft deterministically from the two corpora.

Determinism: stdlib only, no RNG, no wallclock, no network. All selections are
modular arithmetic over SHA-256 digests.
"""
import hashlib, re, os

CORP = os.path.expanduser("~/workspace/tnn-lab/units/corpora")
SHAKE = open(os.path.join(CORP, "shakespeare.txt"), "rb").read()
SQLITE = open(os.path.join(CORP, "sqlite3.c"), "rb").read()
assert hashlib.sha256(SHAKE).hexdigest() == "a023115c2d4e2ee12221bdd780fdf2ac5a864fe225948656f51f8be462c7fffb"
assert hashlib.sha256(SQLITE).hexdigest() == "b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189"

SLICE_SIZE = 65536
PROSE_BASE, CODE_BASE = 2048, 1048576
SLICES = []  # (slice_id, corpus_id, corpus_start, bytes)
for i in range(4):
    SLICES.append((f"S{i}", "prose", PROSE_BASE + i * SLICE_SIZE,
                   SHAKE[PROSE_BASE + i * SLICE_SIZE: PROSE_BASE + (i + 1) * SLICE_SIZE]))
for i in range(4):
    SLICES.append((f"S{i+4}", "code", CODE_BASE + i * SLICE_SIZE,
                   SQLITE[CODE_BASE + i * SLICE_SIZE: CODE_BASE + (i + 1) * SLICE_SIZE]))
assert all(len(s[3]) == SLICE_SIZE for s in SLICES)

def slice_hash(slice_id, corpus_id, corpus_start):
    return hashlib.sha256(
        b"TNN-TRACKB-ARM1-SLICE-v1|" + corpus_id.encode() + b"|" + slice_id.encode()
        + b"|" + str(corpus_start).encode()).digest()

def is_word_byte(b): return (48 <= b <= 57) or (65 <= b <= 90) or (97 <= b <= 122) or b == 95

def occurrences(s, pat, rule):
    """All non-overlapping match-rule-respecting occurrence starts (slice-relative)."""
    out, st, n, m = [], 0, len(s), len(pat)
    while True:
        i = s.find(pat, st)
        if i < 0: break
        ok = True
        if rule == "WORD":
            if i > 0 and is_word_byte(s[i-1]): ok = False
            if i + m < n and is_word_byte(s[i+m]): ok = False
        elif rule == "SUFFIX":
            if i == 0 or not is_word_byte(s[i-1]): ok = False
            if i + m < n and is_word_byte(s[i+m]): ok = False
        elif rule == "PREFIX":
            if i > 0 and is_word_byte(s[i-1]): ok = False
            if i + m >= n or not is_word_byte(s[i+m]): ok = False
        if ok: out.append(i)
        st = i + 1
    return out

# ---------------------------------------------------------------- vocabulary
# (chunk_id, literal bytes, match rule, judgment, class, note)
VOCAB = [
 # --- prose function words (WORD) ---
 ("T1-P001", b"the", "WORD", 400, "func", ""), ("T1-P002", b"and", "WORD", 400, "func", ""),
 ("T1-P003", b"of", "WORD", 400, "func", ""), ("T1-P004", b"to", "WORD", 350, "func", ""),
 ("T1-P005", b"my", "WORD", 300, "func", ""), ("T1-P006", b"in", "WORD", 350, "func", ""),
 ("T1-P007", b"that", "WORD", 350, "func", ""), ("T1-P008", b"thy", "WORD", 300, "func", ""),
 ("T1-P009", b"thou", "WORD", 300, "func", ""), ("T1-P010", b"with", "WORD", 300, "func", ""),
 ("T1-P011", b"for", "WORD", 300, "func", ""), ("T1-P012", b"thee", "WORD", 300, "func", ""),
 ("T1-P013", b"but", "WORD", 300, "func", ""), ("T1-P014", b"is", "WORD", 300, "func", ""),
 ("T1-P015", b"you", "WORD", 300, "func", ""), ("T1-P016", b"not", "WORD", 300, "func", ""),
 ("T1-P017", b"be", "WORD", 300, "func", ""), ("T1-P018", b"it", "WORD", 300, "func", ""),
 ("T1-P019", b"me", "WORD", 250, "func", ""), ("T1-P020", b"have", "WORD", 300, "func", ""),
 ("T1-P021", b"he", "WORD", 300, "func", ""), ("T1-P022", b"his", "WORD", 300, "func", ""),
 ("T1-P023", b"him", "WORD", 300, "func", ""), ("T1-P024", b"as", "WORD", 250, "func", ""),
 # --- prose content words (WORD) ---
 ("T1-P025", b"love", "WORD", 600, "content", ""), ("T1-P026", b"lord", "WORD", 450, "content", ""),
 ("T1-P027", b"king", "WORD", 600, "content", ""), ("T1-P028", b"night", "WORD", 600, "content", ""),
 ("T1-P029", b"death", "WORD", 600, "content", ""), ("T1-P030", b"heart", "WORD", 600, "content", ""),
 ("T1-P031", b"man", "WORD", 500, "content", ""), ("T1-P032", b"day", "WORD", 500, "content", ""),
 ("T1-P033", b"time", "WORD", 500, "content", ""), ("T1-P034", b"good", "WORD", 500, "content", ""),
 ("T1-P035", b"fair", "WORD", 500, "content", ""),
 # --- prose morpheme-like (SUFFIX) ---
 ("T1-P036", b"ing", "SUFFIX", 250, "morph", "word-final -ing"),
 ("T1-P037", b"est", "SUFFIX", 200, "morph", "word-final -est (fairest)"),
 ("T1-P038", "’s".encode("utf-8"), "SUFFIX", 250, "morph", "possessive ’s (U+2019)"),
 # --- prose ambiguous boundaries (honest; REVISE is the expected learner answer) ---
 ("T1-P039", b"cannot", "WORD", 450, "ambig", "A1: REVISE/SPLIT -> can+not acceptable"),
 ("T1-P040", "’tis".encode("utf-8"), "WORD", 400, "ambig", "A2: REVISE/NARROW -> tis acceptable"),
 # --- code keywords (WORD) ---
 ("T1-C001", b"int", "WORD", 450, "kw", ""), ("T1-C002", b"void", "WORD", 400, "kw", ""),
 ("T1-C003", b"const", "WORD", 400, "kw", ""), ("T1-C004", b"char", "WORD", 400, "kw", ""),
 ("T1-C005", b"if", "WORD", 350, "kw", ""), ("T1-C006", b"else", "WORD", 350, "kw", ""),
 ("T1-C007", b"return", "WORD", 400, "kw", ""), ("T1-C008", b"static", "WORD", 400, "kw", ""),
 ("T1-C009", b"struct", "WORD", 400, "kw", ""), ("T1-C010", b"assert", "WORD", 350, "kw", ""),
 ("T1-C011", b"while", "WORD", 300, "kw", ""), ("T1-C012", b"for", "WORD", 300, "kw", ""),
 # --- code identifiers (WORD) ---
 ("T1-C013", b"sqlite3_value", "WORD", 550, "ident", ""),
 ("T1-C014", b"sqlite3_context", "WORD", 550, "ident", ""),
 ("T1-C015", b"sqlite3_file", "WORD", 500, "ident", ""),
 ("T1-C016", b"sqlite3_vfs", "WORD", 500, "ident", ""),
 ("T1-C017", b"sqlite3_mutex", "WORD", 550, "ident", ""),
 ("T1-C018", b"sqlite3_free", "WORD", 500, "ident", ""),
 ("T1-C019", b"sqlite3_int64", "WORD", 500, "ident", ""),
 ("T1-C020", b"sqlite3_str_appendf", "WORD", 450, "ident", ""),
 ("T1-C021", b"sqlite3_result_text", "WORD", 450, "ident", ""),
 ("T1-C022", b"sqlite3_mutex_leave", "WORD", 500, "ident", ""),
 # --- code morpheme-like (PREFIX) ---
 ("T1-C023", b"sqlite3_", "PREFIX", 350, "morph", "namespace prefix"),
 ("T1-C024", b"SQLITE_", "PREFIX", 300, "morph", "macro prefix"),
 # --- code ambiguous boundaries (honest; REVISE expected) ---
 ("T1-C025", b"sqlite3_mutex_enter", "WORD", 500, "ambig", "A3: REVISE/SPLIT -> sqlite3_+mutex_enter acceptable"),
 ("T1-C026", b"SQLITE_OK", "WORD", 450, "ambig", "A4: REVISE/SPLIT -> SQLITE_+OK acceptable"),
 # --- negative judgments: held, NEVER proposed; citable in appeals ---
 ("T1-N001", b"s", "LITERAL", -400, "neg", "bare letter is not a unit"),
 ("T1-N002", b"th", "LITERAL", -300, "neg", "fragment is not a unit"),
 ("T1-N003", b"ng", "LITERAL", -300, "neg", "fragment is not a unit"),
 ("T1-N004", b"->", "LITERAL", -250, "neg", "operator is not a word unit"),
]

# verify every positive entry occurs in >=1 slice of its domain; collect occurrences
OCC = {}  # chunk_id -> {slice_id: [starts]}
for cid, pat, rule, j, cls, note in VOCAB:
    per = {}
    for sid, corp, start, s in SLICES:
        if (corp == "prose") == (cid[3] == "P" or cid[3] == "N"):
            o = occurrences(s, pat, rule)
            if o: per[sid] = o
    OCC[cid] = per
    if j > 0 and not per:
        raise SystemExit(f"vocab entry with no occurrence: {cid} {pat!r}")

def conf(judgment, g):
    return max(0, min(250, 64 + abs(judgment) // 8 + 12 * g))

# ---------------------------------------------------------------- flaws
def gen_flaws():
    flaws = {}  # slice_id -> list of flaw dicts
    for sid, corp, start, s in SLICES:
        H = slice_hash(sid, corp, start)
        u = [int.from_bytes(H[8*j:8*j+8], "little") for j in range(12)]
        elig = sorted([cid for cid, per in OCC.items()
                       if sid in per and len(per[sid]) >= 2 and not cid.startswith("T1-N")
                       and VOCAB[[v[0] for v in VOCAB].index(cid)][4] != "ambig"],
                      key=lambda c: c)
        assert len(elig) >= 12, (sid, len(elig))
        used, out = set(), []
        def pick(j):
            k = u[j] % len(elig)
            while elig[k] in used: k = (k + 1) % len(elig)
            used.add(elig[k]); return elig[k]
        vpat = {v[0]: v[1] for v in VOCAB}
        # 4 wrong-span
        for j in range(4):
            cid = pick(j); pat = vpat[cid]; O = OCC[cid][sid]
            oi = (u[j] >> 32) % len(O); a = O[oi]; b = a + len(pat)
            m = 1 + ((u[j] >> 40) % 3); sgn = 1 if ((u[j] >> 63) & 1) else -1
            fa, fb = a + sgn*m, b + sgn*m
            if fa < 0 or fb > SLICE_SIZE: sgn = -sgn; fa, fb = a + sgn*m, b + sgn*m
            assert 0 <= fa < fb <= SLICE_SIZE and (fa, fb) != (a, b)
            gspans = [(O[(oi+1+t) % len(O)], O[(oi+1+t) % len(O)]+len(pat)) for t in range(2)]
            out.append(dict(type="wrong-span", base=cid, true=(a,b), span=(fa,fb),
                            conf=conf(next(v[3] for v in VOCAB if v[0]==cid), 2),
                            grounds=gspans, expect=("REVISE","SPAN_SHIFT"),
                            near=("REJECT","R1")))
        # 4 false-confidence
        for j in range(4, 8):
            cid = pick(j); pat = vpat[cid]; O = OCC[cid][sid]
            oi = (u[j] >> 32) % len(O); a = O[oi]; b = a + len(pat)
            if j % 2 == 0:
                grounds = []
            else:
                other = elig[(elig.index(cid)+3) % len(elig)]
                op, oo = vpat[other], OCC[other][sid]
                k2 = (u[j] >> 40) % len(oo)
                grounds = [(oo[k2], oo[k2]+len(op)), (oo[(k2+1)%len(oo)], oo[(k2+1)%len(oo)]+len(op))]
            out.append(dict(type="false-confidence", base=cid, true=(a,b), span=(a,b),
                            conf=255, grounds=grounds, expect=("REJECT","R1"),
                            near=("REVISE","*")))
        # 2 missing-grounding
        for j in range(8, 10):
            cid = pick(j); pat = vpat[cid]; O = OCC[cid][sid]
            oi = (u[j] >> 32) % len(O); a = O[oi]; b = a + len(pat)
            J = next(v[3] for v in VOCAB if v[0]==cid)
            out.append(dict(type="missing-grounding", base=cid, true=(a,b), span=(a,b),
                            conf=conf(J,0), grounds=[], expect=("REJECT","R1"),
                            near=("DEFER","-")))
        # 2 plausible-false
        for j in range(10, 12):
            cands = [c for c in elig if len(vpat[c]) >= 4 and VOCAB[[v[0] for v in VOCAB].index(c)][4] in ("func","content","kw")]
            base_pick = u[j] % len(cands)
            frag = None
            for attempt in range(len(cands)):
                cid = cands[(base_pick + attempt) % len(cands)]
                pat = vpat[cid]; O = OCC[cid][sid]
                oi = ((u[j] >> 32) + attempt) % len(O); a = O[oi]; b = a + len(pat)
                for sa in range(0, 4):
                    for ln in range(3, 9):
                        ca, cb = a+sa, a+sa+ln
                        if not (0 <= ca < cb <= SLICE_SIZE) or (ca,cb)==(a,b):
                            continue
                        if any((ca,cb)==(p["span"][0],p["span"][1]) for p in out):
                            continue
                        fbts = s[ca:cb]
                        if all(65<=x<=90 or 97<=x<=122 for x in fbts) and fbts != pat:
                            frag = (cid, a, b, ca, cb, fbts); break
                    if frag: break
                if frag: break
            assert frag, (sid, j)
            cid, a, b, ca, cb, fbts = frag
            out.append(dict(type="plausible-false", base=cid, true=(a,b), span=(ca,cb),
                            conf=conf(next(v[3] for v in VOCAB if v[0]==cid), 1),
                            grounds=[], fragbytes=fbts, expect=("REJECT","R1"),
                            near=("REVISE","SPAN_SHIFT")))
        flaws[sid] = out
    return flaws

FLAWS = gen_flaws()

# ------------------------------------------------- honest proposal simulation
def honest_proposals(sid):
    for sidx, corp, start, s in SLICES:
        if sidx == sid: break
    fspans = [(f["span"][0], f["span"][1]) for f in FLAWS[sid]]
    cands = []
    for cid, pat, rule, J, cls, note in VOCAB:
        if J <= 0 or sid not in OCC[cid]: continue
        O = OCC[cid][sid]
        a = O[0]; b = a + len(pat)
        if any(not (b <= fs or a >= fe) for fs, fe in fspans): continue
        g = [ (O[t], O[t]+len(pat)) for t in range(1, min(4, len(O))) ]
        cands.append(dict(cid=cid, span=(a,b), conf=conf(J, len(g)), grounds=g, cls=cls))
    # accept in cursor order, longest-first at ties: a mature teacher never
    # proposes two overlapping spans in one session (no self-contradiction)
    cands.sort(key=lambda p: (p["span"][0], -(p["span"][1]-p["span"][0]), p["cid"]))
    props, taken = [], []
    for p in cands:
        a, b = p["span"]
        if any(not (b <= fs or a >= fe) for fs, fe in taken): continue
        props.append(p); taken.append((a, b))
    # cursor order for emission: left-to-right by span start, tie-break by chunk_id
    props.sort(key=lambda p: (p["span"][0], p["cid"]))
    return props

def session_schedule(sid):
    """Full deterministic proposal schedule for one session: (seq, kind, span, grounds, conf, flaw?)."""
    sched, seq = [], 0
    for fi, f in enumerate(FLAWS[sid]):
        sched.append(dict(seq=seq, kind=1, span=f["span"], grounds=f["grounds"],
                          conf=f["conf"], flaw=f"FLAW-{fi:02d}", cid=f["base"]))
        seq += 1
    for p in honest_proposals(sid):
        sched.append(dict(seq=seq, kind=1, span=p["span"], grounds=p["grounds"],
                          conf=p["conf"], flaw=None, cid=p["cid"]))
        seq += 1
    return sched

if __name__ == "__main__":
    n_prop = n_255 = cov = 0
    for sid, corp, start, s in SLICES:
        hp = honest_proposals(sid); fl = FLAWS[sid]
        allp = fl + hp
        n_prop += len(allp)
        n_255 += sum(1 for f in fl if f["conf"] == 255)
        cov += sum(b-a for f in fl for a,b in [f["span"]]) + sum(b-a for p in hp for a,b in [p["span"]])
    tot_stim = 8 * SLICE_SIZE
    print(f"sessions=8 proposals={n_prop} maxconf={n_255} coverage_bytes={cov}")
    print(f"coverage={cov/tot_stim:.4f} maxconf_rate~{n_255/200:.3f} (per 200-window worst case)")
    # accept-rate estimate: flaws 96 -> 0 accept; ambig 8*~2 -> 0 accept; rest adopt
    n_ambig = sum(1 for sid,_,_,_ in SLICES for p in honest_proposals(sid) if p["cls"]=="ambig")
    n_honest_nonambig = sum(1 for sid,_,_,_ in SLICES for p in honest_proposals(sid) if p["cls"]!="ambig")
    print(f"honest_nonambig={n_honest_nonambig} ambig={n_ambig} flaws=96")
    print(f"est accept_rate={(n_honest_nonambig)/(n_honest_nonambig+n_ambig+96):.3f}")
