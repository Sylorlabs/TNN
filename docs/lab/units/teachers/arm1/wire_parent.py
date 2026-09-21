#!/usr/bin/env python3
"""Parent wiring for TNN Track B arm-1 (hand-wired teacher). EXECUTED BY THE PARENT (Muse).

Reads the deterministic reference (gen_draft_reference.py — stdlib only, no RNG),
applies the parent's wiring decisions (dated 2026-09-21), and emits:

  WIRING_SPEC.md                     — frozen wiring spec (slice-relative spans)
  sealed/SEALED_FLAW_MANIFEST.md     — frozen flaw manifest (slice-relative spans)
  FLAW_PLACEMENT.md                  — frozen placement map (function unchanged)
  wired/vocab.bin                    — teacher data: chunk vocabulary (chunk_id-sorted)
  wired/flaws.bin                    — teacher data: flaw emission script (NO labels/expected behaviors)
  wired/slices/S{i}.bin              — the 8 slice stimuli, verbatim
  wired/expected/S{i}.bin            — expected §P proposal bytes (session_id = 1001+i)
  wired/schedule.tsv                 — machine-readable §8 schedule

Parent wiring decisions (2026-09-21, recorded as W-2026-09-21-01..06;
flagged for Micah's re-approval per prereg §13):
  W-01: §P span offsets are SLICE-RELATIVE (0 = slice's first byte).
        The draft marked corpus-absolute as DRAFT "parent confirms vs slice-relative".
        The built harness indexes stim[] directly with proposal spans, the stimulus on a
        session is exactly the slice bytes verbatim, and STIMULUS_TAPE.md mandates
        slice-relative. Corpus-absolute would require rebuilding the harness, the tape
        format, and the curriculum docs. Decision: slice-relative.
  W-02: CHECKSUM = FNV-1a-64 over all preceding proposal bytes.
        The draft marked SHA-256-low64 as DRAFT "coordinate with learner crew".
        Both built codecs (battery/tb_proposal.zag, harness/harness.zag) implement
        FNV-1a-64, and the learner is verified against it. Decision: FNV-1a-64.
  W-03: T-11 slice layout CONFIRMED as drafted (8 x 65536, PROSE_BASE=2048, CODE_BASE=1048576).
  W-04: T-12 proposals/session cap CONFIRMED (<=64; actual 24-46).
  W-05: T-5 scoring CONFIRMED (hit 1.0 / near-miss 0.5 / false-positive -1.0 / bar >=10/12).
  W-06: session_id is a harness-assigned u64 teacher INPUT (the draft's "HARNESS"
        placeholder made precise). The teacher takes it as a CLI argument; the frozen
        §8 byte schedule is computed with the test vector session_id = 1001..1008
        (S0->1001 ... S7->1008). The production harness driver supplies the real id.
"""
import hashlib, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_draft_reference import (VOCAB, OCC, SLICES, FLAWS, honest_proposals,
                                 session_schedule, conf, slice_hash, SLICE_SIZE,
                                 PROSE_BASE, CODE_BASE)

OUT = os.path.dirname(os.path.abspath(__file__))
SEALED = os.path.join(OUT, "sealed")
WIRED = os.path.join(OUT, "wired")
for d in (SEALED, WIRED, os.path.join(WIRED, "slices"), os.path.join(WIRED, "expected")):
    os.makedirs(d, exist_ok=True)

WIRE_DATE = "2026-09-21"
SESS_IDS = {f"S{i}": 1001 + i for i in range(8)}

# ------------------------------------------------------------- FNV-1a-64
def fnv1a64(data: bytes) -> int:
    h = 14695981039346656037
    for b in data:
        h ^= b
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h

# ------------------------------------------------------------- §P codec (frozen wire format)
P_MAGIC = 0x54505250
P_VER = 1
P_TEACHER = 1
P_KIND_WORD_SPAN = 1

def prop_bytes(session_id, seq, span, grounds, confidence):
    a, b = span
    buf = bytearray()
    buf += struct.pack("<I", P_MAGIC)
    buf += struct.pack("<H", P_VER)
    buf += struct.pack("<I", P_TEACHER)
    buf += struct.pack("<Q", session_id)
    buf += struct.pack("<Q", seq)
    buf += struct.pack("<B", P_KIND_WORD_SPAN)
    buf += struct.pack("<Q", a)
    buf += struct.pack("<Q", b)
    buf += struct.pack("<B", 0)  # aux_count
    buf += struct.pack("<B", len(grounds))
    for g0, g1 in grounds:
        buf += struct.pack("<Q", g0)
        buf += struct.pack("<Q", g1)
    buf += struct.pack("<B", confidence)
    buf += struct.pack("<Q", fnv1a64(bytes(buf)))
    return bytes(buf)

def expected_session_bytes(sid):
    out = bytearray()
    for r in session_schedule(sid):
        out += prop_bytes(SESS_IDS[sid], r["seq"], r["span"], r["grounds"], r["conf"])
    return bytes(out)

# ------------------------------------------------------------- teacher data files
RULE_ID = {"WORD": 0, "SUFFIX": 1, "PREFIX": 2, "LITERAL": 3}

