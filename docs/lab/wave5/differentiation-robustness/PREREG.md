# PREREG — differentiation-robustness (Wave-5, investigation 10)

Investigator: Wave-5, slug `differentiation-robustness`. Date: 2026-09-19.
Branch: `tnn-native-lab`. All trials native on this VM (Zag, znc).
Nothing in this file is a result; everything below is a prediction made
BEFORE any wave-5 differentiation code was written, compiled, or run.

Designs: DESIGN_GRADED.md (part a), DESIGN_EXTRACT.md (part b).

## The claims under test

**Part (a) — graded refutation.** Replacing wave-4's all-or-nothing
refutation with ledgered doubt + corroborated contradiction
(refute iff doubt ≥ 4 AND ≥ 2 distinct evidence kinds; commit iff exactly
one survivor with doubt == 0):

1. A single evidence event (even max reliability 3) can never refute.
2. The impostor trap (Alice's name + Bob's secret) STILL resolves to
   UNKNOWN with zero slots created — tolerance does not become
   gullibility.
3. A single-event poisoning sequence that makes wave-4 commit the WRONG
   person is absorbed into UNKNOWN by the graded scheme.
4. Corroborated contradiction still refutes (the mechanism is not
   toothless); clean corroborated evidence still commits.

**Part (b) — raw-conversation pipeline.** The smallest native extractor
turning dialogue turns into `(bit, value, kind, rel)` evidence events,
wired dialogue → extraction → graded judgment → partition formation,
trialed on adversarial dialogues with predicted outcomes.

## Mechanism to be built (predicted before construction)

- `gdiff.zag`: person hypotheses `{id, must1, must0, active, refuted,
  doubt, doc, kmask}`; `gdiff_observe(bit,val,kind,rel)` appends DOUBT
  records and refutes only on corroborated contradiction; `gdiff_commit`
  commits iff exactly one non-refuted survivor with doubt == 0 else
  HOLD→UNKNOWN; partition memory ops gated on committed != UNKNOWN;
  `gdiff_replay` reconstructs exact state from the ledger (DOUBT/REFUTE
  re-derived, EXTRACT skipped at ledger level).
- `extract.zag`: case-insensitive substring pattern table (§2 of
  DESIGN_EXTRACT.md), hedge downgrade (−1, floor 1), emits
  `(bit,val,kind,rel)` per turn; no imports, no RNG.
- `gdiff_trial.zag`: graded episodes G1–G10 + scale G9.
- `pipe_trial.zag`: extraction units X1–X6, dialogues D1–D6, end-to-end
  replay.
- `w4baseline.zag`: wave-4 `diff.zag` driven with the G3/D6 bit sequence
  as a comparative baseline (NEW adversarial criterion; not a wave-4
  prereg failure).

Masks (bits 0..10): ALICE (361,1686), BOB (562,1485), CAROL (1156,891).
KIND_REL default: k0→2, k1→3, k2→2, k3→1. DOUBT_LIMIT=4.

## CORRECTION (2026-09-19, after the first trial run — before any
results were accepted)

The G3/D6/baseline sequence as first preregistered —
`(1,0),(0,1),(5,0)` — was based on a hand-computation error: under
wave-4's masks, `(0,1)` ("i am alice") refutes CAROL (bit 0 is must0 for
her), so the wave-4 baseline on that sequence yields HOLD/UNKNOWN (0
survivors), not COMMIT CAROL. The first run caught this: `w4baseline`
printed `W4BASELINE_COMMITTED,-1`, failing the preregistered baseline
falsifier exactly as a falsifier should.

The corrected adversarial sequence is `(1,0),(5,0)`: `(1,0)` "not bob"
refutes BOB (legitimate), and the single poisoned event `(5,0)` "fact K
denied" refutes ALICE (must1) while CAROL (must0) stays consistent —
leaving CAROL the sole survivor under wave-4's all-or-nothing rule.
Under the graded rule the same two events yield ALICE doubt 1 and BOB
doubt 3: nobody refuted, 3 survivors → HOLD → UNKNOWN.

