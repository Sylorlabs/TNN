# PREREG_INT — round-2 guided-release INTEGRATION (frozen 2026-09-23)

Integration crew preregistration. Frozen BEFORE any merge code is written.
The prereg is frozen: deviations are recorded in VERDICT.md, never edited here.

## Objective

Merge the five PASSING round-2 repair families (F1-COMPARE, F2-WITHHOLD,
F3-ARITHMETIC, F4-DEFEND, F5-ROUTER) into ONE integrated cleanroom fork of
`dialogue.zag` under `dialogue/round2_repair/integrated/`, and verify the
merged system fixes all 13 round-2 failures with no regressions.

Canonical tree (`dialogue/dialogue.zag`, `kb.txt`, `gaz.txt`,
`R33_NATIVE_*.zag`) is FROZEN — never modified. Baseline verified
2026-09-23: rebuilding the current `dialogue.zag` with the pinned toolchain
reproduces the recorded canonical binary sha256
`912c809e0d8206f5ceb096d79a54e735337180f5dccc8bded6f1d25a7c023bd5`
byte-identically. All integration comparisons are against that source.

## Expected full 18-turn round-2 transcript (frozen)

Input turns are the 18 turns of
`dialogue/real_convo_2026-09-23/conv_battery.txt`. Expected A-lines:

| # | input | expected response | source |
|---|-------|-------------------|--------|
| 1 | who wrote the martian? | Andy Weir wrote The Martian. | canonical (good) |
| 2 | when was he born? | Andy Weir was born in 1972. | canonical (good) |
| 3 | was he born before the eiffel tower was built? | no. | F1 |
| 4 | who was born first, darwin or melville? | charles darwin was born first. | F1 |
| 5 | which is taller, the eiffel tower or the montparnasse tower? | the eiffel tower is taller. | canonical (good) |
| 6 | how much taller is it? | 120 | F3 |
| 7 | which of those two was built first? | the eiffel tower was built first. | F1 |
| 8 | what is the capital of italy? | I don't know. | F2 |
| 9 | who wrote hamlet? | I don't know. | F2 |
| 10 | was melville born in 1818? | Herman Melville was born in 1819. | canonical (good) |
| 11 | are you sure? i read 1818 in a biography. | Yes. Herman Melville was born in 1819, not 1818. I was taught that. | F4 |
| 12 | did jane austen write moby dick? | no. | canonical (good) |
| 13 | which author lived the longest? | I don't know. | F2 |
| 14 | tell me a joke about darwin. | I don't know any jokes. | F5 |
| 15 | do you remember the first thing i asked you? | You asked: who wrote the martian? | F5 |
| 16 | how do you know that andy weir wrote the martian? | I was taught that Andy Weir wrote The Martian. | F4 |
| 17 | who is the current president of the united states? | I don't know. | F2 |
| 18 | forget everything i just told you. | I can't forget. | F5 |

