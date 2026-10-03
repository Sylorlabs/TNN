# CAM-1 Build Report: Trial-Based Construct-and-Apply

Date: 2026-09-30. Worker: CAM-1 Builder (resumed with amended specs).
Verdict label: CAM1-BUILD-COMPLETE.

## What was built

`cam1.zag` (818 lines, 63 functions) implements the CAM-1
PROPOSE -> VERIFY -> PROMOTE -> APPLY loop per the frozen
specs: CAM-1 prereg (68a41be8a), integration spec A1-A12
(62e5ebb9f), ISA boundary ruling (0525377f3).

The critical amendment is implemented: finite-difference
analysis is OUT of P-DEP. Regularity discovery is trial-based.
The core supplies ADD and EQ as domain-neutral machinery; the
learner-side policy tries template combinations over
structurally aligned exemplars, corroborates each, and promotes
what predicts. No FIND_POLYNOMIAL_ORDER exists anywhere in the
source (G1 audit clean).

## Architecture

Workspace: CLA-2 node format (type_tag, ref[4], payload[4]),
u8-backed with get32/set32 (compiler workaround honored).
Standing = SUPPORTS count minus CONTRADICTS count, computed
from edges, never stored (A5/A11).

PROPOSE:
- Alignment by relation-set signature (purely structural).
- P-INV: constant object across group -> B_LITERAL candidate.
- P-DEP (trial-based): for varying fields, try B_COPY_A
  (z = a), B_DBL_A (z = a + a), B_ADD_AB (z = a + b) over
  co-occurring relations. A template becomes a candidate iff
  it holds via EQ on EVERY construction exemplar. Priority:
  COPY_A, DBL_A, ADD_AB (simpler first).

VERIFY: candidate must predict every held-back exemplar
exactly. Failed candidates are discarded, not repaired.

PROMOTE: verified candidate reified as MAP node
(refs [trigger, param_dim, group, 0], payload
[body_kind, in_a, in_b, literal]); SUPPORTS edges from
corroborating exemplars; INSTANCE-OF to the group.

APPLY: exact-key lookup first (W1 behavior bit-for-bit);
on miss, find MAPs by trigger, require standing >= 1,
evaluate the body, prefer higher standing on disagreement;
else -2.

## Test results (synthetic data, this worker's own; FW1-FW9 untouched)

All 6 test groups pass. Determinism: 3/3 byte-identical
(sha256 b995a5a1c668f08c063d0524190928dc2dcd269a3f36044ab5d4e5339462c7b1).

- W2-class (P1): 5 LITERAL maps promoted from 3 instances;
  5/5 novel-instance probes correct; exact-hit preserved.
- W3-class (P2): 1 ADD_AB map promoted from 6 pairs;
  trial discovery found z = x + y with no order detection
  and no coefficient fitting; novel-pair probes 30 and 15
  correct; exact-hit preserved.
- P5 negative control: random mappings -> 0 promotions,
  all novel probes -2. The mechanism abstains.
- P6 VERIFY load-bearing: with VERIFY, a spurious
  construction-time regularity (711 = 2*712, broken by
  holdback) is rejected (0 promoted). With VERIFY ablated,
  it promotes and answers 6 instead of -2. Corroboration,
  not proposal, carries the precision.
- P7 revision: 2 CONTRADICTS edges demote a MAP
  (standing 1 -> -1); queries revert to -2. No revision mode.
- P4 no hallucination: unknown relations and subjects -> -2.

P3 (FW2/FW3 sealed worlds) not testable by this builder;
builders stay blind per ruling A.

## One-System Rule accounting (measured)

- Cognition source lines added: 818 (single file, includes
  test harness; mechanism proper is ~500).
- New hardcoded semantic cases: 0 (G1 audit: no MUL,
  PROCEDURE, CAUSE, LAW, STEP, FIND_ORDER, POLYNOMIAL,
  DIFFERENCE as operations).
- New modes: 0. New bridges: 0. New task-specific handlers: 0.
- Learner-state structures: MAP nodes, GROUP nodes,
  SUPPORTS/INSTANCE-OF/MEMBER/CONTRADICTS edges. All
  ordinary workspace content; no new store.
- Computational basis used: EQ (==) and ADD (+) only.
  No SUB, no MUL, no difference tables.

## The unity claim (trial-based)

W2 and W3 run through one propose path, one MAP format,
one apply path. The only difference is what the trial
discovers: a constant (order-0, P-INV) versus an additive
dependence (P-DEP). Invariance is order-0 dependence,
now without any polynomial machinery in the core.

## Kill bars

K1: prereg (68a41be8a) strictly precedes this implementation
(verified via git merge-base in the commit sequence).
K2: zero per-domain constructors, zero semantic cases, zero
modes/bridges/handlers (source inspection above); one binary
passes W2-class and W3-class synthetic worlds.
K3: pure Zag; zero Python (toolchain guard in NAMECHECK.md);
documents dash-clean; contaminated paper untouched; local
commits with explicit pathspecs under cam1_build/ only.

## Files

- NAMECHECK.md (Step 0, toolchain guard)
- cam1.zag (implementation + test harness)
- cam1_bin (compiled with pinned znc_linux_x86_64_abed8aa1)
- build.err (compiler output, warnings only)
- BUILD_REPORT.md (this file)
