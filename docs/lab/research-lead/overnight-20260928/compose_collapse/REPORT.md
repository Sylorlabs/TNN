# REPORT: H1+H2 Collapse -- Verdict SUBSUMPTION

Date: 2026-10-02. Worker: compose-collapse (replacement for GPI-3).
Battery: 5 discriminating problems (P1, P2a, P2b, P3, P5), 4 arms
(H1, H2, UNI, UNI-NOKIND), pure Zag, pinned znc.

## Verdict: SUBSUMPTION

H1 (learned typed contracts) and H2 (value-level function composition) collapse
into ONE operation: **behavior-contract composition**. H1 and H2 are
restrictions of it, not distinct mechanisms:

- H1 = the unified operation with kind-sets collapsed to majority singletons
  (finalize at n>=2), no unobserved-kind fallback, no failure-widening, no
  success-recording. Contract as STATIC kind summary: cheap admission.
- H2's discovery = the unified operation's execution rule with the kind filter
  deleted: ordered trial execution with value handoff. Contract as DYNAMIC
  execution: discovery plus complete fallback.

One mechanism (uc_uni.zag) reproduces H1's exact admission profile AND H2's
execution trace on the canonical problem with no mode switch, passes the two
discriminators where H1 fails (P1 mixed-kind, P2a single-shot), and passes P2b
(where the learned contract misleads) via failure-triggered widening. The
contract then grows from that experience and prunes the next query (P5:
7 tries -> 4 tries), connecting to the L2 adaptive matrix.

## The unified operation U (frozen, then transparently amended x2)

Each MAP carries a CONTRACT: observed (input-kind, output-kind) sets as bitmasks
(bit0=NODE, bit1=NUM). ONE admission rule, always on: single A admitted iff goal
kinds are compatible with A.inmask/outmask; pair (A,B) admitted iff kin
compatible with A.inmask, A.outmask INTERSECTS B.inmask, kout compatible with
B.outmask. Empty kind-set = compatible with all. ONE execution rule: ordered
trial (singles, then pairs, MAP-id order) with end-to-end verification;
intermediates logged. WIDENING: on exhaustive admitted failure, retry
filter-rejected pairs once (learner-observed failure triggers it; WIDEN=1
logged). Successful trials record kind observations (Amendment 2). No flag,
mode, or branch selects H1-like vs H2-like behavior (K7 audit).

## Kill bar results

All arms 3/3 byte-identical (sha256 below). Format: ANS / TRIES.

| Arm | P1 mixed-kind | P2a single-shot | P2b mislead | P3 canonical | P5 growth |
|-----|------|------|------|------|------|
| H1 (frozen) | -2 / 1 | -2 / 0 | -2 / 0 | 2 / 3 | - |
| H2 (frozen) | 65 / 1 | 2 / 1 | 2 / 1 | 2 / 1 | - |
| UNI (frozen+amd2) | 65 / 3 | 2 / 3 | 2 / 7 | 2 / 3 | 3 / 4 |
| NOKIND (frozen) | 65 / 3 | 2 / 5 | 2 / 5 | 2 / 5 | - |

- K1 P1: PASS. H1 rejects (X,Y) by majority signature (NUM!=NODE) and fails;
  H2 discovers (MAYBE,WALK) by execution; UNI admits (X,Y) via kind-set
  intersection ({1,2} x {1}); NOKIND passes by brute trial.
- K2 P2a: PASS. H1 admits nothing (n=1 < 2); H2 and UNI pass; NOKIND costs 5.
- K3 P2b: PASS. The sharpest discriminator. H1 fails (no signatures). H2 passes
  by coverageless trial (INTER=44). UNI's contract misleads (X.out={2} from the
  non-representative observation, but the sealed intermediate is NODE): 6
  admitted trials fail, WIDEN=1 fires, rejected pair (X,Y) succeeds at try 7.
  NOKIND passes at try 5.
- K4 P3: PASS. UNI reproduces H1's admission EXACTLY (tries=3: Y, D2, (X,Y))
  AND H2's trace (INTER=34) in one implementation, no mode switch. H2 tries=1.
- K5 P5: PASS (as amended). After Z1, X.outmask={1,2}; Z2 admits (X,Y) with no
  widening: ANS=3 TRIES=4 INTER=53; census m0 inmask=1 outmask=3 n=3, m1
  inmask=1 outmask=2 n=3, m2 inmask=1 outmask=1 n=1, m3 inmask=1 outmask=2 n=1.
  Z1 TRIES=7 > Z2 TRIES=4: H2-like discovery on first contact, H1-like pruning
  after the contract grows. Same mechanism, two temporal phases.