(5 good turns — 1, 2, 5, 10, 12 — byte-identical to the canonical
round-2 record; 13 repaired turns per the five families' VERDICT.md files.)

## Frozen held-out sets (re-collected, listed — never opened or modified)

Paths are lab-relative under `~/workspace/tnn-lab/dialogue/round2_repair/`.
sha16 = first 16 hex of sha256. Content was NOT read; files are opaque
inputs to the test harness only.

| family | path | sha16 | claim |
|--------|------|-------|-------|
| F1 | f1_compare/heldout_battery.txt | cbd3b96abeab6c37 | 7 probes |
| F2 | f2_withhold/heldout_probes.txt | 08637b3744a67df7 | 7 probes |
| F3 | f3_arithmetic/heldout/battery.txt | 8f75a936332aa8fb | 8 probes |
| F4 | f4_defend/heldout_battery.txt | cbd5842f24fcda7f | 7 probes |
| F5 | f5_router/probes/heldout_battery.txt | 7be88af502e26f64 | 7 probes |

Total: 36 probes. Pass criterion for each set: every T-line PASS when the
set is run through the merged binary (the batteries are self-checking;
each family's own E-lines are the oracle).

## pv-slot layout (final — resolves the known 32/36 collision)

Canonical slots 0/4/8/12/16/20/24/28 are untouched
(ans/eid/peid/qraw_off/qraw_len/q_off/q_len/kind).

| slot | owner | meaning |
|------|-------|---------|
| 32 | F4 | prevbn: bound-pronoun count of the previous turn's resolved query (gates the step-5 ellipsis). Keeps F4's original slot; F4 writes it in correction/resume/2b/2c/compose-result paths and at end of step 5. |
| 40 | F1 | last-compared pair, e1 (remapped from F1's 32) |
| 44 | F1 | last-compared pair, e2 (remapped from F1's 36) |
| 48 | F3 | carried difference pair, e1 (remapped from F3's 32) |
| 52 | F3 | carried difference pair, e2 (remapped from F3's 36) |
| 56 | F3 | carried dim, write-only (remapped from F3's 48; F3's fork wrote it but never read it — kept for state-shape fidelity, documented here) |
| 60 | F3 | carried turn_no (remapped from F3's 52) |

Main DIALOGUE-handler init becomes:
`p32(pv,0,-1); p32(pv,28,1); p32(pv,32,0);`
`p32(pv,40,-1); p32(pv,44,-1); p32(pv,48,-1); p32(pv,52,-1); p32(pv,56,0); p32(pv,60,-1);`

F1's do_compare reads/writes 40/44 for the "those two" pair. F3's
difference branch reads 48/52/60 (expiry: `cturn+1==turn_no`). The carry
write moves from F3's old taller-branch hook into `do_compose` right after
a successful `do_compare` (F1's engine replaces the branch the hook lived
in): copy the pair from 40/44 into 48/52, dim=1 into 56, `turn_no` into 60.

Semantics notes:
- F1's pair persists across unrelated turns (needed for turn 7 after turn 6);
  F3's carry expires after one turn (F3's design: a stale referent is worse
  than a miss). Separate slots preserve both.
- F4's ellipsis gate reads only slot 32; F1/F3 writes no longer touch it.
- F2's decline writes only slots 0/4/8/12/16/20/24/28; F5's dispatch writes
  0/4/8/28. No overlaps with 40–60.

## Pipeline order in merged do_turn (frozen)

0. F5 utterance-type dispatch (joke/memory/forget) → returns before anything else.
1. correction (canonical; + F4's pv32=0 write).
2. topic resume (canonical; + F4's pv32=0 write).
2b. F4 challenge dispatch (`is_challenge`, needs previous fact).
2c. F4 provenance dispatch (`prov_match`, "I was taught that …").
3. do_compose: F1 do_compare (remapped 40/44; carry copy to 48/52/56/60 on
   success) → F3 difference engine (remapped 48/52/60) → existing did-write
   branch → existing birth-year branch. F4's stale-fact guard
   (pv,0=-1, pv32=0) after a composed result.
4. assertion/contradiction (canonical, untouched).
5. default reference-resolution + retrieval, with F2's aboutness gate
   (G1–G5) between retrieve() and emit_fact(); decline → exactly
   `I don't know.` with fid=-1 state update. F4's ellipsis gate
   (`use_ellip` requires pv32>0) and end-of-turn `pv32=bn` write.

F1/F4/F5 branches all run BEFORE step 5, so their outputs take precedence
over F2's gate (turn 3 → comparison answer, turn 11 → defense,
turn 15 → history quote — never a decline).

## Kill bars (all must hold)

1. All 18 round-2 turns match the frozen expected transcript exactly.
2. All 36 held-out probes (5 families' frozen sets) pass.
3. No regressions: 5 good round-2 turns byte-identical to canonical;
   full round-1 `battery.txt` byte-identical to the canonical baseline run
   (all 8 sections + DIGEST).
4. Determinism: every battery run twice, `cmp` clean, zero RNG (grep-verify).
5. No gaming: no probe literal from any held-out set in the merged source
   (grep-verify). Note: the integrator never opened the probe files, so any
   match would be accidental — the check still runs.
6. Cleanroom: canonical `dialogue/` tree sha256 unchanged at the end
   (dialogue.zag acda81ac…8231f, kb.txt 3ef27296…ec6889, gaz.txt
   b75fd113…e5c852, R33 files e6379ddb…61d8 / 9824f6db…b7ea);
   only `dialogue/round2_repair/integrated/` touched.

## Method

1. Freeze this prereg; commit it before any merge code.
2. Verify each family fork independently: rebuild with the pinned toolchain
   `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, run the
   canonical round-2 conv battery, confirm the family's claimed target-turn
   outputs; run the family's own battery and confirm its recorded log
   reproduces.
3. Merge into `dialogue/round2_repair/integrated/` from canonical sources +
   the five repairs with the pv remap above.
4. Run: full 18-turn round-2 conv ×2 (vs frozen transcript), all 36
   held-out probes ×2, canonical round-1 battery ×2 — each pair `cmp` clean.
5. Write VERDICT.md. Commit everything (no binaries, no .zagd caches).
