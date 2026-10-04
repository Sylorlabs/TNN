# PREREG: Per-MAP-Shape Applicability Gate Integrated into Composition (UNFROZEN)

Status: FROZEN. This file is committed ALONE before any implementation.
Worker: Per-MAP Gate Integration Worker. Date: 2026-10-02.
Branch: tnn-native-lab. Local only, never pushed. Pure Zag. Frozen read only.

## 1. Hypothesis

H-APPL-INT: the per-MAP-shape APPL gate (APPLICABILITY-PERMAP-COMPLETE,
commit d8e05afc8) improves a real mechanism when integrated into the
collapsed composition mechanism (C234, COMPOSITION-COLLAPSE-COMPLETE,
commit 6e3e1d47d). Gating each candidate fragment by its shape's
applicability BEFORE the fragment DFS tries it cuts wasted DFS
expansions on partial-applicability problems (T4) with no regression on
the passing battery (T1/T2A/T2B/T3/T4B).

## 2. Context inputs (frozen, read only, never modified)

- applicability_permap/ (prereg 1403e0b57, results d8e05afc8): the
  per-candidate gate. Per-MAP-shape APPL: C-block 10 vs problem-gate 49
  vs naive 59; P1-P8 all PASS, 3/3 byte-identical per arm.
- composition_collapse/cl_patch.zag (C234): the collapsed composition
  mechanism. One candidate source (type-15 FRAG marks), one DFS
  (cl_dfs), 382 lines. Battery: T1 107, T2A 109, T2B 111, T3 105,
  T4 FAIL ans=-2, T5 decline -2, T4B 106.
- composition_C/cc_base.zag (1677 lines, frozen): assembly base.

## 3. Design (frozen)

### 3.1 Two arms, one driver

- BASE: C234 mechanism verbatim plus DFS-work counters only (ablation:
  gate removed). No gate logic, no AP region use.
- GATE: BASE plus the per-MAP-shape APPL gate integrated at candidate
  enumeration.
- Both arms: same base (ai_base.zag, verbatim copy of cc_base.zag),
  same driver protocol (ai_driver.zag: the 7 collapse battery tests,
  AP region threaded through), same pinned znc build.
- Build per arm: cat ai_base.zag ai_patch_<arm>.zag ai_driver.zag >
  ai_full_<arm>.zag.

### 3.2 Gate placement and semantics

The gate sits inside cl_candidates, before the cl_satisfy test, for
every non-used FRAG mark:

- Shape key: the fragment triple's len (from the mark aux). This is the
  candidate's operational shape: cl_fetch walks len steps and A's
  contract fallback uses plen len+1. Observable structure, zero domain
  labels. Two marks (m1,0,4) and (m2,1,4) share one shape history.
- Decision-point features F[8]: computed by ma_features_from_paths
  (verbatim from the permap patch) over t2_gather at the CURRENT
  frontier cur, the point where the candidate would apply. Same 8
  features (np, pmax, c5, c4, c3, c2, cx, r), same sim formula
  (10000/(100+2D), D = sum w_j*|d_j|), same consequence-driven weight
  rule (nearest opposite-outcome record over all records,
  w_j += 25*|F_j - G_j|, clamp 800, uniform 100 priors), same 15-point
  pessimistic margin.
- Record keying (composition-specific, preregistered): records are
  keyed by EXACT F match plus shape. Rationale, established by hand
  trace before this prereg: under the faithful permap port (per-shape
  counts, similarity-weighted across frontiers), T4B false-negatives.
  The seeded (my,0,2) fragment fails cl_satisfy at cur=105 and its
  failure record, being similarity-nearer to cur=104 than the
  cur=101 successes, vetoes the same fragment at cur=104 where it
  would succeed via fetch and complete the composition (ans=106).
  A fail at one frontier must not veto the shape at another frontier.
  Exact-F keying is the composition analog of the permap problem
  keying: in permap two problems with identical F shared records;
  here two frontiers with identical observable structure share
  records. Under exact match the sim machinery trivializes
  (avs/avf in {100,0}) and the rule reduces to: skip a shape at a
  frontier once it has failed there and optimism is exhausted.
- Optimism threshold: 2 (preregistered). Justification: per-frontier
  candidate multiplicity is low (few same-shape marks per frontier),
  so two same-shape failures at the identical frontier, where the
  structural constraints are fixed, suffice for a pessimistic prior.
  The winner-first safety argument below holds for any threshold >= 1.
- Outcome recorded per attempted candidate: 1 if cl_satisfy succeeds
  (ln>=1), 0 if it fails; cost 1. pap_observe verbatim otherwise.
- Gate=0: candidate skipped (counted, CGATE diagnostic line). Gate=1:
  cl_satisfy runs, outcome recorded, candidacy proceeds unchanged.
- Verification still arbitrates: the gate only prunes search.
  cl_satisfy, t2_try_verify, assembly, promotion unchanged.

