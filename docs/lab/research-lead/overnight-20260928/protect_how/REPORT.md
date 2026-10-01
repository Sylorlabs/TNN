# Protect-the-How Experiment (Micah Q6)

**Status:** PROTECT-HOW-COMPLETE
**Date:** 2026-10-01
**Worker:** Protect-the-How Worker (retry; prior attempt throttled after
building both binaries and completing control run 1; this run completed
all 6 runs)

**Determinism:** control 3/3 byte-identical (SHA-256
baee80b3c87327a1c20a8d3f0a0defe2a47015218ef7282945b1599099c9e1a0);
treatment 3/3 byte-identical (SHA-256
8204dc203c142631c04008d2c8b20afe8e4984ab74229bcb94c1c4b78e7eb054).
Pure Zag via pinned znc. Safebin active, zero forbidden executables.

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

| metric | control (3/3) | treatment (3/3) |
|---|---|---|
| post_p_map (MAP node alive) | 1 | 1 |
| post_p_cells (walkable op cells) | 0 | 8 |
| post_p_reexec | -999998 (dead) | 5 (alive) |
| post_answers (of 20) | 0 | 0 |
| post_shadow | 0 | 0 |

### Phase 5: 20 new subjects

| metric | control (3/3) | treatment (3/3) |
|---|---|---|
| new_hits | 0 | 0 |
| new_rebind_ok / try | 20 / 20 | 17 / 20 |
| new_trial_ok | 0 | 3 |
| new_trial_verifies | 0 | 9 |

## Analysis

### 1. The Q6 reversal is demonstrated

Control (stock lowest-bid eviction) reproduces the known pathology and
extends it: after 1000 interference teaches, P's MAP node survives as a
fossil (post_p_map=1) but all 8 op cells are evicted (post_p_cells=0,
reexec dead). The executable HOW dies. The 20 cached answers also die
(post_answers=0/20) — under this pressure the control loses both the how
and the what.

Treatment (3-tier: derived answers first, generative structure last)
reverses the retention order: all 8 op cells survive, reexec=5, P fully
executable after the same 1000 interference teaches. The 20 cached
answers are deliberately sacrificed (post_answers=0/20, all Tier-1
victims). This is the Q6 pattern made mechanical: permit cached answers
to die before P, retain the generative procedure.

### 2. Reconstruction economics

The 20 sacrificed answers are cheap facts: each re-derivation is one
`ev_teach` (or one shape-rebind + teach, 0 trial verifies in 17/20 phase-5
cases). P's procedure, by contrast, required a full trial
(build_verifies=3) to learn. Retaining P (8 cells + MAP = 9 nodes)
preserves the ability to regenerate unbounded answers; retaining 20
answer FACTs (20 nodes) preserves only those 20. Per-node, the procedure
dominates: 9 nodes of HOW subsume arbitrarily many WHATs.

### 3. Phase 5: re-derivation from retained shape

With P alive (treatment), 17/20 new subjects re-derive answers via shape
rebind with 0 trial verifies; 3 fall back to trial (9 verifies total,
3 new MAPs). With P's cells dead but MAP node alive (control), 20/20
rebind via driver-held shape. Phase 5 uses driver-held plen, so it
measures re-derivation mechanics, not learner-state shape retention
(see Limitations 4).

### 4. Falsification signature

The ONLY cognition difference between arms is `evict_node`
(`ph_diff.txt`). Same driver, same worlds, same interference. The
survival difference (8 cells vs 0) is causally attributable to the
eviction order. Treatment does not change what is learned, only what is
kept.

### 5. Honest boundary

The 3-tier policy is researcher-authored, not learner-derived. It proves
the retention ORDER works (HOW before WHAT), not that TNN can discover
the order. The protection builder (a298709d5) showed use-driven
protection; this experiment shows value-order-driven eviction. Neither
is yet learner-owned valuation (Micah Q5/Q8 remain open).

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

PROTECT-HOW-COMPLETE: SAVES-HOW-BY-ORDER.

A 3-tier eviction policy (derived cached answers first, generative
structure last) preserves the executable procedure P through 1000
interference teaches that kill it under stock eviction: 8/8 op cells
alive, reexec=5 in treatment vs 0/8 cells, reexec dead in control
(3/3 byte-identical per arm). The 20 cached answers are deliberately
sacrificed in treatment; each is re-derivable for ~1 teach or 0-verify
rebind, while P's procedure required a full trial to learn. The
researcher-authored order (HOW before WHAT) works; whether the learner
can derive the order itself remains open (Q5/Q8).