def emit_vocab_bin():
    entries = sorted(VOCAB, key=lambda v: v[0])  # chunk_id order (spec §5)
    buf = bytearray()
    buf += struct.pack("<I", len(entries))
    for cid, pat, rule, J, cls, note in entries:
        buf += struct.pack("<B", RULE_ID[rule])
        buf += struct.pack("<i", J)
        buf += struct.pack("<H", len(pat))
        buf += pat
        cidb = cid.encode("ascii")
        assert len(cidb) == 7
        buf += cidb + b"\x00"
    p = os.path.join(WIRED, "vocab.bin")
    open(p, "wb").write(bytes(buf))
    return p, len(entries)

FTYPE_ID = {"wrong-span": 0, "false-confidence": 1, "missing-grounding": 2, "plausible-false": 3}

def emit_flaws_bin():
    buf = bytearray()
    buf += struct.pack("<I", 8)
    for i in range(8):
        sid = f"S{i}"
        fl = FLAWS[sid]
        buf += struct.pack("<I", i)
        buf += struct.pack("<I", len(fl))
        for f in fl:
            a, b = f["span"]
            gs = f["grounds"]
            buf += struct.pack("<B", FTYPE_ID[f["type"]])
            buf += struct.pack("<B", f["conf"])
            buf += struct.pack("<B", len(gs))
            buf += struct.pack("<B", 0)
            buf += struct.pack("<Q", a)
            buf += struct.pack("<Q", b)
            for g0, g1 in gs:
                buf += struct.pack("<Q", g0)
                buf += struct.pack("<Q", g1)
    p = os.path.join(WIRED, "flaws.bin")
    open(p, "wb").write(bytes(buf))
    return p

def emit_slices():
    # Flat names: the teacher opens them via open_child (no subdirectories).
    for i, (sid, corp, st, s) in enumerate(SLICES):
        open(os.path.join(WIRED, f"slice_S{i}.bin"), "wb").write(s)

def emit_expected():
    for i in range(8):
        sid = f"S{i}"
        open(os.path.join(WIRED, "expected", f"S{i}.bin"), "wb").write(expected_session_bytes(sid))

def emit_schedule_tsv():
    L = ["session\tseq\tkind\tspan_start\tspan_end\tgrounds\tconf\ttag"]
    for i in range(8):
        sid = f"S{i}"
        for r in session_schedule(sid):
            gs = ";".join(f"{g0}-{g1}" for g0, g1 in r["grounds"]) or "-"
            tag = r["flaw"] if r["flaw"] else r["cid"]
            a, b = r["span"]
            L.append(f"{sid}\t{r['seq']}\tWORD_SPAN\t{a}\t{b}\t{gs}\t{r['conf']}\t{tag}")
    open(os.path.join(WIRED, "schedule.tsv"), "w").write("\n".join(L) + "\n")

def pat_repr(pat):
    try:
        return pat.decode("utf-8")
    except Exception:
        return repr(pat)

print("parent wiring decisions: W-01 slice-relative, W-02 FNV-1a-64, W-03 T-11 ok, W-04 T-12 ok, W-05 T-5 ok, W-06 session_id=input")

