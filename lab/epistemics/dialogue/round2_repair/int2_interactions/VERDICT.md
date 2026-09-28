# VERDICT — INT2 Interaction Repair (round-2 integration)

## Summary

**PASS.** All 7 round-1 regressions fixed by two general mechanism
changes. Round-1 battery is 370/370 with full-program stdout
byte-identical to the canonical baseline run. Round-2 is 18/18 exact.
All 36 family held-out probes pass (byte-identical outputs to the
certified integration logs), plus 8/8 new interaction held-out probes.
Every battery ran twice, all pairs `cmp` clean. Zero RNG. No held-out
probe literal in the source. Canonical tree untouched.

## Per-bar results

1. **7/7 items fixed** — every target turn now emits the exact
   canonical-baseline output (before/after table below).
2. **Round-1 370/370, byte-identical to canonical** — sections
   45/45, 45/45, 60/60, 30/30, 30/30, 60/60, 72/72, 28/28;
   `round1_run1.log` `cmp`-clean against `round1_canonical_baseline.log`
   (full stdout of the frozen canonical binary on the same battery),
   DIGEST `35aaae8ac1bbf764d1f710403a9302ad1f4f9b5327c9b13793cd90299834474b`
   in both. Run pair `cmp` clean.
3. **Round-2 18/18 exact** — all 18 A-lines match the frozen expected
   transcript in `integrated/PREREG_INT.md` character-for-character
   (verified by direct comparison, not just the section tally); run pair
   `cmp` clean; T/D/A/X lines byte-identical to the integration's
   committed `round2_run1.log`.
4. **Held-outs: 36/36 family + 8/8 new** — outputs on all five families'
   frozen sets are byte-identical to the integration's certified logs
   (which its VERDICT records as 36/36 per each family's pass criteria,
   including the F1 H6t2 manual A-line check and the F4/F5 sentinel
   criteria). New `heldout_int2.txt`: 20/20 turns, pair `cmp` clean.
   Discrimination check: the same 8 probes score 17/20 on the *unfixed*
   integrated binary (`heldout_int2_unfixed.log`: IN-B1 t3, IN-C1 t2,
   IN-E1 t4 FAIL) — the set genuinely exercises the two repaired
   mechanisms.
5. **Determinism** — round-1, round-2, all five family held-outs, and the
   new interaction set each ran twice; all 8 pairs `cmp` clean. Zero RNG:
   the only `rand|rng|random` grep hit is the header comment "zero RNG"
   (inherited verbatim from the integrated source).
6. **No gaming** — no literal from any of the five families' frozen probe
   files appears in `dialogue.zag`; after the deviation noted below, no
   literal from `heldout_int2.txt` appears either (the single inherited
   F4 design comment mentioning "What about Big Ben?" no longer collides
   with any probe). No code was tuned against the new probes: the fixes
   are the two preregistered mechanism rules.
7. **Cleanroom** — canonical `dialogue/` hashes verified unchanged at end:
   `dialogue.zag acda81ac…8231f`, `kb.txt 3ef27296…ec6889`,
   `gaz.txt b75fd113…e5c852`, `R33_NATIVE_IO_V1.zag e6379ddb…61d8`,
   `R33_NATIVE_SHA256_V2.zag 9824f6db…b7ea` (all match the
   `integrated/PREREG_INT.md` recorded prefixes). Only
   `dialogue/round2_repair/int2_interactions/` changed.

## Before/after: the 7 items

| # | item | before (integrated) | after (int2) = canonical |
|---|------|---------------------|--------------------------|
| 1 | FU-08 t3 `What about the Amazon River?` | `I don't know.` | `The Amazon River is 6400 kilometers long.` |
| 2 | RE-01 t3 `What about the Louvre?` | `I don't know.` | `The Louvre is in Paris.` |
| 3 | RE-06 t3 `What about the Louvre?` | `I don't know.` | `The Louvre is in Paris.` |
| 4 | RE-11 t3 `What about the Louvre?` | `I don't know.` | `The Louvre is in Paris.` |
| 5 | TO-02 t2 `What about Pride and Prejudice?` | `Jane Austen wrote the novel Pride and Prejudice.` | `Pride and Prejudice was published in 1813.` |
| 6 | TO-07 t2 `What about Pride and Prejudice?` | `Jane Austen wrote the novel Pride and Prejudice.` | `Pride and Prejudice was published in 1813.` |
| 7 | TO-12 t2 `What about Pride and Prejudice?` | `Jane Austen wrote the novel Pride and Prejudice.` | `Pride and Prejudice was published in 1813.` |

## Mechanism changed (general, not per-probe)

The source diff vs the integrated fork is 3 small edits implementing the
2 preregistered rules:

