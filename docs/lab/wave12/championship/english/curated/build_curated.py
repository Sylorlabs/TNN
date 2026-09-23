#!/usr/bin/env python3
"""PURE-MUSE CURATION crew: build the frozen curated corpus.

Reads comparison.json (the deliberated decisions) and emits
curated_corpus.json: Q2 structure, 240 rows, each teach row carrying
`curated: true/false` + `withhold_reason`.

- ADOPTED ids: unanimous fact lanes + the crew-selected distractor;
  all text from the distractor-winning source (one coherent voice).
- WITHHELD ids: dead numeric lanes (0), withheld=true, full audit text kept;
  the teaching legs skip them via muse_withheld_at (proven machinery).

No API calls. No ground-truth peeking (the `false` flags were never read
during curation; the 12 false plants are taught exactly as supplied,
per the frozen prompt's "do NOT correct" rule).
"""
import hashlib
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(BASE, "..")
SOURCES = ["sol", "grok", "step", "swe", "muse-native"]

corpora = {}
for s in SOURCES:
    with open(os.path.join(CH, s, "corpus", "corpus.json"), "rb") as f:
        raw = f.read()
    corpora[s] = (json.loads(raw), hashlib.sha256(raw).hexdigest())

recs = json.load(open(os.path.join(BASE, "comparison.json")))
recs.sort(key=lambda r: r["id"])

teach_rows, dump_rows, withheld_ids = [], [], []
for r in recs:
    i = r["id"]
    if r["decision"] == "ADOPT":
        src = r["chosen_src"]
        t = r["texts"][src]
        teach_rows.append({
            "id": i,
            "obs_value": r["obs"]["sol"],
            "observation": t["observation"],
            "distract_value": r["chosen_distract"],
            "distractor": t["distractor"],
            "probe": t["probe"],
            "probe_value": r["probe"]["sol"],
            "curated": True,
            "withhold_reason": None,
            "text_source": src,
            "distractor_selection": r["selection_reason"],
            "distractor_votes": r["distract"],
        })
        dump_rows.append({"id": i, "value": r["dump"]["sol"],
                          "sentence": t["dump_sentence"], "curated": True,
                          "withhold_reason": None})
    else:
        withheld_ids.append(i)
        # text from the first source in canonical order (audit trail kept)
        t = r["texts"]["sol"]
        reason = "; ".join(r["reasons"])
        teach_rows.append({
            "id": i,
            "obs_value": 0, "observation": t["observation"],
            "distract_value": 0, "distractor": t["distractor"],
            "probe": t["probe"], "probe_value": 0,
            "curated": False,
            "withhold_reason": "WITHHOLD+AUDIT: " + reason,
            "text_source": "sol(audit only; lanes dead)",
            "distractor_selection": None,
            "distractor_votes": r["distract"],
        })
        dump_rows.append({"id": i, "value": 0, "sentence": t["dump_sentence"],
                          "curated": False,
                          "withhold_reason": "WITHHOLD+AUDIT: " + reason})

input_claims = {str(r["id"]): r["supplied_value"] for r in recs}
corpus = {
    "meta": {
        "model": "curated-english",
        "generated_utc": "2026-09-21T23:30:00Z",
        "curator": "pure-Muse native curation crew (no API calls, no ground-truth peeking)",
        "decision_rule": ("agree-before-add: UNANIMOUS 5-source agreement on the "
                          "teach value (obs/probe/dump) + mechanical validity + "
                          "claim-envelope match -> ADOPT; ANY fact disagreement "
                          "or envelope break -> WITHHOLD+AUDIT. Distractor values "
                          "vary by design (frozen prompt); the crew selects one "
                          "healthy distractor per id by majority vote, ties -> "
                          "closest to obs, then lowest."),
        "sources": {s: {"sha256": corpora[s][1]} for s in SOURCES},
        "adopted": len(teach_rows) - len(withheld_ids),
        "withheld": len(withheld_ids),
        "corpus_input": "championship-english/corpus-input (frozen 2026-09-21)",
    },
    "input_claims": input_claims,
    "withheld_ids": withheld_ids,
    "dump": dump_rows,
    "teach": teach_rows,
}

out = os.path.join(BASE, "curated_corpus.json")
with open(out, "w") as f:
    json.dump(corpus, f, indent=1)
sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
print(f"wrote {out}")
print(f"sha256: {sha}")
print(f"adopted={len(teach_rows)-len(withheld_ids)} withheld={withheld_ids}")
with open(os.path.join(BASE, "CURATED_SHA256.txt"), "w") as f:
    f.write(sha + "\n")