- K6 DETERMINISM: PASS. 3/3 byte-identical per arm (digests below).
- K7 NO-MODE AUDIT: PASS. uc_uni.zag has no runtime flag/mode selecting
  H1-vs-H2 behavior. kind_filter_on() is a constant-1 function existing only
  as the one-line ablation point (L2 adapt_on precedent); the full build's
  admission is one rule, always on. The H2 arm's behavior classes are
  researcher-defined (canonical H2's declared boundary); the pair is discovered.
- K8 HYGIENE: PASS. Zero em/en dash bytes; safebin guard attested; pure Zag.

## The reduction, precisely

R1 (H1 as restriction): uc_h1.zag differs from uc_uni.zag exactly in the
admission rule: majority-singleton equality (h1_maj_in/out, finalize n>=2)
instead of kind-set intersection with unobserved-fallback, and no widening or
success-recording. On all four problems the H1 arm reproduces the frozen H1
profile exactly (P1: -2/1, P2a/P2b: -2/0, P3: 2/3). H1's majority vote is a
lossy compression of U's contract; its n>=2 rule is a coverage gate U does not
need (P2a).

R2 (H2 as restriction): uc_nokind.zag differs from uc_uni.zag by EXACTLY one
line (kind_filter_on 1 -> 0; diff verified). Deleting the filter yields ordered
trial execution with value handoff: the H2 principle. Capability profile
matches H2 on every problem (both pass P1/P2a/P2b/P3; both fail nothing the
other passes).

Deviation from the letter of prereg clause (c), reported honestly: try counts
differ (H2: 1 per problem; NOKIND: 3/5). The delta is fully explained: H2
enumerates researcher-defined behavior CLASSES (first MAP per class, singles
skipped); NOKIND enumerates MAPs (singles + ordered pairs). E.g. P3: H2's one
(WALK,COUNT) trial IS NOKIND's 5th trial (X,Y); the 4 extra tries are MAP-level
singles H2's class coarsening skips. So H2 = U-minus-filter with the trial
space coarsened to researcher classes (H2's declared honest boundary). The
capability sets coincide; solvable(H1) and solvable(H2) are both subsets of
solvable(U). This is a granularity difference in a researcher-defined
enumeration, not a mechanism difference. Verdict stands as SUBSUMPTION at the
capability level, with this characterization.

## Why not "genuine distinction"

The prereg's predicted boundary was contract coverage (P2b). U crosses it via
widening: the filter is a preference ordering, not a hard gate. After crossing,
the contract grows (Amendment 2) and the boundary dissolves on repeat contact
(P5). A distinction that the mechanism itself detects (exhaustive admitted
failure), routes around (widening), and learns from (success-recording) is not
a mechanism boundary; it is a knowledge state. H1's majority freezing (P1) and
n>=2 gate (P2a) are strictly weaker forms of the same contract idea.

## L2 connection

P5 demonstrates admission-level adaptation from experience: the composer's own
filter changes what it tries next time, with no researcher mode and no new
operator. This complements the L2 structural operators (extend, truncate,
specialize, substitute, interface-adapt): those adapt STRUCTURES; U's contract
adapts ADMISSION. Natural next step: let the L2 operators and U's contract
share one observation channel (a truncated MAP's success updates the contract
that admitted it).

## Amendments (both transparent, committed before the corrected runs)

- AMEND1: P3 Y-teaching facts had chain geometry (from H2's world) but the
  prereg's stated expectations (50->3, 60->4) require star geometry under this
  battery's subject-count semantics (canonical H1 "count targets of node N").
  Facts fixed to stars; expectations, bars, predictions unchanged. The first P3
  H1 run is discarded as a world-construction error, reported not hidden.
- AMEND2: Section 3 said contracts learn from "teaching executions" but
  Section 5's P5 predicted growth from the Z1 composition. Added
  success-recording (successful trials record kind observations). K1-K4
  provably unaffected (all successes terminal; re-verified empirically).

## Honest limitations

- Four problems is a discrimination battery, not generality proof. SUM to PLAN
  (the open composition frontier) is untouched; U is value-handoff only.
- Expected-answer verification still used (canonical boundary).
- H2's classes and U's behaviors are installed as previously-learned MAPs;
  behavior induction not under test (canonical standing).
- The widening retries filter-rejected pairs blindly; a smarter policy (e.g.
  coverage-directed) is future work.
- Single binary per arm; cross-arm comparison is by construction plus profile
  match, not by shared binary.

## Determinism (K6)

Run-output sha256 (3/3 identical):
- h1: 94e7cf5ea62ac29a75506249279e528479f2c0fb3379b4f8902b347f8373b926
- h2: 5cec6aeb96dee45636620428eb2bfe1e8e6e7df6f78b2ae0ae00ea1496126a52
- uni: 6f9045116b3e7ccd3004cd6e3b6863df366c798f25c08562a8ec65e497edad30
- nokind: c454274b5a4283daf10287320bca6e0c81eafa00f7baa3828f6c222d7d081e03
Binaries: h1 30a5e752752d9497b59f666f7703e3d6a3916c047fc0554ea2e34b16ee2a765f,
h2 83259eb38a09f8b5cf6147517031d9d49176049e62b1a25797e6db613855623d,
uni 01fa257124411de079f5104df2f7188b857fa35ff664a3b11ecdd94fe46439c1,
nokind 30f28c81816a6ca4415c9bb218e3a3e11a7e5b867a3930229b8e5c72e96e416b.
Pinned znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(identical to the safebin znc used for all builds).

## Architecture accounting

- Cognition lines added: ~230 (uc_base.zag) + ~80/90/150 per arm.
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- Researcher-owned: behavior implementations (WALK/COUNT/MAYBE/IDENT),
  H2's class enumeration, U's admission/widening/record rules.
- Learner-owned: kind-set contracts, admitted/rejected sets per query,
  composite outcomes, grown contract on P5.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/compose_collapse/`:
PREREG.md (frozen, committed before implementation), PREREG_AMEND1.md,
PREREG_AMEND2.md (both transparent, committed before corrected runs),
NAMECHECK.md, REPORT.md (this file), uc_base.zag, uc_h1.zag, uc_h2.zag,
uc_uni.zag, uc_nokind.zag (one-line sed ablation of uc_uni.zag, diff
verified), uc_full_*.zag (assembled), uc_*_bin, *_run1/2/3.txt.

## Recommended follow-ups

1. Sealed 5th pair designed by an independent adversary to attack U (the
   consolidation does not claim generality; four problems is a pattern).
2. Coverage-directed widening: use the observed intermediate kind at stage-1
   failure time to widen selectively rather than blindly.
3. Unify U's contract channel with the L2 structural operators (shared
   observation channel).
4. Lift H2's class coarsening: discover behavior classes from structure
   (mode induction, H2's declared future work) rather than receiving them.
