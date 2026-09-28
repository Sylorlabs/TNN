# PREREG_INT2 — interaction repair, round-2 integration (frozen 2026-09-23)

Interaction-repair crew preregistration. Frozen BEFORE any repair code is
written. This file is frozen: deviations are recorded in VERDICT.md, never
edited here.

## Objective

Fix the 7 round-1 regressions of the integrated round-2 repair
(`dialogue/round2_repair/integrated/`, commit
`1cc0913c98e7dbdf48fbf19b1dacc4844b6df187`) with general mechanism
changes only — no per-probe branches — restoring the round-1 battery to
370/370 byte-identical with the canonical baseline while keeping round-2
18/18 and all 36 family held-outs passing.

Work area: `dialogue/round2_repair/int2_interactions/` (cleanroom).
Starting source is a pristine copy of the integrated `dialogue.zag`
(sha256 `ef647ea70e93479dfb992a20f2a9e05597f139c7b212d2c0f34c8edea461862c`).
The canonical `dialogue/` tree is FROZEN and is never touched.

## The 7 target items (exact inputs + canonical-baseline expected outputs)

### Family A — F2 withhold over-fires on "What about X?" follow-ups (4)

A1. FU-08 (FOLLOWUP), turn 3
- t1 `How tall is Mount Everest?` → `Mount Everest is 8849 meters tall.`
- t2 `How tall is it?` → `Mount Everest is 8849 meters tall.`
- t3 `What about the Amazon River?` → `The Amazon River is 6400 kilometers long.`
  (merged: `I don't know.`)

A2/A3/A4. RE-01 / RE-06 / RE-11 (REFERENT), turn 3 (identical shapes)
- t1 `Tell me about the Eiffel Tower.` → `The Eiffel Tower is in Paris.`
- t2 `How tall is it?` → `The Eiffel Tower is 330 meters tall.`
- t3 `What about the Louvre?` → `The Louvre is in Paris.`
  (merged: `I don't know.`)
- t4 `When did it open?` → `The Louvre opened as a museum in 1793.`

### Family B — F4 ellipsis over-fires on "What about X?" topic shifts (3)

B1/B2/B3. TO-02 / TO-07 / TO-12 (TOPIC), turn 2 (identical shapes)
- t1 `Who wrote Moby Dick?` → `Herman Melville wrote the novel Moby Dick.`
- t2 `What about Pride and Prejudice?` → `Pride and Prejudice was published in 1813.`
  (merged: `Jane Austen wrote the novel Pride and Prejudice.`)
- t3 `Back to Moby Dick.` → `Herman Melville wrote the novel Moby Dick.`
- t4 `When was he born?` → `Herman Melville was born in 1819.`

## Root-cause analysis (mechanism level, verified by code inspection)

### R1 — the merge dropped F4's ellipsis gate (causes family B)

F4's passing fork gates the step-5 ellipsis (carry the previous question's
shape with the new entity swapped in) on the previous turn having bound a
pronoun:

`if(cc==0 && ne4>0 && pkind==0 && (g32(pv,32) as i32)>0){ use_ellip=1; }`

Rationale in F4's fork: the ellipsis continues an anaphoric chain; after a
complete question it is a topic shift answered by direct retrieval. F4's
fork also stopped "about", which makes `cc==0` for every "What about X?".

The merge (`merge.py` edit 5g) did NOT carry this conjunct onto the
ellipsis activation. Instead it attached an inverted form (`pv32<=0`) to
the *salience-head* branch — the wrong branch. Result: in the merged
build, "What about Pride and Prejudice?" after "Who wrote Moby Dick?"
(prevbn=0) fires the ellipsis, substitutes into "who wrote moby dick?",
and retrieves the wrote-fact instead of the published-fact. F4's fork
(and canonical) answer these turns by direct retrieval.

F4's battery confirms the designed behavior on exactly these shapes:
"What about the Amazon River?" after "How tall is it?" → the river-length
fact (ellipsis fires, prevbn>0); "What about Pride and Prejudice?" after
"Who wrote Moby Dick?" → `Pride and Prejudice was published in 1813.`
(no ellipsis, prevbn=0).

### R2 — F2's gate judges the previous turn's inherited demand (causes family A)

In family A the ellipsis fires *by design* (t2 bound "it", prevbn>0):
"What about the Amazon River?" → rewritten to "how tall is amazon river?"
→ `retrieve` returns the true KB fact `The Amazon River is 6400 kilometers
long.` F4's fork emits it (correct, canonical-identical). In the merged
build, F2's G2 relation-demand check sees the inherited word "tall",
finds it absent from the fact's keys, and declines with "I don't know.".

