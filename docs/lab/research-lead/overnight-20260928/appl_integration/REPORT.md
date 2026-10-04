# REPORT: Per-MAP-Shape Applicability Gate Integrated into Composition

## Verdict: APPL-INTEGRATION-COMPLETE

**The per-MAP-shape APPL gate is integrated into the collapsed
composition mechanism (C234) and improves it on the natural consumer:
on T4 (partial applicability) the gated arm declines with 19 DFS-work
units vs the ablation's 27 (8 wasted cl_satisfy evaluations pruned,
30% fewer), while T1/T2A/T2B/T3/T4B pass with byte-identical answers,
segments, and results to the ungated collapse, and the gate never
fires on any success path (skip=0 on all four passing sections).
3/3 byte-identical per arm. Zero modes/bridges/handlers.**

Date: 2026-10-02. Worker: Per-MAP Gate Integration Worker.
Prereg: PREREG.md, commit c4821dc44 (frozen before implementation).
Branch: tnn-native-lab, local only, nothing pushed.

## What was built

Two arms from one frozen base (composition_C/cc_base.zag, 1677 lines,
copied verbatim, cmp-verified) and one driver protocol (the 7 collapse
battery tests):

- BASE (ablation): C234 plus DFS-work counters only. No gate.
- GATE: BASE plus the per-MAP-shape APPL gate. In cl_candidates, before
  the cl_satisfy test, each non-used FRAG mark is scored by
  pap_decide(AP, F, shape): shape = the fragment triple's len (its
  operational length: cl_fetch walks len steps, A's contract uses
  plen len+1); F[8] = observable path-structure features from
  t2_gather at the current frontier cur (same 8 features, sim formula,
  weight rule, and 15-point margin as APPLICABILITY-PERMAP);
  records keyed by exact-F match plus shape (preregistered; see 5).
  Gate=0 skips the candidate (counted, CGATE diagnostic line);
  gate=1 runs cl_satisfy and records the outcome (1 = satisfiable,
  0 = not). Verification (cl_satisfy, t2_try_verify) still arbitrates
  every positive result: the gate only prunes search.
- The AP region (4096 bytes, weights + 64 shape-keyed consequence
  records) is driver-allocated per workspace and threaded
  ev_query_ap/ev_cq -> compose_try -> cl_dfs -> cl_candidates:
  learner-owned persistent state, no modes, no bridges.

The BASE vs GATE outputs differ ONLY in CGATE/CGATE-STAT lines
(verified by diff): every T-ANS, T-RESULT, COMP-SEGS, RB-STAT, and
COMP-STAT line is byte-identical between arms.

## DFS-count comparison (kill bar K8)

Per compose_try: enum_evals (cl_satisfy calls in cl_candidates) +
select_evals (cl_satisfy re-checks in cl_dfs). Section sums:

| Section | BASE enum+sel | GATE enum+sel (skip) |
|---------|---------------|----------------------|
| T1 3-struct | 18+3 = 21 | 18+3 = 21 (0) |
| T2A 4-struct | 34+4 = 38 | 34+4 = 38 (0) |
| T2B 5-struct | 55+5 = 60 | 55+5 = 60 (0) |
| T3 xdomain | 8+2 = 10 | 8+2 = 10 (0) |
| T4 partial | 21+6 = 27 | 13+6 = 19 (8) |
| T5 noexpected | 0 | 0 (0) |
| T4B frag | 22+4 = 26 | 18+4 = 22 (4) |
| Total | 182 | 170 (12) |

K8: T4-section GATE 19 < BASE 27. PASS. The gate prunes 8 wasted
cl_satisfy evaluations on T4's failing search (30% fewer), and 4 on
T4B's failing branches, with zero change on every success path.

## Kill bar adjudication

