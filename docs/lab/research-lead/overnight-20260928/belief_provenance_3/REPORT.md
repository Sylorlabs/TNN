# REPORT: BP-3 (domain-blindness + abstention)

Worker: BELIEF-PROVENANCE-3 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance_3/
Verdict: **BP-3-PASS** (all 17 preconditions, all 14 kill
bars, K-DET 3/3 byte-identical, K-HYG clean). Method: frozen
prereg (committed as 2b589e521 before any implementation),
BP-2's belief machinery reused verbatim, three permuted
worlds for FP6 and three abstention worlds for FP7 plus the
help-question policy comparison, in-driver bars.

## 0. What was built

`bp3_learner.zag` is BP-2's `bp2_learner.zag` copied
verbatim (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
on both files): the learner-owned u8 belief table, R1-R7,
eff(), b_retire with kind-3 reason edges, the lg()
liveness-gating baseline. No redesign; the task's "build on
BP-2" is literal.

`bp3_driver.zag` is the only new code: `bp3_perm` (opaque
relabeling bijection: pm=0 identity, pm=1 offset +100000,
pm=2 reflection 1000000-x), `bp3_build` (the BP-2 world
replay with every entity/relation literal relabeled;
structural parameters untouched), `bp3_force` (forced
argmax ignoring bar and tie: the "always guess" baseline
policy), `bp3_fp6_run` (t0-t4+persistence step runner with
store/compare modes), `bp3_degrade`, and the three arms.

`bp3_full.zag` = `xf_block.zag` (patched block, verbatim,
SHA-256 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
re-verified before and after the build) + `bp3_learner.zag`
+ `bp3_driver.zag`. One `main`. Pinned znc, build exit 0;
the A0102 warnings are the benign ignored-return-value
pattern pervasive in the frozen block itself.

One driver bug was found and fixed before the scored runs:
the FP6 compare mode measured pm=1/pm=2 traces against a
fresh zeroed buffer instead of the pm=0 reference trace,
failing K-FP6-TAB/TRC spuriously on the first build. The
fix passes the reference trace and reports table-equality
vs trace-equality as separate bitmask bits. It aligns the
driver with the frozen prereg; no bar or prediction was
changed. Disclosed here, not hidden.

## 1. Kill-bar results

Preconditions: PC6-0A/B/C, PC6-1A/B/C, PC6-2A/B/C (all
three permuted worlds build: singleton==mv2, prov rel
87/100087/999913 with 4 live type-1 facts, mz2 is MAP_Z
with agg==mv3), PC7a-0..3, PC7b-0..3 (W7a/W7b rival
worlds). All 17 PASS.

FP6 (domain-blindness), all PASS:
- K-FP6-VAL: the pm=0 arm reproduces the BP-2 hand-derived
  sequence exactly (100/100, 75/75, 37/37, 9/9, 0/0 with
  kind-3 retirement; R7 mz2,-3,-3,-3; lg mz2 throughout;
  persistence -3,-3,-3).
- K-FP6-IDX: node ids byte-identical across identity,
  offset, and reflection: navx=27, mv2=194, mv3=274,
  mz2=299 in all three arms.
- K-FP6-TAB: the full 8192-byte belief tables and the
  1024-byte hasb vectors byte-identical across all three
  arms at each of t0,t1,t2,t3,t4 (5 x 9216 bytes compared
  per arm pair).
- K-FP6-TRC: the per-step belief trace (live, b_sup[V3],
  b_sup[Z2], R7, lg) identical across arms, including the
  R7 abstention column.

FP7a (core abstention), all PASS:
- K-FP7-A1: b_sup = 37/37/37/37 (V3,V2,Z2,Z3), all below
  BAR0=50 after degrading both rivals' provenance by 2
  facts each.
- K-FP7-A2: R7({Z2,Z3}) = -3 (exact tie at 37; also
  below bar).
- K-FP7-A3: R7({Z2}) = -3, R7({Z3}) = -3.
- K-FP7-A5: R7({}) = -3; R7({Z2,999}) = -3 (recordless
  candidate skipped, weak Z2 below bar).
- K-FP7-A4: the 8192-byte belief table byte-identical
  before and after all five R7 queries; no kind-3 edge on
  either composite. Abstention writes nothing.

FP7b (does abstention help), all PASS:
- K-FP7-B1: setup Z2=37, Z3=9; R7(50) = -3; forced
  argmax = MAP_Z2 (299). The guesser picks the weak
  leader; the belief layer refuses.
- K-FP7-B3: R7 with bar=30 pre-evidence = MAP_Z2. The
  less-cautious bar commits to the claim the Seq D
  evidence then disconfirms. The bar is load-bearing.
- K-FP7-B2: Seq D post-evidence Z2=17 (disconfirmed),
  Z3=29 (confirmed); R7(50) = -3. The abstainer never
  endorsed Z2 at any point.
- K-FP7-B0: W7c setup 37/9, R7(50) = -3 (independent
  build verified).
