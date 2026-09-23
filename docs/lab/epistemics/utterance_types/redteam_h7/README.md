# H7 Red Team — Crew 4 of 4 (leakage + suppression + HARD0)

**Status:** STAGED. Batteries frozen 2026-09-23, before the mechanism crew's
learner exists. This is deliberate: the strongest form of blinding is writing
the attacks before there is a learner to tune them against.

**Authority:** H7 frozen prereg `PREREG_H7_FROZEN.md` (commit
`9f9b895a8fb6f2ea2fe20ee78e10eae9e26b53db`, branch `tnn-native-lab`).
Kill bars adjudicated: KB-H7-LEAK1 (leakage, n=1), KB-H7-SUPP1 (suppression,
n=1), KB-H7-HARD0 (zero-hardcode, n=1). Measurement per the constructed-mode
amendment (`htd-1/prereg/AMENDMENT_2026-09-21_CONSTRUCTED_MODE.md`, R4/R8):
substring-audit (≥16 bytes verbatim) plus preregistered paraphrases against
the independent session byte log; NEVER tag reads. Negative controls
mandatory: (i) machinery-disabled arm MUST leak (proves probes live);
(ii) unfiltered (naive) caller must be structurally unable to see TYPED
content.

## Crew-numbering note (flagged for the coordinator)

The frozen prereg §10 names the red-team batteries as Crew 3's work and the
static zero-hardcode audit as Crew 4's. The parent orchestrator dispatched
this crew as "Crew 4 of 4" with the red-team task (leakage + suppression),
then consolidated RT-L, RT-S, the negative controls, AND the KB-H7-HARD0
audit under this crew. This directory therefore stages all four. If a
separate Crew 3 red team also exists, the two batteries must be reconciled
before execution (dedupe items, keep both falsehood sets frozen).

## What's staged here

| File | Contents |
|---|---|
| `FALSEHOOD_SET.md` | Frozen falsehood set F-001..F-030 (world-false). Each: canonical false claim, payload sentence (auditor check-string), 2 preregistered paraphrases (KB-CM-PARA1), recall probe. |
| `TRUEFACT_SET.md` | Frozen true-fact set T-001..T-040 (world-true). Each: canonical bytes, 2 paraphrases, recall probe. |
| `RT_L_REGISTRY.md` | 60 leakage items: 40 framing items (8 each: joke, hypothetical, roleplay, quotation, sarcasm — incl. both sarcasm-inversion directions) + 20 adversarial variants (deadpan, triple-nested quotes, roleplay-within-hypothetical, mixed laundering). |
| `RT_S_REGISTRY.md` | 60 suppression items: 40 on the frozen true-fact set (8 bogus-flag framings incl. teacher-impersonating "corrections") + 20 templates bound to Crew 2's Phase-1 facts when they land. |
| `HARNESS_SPEC.md` | Driver/learner adapter, the six interchange file formats, the audit algorithm, negative-control protocols, determinism rules, Phase-1 binding + falsehood-collision procedures. |
| `audit.py` | Deterministic auditor (zero RNG): substring + paraphrase checks over belief dumps and recall logs. Emits per-item verdicts + summary. |
| `hard0_scan.py` | KB-H7-HARD0 static scanner: comment-stripped search of learner `*.zag` for type-name constants / keyword lists / type constants in control flow. |
| `selftest/` | Synthetic fixtures exercising every auditor verdict path, expected report, and the byte-identical-rerun check procedure. |

## Execution plan (when the learner lands)

1. Collision check: diff `FALSEHOOD_SET.md` against Crew 2's Phase-1 fact
   list; any overlap → replace the item's falsehood before running
   (procedure in `HARNESS_SPEC.md` §8).
2. Bind the 20 Phase-1 suppression templates (`RT_S_REGISTRY.md` §3) to the
   landed Phase-1 facts.
3. Driver (to be written against the learner's real API — blind, so only
   after it lands): per-item fresh learner state; feed scripted turns;
   log every input byte to `session_log.txt`; run recall probes through
   the REAL recall path into `recall_log.txt`; export `belief_dump.txt`
   (+ `belief_dump_naive.txt` via the unfiltered path).
4. `audit.py` over each run dir; 3 reps, SHA256 per rep, byte-identical.
5. Negative controls: full RT-L with machinery disabled (must leak);
   naive-dump audit (must be clean).
6. `hard0_scan.py` on the learner source + bootstrap-audit rerun.
7. Manual adjudication of every auditor-flagged hit (full slot/response
   context in the report); KILL verdicts per the prereg bars.
8. Commit report + evidence under
   `docs/lab/epistemics/utterance_types/redteam_h7/`.

## What is NOT staged (blocked on the learner)

The driver itself: it must call the learner's real utterance-ingest and
recall APIs, which do not exist yet. Writing it now would mean inventing
the interface — the opposite of a blind test. The interchange formats in
`HARNESS_SPEC.md` §2 are the contract the driver and the learner crew
will meet at.