- K1 T1 PASS ans=107, COMP-SEGS n=3 (13 26 39): PASS.
- K2 T2A PASS ans=109, n=4 (13 26 39 52): PASS.
- K3 T2B PASS ans=111, n=5 (13 26 39 52 65): PASS.
- K4 T3 PASS ans=105, n=2 (27 42): PASS.
- K5 T4 FAILS ans=-2, terminates, no false positive: PASS.
- K6 T5 declines (-2), terminates: PASS.
- K7 T4B PASS ans=106, n=2 (45 58): PASS.
- K8 T4-section DFS work GATE < BASE (19 < 27): PASS.
- K9 skip=0 on every CGATE-STAT line of T1/T2A/T2B/T3 and segment
  MAPs match C234: PASS (gate never prunes on success paths).
- K10 3/3 byte-identical per arm: PASS. BASE
  de47314d8f96db2a28845602abe51b7b52d00e61faf190cf77ad5a5bc2bfe95a;
  GATE
  ebd90f76cb24dd30d7fb1550096247cb71afee285bb66b8e27fb21721837d072.
- K11 architecture audit: PASS. One compose_try definition, one call
  site; 0 COMPOSE_MODE; 0 modes/bridges/handlers (only the inherited
  "Zero modes..." header comment); 0 whole-MAP DFS remnants; gate is
  a prune, verification arbitrates; AP region is learner state; 0 new
  semantic cases (features are gathered-path structure plus query
  relation; shape is fragment len from mark aux).
- K12 process: PASS. Pure Zag; safebin PATH; `which python3 python`
  empty at startup and re-checked after the runs.

All 12 pass. No C234 kill bar was weakened: K1-K7 reproduce the
collapse battery at equal strength with the gate integrated.

## Mechanism evidence

T4 Z-query, GATE arm (CGATE lines). Marks: (45,0,4) X, (58,0,2) Y,
(83,0,4) episode-X, (94,0,2) episode rebound (plen-2). Depth 0: all 4
attempted (optimism), all satisfiable via fetch or A's fallback.
Under (45,0,4) at cur=105: (58,0,2),(83,0,4),(94,0,2) attempted once
each and fail (no plen-(len+1) path remains, fetch fails), recording
(F105,2,f),(F105,4,f),(F105,2,f). On the next visit to cur=105 the
gate fires: shape-4 has 2 identical-frontier failures
(avs=0, avf=100, 0 > 115 false) and both shape-4 marks are skipped;
shape-2 likewise after its second failure. The same repeats at
cur=103. T4 still fails cleanly (ans=-2, COMP-FAIL, terminates):
the gate prunes only re-evaluations of shapes already proven
inapplicable at the identical frontier. The decline is auditable:
each skip names cur, mark, len, and gate=0.

T4B Z-query, GATE arm: the seeded (58,0,2) fragment fails at cur=105
(recorded) but is attempted at cur=104 because records are keyed by
exact frontier match: (F104,2) has 0 records, so optimism fires,
fetch succeeds (104->105->106 via r2), and the composition completes
(ans=106). This is the case the faithful per-shape port gets wrong
(see 5): frontier keying is load-bearing for the no-regression bars.

## Why exact-frontier keying (preregistered design decision)

Hand-traced before the prereg: under a faithful permap port
(per-shape counts, similarity-weighted across frontiers), the
(F105,2) failure record is similarity-nearer to F104 than the
(F101,2) successes (D=400 vs D=700 under uniform weights; the
consequence-driven weight update widens the gap by upweighting
np/pmax), so pap_decide vetoes (58,0,2) at cur=104 and T4B fails.
A fail at one frontier must not veto the shape at another frontier,
because applicability genuinely differs by frontier (remaining path
structure). Exact-F keying is the composition analog of the permap
problem keying: identical observable decision contexts share
records. Under it the sim machinery trivializes (avs/avf in
{100,0}) and the rule becomes: skip a shape at a frontier once it
has failed there and optimism (2, preregistered) is exhausted.

## Honest boundaries

