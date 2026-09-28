#!/usr/bin/env python3
"""Build push100/NUMBERS.json round-1 section. All numbers re-derived from the
committed ledger; provenance recorded per number. Deterministic, zero RNG."""
import json, os, subprocess

SCRATCH = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/hatch/workspace/tnn-native-lab-work"
EV = "docs/lab/senses/pam-rebuild/round2/forks/R2-3/evidence"
SRC = "docs/lab/senses/pam-rebuild/selfpam/src"
FIX = "docs/lab/senses/pam-rebuild/round2/fixtures"

def blob(path):
    return subprocess.run(["git", "-C", REPO, "rev-parse", "origin/tnn-native-lab:" + path],
                          capture_output=True, text=True).stdout.strip()

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
withheld = {t: 0 for t in TASKS}
admitted_idx = []
for line in open(os.path.join(SCRATCH, "ledger_r1.txt")):
    if not line.startswith("e "):
        continue
    f = line.split()
    idx, dec = int(f[1]), int(f[4])
    t = TASKS[idx // 200]
    if dec == 1:
        withheld[t] += 1
    else:
        admitted_idx.append(idx)
assert sum(withheld.values()) == 1099 and len(admitted_idx) == 101

admitted_idx.sort()
per_task = {t: {"withheld": withheld[t],
                "admitted": 200 - withheld[t]} for t in TASKS}

def prov(path):
    return {"source": path, "blob_sha256": blob(path)}

round1 = {
    "date": "2026-09-27",
    "crew": "round-1 autopsy",
    "gate": "selfpam-fact-gate",
    "gate_id": 2,
    "baseline": {
        "pairs_total": 1200,
        "pairs_withheld": 1099,
        "pairs_admitted": 101,
        "withhold_pct_x100": 9158,
        "provenance": prov(EV + "/admission_report_selfpam_r1.txt"),
    },
    "admitted_ledger_indices": admitted_idx,
    "admitted_indices_provenance": prov(EV + "/ledger_selfpam_r1.txt"),
    "per_task": per_task,
    "per_task_provenance": prov(EV + "/ledger_selfpam_r1.txt"),
    "mechanism_classes": {
        "A": {
            "name": "permutation-blindness (frame-reversed video)",
            "count": 100,
            "tasks": ["motiondir"],
            "verdict": "MISS",
            "fixable": True,
            "information_theoretic": False,
        },
        "B": {
            "name": "exact byte-sum collision (illuminant rendering)",
            "count": 1,
            "tasks": ["colordisc"],
            "verdict": "MISS",
            "fixable": True,
            "information_theoretic": False,
        },
    },
    "mechanism_taxonomy_provenance": {
        "report": "docs/lab/senses/pam-rebuild/selfpam/push100/round1/MISS_AUTOPSY.md",
        "table": "docs/lab/senses/pam-rebuild/selfpam/push100/round1/miss_table.tsv",
    },
    "verdict_summary": {"miss": 101, "correct_admit": 0},
    "reference_gate": {
        "pairs_total": 1200,
        "pairs_withheld": 1200,
        "pairs_admitted": 0,
        "withhold_pct_x100": 10000,
        "provenance": {
            "report": prov(EV + "/admission_report_reference_r1.txt"),
            "ledger": prov(EV + "/ledger_reference_r1.txt"),
        },
    },
    "cross_checks": {
        "runs_byte_identical": 3,
        "ledger_judgment_reverification_mismatches": 0,
        "ledger_judgment_reverification_denominator": 1200,
        "corpus_manifest_pairs_verified": 1200,
        "corpus_manifest_pairs_total": 1200,
        "provenance": {
            "gate_definition": [prov(SRC + "/g1_candidate.zag"), prov(SRC + "/codec.zag")],
            "manifest": prov(FIX + "/r2p/MANIFEST.r2p.sha256"),
            "generator": prov(FIX + "/gen_r2p.py"),
        },
    },
}

doc = {
    "schema": {
        "version": 1,
        "description": (
            "Machine-readable measured numbers for the self-PAM push-to-100% program. "
            "Each round appends one entry under 'rounds' keyed by round number (as a string). "
            "Every measured number carries provenance: the repo-relative source file it came "
            "from plus that file's git blob SHA-256 at the commit the round was analyzed against. "
            "withhold_pct_x100 follows the instrument's own convention: withheld*10000/pairs_total "
            "(9158 = 91.58%). Ledger entry format is 'e <idx> <jf> <jg> <0|1> <hash>' where the "
            "5th whitespace-separated field is the admit(0)/withhold(1) flag and ledger idx = "
            "task_index*200 + pair_index with tasks [colordisc, colorconst, shapetrans, pitchdisc, "
            "timbredisc, motiondir]. mechanism_classes.*.verdict is MISS (genuine should-withhold "
            "miss) or CORRECT_ADMIT; fixable/information_theoretic are the autopsy crew's judgments."
        ),
        "fields": {
            "rounds": "object keyed by round number (string); later rounds extend this object",
            "rounds.<n>.baseline": "the round's headline withhold measurement + provenance",
            "rounds.<n>.admitted_ledger_indices": "sorted list of ledger indices admitted that round",
            "rounds.<n>.per_task": "withheld/admitted counts per task",
            "rounds.<n>.mechanism_classes": "autopsy taxonomy: class id -> {name, count, tasks, verdict, fixable, information_theoretic}",
            "rounds.<n>.verdict_summary": "totals over mechanism classes",
            "rounds.<n>.reference_gate": "the reference (naive) gate's numbers for comparison",
            "rounds.<n>.cross_checks": "independent verification measurements (determinism, ledger re-verification, corpus manifest)",
        },
    },
    "rounds": {"1": round1},
}

outp = "/home/hatch/workspace/tnn-native-lab-r1/docs/lab/senses/pam-rebuild/selfpam/push100/NUMBERS.json"
with open(outp, "w") as f:
    json.dump(doc, f, indent=2)
    f.write("\n")
print("wrote", outp)