What changed: G3's graded event list (`(1,0,k0,r2)`, `(5,0,k3,r1)`; the
"BOB doubt 4 on one kind" mid-step moves to G7, which already trials
kind-diversity), D6's dialogue (`"i am not bob"` / `"kestrel is not
true"`), and the `w4baseline.zag` bit sequence. The graded predictions
(UNKNOWN, no attribution, no slots) and the baseline prediction (wave-4
commits CAROL) are unchanged in substance; nothing about the mechanism
was altered to fit the data. All other criteria are untouched.

## Falsification criteria — graded (G) [G3 corrected as above]

- **G1 — corroborated identification commits.** `(0,1,k0,r2)` then
  `(3,1,k1,r3)`. REQUIRED: after event 1, zero refutations and 3
  survivors (single event never refutes); after event 2, BOB and CAROL
  refuted (doubt 5, kinds {0,1}); commit → ALICE; ALICE doubt == 0;
  judgment cites ≥2 DOUBT records per rival + both REFUTEs; subsequent
  MEM_ADD creates a slot with owner == ALICE and `knows` reads it back
  in ALICE's partition only. FAIL on any deviation.
- **G2 — impostor trap still UNKNOWN (HARD CONSTRAINT).**
  `(0,1,k0,r2)` then `(4,1,k1,r3)`. REQUIRED: CAROL refuted; ALICE doubt
  == 3 (kinds {1}); BOB doubt == 2 (kinds {0}); survivors == 2; commit →
  HOLD; committed == UNKNOWN; MEM_ADD → REFUSED_UNKNOWN; live-slot count
  unchanged (zero slots created). FAIL if: any attribution occurs, any
  slot is created, or the outcome is not explicit UNKNOWN.
- **G3 — single-event poison absorbed (wave-4 gullibility case).**
  [CORRECTED 2026-09-19; see CORRECTION above.]
  `(1,0,k0,r2)`, `(5,0,k3,r1)`. REQUIRED under graded: after event 1,
  BOB doubt == 2, nobody refuted; after the poison, ALICE doubt == 1,
  BOB doubt == 3, CAROL doubt == 0, nobody refuted; survivors == 3 →
  HOLD → UNKNOWN; no attribution; MEM_ADD refused. REQUIRED as
  baseline: `w4baseline.zag` driving wave-4's mechanism with bit sequence
  (1,0),(5,0) prints committed == CAROL(3) — demonstrating the
  all-or-nothing scheme misattributes on one poisoned event. FAIL if:
  graded attributes to anyone, or the wave-4 baseline does not commit
  CAROL (the comparison would be vacuous).
- **G4 — ambiguity abstains.** `(5,1,k3,r1)` only. REQUIRED: CAROL doubt
  == 1, 3 survivors → HOLD → UNKNOWN.
- **G5 — confusion resolved with honest attribution.**
  `(5,1,k3,r1)`, `(6,1,k2,r2)`, `(3,1,k1,r3)`. REQUIRED: commit ALICE
  with doubt 0; CAROL refuted with DOUBT records on bits {5,6,3}; BOB
  refuted with DOUBT records on bits {6,3}; the judgment shows the
  shared fact (bit 5) contributed only to CAROL's doubt, not BOB's.
- **G6 — corroborated refutation of the claimant.**
  `(0,1,k0,r2)`, `(4,1,k1,r3)`, `(6,0,k2,r2)`. REQUIRED: ALICE refuted
  (doubt 5, kinds {1,2}); survivors == 1 (BOB, doubt 2) → sticky doubt →
  HOLD → UNKNOWN. (Refutation works; dirty survivors still block commit.)
- **G7 — kind-diversity clause.** `(0,1,k0,r2)` twice. REQUIRED: BOB
  doubt == 4 and CAROL doubt == 4, but NEITHER refuted (one kind each);
  3 survivors → HOLD. (Repetition is not corroboration.)
- **G8 — single-event sweep.** Four fresh sessions, each one event
  `(3,0,kK,rRel)` for K=0..3. REQUIRED: in all four, ALICE not refuted,
  doubt == rel(K) (2,3,2,1), 3 survivors → HOLD.
