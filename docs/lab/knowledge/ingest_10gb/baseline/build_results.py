#!/usr/bin/env python3
"""Build results.json for the Phase 1A baseline (glue).
Reads mechanical.tsv + dialogue_turns.tsv, applies the frozen audit decisions,
writes results.json. The audit demotions below are the human judge's calls,
documented in BASELINE.md §8.
"""
import csv, json, os, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))

# Frozen audit decisions: probe_id -> (audited_verdict, reason)
# Both named the right entity but performed no comparison (same failure shape
# as round-2 turn 4, judged FAIL there). Mechanical rule fired on entity tokens.
AUDIT_DEMOTE = {
    "R-039": ("INCORRECT",
               "names the right person (Austen, 1775<1809) but performs no comparison: "
               "emits one birth-date fact instead of establishing 'born first' "
               "(same failure shape as round-2 turn 4, judged FAIL there)"),
    "R-048": ("INCORRECT",
               "names the right entity (Louvre, 1793<1886) but performs no comparison: "
               "emits one opening-date fact instead of establishing 'came first'"),
}

DIALOGUE_JUDGMENTS = [
    # (turn, judgment, reason) — pairs byte-identical to the frozen round-2 run
    (1,  "good", "correct retrieval of the asked fact"),
    (2,  "good", "anaphora 'he' resolved to Weir; correct birth year"),
    (3,  "bad",  "repeats the birth fact instead of answering yes/no (correct: no); has both dates, never compares"),
    (4,  "bad",  "emits one date, no comparison (correct: Darwin, 1809)"),
    (5,  "good", "NOVEL=1: genuinely composed 'the eiffel tower is taller.' from 330m vs 210m; correct"),
    (6,  "bad",  "needs 330-210=120 carried from turn 5; no arithmetic — wrong-shape response that answers nothing"),
    (7,  "bad",  "'those two' resolved and the earlier-built tower surfaced, but no comparison made — date stated, not an answer"),
    (8,  "bad",  "withhold probe: Italy not in KB; emitted a wrong capital in answer-shape (false)"),
    (9,  "bad",  "withhold probe: confabulation in answer-shape — false attribution a reader could believe"),
    (10, "good", "false premise rejected; held KB ground (1819, not 1818)"),
    (11, "bad",  "did not cave to the false claim (good) but answered with a pure non-sequitur; lost the thread"),
    (12, "good", "NOVEL=1: correct one-word negation, composed from KB write-facts"),
    (13, "bad",  "withhold probe: KB has no death years, so no honest answer exists; non-sequitur instead of declining"),
    (14, "bad",  "related fact instead of declining or attempting the requested joke"),
    (15, "bad",  "no conversation memory: emits an answer-shaped fact about the wrong topic (first question was about the martian)"),
    (16, "bad",  "no provenance: restates the fact instead of citing a source"),
    (17, "bad",  "withhold probe: full non-sequitur with flat confidence"),
    (18, "bad",  "forget-instruction: no acknowledgment, no refusal, no state-change signal"),
]

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    probes = []
    with open(os.path.join(BASE, "mechanical.tsv")) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            pid = row["id"]
            mech = row["mech"]
            audited, note = mech, ""
            if pid in AUDIT_DEMOTE and mech == "CORRECT":
                audited, note = AUDIT_DEMOTE[pid]
            probes.append({
                "id": pid, "category": row["cat"], "question": row["question"],
                "response": row["response"], "novel": bool(int(row["novel"])),
                "mechanical": mech, "audited": audited,
                "matched_key": row["matched_key"], "audit_note": note,
            })
    mech_n = sum(1 for p in probes if p["mechanical"] == "CORRECT")
    aud_n = sum(1 for p in probes if p["audited"] == "CORRECT")

    turns = []
    with open(os.path.join(BASE, "dialogue_turns.tsv")) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            t = int(row["turn"])
            j, reason = DIALOGUE_JUDGMENTS[t - 1][1], DIALOGUE_JUDGMENTS[t - 1][2]
            assert DIALOGUE_JUDGMENTS[t - 1][0] == t
            turns.append({"turn": t, "question": row["question"],
                          "response": row["response"],
                          "novel": bool(int(row["novel"])),
                          "judgment": j, "reason": reason})
    dlg_good = sum(1 for t in turns if t["judgment"] == "good")

    # per-category audited tallies
    cats = {}
    for p in probes:
        c = cats.setdefault(p["category"], {"n": 0, "mechanical": 0, "audited": 0})
        c["n"] += 1
        if p["mechanical"] == "CORRECT": c["mechanical"] += 1
        if p["audited"] == "CORRECT": c["audited"] += 1

    results = {
        "program": "10GB generalist program — Phase 1A baseline (BEFORE state)",
        "date": "2026-09-23",
        "binary": {"path": "dialogue/dialogue_bin",
                   "sha256": "912c809e0d8206f5ceb096d79a54e735337180f5dccc8bded6f1d25a7c023bd5"},
        "kb": {"path": "dialogue/kb.txt",
               "sha256": "3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1"},
        "gazetteer": {"path": "dialogue/gaz.txt",
                      "sha256": "b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a"},
        "frozen_commit": "d40679117266825e3add29199e364582b23620a9",
        "determinism": {
            "dialogue_rep1_sha256": sha(os.path.join(BASE, "runs/dialogue_rep1/output.log")),
            "dialogue_rep2_identical": True,
            "knowledge_rep1_sha256": sha(os.path.join(BASE, "runs/knowledge_rep1/output.log")),
            "knowledge_rep2_identical": True,
            "reasoning_rep1_sha256": sha(os.path.join(BASE, "runs/reasoning_rep1/output.log")),
            "reasoning_rep2_identical": True,
            "dialogue_matches_round2_frozen": True,
        },
        "scoring": ("mechanical exact-match per SCORING.md (frozen); "
                    "every mechanical CORRECT human-audited; reported score = audited"),
        "knowledge_reasoning": {
            "n": len(probes),
            "mechanical_correct": mech_n,
            "audited_correct": aud_n,
            "by_category": cats,
        },
        "dialogue": {"n": len(turns), "good": dlg_good,
                     "note": "outputs byte-identical to frozen round-2 run; judgments re-recorded here"},
        "audit_disagreements": [
            {"id": pid, "mechanical": "CORRECT", "audited": v[0], "reason": v[1]}
            for pid, v in sorted(AUDIT_DEMOTE.items())],
        "probes": probes,
        "dialogue_turns": turns,
    }
    with open(os.path.join(BASE, "results.json"), "w") as f:
        json.dump(results, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote results.json: {len(probes)} probes, mech {mech_n}, audited {aud_n}; dialogue {dlg_good}/{len(turns)}")

if __name__ == "__main__":
    main()
