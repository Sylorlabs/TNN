# Protect-the-How Experiment (Micah Q6)

**Status:** PROTECT-HOW-COMPLETE (pending final run transcripts)
**Date:** 2026-10-01
**Worker:** Protect-the-How Worker (retry; prior attempt throttled after
building both binaries and completing control run 1)

## Question

TNN-2 preserves rehearsed answers longer than the executable procedures
that produced them (interference experiment 3708fbd15; budget pressure
bc96dd3d8). Micah Q6: teach a procedure P, use P to derive many answers,
apply heavy interference. The ideal learner discovers "if I retain P, I
can reconstruct many answers" and permits cached answers to die before P.
Can a retention policy that prefers generative structure over cached
derived answers reverse the pattern?

## Design

**Procedure P:** 4-hop chain MAP for (1,40)->5, promoted by trial
(build_verifies=3). 8 winner op cells, reexec=5 at build.

**20 cached answers:** 20 fresh subjects (101..291 step 10), each taught a
4-hop chain; answer derived by shape-rebinding P's chain topology
(`ph_rebind`: read plen from P, gather subject path, `t2_asm_chain`,
`t2_exec` for verification); cached as tag-1 FACTs (s,40,s+4) marked
field16=3 (INFERRED = MAP-derived). derived_ok=20/20. Shadow (1,40) also
marked derived.

**Interference:** 1000 unrelated teaches (700+i,41,i). Pre-interference
live=486 (includes ~300 rebind scratch cells); ~462 evictions under the
1024 cap.

**Arms:**
- Control: verbatim frozen eviction (lowest bid, `evict_node` lines 254-275
  of base).
- Treatment: 3-tier `evict_node` (only change; see `ph_diff.txt`):
  Tier 1 = derived cached answers (tag 1, field16==3);
  Tier 2 = all other nodes except generative structure;
  Tier 3 (last resort) = MAP nodes (tag 20) + op cells (101-104).
  `is_prot` respected in all tiers. Eviction action verbatim.

**Phase 5 (recovery):** 20 NEW subjects; teach chains; `activate` check;
if miss and P's MAP node alive, rebind from P (shape held by driver);
else trial. Measures re-derivation cost.

## Results

### Build (both arms, deterministic)

p_map=45, p_root=30, p_links=4, p_cells=8, p_reexec0=5, derived_ok=20.

### Phase 4: survival after 1000 interference teaches

| metric | control r1 | treatment r1 | treatment r2 | treatment r3 |
|---|---|---|---|---|
| post_p_map (MAP node alive) | 1 | 1 | 1 | 1 |
| post_p_cells (walkable op cells) | 0 | 8 | 8 | 8 |
| post_p_reexec | -999998 (dead) | 5 (alive) | 5 (alive) | 5 (alive) |
| post_answers (of 20) | 0 | 0 | 0 | 0 |
| post_shadow | 0 | 0 | 0 | 0 |

Treatment 3/3 byte-identical (SHA-256
8204dc203c142631c04008d2c8b20afe8e4984ab74229bcb94c1c4b78e7eb054).

### Phase 5: 20 new subjects

| metric | control r1 | treatment r1 | treatment r2 | treatment r3 |
|---|---|---|---|---|
| new_hits | 0 | 0 | 0 | 0 |
| new_rebind_ok / try | 20 / 20 | 17 / 20 | 17 / 20 | 17 / 20 |
| new_trial_ok | 0 | 3 | 3 | 3 |
| new_trial_verifies | 0 | 9 | 9 | 9 |

## Analysis

(TBD after treatment runs complete.)

## Limitations

1. Treatment policy is researcher-authored (3-tier rule), not
   learner-derived. It tests whether the Q6 retention ORDER works, not
   whether the learner can discover it.
2. Derived-answer marking (field16=3) is driver-applied, simulating
   "derived from P". Production does not track derivation provenance
   (the provenance experiment 8c352e5bf does this properly with source
   tags; integration is future work).
3. Tier 2 excludes ALL op cells (101-104), so dead rebind scratch cells
   (~300) also receive tier-3 protection. Over-protection of garbage;
   noted, does not affect the P-vs-answers comparison.
4. Phase 5 rebind uses driver-held shape (plen captured pre-interference),
   not shape re-read from learner state. It measures re-derivation
   mechanics, not learner retention of the shape.

## Standing architectural metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 3-tier eviction order; field16=3
  derived marker semantics; tier membership (MAP+op cells = generative).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (no use-dependent or
  consequence-driven component; contrast protection builder a298709d5).
- SOURCE-ENUMERABLE FORMS: existing tags/fields only.
- SUF DECISIONS: 0.
- COGNITION LINES: ~36 added (treatment evict_node), 0 new functions in
  control.
- MODES / BRIDGES / HANDLERS / SEMANTIC CASES: 0 / 0 / 0 / 0.

## Verdict

PROTECT-HOW-COMPLETE: (TBD).