- K-FP7-B4: Seq C post-evidence Z2=57 (confirmed),
  Z3=0 (disconfirmed); R7(50) = MAP_Z2. The abstainer
  DOES commit once the evidence makes the claim
  endorsable.

K-DET: 3/3 runs byte-identical, SHA-256
e1f5fb137a4b29b8d28d415ca5ac131afe806a7f7a22032c66a0018a262c6043.
K-HYG: pure Zag under safebin (`which python3` empty at
build and run); zero em/en dash bytes; 0 new edge types
(1/14/3 only), 0 new node types, 0 modes, 0 bridges,
0 handlers; xf_block.zag hash unchanged; opaque ids;
learner file verbatim. BP3-SUMMARY 31/31.

## 2. What this means

FP6 is confirmed as preregistered, and more strongly than
the minimum: not just one permutation but two (an
order-preserving offset and an order-reversing
reflection) leave the belief tables and the selection
trace byte-identical, with allocator-assigned node ids
themselves unchanged. The belief layer never reads a
relation or entity value anywhere in its code path
(liveness, edge types, counts, field16 partition, table
indices only), and the sealed test now proves the whole
pipeline from world build through R7 selection is
value-blind. Dependence on human domain identity would
have shown up as any byte difference; there was none
across 9216 bytes x 5 steps x 2 arm pairs. This seals
DESIGN.md Section 7 empirically.

FP7 is confirmed as preregistered: with no candidate above
bar, R7 returns -3 across the pair, each single, the empty
set, and the recordless-candidate edge case, and the
abstention is side-effect-free (belief table untouched, no
retirement edges, no meta rows to write since B-META is
not implemented). This is the BP-1 K-4 result now at the
belief layer, with the mechanism (not just the outcome)
under test.

The help question gets an honest, measured answer, not a
slogan. Abstention does BOTH: it avoids wrong answers AND
it avoids answering, and the preregistered evidence
sequences separate the two. In Seq D the abstention policy
(bar=50) never endorsed the weak leader that the evidence
disconfirmed, while the forced-guess policy and the
bar=30 policy both endorsed it: abstention avoided a wrong
answer that less-cautious policies gave. In Seq C the same
policy endorsed the leader once confirming evidence moved
it to 57>=50: abstention is not never-answering. The bar
prices the tradeoff, and K-FP7-B3 shows the price is real:
lowering it to 30 buys a commitment that the evidence
then breaks. The disclosure stands: the Seq C/D evidence
is researcher-scripted ground truth for the policy
comparison, not emergent world behavior. What the test
establishes is that the mechanism enforces its own
endorsement standard (DESIGN.md I3: no selection without
support) and that the standard is load-bearing, not
decorative.

## 3. One-system accounting

New learner machinery in this lane: none. The belief
table, R1-R7, eff(), lg() are BP-2's, reused verbatim.
New test-harness code only: the permutation bijection, the
parameterized build, the forced-argmax baseline, the step
runner. 0 new edge types (1/14/3 only), 0 new node types,
0 modes, 0 bridges, 0 handlers, 0 semantic cases. Beliefs
remain learner-state records, not a subsystem.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): the FP6 byte-identity
across two non-trivial permutations at every step of a
5-step belief trajectory; the FP7 abstention across pair,
single, empty, and recordless cases with side-effect
freedom; the help-question policy comparison (abstain vs
forced-guess vs bar=30) under two preregistered evidence
sequences; determinism; hygiene.

Reasoned: that the offset+reflection pair is an adequate
adversary for "opaque permutation" (a keyed
pseudo-random permutation would be stronger against
hypothetical range-based value branching; the current
pair covers value-identity and value-order dependence);
that bar=50 is the right operating point rather than
merely the preregistered BAR0 (sensitivity analysis is
future work); that the scripted Seq C/D evidence fairly
models world revelation (it is disclosed as scripted).

## 5. Open questions (not claimed)

FP1/FP4/FP5, R3/R5 dynamics beyond the scripted evidence,
bar-adjustment trajectories, d_self learning, B-FACT/
B-META records, multi-hop/cyclic propagation fixpoints,
combiner alternatives to min, eviction interaction,
constant sensitivity. The belief layer's falsifiable
predictions FP2/FP3/FP6/FP7 are now sealed; FP1 (graded
flip point), FP4 (learned source discount), and FP5
(independence discount) remain open per DESIGN.md
Section 10.

## 6. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on tnn-native-lab only,
  explicit pathspecs. This report is committed with the
  lane's implementation artifacts.
- DESIGN.md is untouched; this lane tests it and does
  not reinterpret it. BP-1's and BP-2's REPORT.md files
  are untouched.
- Suggested next step if approved: FP1 (the graded
  weakening flip point, the last cheap sealed arm in the
  FP family), then FP4/FP5 which need new world shapes
  (self-amplification failure arms, disjoint-set
  confirmations).
- Style: no em/en dashes in this file (hyphens only),
  opaque identifiers throughout.