### 3.3 Learner state

- AP region: 4096 bytes, driver-allocated per workspace, pap_init once.
  Threaded ev_query/ev_cq -> compose_try -> cl_dfs -> cl_candidates.
  Learner-owned persistent state (weights, records, decisions);
  researcher-owned: feature list, sim formula, 15-point margin, ETA=25,
  cap 800, optimism 2, exact-F shape-partition rule, uniform priors.
- 0 new modes, 0 bridges, 0 handlers, 0 new semantic cases.
  No COMPOSE_MODE. One compose_try definition, one call site.

### 3.4 Instrumentation (both arms)

Per compose_try call: enum_evals (cl_satisfy calls in cl_candidates),
select_evals (cl_satisfy re-checks in cl_dfs), gate skips, gate
attempts. Emitted as one CGATE-STAT line at the end of compose_try.
GATE additionally emits one CGATE diagnostic line per mark evaluation
(cur, m, start, len, gate, tried, ok), mirroring the permap CAND lines.

### 3.5 Safety argument (why no regression is expected)

On the battery the winning segment at each DFS depth is the
smallest-edge-id remaining candidate, hence the first evaluated at its
(frontier, shape): component MAPs precede episode rebounds in id
order and the Z chain consumes components in creation order. A
winning candidate therefore always meets ns=0 at its (F, shape) and
is attempted under any optimism threshold >= 1. The gate can only
ever skip non-winning candidates on T1/T2A/T2B/T3/T4B. On success
paths every cl_satisfy evaluation succeeds (true segments via fetch,
others via A's contract fallback, which depends only on (cur, len)),
so no fail is ever recorded before success and the gate never fires.

## 4. Predictions (hand-traced before implementation)

- T1/T2A/T2B/T3: PASS, answers 107/109/111/105, segment MAPs identical
  to C234 (13 26 39 / 13 26 39 52 / 13 26 39 52 65 / 27 42). Gate never
  skips (all CGATE-STAT skip=0 on these sections).
- T4B: PASS ans=106, segments (45 58) as C234. The gate prunes only
  doomed re-evaluations at cur=105 (all would fail again).
- T4: FAILS ans=-2, terminates, no false positive, in both arms.
  T4-section DFS work (enum_evals + select_evals, Y-train compose plus
  Z-query compose): BASE 21 (enum 17 + sel 4), GATE 15 (enum 11 +
  sel 4). The gate skips 6 doomed re-evaluations (shape-4/shape-2 at
  cur=105 and cur=103 after identical-frontier failures).
- T5: declines -2, terminates, both arms.
- BASE reproduces C234 answers/segments/T-RESULTs exactly (plus
  counter lines); it is the causal ablation for K8.

## 5. Kill bars (all must pass for APPL-INTEGRATION-COMPLETE)

- K1: T1 PASS ans=107, segments (13 26 39), GATE arm.
- K2: T2A PASS ans=109, GATE arm.
- K3: T2B PASS ans=111, GATE arm.
- K4: T3 PASS ans=105, GATE arm.
- K5: T4 FAILS ans=-2, terminates, no false positive, GATE arm.
- K6: T5 declines (-2), terminates, GATE arm.
- K7: T4B PASS ans=106, segments (45 58), GATE arm.
- K8: T4-section DFS work (enum_evals + select_evals) GATE < BASE.
- K9: on T1/T2A/T2B/T3 sections, every CGATE-STAT line shows skip=0
  and segment MAPs match C234 (gate never prunes on success paths).
- K10: 3/3 byte-identical runs per arm (SHA-256 recorded).
- K11: architecture audit: 0 modes/bridges/handlers/semantic cases;
  exactly one compose_try definition and one call site; no
  COMPOSE_MODE; gate is a search prune (verification arbitrates);
  AP region is learner state; no whole-MAP DFS remnants.
- K12: process: pure Zag, safebin PATH, `which python3 python` empty
  (toolchain guard in NAMECHECK.md Step 0).

No C234 kill bar is weakened: K1-K7 reproduce the collapse battery at
equal strength with the gate integrated.

## 6. Verdict names

- All bars pass: APPL-INTEGRATION-COMPLETE (report the DFS-count
  comparison and the per-section skip table).
- Any bar missed: BUILD-FAIL (report which bar and the exact
  mechanism: which candidate was wrongly gated or which count moved).

## 7. Method

- Toolchain guard recorded in NAMECHECK.md Step 0 before any work.
- This PREREG.md committed ALONE first (commit-order self-check).
- Then: verbatim base copy (cmp-verified), two patch variants
  (BASE = counters only; GATE = counters + gate; diff between them
  is exactly the gate), one driver (AP threading, identical for both
  arms), pinned znc builds, 3 runs per arm, byte-identity check.
- Commits with explicit pathspecs. Local only, never pushed.
- Zero em/en dashes in all documents (byte-verified before commit).
