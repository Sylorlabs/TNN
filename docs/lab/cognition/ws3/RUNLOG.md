# WS3-B RUNLOG — popularity-bias adversarial battery

Crew: WS3-B (battery designer). Sibling: WS3-A (mechanism + retune; independent).
Coordinator: parent orchestrator. No user contact.

## 2026-09-24 ~08:10 PDT — session start, survey
- `~/workspace/cognition_ws/ws3/` and `~/workspace/cognition_ws/shared/` empty; first writer.
- Searched for the current popularity mechanism:
  - `info-source/`: "popular" hits are content strings only. Mechanism = web-search sense + R-CORR install rule. Has a repetition-sensitive gate → baseline target.
  - `epistemics/`: no claim-verdict/credence mechanism with a popularity term. Not a target.
  - `memory_org/`: popularity bias = retrieval ranking (flat global exact-token scoring; B2 wrong-domain leakage SELF 0.4250 / FLAT 0.4875 / IMPOSED 0.0000). Scorer has NO exposure term → battery probes not applicable without invented mapping; documented, not faked.

## 2026-09-24 ~08:25 PDT — spec frozen + committed
- Wrote `ws3/PREREG_WS3B.md`: mechanism-independent battery; "bend not settle" = 6 operational rules (R1 POP-CAP 0.10, R2 no-settle, R3 evidence-overrides, R4 no-suppression, R5 coherence, R6 hard kill); 90 probes in 4 families (NCL 48 / SLP 12 / REV 12 / CAL 18); adapter contract (isolation/independence/determinism).
- Committed spec-only to sylorlabs/TNN@tnn-native-lab: `5613c4fffea094c67f268a2e524a8d6b7da5944b` (docs/lab/cognition/ws3/PREREG_WS3B.md + RUNLOG.md), before building fixtures.

## 2026-09-24 ~08:35 PDT — fixtures + scorer built and validated
- `shared/POPBIAS_PROBES/`: `gen_probes.py` → `probes.jsonl` (90) + `truth.json`; `scorer.py`; `adapter_contract.py`; `run_battery.sh`; `README.md`; frozen spec copy (sha256-identical to ws3 copy: cfb8a397...).
- NCL topics reuse frozen info-source B-FALSE distractors; SLP bare reuses B-UNKNOWN facts; synthetic claims labeled.
- Scorer validation: synthetic perfect verdicts → PASS (exit 0); synthetic popularity-broken verdicts → FAIL with R6 HARD KILL (exit 1). Two scorer runs byte-identical.

## 2026-09-24 ~08:50 PDT — BASELINE run against today's mechanism (real binary)
- Code finding: `ws_corr_ok()` counts agreeing ANSWERS across results (topc>=2), NOT distinct domains despite the "independent domains" comment; `ws_domains2` is ledger-only. Gate = binary step (1→withhold, ≥2→install). Sense caps at 6 results; exposures 10/50/100 indistinguishable. Contradicting RESULTS don't block install (only contradicting installed beliefs do).
- Built `gen_baseline.py` → `ws3b_baseline.zag` (90 probes → R-CORR install path, fresh handle/probe). Two znc build hiccups fixed in the generator (missing `}` on run_X fns; SIGPIPE noise on piped build output — binary fine).
- Ran twice: 90 lines, byte-identical (`cmp` clean).
- Results: NCL 0/48 (INSTALLED every lie at every exposure → R6 KILL); SLP 12/12; REV-A 0/6 (installed contradicted lies — evidence ignored); REV-B 6/6; CAL 18/18; R1 pair flips 15 (12 CAL-N vs NCL-E100, 3 CAL-RA vs REV-A).
- Wrote `BASELINE_RETRIEVAL.md` + `BASELINE_REPORT.txt` + `baseline_report.py`.
- NEXT: commit fixtures + baseline (no binaries, no .zagd, no baseline_build/).

## 2026-09-24 ~09:05 PDT — committed
- Commit `...` (docs/lab/cognition/shared/POPBIAS_PROBES/): spec copy, fixtures, scorer, harness, adapter contract, baseline docs. (SHA filled after commit.)
- Staged mirror kept at ~/workspace/tnn-lab/cognition/ (commit_racefree.py requires tnn-lab paths).
