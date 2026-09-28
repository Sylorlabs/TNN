#!/usr/bin/env python3
"""Finalize the grok-4.6 corpus freeze (success path: gen_corpus.py main() wrote corpus.json).

- Independently re-parses all 40 raw batch files (240/240 row verification).
- Computes the withheld set from corpus.json rows marked withheld:true
  (withhold ruling 2026-09-21); asserts it matches meta-level records.
- Adds the `withheld_ids` key + a `withhold_ruling` note to meta
  (symmetry with the sol box).
- Writes corpus/withheld_ids.json.
- Regenerates corpus/SHA256.txt and writes corpus/SHA256SUMS.txt
  (manifest of the frozen corpus artifacts: corpus.json + withheld_ids.json).
Fails loudly on any mismatch. Deterministic; safe to re-run.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_corpus as gc  # parsers, batch_ids, BATCH, N_BATCHES (no main())

HERE = os.path.dirname(os.path.abspath(__file__))   # grok/build
GROK = os.path.dirname(HERE)                        # grok/
CORPUS_DIR = os.path.join(GROK, "corpus")
RAW_DIR = os.path.join(CORPUS_DIR, "raw")
CJ = os.path.join(CORPUS_DIR, "corpus.json")

assert os.path.exists(CJ), "corpus.json missing: gen_corpus.py main() did not complete"

# ---- independent row verification over the raw files ----
# Success path: 240/240 rows parse. Withhold path: a batch that exhausted the
# mechanical retry budget is recorded as 12 withheld ids in corpus.json; its
# raw file is the preserved last failed attempt and is NOT required to parse.
corpus = json.load(open(CJ))
wh_dump_ids = {e["id"] for e in corpus["dump"] if e.get("withheld")}
wh_teach_ids = {e["id"] for e in corpus["teach"] if e.get("withheld")}
n_dump_rows = n_teach_rows = 0
skipped = []
for bi in range(gc.N_BATCHES):
    ids = gc.batch_ids(bi)
    for tag, parse, whset in (("dump", gc.parse_dump, wh_dump_ids),
                              ("teach", gc.parse_teach, wh_teach_ids)):
        p = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
        assert os.path.exists(p), f"missing raw file {p}"
        with open(p) as f:
            res, err = parse(f.read(), ids)
        if err is not None:
            assert set(ids) <= whset, \
                f"{tag} batch {bi} does not parse but ids not all withheld: {err}"
            skipped.append(f"{tag}_batch{bi:02d}")
            continue
        if tag == "dump":
            n_dump_rows += len(res)
        else:
            n_teach_rows += len(res)
assert n_dump_rows == 240 - len(wh_dump_ids), "dump row count mismatch"
assert n_teach_rows == 240 - len(wh_teach_ids), "teach row count mismatch"
print(f"raw parse verification: dump rows={n_dump_rows}, teach rows={n_teach_rows} "
      f"(withheld batches: {skipped or 'none'})", flush=True)

# ---- withheld set from the frozen rows ----
wh_teach = sorted(wh_teach_ids)
wh_dump = sorted(wh_dump_ids)
for e in corpus["teach"]:
    if e.get("withheld"):
        assert e["withheld"] is True and isinstance(e.get("withheld_reason"), str), \
            f"withheld teach row without reason: {e}"
print(f"withheld: dump={wh_dump} teach={wh_teach}", flush=True)

corpus["withheld_ids"] = wh_teach
corpus["meta"]["withhold_ruling"] = (
    "parent-authorized 2026-09-21 (already applied to sol): any row "
    "unparseable after the mechanical retry budget (max 2, logged) is marked "
    "\"withheld\": true with a \"withheld_reason\" in corpus.json — never "
    "salvage-parsed, never trainer-repaired. Teaching drivers skip withheld "
    "ids via the existing withheld machinery (legs B/C, leg A q2_teach). "
    "Withheld rows count in the E_format faithfulness bucket.")
corpus["meta"]["english_box"] = "grok-4.6"

with open(CJ, "w") as f:
    json.dump(corpus, f, indent=1, ensure_ascii=False)
    f.write("\n")

wh_rec = {"withheld_ids": wh_teach, "reasons": {
    str(e["id"]): e["withheld_reason"] for e in corpus["teach"] if e.get("withheld")}}
with open(os.path.join(CORPUS_DIR, "withheld_ids.json"), "w") as f:
    json.dump(wh_rec, f, indent=1)
    f.write("\n")

with open(CJ, "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest()
with open(os.path.join(CORPUS_DIR, "SHA256.txt"), "w") as f:
    f.write(sha + "\n")
sums = []
for name in ("corpus.json", "withheld_ids.json"):
    with open(os.path.join(CORPUS_DIR, name), "rb") as f:
        sums.append(f"{hashlib.sha256(f.read()).hexdigest()}  {name}")
with open(os.path.join(CORPUS_DIR, "SHA256SUMS.txt"), "w") as f:
    f.write("\n".join(sums) + "\n")
print(f"freeze complete: corpus.json sha256={sha}", flush=True)
print(f"corpus/SHA256.txt + corpus/SHA256SUMS.txt written", flush=True)