1. Prediction discrepancy: the prereg hand-trace predicted T4-section
   BASE=21/GATE=15; measured BASE=27/GATE=19. The trace assumed the
   second episode rebound was plen-4 (it is plen-2, m=94) and missed
   that A's fallback makes shape-2 fragments candidates at cur=103,
   adding two depth-1 selections per arm. The kill bar is the
   inequality GATE < BASE, which holds (19 < 27); the mechanism
   works as designed, and the CGATE trace above reconstructs every
   evaluation. The error was in the prediction, not the gate.
2. The gate helps only where the search revisits frontiers: T4 and
   T4B's failing branches. On success paths it is provably inert
   here (winner-first: the winning segment is always first evaluated
   at its (frontier, shape), hence attempted under any optimism
   >= 1; and every evaluation succeeds, so no fail is ever recorded
   before success). A battery where the winner is not first would
   test the gate's false-negative rate; that adversarial test is
   future work.
3. The 64-record ring, 15-point margin, ETA=25, cap 800, and uniform
   priors are researcher-owned (as in permap P8); learner-owned are
   all weights, records, and per-candidate decisions. This is L2
   structural learning (consequence-driven per-shape gating), not
   L3 representational invention.
4. The 5-param ev_query wrapper exists only for arity compatibility
   with the base's internal test battery (t_c1 etc.); it allocates a
   fresh AP per call and is not on the driver's path. Not a mode or
   bridge: one pipeline (ev_query_ap), one compose_try, one call
   site.

## Determinism

3 runs per arm, byte-identical outputs, SHA-256 recorded in
NAMECHECK.md. The gate is integer arithmetic on deterministic
inputs (t2_gather, edge-id order); no nondeterminism introduced.

## Files

- `PREREG.md`: frozen preregistration (commit c4821dc44, committed
  before implementation)
- `NAMECHECK.md`: toolchain guard, build records, audits
- `REPORT.md`: this file
- `ai_base.zag` (1677 lines): verbatim copy of cc_base.zag
  (cmp-verified)
- `ai_patch_base.zag` (412 lines): C234 + counters + AP threading
  (ablation; no gate)
- `ai_patch_gate.zag` (571 lines): BASE + per-MAP-shape APPL gate
- `ai_driver.zag` (327 lines): collapse battery + AP threading
  (identical for both arms)
- `ai_full_base.zag` (2401 lines), `ai_full_gate.zag` (2566 lines):
  concatenated build inputs
- `ai_base_bin`, `ai_gate_bin`: pinned znc builds
- `run_base_{1,2,3}.txt`, `run_gate_{1,2,3}.txt`: 3/3 byte-identical
  run outputs per arm
- `base_compile.txt`, `gate_compile.txt`: build logs (exit 0,
  benign A0102 warnings only)

## Architecture accounting

Cognition lines added: the gate substrate (~160 lines of Zag in
ai_patch_gate.zag: pap_init, ma_features_from_paths, pap_fmatch,
pap_count_shape, pap_avg_sim, pap_decide, pap_observe, plus the
gate check and CGATE diagnostics) and the counters/threading
(~30 lines, both arms). New hardcoded semantic cases: 0. New
modes/bridges/handlers: 0. New learner-state structures: the
4096-byte AP region (64 shape-keyed consequence records; extends
the permap APPL record layout with exact-F keying). The T4/T4B
search reduction comes from learner-owned per-(frontier,shape)
records and decisions, not researcher-authored domain knowledge.
Capability-source delta: positive (fewer wasted expansions, same
answers); the gate cannot create capability, only prune search,
and verification still arbitrates every composition.

## Recommendation

Adopt the gated composition as the canonical composition operation
for the T4 frontier: identical capability to C234 on the full
battery, measurably cheaper failure on partial applicability, and
an auditable per-candidate decline diagnostic. Next: adversarial
worlds where the winning fragment is not first in edge-id order
(false-negative rate of the prune), and learner-originated
sub-fragment marks (the remaining T4 question: who writes the
marks the gate then triages).