Per PREREG_F2 §2, G2's contract is "the fact cannot satisfy the question's
demand" — the demand must be the *current* turn's question's. Under an
ellipsis rewrite the relation words are inherited from the previous turn's
shape (a retrieval heuristic); the current turn ("What about X?") demands
no relation. F2's direct-question declines are unaffected: there the
ellipsis never fires (a genuine relation word such as "built" keeps
`cc>0`), so the gate sees `ellip==0` and G2 applies exactly as before.

## Planned mechanism changes (general rules only — no per-probe branches)

### P-INT2-1 — restore F4's ellipsis gate verbatim (fixes family B)

In `do_turn` step 5:
1. Ellipsis activation becomes F4's exact condition:
   `if(cc==0 && ne4>0 && pkind==0 && (g32(pv,32) as i32)>0){ use_ellip=1; }`
2. The salience-head branch returns to F4's exact form:
   `if(use_ellip==0 && ne4==0 && bn==0){`
   (removing the merge's misapplied, inverted `&& pv32<=0`).

This is a restoration of a passing family's specified mechanism, not a
new rule and not probe-specific: the ellipsis is licensed only when the
previous turn established an anaphoric chain (bound a pronoun).

### P-INT2-2 — withhold gate judges the current turn's demand (fixes family A)

`withhold_check` gains a trailing `ellip:i32` parameter (single call
site passes `use_ellip`). The G2 relation-demand block is skipped when
`ellip==1`; G1, G3, G4, G5 are unchanged.

General rule: a relation demand that the current turn's question did not
make (inherited via ellipsis rewrite from the previous turn's shape)
cannot be grounds for declining a fact that is about the current turn's
named entity. The gate still declines whenever the *current* question's
own demand is unsatisfied, whenever the fact is not about a named entity
(G1), and on all orphan/score conditions (G4/G5).

No other code changes are planned. In particular: no new stopwords, no
pv-slot changes, no pipeline reorder, no literal matching on any probe
text.

## Frozen interaction held-out set (`heldout_int2.txt`, frozen with this prereg)

8 new "What about X?"-style probes with X entities disjoint from the 7
failing items' X entities (amazon river, louvre, pride and prejudice).
E-lines are derived BEFORE implementation from (i) the canonical frozen
binary as oracle for direct-retrieval turns, and (ii) kb.txt fact text for
single-best-fact ellipsis turns (retrieve's tie-break is lower-fid-wins;
each E fact is the unique max-Jaccard match). The file is committed with
this prereg and treated as opaque during development: no probe literal
may appear in the source, and no code is tuned against these probes.

- IN-A1: ellipsis, carried relation present in KB (regression guard for
  the designed Big Ben case).
- IN-A2: ellipsis, carried relation present; the correct fact wins
  outright on Jaccard (no tie).
- IN-A3: ellipsis over a born-shape; carried relation present.
- IN-B1: ellipsis, carried relation ABSENT from KB → the entity's best
  fact is emitted, not declined (discriminator for P-INT2-2).
- IN-C1/C2: no ellipsis (previous turn bound no pronoun) → direct
  retrieval, canonical-oracle E (discriminators for P-INT2-1).
- IN-E1: ellipsis turn followed by another "What about Y?" — the second
  one must NOT chain the ellipsis (prevbn==0 after an ellipsis turn) →
  direct retrieval, canonical-oracle E (discriminator for P-INT2-1
  non-chaining).

## Kill bars (all must hold)

1. The 7 round-1 items produce exactly the canonical-baseline outputs above.
2. Round-1 battery 370/370, full-program stdout byte-identical to the
   canonical baseline run (all 8 sections + DIGEST).
3. Round-2 conversation 18/18 exact vs the frozen expected transcript in
   `integrated/PREREG_INT.md`.
4. All 36 family held-out probes pass, plus all 8 new interaction
   held-out probes pass.
5. Determinism: every battery run twice, `cmp` clean; zero RNG in source
   (grep for `rand|rng|random`).
6. No gaming: no held-out probe literal in `dialogue.zag`
   (grep over the five families' frozen probe files plus
   `heldout_int2.txt`).
7. Cleanroom: canonical `dialogue/` sha256 hashes unchanged at the end;
   only `dialogue/round2_repair/int2_interactions/` changed.

## Method

1. Freeze this prereg + `heldout_int2.txt`; commit before any repair code.
2. Apply P-INT2-1 and P-INT2-2 to the cleanroom `dialogue.zag`.
3. Build with the pinned toolchain
   `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
4. Run: the 7 target items; round-2 ×2; all five families' frozen
   held-out sets ×2 (opaque inputs, paths in `integrated/PREREG_INT.md`);
   `heldout_int2.txt` ×2; the full canonical round-1 `battery.txt` ×2,
   diffing full stdout against the canonical baseline run.
5. Grep checks: RNG, probe literals, canonical-tree hashes.
6. Write VERDICT.md; commit everything (no binaries, no .zagd caches).

If any bar fails after principled attempts, VERDICT.md documents exactly
what failed and the repair is reported as failed. No bar is weakened to
pass it.