- **G9 — scale.** 8 persons (ids 1..8, must1 = single bit, must0 =
  complement over bits 0..7); target 5; events `(4,1,k1,r3)` then
  `(4,1,k0,r2)`. REQUIRED: all 7 rivals refuted; commit == 5; audit
  entries ≤ 64; `gdiff_replay` exact.
- **G10 — hard poison absorbed.** `(0,1,k0,r2)`, `(3,1,k1,r3)` (ALICE
  clean, rivals refuted), then poison `(3,0,k1,r3)`. REQUIRED: ALICE not
  refuted (single event, even rel 3); ALICE doubt == 3; 1 survivor →
  sticky doubt → HOLD → UNKNOWN.
- **G11 — white box.** Two runs byte-identical (sha256); `gdiff_replay`
  over all main episodes reconstructs committed, clock, person fields
  (incl. doubt/doc/kmask/refuted), slot fields, entry count exactly.
- **G12 — zero RNG + commit-region exclusion.** Static grep clean over
  all five sources; the GCOMMIT region references no must1/must0/pm1/pm0
  tokens (doubt IS visible to commit — by design).

## Falsification criteria — extraction & pipeline (X / D / P)

- **X1** `"Hello, I AM ALICE"` → exactly 1 event: (0,1,k0,2).
  **X2** `"maybe the secret is quartz"` → (4,1,k1,2) (hedge 3→2).
  **X3** `"kestrel is not true"` → (5,0,k3,1) (denial, no positive).
  **X4** `"the weather is nice today"` → 0 events.
  **X5** `"i am alice and the secret is ember"` → 2 events
  (0,1,k0,2),(3,1,k1,3) in table order.
  **X6** `"i think the blue door was closed"` → (6,1,k2,1) (hedge 2→1).
- **D1** impostor dialogue → UNKNOWN, zero slots created.
- **D2** confused/hedged dialogue → UNKNOWN (no attribution).
- **D3** evolving claims → UNKNOWN (ALICE doubt == 2, sticky).
- **D4** clean Alice dialogue → COMMIT ALICE; MEM_ADD ok, owner ALICE;
  `knows(100,ALICE)` found, `knows(100,BOB)` NOTFOUND.
- **D5** poisoned clean dialogue → UNKNOWN (ALICE doubt == 1); the clean
  commit is downgraded, never misattributed.
- **D6** denial-poison dialogue. [CORRECTED 2026-09-19; see CORRECTION
  above.] `"i am not bob"` / `"kestrel is not true"` → UNKNOWN under
  graded (ALICE doubt 1, BOB doubt 3, CAROL doubt 0, 3 survivors); the
  extracted bit sequence (1,0),(5,0) under wave-4 commits CAROL (same
  comparison as G3, end-to-end from text).
- **P1 — pipeline white box.** Two runs byte-identical; end-to-end
  replay (re-extract + re-judge into a fresh state) reconstructs
  committed, clock, person fields, slot fields, entry count exactly.

## Predicted verdict logic (before running)

- All G, X, D, P criteria pass → POSITIVE: graded refutation removes the
  single-event brittleness while the impostor trap still resolves to
  UNKNOWN, and the raw-conversation pipeline runs end-to-end with
  extraction errors degrading to abstention.
- G2 fails (impostor attributed, or slots created) → NEGATIVE: tolerance
  became gullibility; the graded scheme must not proceed.
- G3 fails under graded (attributes to anyone under poison) →
  NEGATIVE: the robustness claim is false.
- G criteria pass but X/D/P fail → MIXED: graded judgment works on
  tagged events, but raw-conversation extraction is not yet viable.
- Any znc bug blocking native execution → BLOCKED (with minimal repro).

## Out of scope (stated before running)

Retraction modeling, anaphora/coreference, paraphrase beyond the table,
prompt-injection resistance of the extractor, person discovery,
multi-speaker sessions, and whether DOUBT_LIMIT=4 is the "right"
constant beyond its structural justification (smallest integer > max
single-event reliability).
