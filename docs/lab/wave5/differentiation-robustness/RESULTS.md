# RESULTS — differentiation-robustness (Wave-5, investigation 10)

Date: 2026-09-19. Runner: `run_graded.sh`. Sources: `gdiff.zag`
(graded mechanism), `gdiff_trial.zag` (graded episodes), `extract.zag`
(extractor), `pipe_trial.zag` (dialogue pipeline), `w4baseline.zag`
(wave-4 comparative baseline).

## Runner verdict

**ALL RUNNER CHECKS PASS.**
- gdiff: 135/135 GDIFF_CHECK lines match; GDIFF_FAILURES=0.
- pipe: 79/79 PIPE_CHECK lines match; PIPE_FAILURES=0.
- Determinism: two runs byte-identical for all three binaries
  (gdiff `a1e7df10e8eb5d24e82480ea8493aa50e120f3ba7197c219ac7ba569766cf43e`,
  pipe `67c218b62d1eb85de075119b916f22c2384b6c795f03bb8575f19eb5f614aebf`,
  w4baseline `501e8e5da2ba1b5930af0a5dd95800ac974528a61440e9e4db78e460a9b037d7`).
- Static: no-RNG grep clean over all five sources; GCOMMIT region
  references no evidence masks (doubt visible by design).
- Judgment shapes: gdiff 2 judgments / 9 doubt citations / 4 refuted
  citations / 10 UNKNOWNs; pipe 1 judgment / 5 UNKNOWNs — all as
  preregistered.

## Prereg criterion disposition (PREREG.md, incl. the 2026-09-19 correction)

| Criterion | Result | Key evidence |
|---|---|---|
| G1 corroborated identification | PASS | e1: 0 refuted, 3 survivors (single event never refutes); e2: BOB+CAROL refuted (doubt 5, kinds {0,1}); commit ALICE, doubt 0; judgment cites 4 DOUBT + 2 REFUTE records; slot owner=ALICE, partition reads correct |
| G2 impostor trap (HARD CONSTRAINT) | PASS | (0,1)+(4,1): CAROL refuted; ALICE doubt 3, BOB doubt 2; 2 survivors → HOLD → UNKNOWN; MEM_ADD → REFUSED_UNKNOWN; live slots unchanged (zero created) |
| G3 single-event poison | PASS | (1,0)+(5,0): BOB doubt 3, ALICE doubt 1, CAROL doubt 0; nobody refuted; 3 survivors → HOLD → UNKNOWN; baseline `w4baseline` on (1,0),(5,0): refuted 1,1 → 1 survivor → COMMIT CAROL(3) |
| G4 ambiguity abstain | PASS | (5,1): CAROL doubt 1 → 3 survivors → HOLD |
| G5 confusion resolved | PASS | commit ALICE; CAROL doubt records on bits {5,6,3}, BOB on {6,3}, bit-5 never touched BOB (honest attribution) |
| G6 claimant refuted, dirty survivor blocks | PASS | ALICE refuted (doubt 5, kinds {1,2}); BOB survives doubt 2 → sticky HOLD → UNKNOWN |
| G7 kind-diversity | PASS | same name claim twice: doubt 4 each, NEITHER refuted (one kind) → HOLD |
| G8 single-event sweep (4 kinds) | PASS | doubts 2,3,2,1; zero refutations; all HOLD |
| G9 scale (8 persons) | PASS | two-kind corroboration refutes all 7 rivals; commit == 5; entries ≤ 64; replay exact |
| G10 hard poison (rel 3) | PASS | ALICE doubt 3, not refuted by the single event → sticky HOLD → UNKNOWN |
| G11 replay | PASS | `gdiff_replay` exact over all main episodes |
| G12 zero-RNG + region exclusion | PASS | static checks clean |
| X1–X6 extraction units | PASS | case-insensitivity, hedge downgrades (3→2, 2→1), denial suppression, no-event turn, multi-pattern turn |
| D1 impostor dialogue | PASS | 2 events extracted from text → UNKNOWN, zero slots (trap end-to-end) |
| D2 confused/hedged | PASS | hedged rels (1,2) → doubts 3,3 → UNKNOWN |
| D3 evolving claims | PASS | ALICE doubt 2 → sticky HOLD → UNKNOWN |
| D4 clean Alice | PASS | 4 events extracted → COMMIT ALICE → slot owner=ALICE; knows(ALICE)=7, knows(BOB)=NOTFOUND |
| D5 poisoned clean | PASS | ALICE doubt 1 → UNKNOWN (downgraded, never misattributed) |
| D6 denial-poison | PASS | UNKNOWN under graded; extracted (1,0),(5,0) commits CAROL under wave-4 |
| P1 pipeline white box | PASS | ledger replay exact (p1a); full re-execution replay: byte-identical ledger + state (p1b) |

## The headline results

1. **The impostor trap still resolves to UNKNOWN under the graded
   scheme** — with zero slots created. Under graded it yields
   "ambiguous, everyone carries doubt" (ALICE 3, BOB 2, CAROL refuted)
   rather than wave-4's "everyone refuted", but both map to the same
   fail-safe: explicit UNKNOWN, `REFUSED_UNKNOWN` on write. Tolerance
   did not become gullibility.
2. **The poisoning comparison is real and runs natively.** Wave-4's
   mechanism on `(1,0),(5,0)` prints `W4BASELINE_COMMITTED,3` — one
   poisoned event flips the session into a CAROL attribution. The graded
   mechanism on the same bits abstains (doubts 1 and 3, nobody refuted).
   This is a new adversarial criterion, not a wave-4 prereg failure.
3. **The raw-conversation pipeline works end-to-end.** Dialogue text →
   extraction (with per-event reliability, hedge downgrades, denial
   handling) → graded judgment → partition formation, all native,
   deterministic, replay-exact. Extraction errors (hedges, poisons,
   self-contradictions) degrade into UNKNOWN, never into wrong-person
   attribution.

## Honest notes

- A prereg hand-computation error was caught by the first run (the
  original G3/D6/baseline sequence `(1,0),(0,1),(5,0)` yields
  HOLD/UNKNOWN under wave-4, not COMMIT CAROL, because `(0,1)` refutes
  CAROL). Corrected transparently in PREREG.md (dated correction
  section); the corrected sequence `(1,0),(5,0)` genuinely demonstrates
  the gullibility. The falsifier did its job.
- A replay bug was caught the same way: EXTRACT entries consume a clock
  tick, which the first replay implementation skipped. Fixed by
  reproducing EXTRACT entries verbatim in `gdiff_replay`.
- The graded scheme is strictly less decisive than wave-4: name-claim
  alone no longer identifies (G1 needs name + secret corroboration);
  any dirty survivor blocks commit. That is the stated price of
  robustness (DESIGN_GRADED.md §1, §5).
- DOUBT_LIMIT=4 and the kind-reliability map remain preregistered
  constants, not derived truths; kind-diversity (repetition ≠
  corroboration) is a design choice with G7 as its trial.
- The extractor is a fixed pattern table (DESIGN_EXTRACT.md §6):
  no retraction modeling (D3's doubt is the price), no paraphrase
  coverage, no prompt-injection resistance claimed. Its errors are
  absorbed by the graded layer — that absorption is what was trialed.

## Verdict: POSITIVE

All G, X, D, P criteria pass. Graded refutation removes the
single-event brittleness while the impostor trap still resolves to
UNKNOWN with zero slots created, and the raw-conversation pipeline runs
end-to-end with extraction errors degrading to abstention.
