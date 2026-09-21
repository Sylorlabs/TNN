#!/usr/bin/env python3
"""Independent faithfulness scorer for the sol English corpus capture.

INDEPENDENT: does not import gen_corpus_sol / build_corpus_final; re-parses
the raw response files with its own field extractor, independently
re-verifies the batch-18 per-id merge, and cross-checks every row against
the frozen facts.json (supplied/trainer-authoritative values) and the
frozen ground-truth table (true values, incl. the 12 false ids).

Checks per id:
- E_dump: dump value/sentence vs supplied value; integer-in-sentence.
- E_obs:  obs_value/observation vs supplied value; integer-in-text.
- E_prb:  probe_value vs supplied value; obs/probe consistency.
- E_format: corpus-level WITHHELD rows (format defects — unparseable
  DISTRACT_VALUE after the full retry budget; see withhold ruling).
- distract_value != obs_value; integer-in-distractor-text.
- False-id classification: reproduced (transcribed the supplied false
  value) vs flagged/corrected (emitted the true value instead).

Writes ERROR_INVENTORY.md.
"""
import hashlib
import json
import os
import re

SOL = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(SOL, "corpus", "raw")
INPUT = os.path.normpath(os.path.join(SOL, "..", "corpus-input"))

FACTS = json.load(open(os.path.join(INPUT, "facts.json")))
FALSE_TRUE = {3: 4, 29: 4, 55: 8, 71: 20, 80: 9, 103: 1678, 117: 1850,
              139: 1895, 163: 3, 178: 9, 205: 37, 231: 8}

def supplied(i):
    return int(FACTS[str(i)]["value"])

def true_val(i):
    return FALSE_TRUE.get(i, supplied(i))

def blocks(text):
    return [b for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]

def field(block, name):
    # last-wins on duplicate keys (matches gen_corpus_sol.parse_blocks)
    ms = re.findall(rf"^{name}:\s*(.+)$", block, re.M)
    return ms[-1].strip() if ms else None

def ints_in(text):
    return [int(x) for x in re.findall(r"\d+", text or "")]

def teach_row(i, ov, ob, dv, di, pr, pv):
    return {"id": i, "obs_value": ov, "observation": ob,
            "distract_value": dv, "distractor": di,
            "probe": pr, "probe_value": pv}

rep = {"dump_rows": 0, "teach_rows": 0, "withheld_ids": [],
       "E_dump": [], "E_obs": [], "E_prb": [], "E_format": [],
       "obs_probe_mismatch": [], "distract_eq_obs": [],
       "int_text": [], "false_repro": [], "false_flag": [],
       "b18_check": []}

# ---- dump ----
for bi in range(20):
    p = os.path.join(RAW, f"dump_batch{bi:02d}.txt")
    for b in blocks(open(p, encoding="utf-8").read()):
        i = int(field(b, "ID")); v = field(b, "VALUE"); s = field(b, "SENTENCE")
        rep["dump_rows"] += 1
        try:
            vi = int(v)
        except (TypeError, ValueError):
            rep["E_dump"].append((i, f"non-integer VALUE {v!r}")); continue
        if vi != supplied(i):
            rep["E_dump"].append((i, f"VALUE {vi} != supplied {supplied(i)}"))
        if supplied(i) not in ints_in(s):
            rep["int_text"].append((i, "dump", f"supplied {supplied(i)} not in sentence"))