**P-INT2-1 — restored F4's ellipsis gate verbatim (fixes items 5–7).**
Root cause was a *merge bug*, not a design flaw, exactly as the task
hypothesized. F4's passing fork gates the step-5 ellipsis on the
previous turn having bound a pronoun:
`cc==0 && ne4>0 && pkind==0 && pv32>0`. `merge.py` edit 5g dropped the
`pv32>0` conjunct from the ellipsis activation and instead attached an
inverted form (`pv32<=0`) to the *salience-head* branch — the wrong
branch. Because F4 also stopped "about", `cc==0` holds for every
"What about X?", so the un-gated ellipsis fired after complete questions
("Who wrote Moby Dick?"), substituting the new entity into the old
question's shape ("who wrote pride and prejudice?"). Fix: the activation
is now F4's exact condition, and the salience-head branch is back to
F4's exact `use_ellip==0 && ne4==0 && bn==0`. General rule: the ellipsis
continues an anaphoric chain; after a complete question, "What about X?"
is a topic shift answered by direct retrieval.

**P-INT2-2 — the withhold gate judges the current turn's demand (fixes
items 1–4).** When the ellipsis fires *by design* (previous turn bound
"it"), the rewritten query ("how tall is amazon river?") retrieves a
true KB fact about the named entity — exactly what F4's fork and
canonical emit. F2's G2 then declined it because the *inherited* word
"tall" was absent from the fact's keys. Per PREREG_F2 §2, G2's contract
is "the fact cannot satisfy the question's demand" — the demand must be
the current turn's question's, and "What about X?" demands no relation.
`withhold_check` takes a new trailing `ellip` parameter (single call site
passes `use_ellip`); G2 is skipped when `ellip==1`. G1/G3/G4/G5 are
untouched, and direct questions always have `ellip==0` (a genuine
relation word keeps `cc>0`, blocking the ellipsis), so every F2-designed
decline — round-2 turns 8/9/13/17, all F2 held-outs — behaves exactly as
before (verified byte-identical).

## Prereg deviation (1, documented)

`heldout_int2.txt` IN-A1 t3 and IN-E1 t3 were reworded before the final
verification runs: the original wording (`What about Big Ben?`) appears
verbatim in an *inherited* F4 design comment in `dialogue.zag`
(documenting F4's own dev-battery case for stopping "about"). To keep
kill bar 6 letter-clean ("no held-out probe literal in the source") the
probes were reworded to `What about the Statue of Liberty?` (IN-A1,
E `The Statue of Liberty is 93 meters tall.`) and `What about the
Eiffel Tower?` (IN-E1, E `The Eiffel Tower is 330 meters tall.`). Both
E-lines are first-principles derivations (unique max-Jaccard facts:
3/5 vs ≤2/6, lower-fid tie-break not needed). No source change
accompanied this; the mechanism was already frozen and built. The
committed `heldout_int2.txt` is the final wording actually run.

## What the parent should know (F2-gate × F4-ellipsis interactions)

1. **The integration crew's "pe3/eout state" diagnosis was a red
   herring.** The real defect was simpler: `merge.py` put F4's gate on
   the wrong branch and inverted it. Lesson for future merges: when a
   family repair has a *condition* on shared logic, the merge must carry
   the condition onto the same branch it guarded in the fork — diffing
   each family's fork against the merged output branch-by-branch would
   have caught this mechanically.
2. **Gates that judge retrieved facts must know which turn's question
   they are judging.** The F2/F4 interaction is the general pattern:
   any rewrite step (ellipsis, anaphora resolution, topic resume) can
   smuggle a *previous* turn's demands into the current turn's gate
   evaluation. The durable fix is the one applied here — thread a
   provenance flag (`ellip`) into the gate — not relaxing the gate.
3. **F4's `prevbn` (pv32) is the load-bearing discourse signal.** Both
   fixes pivot on it: it licenses the ellipsis (P-INT2-1) and, via
   `use_ellip`, tells the gate the demand is inherited (P-INT2-2). Any
   future pipeline path that answers without going through step 5 must
   keep pv32 semantics ("bound-pronoun count of the previous turn's
   resolved query") or these interactions regress. Note the F2 decline
   path does not write pv32 (inherited from the merge); it is stale
   after a decline, but the `ppe<0` check and the frozen batteries make
   this currently harmless — flagged, not changed, per minimal
   intervention.
4. **F4's battery was the oracle that made this repair safe.** Its
   E-lines on the exact failing shapes confirmed the designed behavior
   before any code was touched, and the canonical binary served as the
   oracle for direct-retrieval E-lines in the new held-outs.

## Build / evidence

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned). Clean build, 6 analyzer warnings (all inherited).
- Binary built in /tmp (never committed); cleanroom dir holds source +
  logs only.
- Logs in this dir: `round1_run1/2.log` (+ `round1_canonical_baseline.log`,
  the frozen canonical binary's full stdout, `cmp`-clean vs run1),
  `round2_run1/2.log`, `heldout_f1..f5_run1/2.log`,
  `heldout_int2_run1/2.log`, `heldout_int2_unfixed.log` (17/20 on the
  unfixed integrated binary — discrimination evidence).

## Verdict

**PASS** — all 7 kill bars hold. The integration's round-1 regressions
are repaired with no per-case hacks; the full battery is byte-identical
to the canonical baseline.