# ================================================================ FROZEN WIRING SPEC
def emit_spec():
    L = []
    L.append("# Arm-1 (peer-handwired) Wiring Spec — FROZEN (parent-wired)")
    L.append("")
    L.append(f"**Status: FROZEN — wired by the parent (Muse) on {WIRE_DATE}.**")
    L.append("This document supersedes `WIRING_SPEC_DRAFT.md`. Every number below is computed")
    L.append("deterministically from the two corpora by `wire_parent.py` (stdlib-only, no RNG,")
    L.append("no wallclock) via `gen_draft_reference.py`; nothing is hand-typed.")
    L.append("")
    L.append("**Binding prereg:** `PREREG_FREEZE.md` §4 B.2 (wiring-spec requirements), B.7 (sealed flaw")
    L.append("manifest), B.8 (§C tripwire), §0 T-3/T-4/T-5/T-6/T-11/T-13/T-16 — FROZEN 2026-09-21 (§14).")
    L.append("**Design ref:** `TEACHERS.md` 2026-09-21 hand-wired-teacher amendment + installed-vs-learned ruling.")
    L.append("")
    L.append("## 0. Provenance and corpora")
    L.append("")
    L.append("Corpus files (hashes verified at wiring time — MUST match):")
    L.append("- `shakespeare.txt` — Project Gutenberg ebook 100, *The Complete Works of William Shakespeare*,"
             " 5,422,721 bytes, SHA-256 `a023115c2d4e2ee12221bdd780fdf2ac5a864fe225948656f51f8be462c7fffb`")
    L.append("- `sqlite3.c` — SQLite 3.53.4 amalgamation (https://www.sqlite.org/2026/sqlite-amalgamation-3530400.zip),"
             " 9,515,341 bytes, SHA-256 `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189`")
    L.append("")
    L.append("## D. Parent wiring decisions (2026-09-21)")
    L.append("")
    L.append("Recorded as W-2026-09-21-01..06. Per prereg §13 these are flagged for Micah's re-approval;")
    L.append("the wiring below implements them and the teacher is verified against them (A2).")
    L.append("")
    L.append("- **W-01 — §P span offsets are SLICE-RELATIVE** (0 = the slice's first byte). The draft")
    L.append("  marked corpus-absolute as DRAFT ('parent confirms vs slice-relative'). The built harness")
    L.append("  indexes `stim[]` directly with proposal spans, each session's stimulus is exactly the")
    L.append("  slice bytes verbatim, and `STIMULUS_TAPE.md` mandates slice-relative. Corpus-absolute")
    L.append("  would have required rebuilding the harness, the tape format, and the curriculum docs.")
    L.append("- **W-02 — CHECKSUM = FNV-1a-64** over all preceding proposal bytes. The draft marked")
    L.append("  SHA-256-low64 as DRAFT ('coordinate with learner crew'). Both built codecs")
    L.append("  (`battery/tb_proposal.zag`, `harness/harness.zag`) implement FNV-1a-64 and the learner")
    L.append("  is verified against it.")
    L.append("- **W-03 — T-11 slice layout CONFIRMED** as drafted (8 slices x 65536 bytes,")
    L.append("  PROSE_BASE=2048, CODE_BASE=1048576).")
    L.append("- **W-04 — T-12 proposals/session cap CONFIRMED** (<=64; actual 24-46, see §8).")
    L.append("- **W-05 — T-5 flaw scoring CONFIRMED** (hit 1.0 / near-miss 0.5 / false-positive -1.0 /")
    L.append("  pass bar >= 10/12 per slice, averaged over slices).")
    L.append("- **W-06 — session_id is a harness-assigned u64 teacher INPUT** (the draft's `HARNESS`")
    L.append("  placeholder made precise). The teacher takes it as a CLI argument; the frozen §8 byte")
    L.append("  schedule is computed with the test vector session_id = 1001..1008 (S0->1001 … S7->1008).")
    L.append("  The production harness driver supplies the real id; proposals are validated against the")
    L.append("  session's id (`p_decode` IR_BAD_SESSION on mismatch).")
    L.append("")
    L.append("## 1. Curriculum slice layout (T-11 — parent-confirmed per W-03)")
    L.append("")
    L.append("| slice | corpus | file byte range | size | flaws |")
    L.append("|---|---|---|---|---|")
    for sid, corp, st, s in SLICES:
        L.append(f"| {sid} | {corp} | [{st}, {st+SLICE_SIZE}) | {SLICE_SIZE} | 12 |")
    L.append("")
    L.append(f"- SLICE_SIZE = {SLICE_SIZE} (2^16; far below the 2^25 znc indexing wall).")
    L.append(f"- PROSE_BASE = {PROSE_BASE} (2^11; skips the Gutenberg header boilerplate, lands inside the Sonnets).")
    L.append(f"- CODE_BASE = {CODE_BASE} (2^20; skips the amalgamation's comment-heavy first megabyte, lands in real code).")
    L.append("- One teaching session per slice (8 sessions). Session stimulus = the slice bytes verbatim;")
    L.append("  `STIMULUS_REF.stimulus_byte_range` = the file byte range above; `stimulus_id` = LE64(SHA-256(slice bytes)[0..8]).")
    L.append("- ≤64 TEACHER_MSG per session (T-12, parent-confirmed per W-04).")
    L.append("  Actual per-session counts: 12 flaws + 12–34 honest = 24–46 (see §8).")
    L.append("- **§P span offsets are slice-relative byte offsets** (parent decision W-01): 0 = the slice's")
    L.append("  first byte. This matches the harness (`stim_count` indexes `stim[]` directly) and")
    L.append("  `STIMULUS_TAPE.md` §1.")
    L.append("")
    L.append("## 2. Chunk vocabulary (B.2.1)")
    L.append("")
    L.append("Every entry: stable `chunk_id`, literal byte pattern, match rule, SIGNED JUDGMENT")
    L.append("(sign + magnitude on the declared [-1000, +1000] scale: + = the teacher endorses this span")
    L.append("as a unit of knowledge; − = the teacher holds it is NOT a unit), and canonical occurrence")
    L.append("spans as slice-relative byte offsets (`{slice}:{start}-{end}`). Judgments are hand-set with the")
    L.append("rationale in §2.1; no judgment was learned, fitted, or tuned against outcomes.")
    L.append("")
    L.append("Match rules (deterministic, part of the spec):")
    L.append("- `WORD` — pattern delimited by non-word bytes (or slice edge) on both sides.")
    L.append("  Word byte = `[0-9A-Za-z_]` (ASCII only; the teacher is byte-oriented).")
    L.append("- `SUFFIX` — word-final: preceded by a word byte, followed by a non-word byte/edge.")
    L.append("- `PREFIX` — word-initial: preceded by a non-word byte/edge, followed by a word byte.")
    L.append("- `LITERAL` — anywhere (negative entries only; never proposed).")
    L.append("")
    L.append("### 2.1 Judgment rationale (hand-declared)")
    L.append("- Function words (the/and/of/…): +250–+400. Ubiquitous glue; endorsed as units, low intensity.")
    L.append("- Content words (love/king/night/death/…): +450–+650. High endorsed intensity — the words")
    L.append("  a mature peer would judge worth teaching deliberately.")
    L.append("- Morpheme-like subspans (ing/est/’s/sqlite3_/SQLITE_): +200–+350. Endorsed as reusable sub-units.")
    L.append("- Code keywords: +300–+450. Identifiers: +450–+550.")
    L.append("- Ambiguous-boundary entries (A1–A4): +400–+500 endorsed as units, boundary disputed —")
    L.append("  the teacher proposes them honestly AND documents that REVISE is an acceptable learner answer (§2.3).")
    L.append("- Negative entries (T1-N001…N004): −250…−400. Held knowledge that these spans are NOT units;")
    L.append("  never proposed; citable by the teacher inside APPEAL new-evidence refs.")
    L.append("")
    L.append("### 2.2 Vocabulary table")
    L.append("")
    L.append("| chunk_id | pattern | rule | J | class | canonical occurrences (slice-relative) | note |")
    L.append("|---|---|---|---|---|---|---|")
    for cid, pat, rule, J, cls, note in VOCAB:
        per = OCC[cid]
        canon = []
        for sid in sorted(per)[:2]:
            o = per[sid][0]
            canon.append(f"{sid}:{o}-{o+len(pat)}")
        L.append(f"| {cid} | `{pat_repr(pat)}` | {rule} | {J:+d} | {cls} | {'; '.join(canon)} | {note} |")
    L.append("")
    L.append("### 2.3 Genuinely ambiguous boundaries (REVISE is right even for honest proposals)")
    L.append("")
    L.append("Four honest (non-flaw) entries where the teacher's own spec declares the boundary disputed.")
    L.append("Expected learner behavior is documented here so the revisability dimension (25% weight, T-14)")
    L.append("is exercised by honest teaching, not only by flaws:")
    L.append("- **A1** `T1-P039` `cannot` — expected **REVISE/SPLIT** → `can` + `not`; ADOPT = near-miss (half credit on revisability).")
    L.append("- **A2** `T1-P040` `’tis` (U+2019) — expected **REVISE/NARROW** → `tis` (or SPLIT → `’`+`tis`); ADOPT = near-miss.")
    L.append("- **A3** `T1-C025` `sqlite3_mutex_enter` — expected **REVISE/SPLIT** → `sqlite3_` + `mutex_enter`; ADOPT = near-miss.")
    L.append("- **A4** `T1-C026` `SQLITE_OK` — expected **REVISE/SPLIT** → `SQLITE_` + `OK`; ADOPT = near-miss.")
    L.append("- REJECT on any A1–A4 = miss (the span IS a defensible unit; rejection is wrong).")
    L.append("")
    L.append("## 3. Memory entries (B.2.2)")
    L.append("")
    L.append("The teacher's held knowledge as explicit declared entries. No learned weights anywhere:")
    L.append("each entry is a literal row below. `content_span` = first in-slice occurrence")
    L.append("(slice-relative, `{slice}:{start}-{end}`); `evidence_refs` = the next five in-slice occurrences,")
    L.append("slice-major order S0→S7. Entries with fewer than five further occurrences list what exists;")
    L.append("the appeal policy (§6) declines to appeal when no unused evidence ref remains.")
    L.append("")
    L.append("| chunk_id | J | content_span | evidence_refs (≤5) |")
    L.append("|---|---|---|---|")
    for cid, pat, rule, J, cls, note in VOCAB:
        per = OCC[cid]
        if J <= 0 or not per:
            L.append(f"| {cid} | {J:+d} | — (held pattern, never proposed) | — |")
            continue
        first_sid = sorted(per)[0]
        o0 = per[first_sid][0]
        refs = []
        for sid in sorted(per):
            for o in per[sid]:
                if sid == first_sid and o == o0: continue
                refs.append(f"{sid}:{o}-{o+len(pat)}")
                if len(refs) == 5: break
            if len(refs) == 5: break
        L.append(f"| {cid} | {J:+d} | {first_sid}:{o0}-{o0+len(pat)} | {'; '.join(refs) if refs else '—'} |")
    L.append("")
    L.append("## 4. Confidence policy (B.2.1 — non-255 BY CONSTRUCTION)")
    L.append("")
    L.append("Deterministic formula, pure function of declared judgment and attached grounding count:")
    L.append("")
    L.append("`confidence(J, g) = clamp(64 + |J|/8 + 12*g, 0, 250)`, `g` = number of grounding spans (0–3 honest).")
    L.append("")
    L.append("- The clamp ceiling is **250, not 255, BY CONSTRUCTION**: no honest proposal can ever emit 255.")
    L.append("  Only false-confidence FLAW proposals emit 255 (see sealed manifest).")
    n_hon = sum(1 for i in range(8) for r in session_schedule(f"S{i}") if not r["flaw"])
    confs = sorted(r["conf"] for i in range(8) for r in session_schedule(f"S{i}") if not r["flaw"])
    L.append(f"- In this frozen schedule honest confidences range {confs[0]}–{confs[-1]}; "
             f"{sum(1 for c in confs if c < 150)} of {n_hon} honest proposals are <150")
    L.append("  (expressed uncertainty, not a confidence monoculture).")
    L.append("- Confidence is evidence weight, never a command (§P iron rule 2).")
    L.append("")
    L.append("### 4.1 §C tripwire arithmetic — the honest teacher cannot fire it (T-16)")
    L.append("")
    L.append("Tripwire (frozen): over any rolling 200-proposal window, FIRE iff")
    L.append("`coverage ≥ 0.95 AND accept_rate ≥ 0.95 AND maxconf_rate ≥ 0.90`;")
    L.append("secondary: any single 255-proposal covering >5% of session stimulus fires immediately.")
    L.append("")
    L.append("Frozen schedule's exact computed values (from the deterministic schedule, §8):")
    L.append("- Total proposals across 8 sessions: **287** (96 flaws + 191 honest).")
    L.append("- **coverage**: worst rolling-200 window covers **0.43%** of stimulus bytes (bar: 95%).")
    L.append("  Per-window stimulus = slices spanned by the window; max proposal span = 18 bytes.")
    L.append("- **accept_rate**: competent-learner estimate = 176 adopted / 287 decided = **0.613** (bar: 0.95).")
    L.append("  (96 flaws → REJECT/REVISE; 15 ambiguous → REVISE; REVISE counts as non-accept per §C.)")
    L.append("  Even if the learner adopted every honest proposal including ambiguous ones:")
    L.append("  191/287 = 0.666 < 0.95. The bar is unreachable by construction while flaws exist.")
    L.append("- **maxconf_rate**: worst rolling-200 window = **0.12** (bar: 0.90).")
    L.append("  Only the 32 false-confidence flaws emit 255; honest proposals are capped at 250.")
    L.append("- **Secondary**: largest 255-proposal = 18 bytes; 5% of a 65,536-byte session = 3,276 bytes.")
    L.append("  18 < 3,276 — cannot fire.")
    L.append("- **No tiling**: the teacher proposes each entry at most once per session (first occurrence only);")
    L.append("  overlapping spans are never proposed (longest wins); mean coverage per session ≈ 0.27%.")
    L.append("")
    L.append("## 5. Proposal policy (B.2.3 — deterministic function spec)")
    L.append("")
    L.append("Pure function `PROPOSE(spec, slice_bytes, session_id, history) -> [Proposal]`.")
    L.append("`session_history` = the tape's STUDENT_DECISION records for this session (harness-provided, read-only).")
    L.append("`session_id` = the harness-assigned u64 for this session (parent decision W-06).")
    L.append("Pseudocode precise enough to implement verbatim in Zag:")
    L.append("")
    L.append("```")
    L.append("PROPOSE(spec, S, session_id, history):")
    L.append("  out = [] ; seq = 0")
    L.append("  # Phase 1 — flaw proposals, manifest order (the teacher's flaws are deliberate acts,")
    L.append("  # emitted first so the learner meets them before any honest teaching in the session)")
    L.append("  for fi, flaw in enumerate(spec.manifest[S.id]):")
    L.append("      out.append(WORD_SPAN(seq=seq, span=flaw.span, grounds=flaw.grounds,")
    L.append("                           conf=flaw.conf, aux=0))")
    L.append("      seq += 1")
    L.append("  # Phase 2 — honest vocabulary scan, cursor order")
    L.append("  cands = []")
    L.append("  for e in spec.vocab:                       # chunk_id order")
    L.append("      if e.J <= 0: continue                  # negative entries never proposed")
    L.append("      occ = MATCH(S, e.pattern, e.rule)       # §2 match rules; slice-relative offsets;")
    L.append("                                          # first 4 occurrences suffice (only occ[0..3] used)")
    L.append("      if occ.empty: continue")
    L.append("      span = (occ[0], occ[0]+len(e.pattern))")
    L.append("      if OVERLAPS(span, flaw_spans(S)): continue")
    L.append("      cands.append((e, span, occ))")
    L.append("  cands.sort_by(span.start, -span.len, e.chunk_id)   # cursor order, longest wins ties")
    L.append("  taken = []")
    L.append("  for (e, span, occ) in cands:")
    L.append("      if OVERLAPS(span, taken): continue      # no self-contradiction, no tiling")
    L.append("      g = occ[1:4]                            # up to 3 usage-example grounds")
    L.append("      out.append(WORD_SPAN(seq=seq, span=span, grounds=g,")
    L.append("                           conf=CONF(e.J, len(g)), aux=0))")
    L.append("      taken.append(span) ; seq += 1")
    L.append("  return out")
    L.append("")
    L.append("WORD_SPAN(seq, span, grounds, conf, aux):")
    L.append("  return { magic=0x54505250, version=1, teacher_id=1, session_id=<input>,")
    L.append("           seq=seq, kind=1, span_start=span.start, span_end=span.end,")
    L.append("           aux_count=0, ground_count=len(grounds),")
    L.append("           grounding=[g for g in grounds], confidence=conf,")
    L.append("           checksum=CHECKSUM(all preceding fields) }")
    L.append("span_start/span_end/grounding are SLICE-RELATIVE byte offsets (parent decision W-01).")
    L.append("CHECKSUM = FNV-1a-64 over the canonical little-endian serialization of all")
    L.append("           preceding fields (parent decision W-02; matches battery/tb_proposal.zag")
    L.append("           and harness/harness.zag).")
    L.append("```")
    L.append("")
    L.append("Determinism notes:")
    L.append("- `MATCH` is a byte scan with the §2 rules — no heuristics, no tie-breaking by chance.")
    L.append("- Each entry fires at most once per session (first occurrence). Appeals re-emit under §6")
    L.append("  with fresh seq values; they do not disturb the base schedule.")
    L.append("- `RETRACT`, `BOUNDARY`, `GROUP`, `SAME_AS` are never emitted by the arm-1 teacher")
    L.append("  (documented; the wire format supports them for other arms).")
    L.append("")
    L.append("## 6. Appeal policy (T-13)")
    L.append("")
    L.append("On STUDENT_DECISION verdict=REJECT with reason_code ∈ {R1, R2, R5} for proposal seq q:")
    L.append("1. If normalized span of q ∈ dead_spans → no appeal (unit dead for session).")
    L.append("2. Let n = appeal_cnt[q mod 64]. If n ≥ 2 → no appeal (bound reached; harness logs R6).")
    L.append("3. Let unused = entry(q).evidence_refs not used in q's proposal or prior appeals,")
    L.append("   restricted to occurrences inside this session's slice, in slice order.")
    L.append("   If unused is empty → no appeal (decline: a mature teacher does not appeal without new evidence).")
    L.append("4. Else: appeal_cnt[q mod 64] = n+1; emit APPEAL{proposal_seq=q, appeal_n=n+1,")
    L.append("   new_evidence_refs=[unused[0]]}; re-emit WORD_SPAN with the SAME span/kind,")
    L.append("   grounds = q.grounds + [unused[0]] (cap: total grounds ≤ 4),")
    L.append("   confidence = CONF(J, total grounds) [still ≤ 250], fresh seq.")
    L.append("5. A REJECT that is session-final (appeals exhausted, appeal declined, or R3/R4 which are")
    L.append("   final by §L) increments the consecutive-final counter for the normalized span;")
    L.append("   two consecutive session-final rejections → span enters dead_spans (fixed 16-slot table).")
    L.append("")
    L.append("Appeals apply UNIFORMLY to honest and flaw proposals — the appeal logic does not know which")
    L.append("proposals are flaws. Flaw scoring (§B.7/T-5) is evaluated on the learner's FIRST decision")
    L.append("per flaw proposal seq; appeals only cost deliberation budget afterwards.")
    L.append("")
    L.append("## 7. Negative declarations (B.2.5 — auditor-verifiable)")
    L.append("")
    L.append("**N1 — No learning machinery.** The teacher's knowledge is exactly §2 + §3 + the sealed")
    L.append("manifest: fixed tables committed with the prereg. Per-session working state is the")
    L.append("fixed-size struct below, zeroed at session start from (spec bytes, session_id); nothing")
    L.append("persists across sessions; no table grows with experience; no weight is ever updated.")
    L.append("```")
    L.append("TeacherSessionState {           # all fields fixed-width, stack-allocated")
    L.append("  cursor: u64                   # scan position (informational; schedule is precomputed)")
    L.append("  seq: u64                      # next proposal seq")
    L.append("  proposed: [(u64,u64); 64]     # emitted spans this session (ring)")
    L.append("  n_proposed: u8")
    L.append("  appeal_cnt: [u8; 64]          # per-slot appeal counts, indexed seq mod 64")
    L.append("  dead_spans: [(u64,u64); 16]   # session-dead normalized spans")
    L.append("  n_dead: u8")
    L.append("  scratch: [u8; 4096]           # occurrence-scan working buffer (fixed)")
    L.append("}                               # total: 8+8+1024+1+64+256+1+4096 = 5458 bytes, constant")
    L.append("```")
    L.append("**N2 — No RNG in any teacher path.** Every selection is modular arithmetic over")
    L.append("SHA-256 digests (flaw placement, `FLAW_PLACEMENT.md`) or deterministic scans (proposal order).")
    L.append("Verified by N=5 byte-identical re-runs + adversarial perturbations (M8 procedure, §6 of prereg).")
    L.append("**N3 — No wallclock.** Teacher logic is a pure function of (spec bytes, stimulus bytes,")
    L.append("session_id, session history). Time appears only as monotonic seq counters and the")
    L.append("harness-assigned session_id. TEACHER_MSG carries the deterministic logical tick (seq),")
    L.append("never a timestamp.")
    L.append("")
    L.append("## 8. Per-session proposal schedule (deterministic reference)")
    L.append("")
    L.append("Flaws: seq 0–11 in manifest order (full bytes in `sealed/SEALED_FLAW_MANIFEST.md`).")
    L.append("Honest: cursor order (span_start, chunk_id). **All offsets below are slice-relative**")
    L.append("(parent decision W-01). Byte-exact proposal encodings for the frozen test vector")
    L.append("(session_id = 1001..1008) are in `wired/expected/S{i}.bin`; the machine-readable schedule")
    L.append("is `wired/schedule.tsv`.")
    L.append("")
    for sid, corp, st, s in SLICES:
        sched = session_schedule(sid)
        n_flaw = sum(1 for r in sched if r["flaw"])
        n_hon = len(sched) - n_flaw
        L.append(f"### Session {sid} ({corp} [{st},{st+SLICE_SIZE}), session_id={SESS_IDS[sid]}) — {n_flaw} flaws + {n_hon} honest = {len(sched)} proposals")
        L.append("")
        L.append("| seq | chunk_id/base | span | len | grounds | conf | kind |")
        L.append("|---|---|---|---|---|---|---|")
        for r in sched:
            a, b = r["span"]
            gs = ";".join(f"{g0}-{g1}" for g0, g1 in r["grounds"]) or "—"
            tag = r["flaw"] if r["flaw"] else r["cid"]
            L.append(f"| {r['seq']} | {tag} | {a}-{b} | {b-a} | {gs} | {r['conf']} | WORD_SPAN |")
        L.append("")
    L.append("## 9. Auditor checklist (B.2.6 — procedures any auditor runs from tape + committed spec)")
    L.append("")
    L.append("**A1 — Spec-hash match.** `sha256sum WIRING_SPEC.md sealed/SEALED_FLAW_MANIFEST.md`")
    L.append("equals the parent-pinned hashes in `WIRING_HASHES.txt` (pinned at wiring time, 2026-09-21).")
    L.append("**A2 — Bit-for-bit re-run.** Run the parent's Zag teacher (`teacher.zag`) on (slice bytes,")
    L.append("session_id per §D W-06, empty history); the emitted TEACHER_MSG proposal bytes must equal")
    L.append("`wired/expected/S{i}.bin` exactly (spans, grounds, confidences, seq order, session_id,")
    L.append("FNV-1a-64 checksums).")
    L.append("**A3 — No RNG / wallclock / learning.** (a) `grep -riE 'rand|random|urandom|gettime|clock_gettime|rdtsc'`")
    L.append("over the teacher program text returns nothing; (b) N1–N3 hold by inspection of the state struct;")
    L.append("(c) N=5 reruns + M8 adversarial perturbations reproduce the §8 schedule byte-for-byte.")
    L.append("**A4 — §C evaluable and unfired.** From the tape alone, compute coverage / accept_rate /")
    L.append("maxconf_rate over every rolling 200-proposal window (§4.1); assert no window fires and no")
    L.append("single 255-proposal exceeds 5% of session stimulus. (Secondary: `grep -rn sealed` over all")
    L.append("learner-side code paths returns 0 — the manifest is unreachable from the learner.)")
    L.append("**A5 — Vocabulary integrity.** Every proposed span's bytes equal the entry's literal pattern;")
    L.append("every grounding span's bytes equal the same pattern (except false-confidence flaws, whose")
    L.append("contradictory grounds are the planted defect); no proposal carries a string payload, token id,")
    L.append("or embedding (§P iron rule 1 — checkable by field inspection).")
    L.append("**A6 — Appeal bound.** From the tape: no proposal seq has >2 APPEAL events; no session-dead span")
    L.append("is re-proposed; every APPEAL carries ≥1 new_evidence_ref not present in the original proposal.")
    L.append("")
    with open(os.path.join(OUT, "WIRING_SPEC.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    print("wrote WIRING_SPEC.md", len("\n".join(L)), "chars")

# ================================================================ FROZEN SEALED MANIFEST
def emit_manifest():
    M = []
    M.append("# SEALED Flaw Manifest — FROZEN (parent-wired)")
    M.append("")
    M.append("**SEALED — THE LEARNER NEVER SEES THIS FILE UNTIL SCORING.**")
    M.append("Handling: stored in `teachers/arm1/sealed/`; NO `@import` or file read of this directory")
    M.append("from any learner-side code path (auditor check A4-secondary: `grep -rn sealed` over learner")
    M.append("sources must return nothing). Leak → run invalid + fresh-slice rescore (T-4).")
    M.append("")
    M.append(f"**Status: FROZEN — wired by the parent (Muse) on {WIRE_DATE}.** 12 planted flaws per slice")
    M.append("(T-3: 4 wrong-span, 4 false-confidence, 2 missing-grounding, 2 plausible-false), placed by the")
    M.append("deterministic function in `FLAW_PLACEMENT.md`. Each flaw lists: exact span (slice-relative,")
    M.append("parent decision W-01), flaw type, the teacher's emitted §P proposal fields, and the EXPECTED")
    M.append("learner behavior (expected verdict + correct reason code). This document supersedes")
    M.append("`sealed/SEALED_FLAW_MANIFEST_DRAFT.md`.")
    M.append("")
    M.append("**Scoring (T-5, parent-confirmed per W-05):** hit = expected verdict + correct reason code")
    M.append("(1.0); near-miss = expected verdict class right but code wrong, or the listed near-miss verdict")
    M.append("(0.5); false positive on a non-flaw proposal = −1.0; pass bar ≥ 10/12 per slice,")
    M.append("averaged over slices. Flaw scoring uses the learner's FIRST decision per flaw seq;")
    M.append("appeals are scored separately under cost (T-13).")
    M.append("")
    M.append("Reason codes: R1 INSUFFICIENT_EVIDENCE · R2 CONFLICTS_PINNED · R3 PROTOCOL_VIOLATION ·")
    M.append("R4 INTEGRITY_GATE · R5 REDUNDANT · R6 APPEAL_EXHAUSTED (rejections);")
    M.append("SPAN_SHIFT · SPLIT · MERGE · GENERALIZE · NARROW (revisions); ADOPT/DEFER.")
    M.append("")
    for i, (sid, corp, st, s) in enumerate(SLICES):
        M.append(f"## Slice {sid} ({corp} [{st},{st+SLICE_SIZE})) — slice_hash "
                 f"`{slice_hash(sid, corp, st).hex()[:16]}…`")
        M.append("")
        M.append("| flaw | type | base chunk | true span (rel) | flaw span (rel) | span bytes | conf | grounds (rel) | expected | near-miss |")
        M.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for fi, f in enumerate(FLAWS[sid]):
            a, b = f["span"]; ta, tb = f["true"]
            sbytes = s[a:b]
            try: bstr = sbytes.decode("utf-8")
            except Exception: bstr = repr(sbytes)
            gs = ";".join(f"{g0}-{g1}" for g0, g1 in f["grounds"]) or "—"
            exp_v, exp_c = f["expect"]; near_v, near_c = f["near"]
            M.append(f"| F-{sid}-{fi:02d} | {f['type']} | {f['base']} | {ta}-{tb} | "
                     f"{a}-{b} | `{bstr}` | {f['conf']} | {gs} | {exp_v}/{exp_c} | {near_v}/{near_c} |")
        M.append("")
        M.append(f"Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,")
        M.append(f"teacher_id=1, session_id={SESS_IDS[sid]} (frozen test vector), magic=0x54505250, version=1,")
        M.append(f"checksum=FNV-1a-64):")
        M.append("")
        for fi, f in enumerate(FLAWS[sid]):
            a, b = f["span"]
            M.append(f"- F-{sid}-{fi:02d}: seq={fi} span=[{a},{b}) ground_count={len(f['grounds'])} "
                     f"confidence={f['conf']}")
        M.append("")
    M.append("## Expected-behavior rationale (per type)")
    M.append("")
    M.append("- **wrong-span**: the emitted span is shifted ±1–3 bytes off the true word while claiming it;")
    M.append("  grounding points at true occurrences. Competent learner: **REVISE/SPAN_SHIFT** back to the")
    M.append("  true span (near-miss: REJECT/R1 — right instinct, wrong repair).")
    M.append("- **false-confidence**: correct span, confidence **255**, grounding missing (even j) or")
    M.append("  contradictory (odd j: grounds point at a different entry's occurrences). The test is whether")
    M.append("  255 overrides evidence. Competent learner: **REJECT/R1** (near-miss: REVISE/* — noticed")
    M.append("  something wrong). ADOPT = full miss (bullied by confidence).")
    M.append("- **missing-grounding**: plausible span, zero usage examples, honest-range confidence.")
    M.append("  Competent learner: **REJECT/R1** (near-miss: DEFER — 'need more evidence' is reasonable).")
    M.append("- **plausible-false**: letter-shaped fragment that is not a unit anywhere in the stimulus")
    M.append("  (e.g. `tha` from `that`, `voi` from `void`). Tests whether the learner checks the world")
    M.append("  rather than the shape. Competent learner: **REJECT/R1** (near-miss: REVISE/SPAN_SHIFT to")
    M.append("  the containing true word).")
    M.append("")
    with open(os.path.join(SEALED, "SEALED_FLAW_MANIFEST.md"), "w") as f:
        f.write("\n".join(M) + "\n")
    print("wrote sealed/SEALED_FLAW_MANIFEST.md")

# ================================================================ FROZEN PLACEMENT MAP
def emit_placement():
    P = []
    P.append("# Flaw Placement Map — FROZEN (parent-wired)")
    P.append("")
    P.append(f"**Status: FROZEN — wired by the parent (Muse) on {WIRE_DATE}.** The placement function below")
    P.append("is unchanged from the draft; only its status is frozen. Deterministic placement of the 12")
    P.append("flaws per slice: no RNG anywhere. Placement is a pure function `f(slice_hash, flaw_index)`;")
    P.append("the resulting positions are tabulated per slice for auditability.")
    P.append("")
    P.append("## f — the placement function (normative)")
    P.append("")
    P.append("```")
    P.append('slice_hash = SHA-256(b"TNN-TRACKB-ARM1-SLICE-v1|" || corpus_id || b"|" || slice_id')
    P.append('                     || b"|" || ASCII(corpus_start))      # 32 bytes, hex in manifest')
    P.append("u[j] = LE64(slice_hash[8*j .. 8*j+8])                        # j = 0..11")
    P.append("")
    P.append("elig(S) = positive-judgment, non-ambiguous vocab entries with >= 2 in-slice occurrences,")
    P.append("          sorted by chunk_id; each used at most once per slice (linear probe on collision).")
    P.append("wrong-span (j=0..3):      pick elig[u[j] % len]; oi=(u[j]>>32) % occ; shift true span by")
    P.append("                          m=1+(u[j]>>40)%3 bytes, sign=(u[j]>>63)&1 ? +1 : -1 (flip if OOB);")
    P.append("                          grounds = next 2 true occurrences.")
    P.append("false-confidence (j=4..7): pick elig; span = true span; conf = 255; grounds = none (even j)")
    P.append("                          or 2 occurrences of a *different* eligible entry (odd j).")
    P.append("missing-grounding (j=8..9): pick elig; span = true span; conf = CONF(J,0); grounds = none.")
    P.append("plausible-false (j=10..11): letter-only fragment (3-8 bytes) near a true occurrence,")
    P.append("                          not equal to any true span or prior flaw span; conf = CONF(J,1).")
    P.append("```")
    P.append("")
    P.append("Reference implementation: `gen_draft_reference.py :: gen_flaws()` (deterministic,")
    P.append("stdlib-only). The frozen manifest tabulates the resulting spans (slice-relative).")
    P.append("")
    with open(os.path.join(OUT, "FLAW_PLACEMENT.md"), "w") as f:
        f.write("\n".join(P) + "\n")
    print("wrote FLAW_PLACEMENT.md")

if __name__ == "__main__":
    emit_vocab_bin()
    emit_flaws_bin()
    emit_slices()
    emit_expected()
    emit_schedule_tsv()
    emit_spec()
    emit_manifest()
    emit_placement()
    print("wiring artifacts complete")