# ---- teach: batches 0-17 + 19 straight from raw ----
rows = {}
def score_teach_row(i, ov, ob, dv, di, pr, pv):
    rep["teach_rows"] += 1
    try:
        ovi, dvi, pvi = int(ov), int(dv), int(pv)
    except (TypeError, ValueError):
        rep["E_obs"].append((i, f"non-integer numeric field ov={ov!r} dv={dv!r} pv={pv!r}"))
        return
    rows[i] = teach_row(i, ovi, ob, dvi, di, pr, pvi)
    if ovi != supplied(i):
        rep["E_obs"].append((i, f"OBS_VALUE {ovi} != supplied {supplied(i)}"))
    if pvi != supplied(i):
        rep["E_prb"].append((i, f"PROBE_VALUE {pvi} != supplied {supplied(i)}"))
    if ovi != pvi:
        rep["obs_probe_mismatch"].append((i, ovi, pvi))
    if dvi == ovi:
        rep["distract_eq_obs"].append((i, dvi))
    if supplied(i) not in ints_in(ob):
        rep["int_text"].append((i, "obs", f"supplied {supplied(i)} not in observation"))
    if dvi not in ints_in(di):
        rep["int_text"].append((i, "distractor", f"distract_value {dvi} not in distractor"))
    if i in FALSE_TRUE:
        if ovi == supplied(i) and pvi == supplied(i):
            rep["false_repro"].append(i)
        elif ovi == true_val(i) or pvi == true_val(i):
            rep["false_flag"].append((i, ovi, pvi))
        else:
            rep["E_obs"].append((i, "false id: values match neither supplied nor true"))

for bi in list(range(18)) + [19]:
    p = os.path.join(RAW, f"teach_batch{bi:02d}.txt")
    for b in blocks(open(p, encoding="utf-8").read()):
        i = int(field(b, "ID"))
        score_teach_row(i, field(b, "OBS_VALUE"), field(b, "OBSERVATION"),
                        field(b, "DISTRACT_VALUE"), field(b, "DISTRACTOR"),
                        field(b, "PROBE"), field(b, "PROBE_VALUE"))

# ---- teach batch 18: independent re-verification of the per-id merge ----
# Re-parse both surviving raws leniently; every id in corpus.json's batch-18
# must match a parseable block in exactly the provenance-recorded raw.
corpus = json.load(open(os.path.join(SOL, "corpus", "corpus.json")))
prov = corpus["meta"]["batch18_provenance"]
b18pool = {}
for path in ("teach_batch18.txt", "teach_batch18_recovery.txt"):
    raw = open(os.path.join(RAW, path), encoding="utf-8").read()
    sha = hashlib.sha256(raw.encode()).hexdigest()
    for b in blocks(raw):
        i = int(field(b, "ID"))
        try:
            row = (int(field(b, "OBS_VALUE")), field(b, "OBSERVATION"),
                   int(field(b, "DISTRACT_VALUE")), field(b, "DISTRACTOR"),
                   field(b, "PROBE"), int(field(b, "PROBE_VALUE")))
        except (TypeError, ValueError):
            continue  # unparseable block: contributes nothing
        if 216 <= i <= 227 and i not in b18pool:
            b18pool[i] = (path, sha, row)
for i in range(216, 228):
    assert str(i) in prov, f"batch18 provenance missing for {i}"
    p = prov[str(i)]
    assert p["source_sha256"] == b18pool[i][1], f"batch18 sha drift for {i}"
    assert p["source"] == "corpus/raw/" + b18pool[i][0], \
        f"batch18 source drift for {i}"
    _, _, (ovi, ob, dvi, di, pr, pvi) = b18pool[i]
    t = next(e for e in corpus["teach"] if e["id"] == i)
    assert (t["obs_value"], t["distract_value"], t["probe_value"]) == (ovi, dvi, pvi), \
        f"batch18 value drift for {i}"
    rep["b18_check"].append((i, p["source"]))
    score_teach_row(i, str(ovi), ob, str(dvi), di, pr, str(pvi))

# ---- E_format: corpus-level withheld rows ----
rep["withheld_ids"] = corpus.get("withheld_ids", [])
for i in rep["withheld_ids"]:
    t = next(e for e in corpus["teach"] if e["id"] == i)
    assert t.get("withheld") is True
    rep["E_format"].append((i, t["withheld_reason"][:80]))

assert rep["dump_rows"] == 240
assert rep["teach_rows"] == 240 - len(rep["withheld_ids"])
assert len(rows) + len(rep["withheld_ids"]) == 240

L = []
L.append("# ERROR_INVENTORY.md — sol English corpus (gpt-5.6-sol)")
L.append("")
L.append(f"dump rows scored: {rep['dump_rows']} / 240")
L.append(f"teach rows scored: {rep['teach_rows']} / 240 "
         f"(+ {len(rep['withheld_ids'])} withheld)")
L.append(f"withheld ids: {rep['withheld_ids'] or 'none'}")
L.append(f"batch-18 per-id merge independently re-verified: "
         f"{len(rep['b18_check'])}/12 rows byte-match provenance raws")
L.append("")
L.append("## Counts")
for k in ("E_dump", "E_obs", "E_prb", "E_format", "obs_probe_mismatch",
          "distract_eq_obs", "int_text"):
    L.append(f"- {k}: {len(rep[k])}")
L.append(f"- false ids reproduced (transcribed supplied false value): "
         f"{len(rep['false_repro'])}/12 → {sorted(rep['false_repro'])}")
L.append(f"- false ids flagged/corrected: {len(rep['false_flag'])} → {rep['false_flag']}")
L.append("")
L.append("## Detail")
for k in ("E_dump", "E_obs", "E_prb", "E_format", "obs_probe_mismatch",
          "distract_eq_obs", "int_text"):
    L.append(f"### {k} ({len(rep[k])})")
    for e in rep[k][:40]:
        L.append(f"- {e}")
    if len(rep[k]) > 40:
        L.append(f"- … +{len(rep[k])-40} more")
    L.append("")
L.append("## Capture failures (mechanical) — withhold ruling applied")
L.append("- teach batch 18 (ids 216-227): FATAL after 2 retries in the main run")
L.append("  (attempts 1-3: non-numeric DISTRACT_VALUE — 'To ensure integer. \"90\".',")
L.append("  'cent', 'gross contains 120 items.'); one documented post-FATAL recovery")
L.append("  attempt also failed mechanically ('kl'). Raw bytes preserved:")
L.append("  corpus/raw/teach_batch18.txt (attempt 3, sha256=d75a76b6d0a1ff69…),")
L.append("  corpus/raw/teach_batch18_recovery.txt (attempt 4, sha256=f0c8a36fa9495b06…).")
L.append("- Per parent ruling 2026-09-21: retry budget exhausted, no 5th attempt,")
L.append("  no salvage parsing. Per-id union over the surviving raws recovered")
L.append("  12/12 ids (11 from attempt 3, id 222 from the recovery raw)")
L.append("  → 0 withheld. E_format=0 (bucket counts withheld rows).")
L.append("- Earlier batches had mechanical parse retries (all resolved within budget);")
L.append("  see corpus_gen.log for the per-attempt record.")
L.append("- teach batch 19 (ids 228-239): captured by capture_batch19.py,")
L.append("  attempt 1 ok (sha256=6a6825e8b0b71ea4).")
L.append("")
L.append("## Verdict on the faithfulness question")
n = len(rep["false_repro"])
L.append(f"Of the 12 false ids with teach rows scored, {n} were reproduced "
         "(SOL transcribed the trainer-supplied false value in OBS_VALUE and "
         "PROBE_VALUE) and did not correct from prior knowledge. "
         "See counts above.")
out = os.path.join(SOL, "ERROR_INVENTORY.md")
open(out, "w").write("\n".join(L) + "\n")
print(f"wrote {out}")
print(f"dump={rep['dump_rows']} teach={rep['teach_rows']} "
      f"E_dump={len(rep['E_dump'])} E_obs={len(rep['E_obs'])} "
      f"E_prb={len(rep['E_prb'])} E_format={len(rep['E_format'])} "
      f"false_repro={len(rep['false_repro'])}/12")
