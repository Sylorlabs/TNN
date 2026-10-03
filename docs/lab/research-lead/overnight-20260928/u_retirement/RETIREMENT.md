# RETIREMENT: U retired as a separate mechanism

Date: 2026-10-03. Worker: U-RETIREMENT. Lane:
`docs/lab/research-lead/overnight-20260928/u_retirement/`.
Branch: `tnn-native-lab` (explicit pathspecs; local only, never pushed).

## Verdict

U, the unified behavior-contract composition operation, is retired as a
separate mechanism. GEN, the value-graph generalization of U, subsumes it
fully and is the single surviving composition mechanism. U is retained
only as the documented restricted form of GEN (Section 9), for historical
reference. No capability is lost. Nothing is reimplemented. One mechanism
replaces two. This is Micah's architecture-compression priority #10 in
action.

This document states exactly what U was, exactly what GEN is, proves the
subsumption empirically, defines the reduction U = GEN restricted to
(single-round linear pool, predicted handshake, stateless trial
enumeration), and records the fresh byte-identical verification runs that
underwrite every claim.

## 1. What U was

U was the unified behavior-contract composition operation built in the
COMPOSE-COLLAPSE lane (2026-10-02, verdict SUBSUMPTION). It collapsed H1
(learned typed contracts) and H2 (value-level function composition) into
one operation, proving both were restrictions of it.

U, precisely (frozen `compose_collapse/uc_uni.zag`):

* Each MAP carries a CONTRACT: observed (input-kind, output-kind) sets as
  bitmasks (bit0=NODE, bit1=NUM). Empty kind-set = compatible with all.
* ONE admission rule, always on. Single MAP A admitted iff the goal kinds
  are compatible with A.inmask and A.outmask. Ordered pair (A,B), A != B,
  admitted iff kin compatible with A.inmask AND A.outmask INTERSECTS
  B.inmask (the predicted handshake) AND kout compatible with B.outmask.
* ONE execution rule: ordered trial with end-to-end verification. All
  admitted singles in MAP-id order, then all admitted ordered pairs in
  MAP-id order. Pair trial: apply A to the start value, log the
  intermediate (INTER=), apply B to the intermediate, accept iff the
  result equals the expected answer.
* WIDENING: on exhaustive admitted failure, retry filter-rejected pairs
  once (WIDEN=1 logged). Triggered solely by learner-observed failure.
* SUCCESS-RECORDING: successful trials record kind observations
  (observe/observe2), growing the contracts. The grown contract prunes
  the next query (P5: 7 tries to 4 tries on repeat contact).
* Trial space: {singles, ordered pairs}. Stateless per-query enumeration.
  No modes, no flags, no domain handlers.

U's proven boundary: the diamond (fan-out). COMPOSE-PAIR6-ADV
(2026-10-02, verdict INFORMATIVE-FAIL for U) proved U exhausts its trial
space on one intermediate feeding two consumers (UNI-D Q1: TRIES=14,
ANS=-2, WIDEN=1) because a value produced once can never be consumed
twice in {singles, pairs}.

## 2. What GEN is

GEN is the value-graph generalization of U built in COMPOSE-PAIR6-ADV to
cross U's diamond boundary with no new mechanism, then carried through
GEN-SUBSUMES-U and GEN-STATEFIX (frozen
`gen_statefix/gsf_gen.zag`, sha256
`9d33729e1c2e6dbd6d2fb7de39c84afb99190980e8a0aac58cfbee72171206bb`).

GEN, precisely:

* Rounds over a VALUE POOL (64 entries, seeded with the query start
  value), up to 6 rounds, instead of U's singles-then-pairs enumeration.
  Each round applies every 1-arity MAP to every pool value admitted, then
  every 2-arity MAP to every admitted pool pair. Results are memoized in
  the pool with provenance (which MAP, which inputs). The diamond fork is
  what the value graph does when one value sits in the pool and two
  consumers admit it. No diamond-specific code anywhere.
* OBSERVED-KIND CHECKING instead of U's predicted handshake. Stage 1
  executes the MAP on the actual pool value; stage 2 tests the observed
  value's kind against the contract. The outmask remains learned contract
  state (census-visible, grown by recording) but does not gate pool
  expansion.
* Tried-state tables (tried1/tried2) prevent re-trial within a query.
  GEN-STATEFIX (C406) added the per-query reset of these tables, closing
  the one residual boundary from GEN-SUBSUMES-U (C397): a second query on
  the same arena now re-enumerates the trial space, restoring sequential
  contract growth (P5: ANS=3, TRIES=6, no widening).
* Keeps every U principle unchanged: kind-set contracts, compatibility
  admission, deterministic ordered trial, end-to-end verification
  (result == expected), failure-triggered widening (admission-off phase,
  WIDEN=1 logged once), provenance-based success-recording with contract
  growth. Zero modes, zero bridges, zero handlers, zero new opcodes.

## 3. The subsumption, empirically

GEN's capability set contains U's on every tested arm, and strictly
extends it. All numbers below are from outputs freshly re-verified in
this lane (Section 6): each battery rebuilt from frozen sources with the
pinned znc via safebin, 3 runs, byte-identical to the frozen outputs.

Per-problem answers (U's test battery):

| Problem | U (frozen) | GEN (frozen) | GEN-R (this lane) |
|---------|-----------|--------------|-------------------|
| P1 mixed-kind | 65 | 65 | 65 |
| P2a single-shot | 2 | 2 | 2 |
| P2b misleading contract | 2 | 2 | 2 |
| P3 canonical | 2 | 2 | 2 |
| P5 sequential growth | 3 | 3 | 3 |

Answer-level byte identity: the per-problem ANS sequences are identical
across all three mechanisms. No problem U solves does GEN fail; no
problem U fails honestly does GEN solve spuriously.

Beyond U's battery, GEN additionally covers:

* Q1 (5th pair, spatial-layout x task-scheduling): ANS=1, TRIES=6.
  U's 5th pair, reproduced by GEN on first contact.
* Q2, Q3 (honest failures): ANS=-2 with WIDEN=1 exactly once each.
  GEN fails honestly where U fails honestly; the larger trial space
  introduces no false positives.
* Q4 (fresh learner, all masks empty): ANS=1, TRIES=6. Same as U.
* The diamond (COMPOSE-PAIR6-ADV Q1): GEN ANS=5, TRIES=8; U ANS=-2,
  TRIES=14 after exhausting its trial space. Strict superset, proved.
* P5 sequential contract growth: GEN ANS=3, TRIES=6, no widening,
  riding the grown contract (m0 outmask={1,2}). The C397 residual
  boundary is closed by the C406 tried-state reset.

Contract convergence: the learner-owned kind-set contracts converge to
identical masks under all three mechanisms (census after P5: m0
inmask=1 outmask=3, m1 inmask=1 outmask=2, m2 inmask=1 outmask=1, m3
inmask=1 outmask=2). Only observation counts (n) and the enumeration
differ. The knowledge learned is the same; the trial machinery differs.

## 4. The reduction: U = GEN restricted

U is GEN under three restrictions, each empirically isolated:

(a) SINGLE-ROUND LINEAR POOL. U enumerates in one pass (admitted
    singles, then admitted pairs, then one widening pass), never
    iterating to a fixpoint. Each trial chain is linear: start value,
    at most one intermediate, result. Intermediates are recomputed per
    pair, never memoized or shared across trials, so no value is ever
    consumed twice. This is exactly why the diamond defeats U and why
    GEN's pool (memoized, shared, iterated to quiet) crosses it. The
    restriction is load-bearing for the U-to-GEN direction: GEN-R with
    U's admission still solves P2b with no widening (Section 7),
    proving the pool-rounds trial space does work U's pair space
    cannot, independent of the admission rule.

(b) PREDICTED HANDSHAKE. U admits singles by query-kinds vs masks and
    pairs by the outmask INTERSECTS inmask prediction between the two
    MAPs. GEN checks the observed kind of the actual pool value instead.
    Isolated empirically in this lane by GEN-R (Section 7): the
    predicted handshake is strictly stronger (admits a subset). It
    costs tries on P2a/P3 (forces widening where GEN needs none) and
    it is not load-bearing for solvability: GEN-R keeps ANS parity
    with U on all 5 problems.

(c) STATELESS TRIAL ENUMERATION. U carries no tried-state across
    queries; each query enumerates fresh. GEN's frozen tried1/tried2
    tables violated this until GEN-STATEFIX landed the per-query reset
    (10 lines in gen_solve, C406). With the reset, GEN matches U's
    statelessness exactly: the reset is a no-op on fresh arenas (zero
    regression, K2/K3) and restores P5 growth on reused arenas (K1).

Together: restrict GEN's pool to linear single-pass chains, replace
observed-kind checking with the predicted handshake, keep trial
enumeration stateless per query, and you have U's behavior class. The
composition operation is one; U was its restricted form all along.

## 5. Capability inventory: every U capability, GEN's coverage

| # | U capability (source) | GEN coverage (evidence) |
|---|----------------------|-------------------------|
| 1 | P1 mixed-kind: contract admits what majority-vote rejects (collapse K1) | GEN P1 ANS=65. Observed-kind admits (X,Y) directly, no widening (C397 K1) |
| 2 | P2a single-shot: no coverage gate (collapse K2) | GEN P2a ANS=2. No n>=2 rule anywhere in GEN (C397 K1) |
| 3 | P2b misleading contract: widen, then contract grows (collapse K3) | GEN P2b ANS=2 with NO widening; contract grows identically (census masks match). Strictly better (C397 K1, pair6 K4) |
| 4 | P3 canonical: H1 admission + H2 trace, no mode switch (collapse K4) | GEN P3 ANS=2 via the same X-then-Y route (INTER=34 as U logged) (C397 K1) |
| 5 | P5 sequential growth: admission adapts from experience (collapse K5) | GEN P5 ANS=3, no widening, on the P2b arena (C406 K1) |
| 6 | 5th pair unmodified (pair5 C368) | GEN Q1 ANS=1 on the pair5 world, first contact, same intermediate U found (INTER=213) (C397 K1) |
| 7 | Honest failure, no false positives | GEN Q2/Q3 ANS=-2, WIDEN=1 once each (C397 K2) |
| 8 | Fresh-learner solving | GEN Q4 ANS=1, all masks empty (C397 K3) |
| 9 | Failure-triggered widening | GEN keeps it, generalized: admission-off phase on quiet round (pair6 K5, C397 K2) |
| 10 | Success-recording with contract growth | GEN keeps it, strengthened: provenance-closure recording over the dependency chain (gsf_gen.zag gen_record) |
| 11 | Deterministic ordered trial | GEN: round, MAP-id, pool-index order; 3/3 byte-identical everywhere |
| 12 | End-to-end verification (result == expected) | GEN: unchanged; every admission is verified against exp before acceptance |
| 13 | Kind-set contracts, census-visible | GEN: identical masks learned (Section 3, contract convergence) |
| 14 | Domain-blindness (opaque identifiers) | U proved label-independent (node-relabeling lane: 3 arms byte-identical; domain-blindness lane: ORIG/OPAQUE/PERMUTED byte-identical sha 1f3bbad0). GEN inherits the property: it consults only learned masks and observed kinds, never identifiers. All batteries use opaque integer identifiers throughout. |
| 15 | Diamond/fan-out | U: INFORMATIVE-FAIL (provable). GEN: SOLVES (ANS=5). Strict superset. |

Try-efficiency is explicitly out of scope (GEN trades tries for
generality by design; documented in C397/C406). No U capability is lost;
one (P2b without widening) and the diamond are gained.

## 6. Fresh verification (this lane, pure Zag, safebin)

Every number in Sections 3 and 5 was re-verified from frozen sources.
Toolchain: safebin PATH, pinned znc, `which python3` and `which python`
return nothing, zero forbidden invocations. No em/en dash bytes in lane
docs (byte-verified).

(a) U battery re-verified. Assembled `uc_base.zag + uc_uni.zag`
    (byte-identical to frozen `uc_full_uni.zag`). Fresh binary sha256
    `01fa257124411de079f5104df2f7188b857fa35ff664a3b11ecdd94fe46439c1`,
    byte-identical to the frozen collapse binary. 3 runs byte-identical
    (stdout sha256
    `6f9045116b3e7ccd3004cd6e3b6863df366c798f25c08562a8ec65e497edad30`,
    matching the frozen collapse run digest), stderr empty, and
    byte-identical to frozen `compose_collapse/uni_run1.txt`.

(b) GEN subsumption battery re-verified. Fresh build of frozen
    `gsf_full_gsu.zag`: binary sha256
    `723cc7a3aab0f4659e6ae2abb5b4cc48473f19285869509dc193e5eaa599b2b9`,
    byte-identical to frozen `gsf_bin_gsu`. 3 runs byte-identical
    (stdout sha256
    `c87c18964a6fd9a7554e76c23b96d0c1034c7cd5884afbc3bc9e686024925fad`),
    stderr empty, byte-identical to frozen `gsf_gsu_run1.txt`.

(c) GEN diamond battery re-verified. Fresh build of frozen
    `gsf_full_diamond.zag`: binary sha256
    `f8c9b1c45be7ce8ac25f4f35a23da170785fa32ba1a8715bfe17ca1a16084ea8`,
    byte-identical to frozen `gsf_bin_diamond`. 3 runs byte-identical
    (stdout sha256
    `962ca4f0f65228d92b007b5194852f2778d7b52e583442e8bf687b451bc76f84`),
    stderr empty, byte-identical to frozen `gsf_diamond_run1.txt`.

Bit-reproducible builds across all three batteries: same frozen source
plus the pinned compiler yields byte-identical binaries and outputs.

## 7. Restriction experiment: GEN-R (this lane)

To isolate restriction leg (b), the predicted handshake, I built GEN-R:
the frozen GEN composer with exactly one compile-time parameter change.
`ur_genr.zag` diff vs frozen `gsf_gen.zag` is minimal and audited: a
`ur_predicted()` constant returning 1, kin/kout threaded through
gen_solve, gen_round, gen_m1, gen_cell1, and the 1-app admission rule
switched from observed-kind (`g_khas(mg(A,m,3),gK(A,i))`) to U's
predicted handshake (`g_khas(mg(A,m,3),kin)` and
`g_khas(mg(A,m,4),kout)`). Everything else, rounds, pool, logging,
widening, the C406 tried-state reset, provenance recording, is
untouched. No new mechanism; a configuration, not a redesign.

GEN-R ran on U's exact battery (P1, P2a, P2b, P3 fresh arenas; P5 on the
P2b arena; census), 3/3 byte-identical, stderr empty. Binary sha256
`aacb43633e9ba396727a64b374bca9083ea74861caae3ed559b5d62f296aebc4`.

Results (ANS / TRIES / WIDEN):

| Problem | U | GEN | GEN-R |
|---------|---|-----|-------|
| P1 | 65 / 3 | 65 / 4 | 65 / 4 |
| P2a | 2 / 3 | 2 / 6 | 2 / 10, WIDEN=1 |
| P2b | 2 / 7, WIDEN=1 | 2 / 6 | 2 / 6 |
| P3 | 2 / 3 | 2 / 6 | 2 / 10, WIDEN=1 |
| P5 | 3 / 4 | 3 / 6 | 3 / 6 |

Findings:

* ANS parity holds on all 5 problems. The predicted handshake loses no
  U solution, even inside GEN's different trial space.
* P2b is the decisive decomposition. U needed WIDEN=1 (7 tries) because
  its predicted pair-handshake (X.out INTERSECTS Y.in) rejected the true
  pair under the misleading contract. GEN-R keeps the predicted
  admission but runs GEN's pool-rounds: it solves P2b in 6 tries with NO
  widening, via pool chaining (X on 41 gives 44 in round 1; Y on 44
  gives 2 in round 2). The 1-app predicted admission checks each MAP
  against the query kinds only, never MAP against MAP, so the
  misleading X.out never blocks the chain. Conclusion: it is the trial
  space (pool-rounds vs {singles,pairs}), not the admission rule, that
  does the work on P2b. Restriction leg (a) is load-bearing; leg (b)
  is not.
* P2a/P3 show the cost of leg (b): predicted admission is strictly
  stronger, admits a subset of GEN's trials, and on these problems the
  subset goes quiet, forcing the widening phase (admission-off) to
  recover GEN's route at 10 tries. U avoids this only because its pair
  enumeration re-checks MAP-MAP compatibility per pair rather than
  per-MAP query compatibility per round. A stricter filter with a
  poorer enumeration can beat a looser filter with a richer one on
  tries, while losing on capability. Try-efficiency remains out of
  scope; capability is what retires U.
* P5 sequential growth works under the restriction (ANS=3, no widening):
  the C406 tried-state reset is orthogonal to admission, as designed.
* Census masks identical to U and GEN (Section 3). The learned
  contracts do not depend on which admission rule or enumeration found
  the solution.

## 8. On trace-level byte-identity (honest boundary)

The reduction is proved at the capability level, which is the level at
which mechanism subsumption is claimed in this program. Trace-level
byte-identity between restricted GEN and U does not hold, and the
reason is structural, not a gap in the proof:

* GEN logs every application (INTER=/INTER2=); U logs only pair
  intermediates and its singles phase is silent.
* GEN enumerates (round, MAP-id, pool-index); U enumerates (singles by
  MAP-id) then (ordered pairs by MAP-id).
* GEN memoizes intermediates in the pool (each value computed once,
  consumed many times); U recomputes the first stage per pair.

No parameter restriction turns one enumeration into the other; doing so
would be reimplementing U inside GEN, which proves nothing. What the
empirical record establishes instead, with byte-identical outputs at
every step: identical answers on the full battery, identical learned
contracts, honest-failure parity, fresh-learner parity, sequential
growth parity, and strict superset on the diamond. That is the
subsumption. U's traces remain in the frozen record for reference.

## 9. U as the documented restricted form (historical reference)

U is not deleted from the record. It is reclassified:

* U = GEN restricted to (single-round linear pool, predicted handshake,
  stateless trial enumeration). See Section 4 for the exact mapping.
* The frozen U implementation (`compose_collapse/uc_uni.zag`), its
  battery (`uc_full_uni.zag`), and its outputs (`uni_run1/2/3.txt`,
  binary sha `01fa2571...`) remain canonical for U's historical claims:
  the H1+H2 collapse (SUBSUMPTION verdict), the 5th pair, the P2b
  widening analysis, and the diamond INFORMATIVE-FAIL boundary.
* Any future work that needs "the restricted composition operation"
  should parameterize GEN, not resurrect U. The GEN-R experiment in
  this lane (Section 7) is the template: compile-time restriction
  constants on the frozen GEN composer, diff-audited, battery-verified.
* The H1 and H2 restrictions documented in the collapse report (H1 = U
  with majority-singleton contracts; H2 = U minus the kind filter with
  class-coarsened enumeration) now read as restrictions of restrictions
  of GEN. The chain is H1/H2 < U < GEN, one mechanism at the top.

## 10. Architecture accounting

* Cognition lines added by this retirement: 0. GEN-R's restriction is
  ~15 changed lines in a verification scaffold, not architecture.
* New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
* Mechanisms before: 2 (U, GEN). Mechanisms after: 1 (GEN).
* Researcher-owned: this document, the GEN-R scaffold and driver,
  verification commands. Learner-owned: unchanged (kind-set contracts,
  grown contracts, pool contents per query).
* Pinned znc via safebin throughout; pure Zag; zero
  forbidden-executable invocations.

## 11. References (unambiguous; ledger numbers collide, commits do not)

* COMPOSE-COLLAPSE (U built; H1+H2 SUBSUMPTION):
  `docs/lab/research-lead/overnight-20260928/compose_collapse/`
  (REPORT.md, uc_uni.zag, uc_full_uni.zag, uni_run1/2/3.txt).
* COMPOSE-PAIR6-ADV (GEN built; U INFORMATIVE-FAIL on diamond;
  GENERAL-EXTENSION-EXISTS): lane `lane-composepair6-20261002`,
  implementation commit `82732a9e8`.
* COMPOSE-PAIR5 (U's 5th pair, BUILD-PASS): commits `fcc9b7a80`,
  `b5cb711be`.
* GEN-SUBSUMES-U (PARTIAL; single-query subsumption; P5 boundary
  characterized): `docs/lab/research-lead/overnight-20260928/gen_subsumes_u/`,
  prereg `483243867`, implementation `0ab573658`, verdict `a1a9aefc4`.
  Watchdog-ledger label C397 (collides with canonical CLAIM_LEDGER
  C397 = GPI-3; the commit hashes above are authoritative).
* GEN-STATEFIX (UPGRADE-TO-SUBSUMES; tried-state reset; P5 fixed; zero
  regression; retirement recommended):
  `docs/lab/research-lead/overnight-20260928/gen_statefix/`, prereg
  `c90dabbc9`, implementation `983a46331`, verdict `cd703e8c2`.
  Watchdog-ledger label C406 (collides with canonical CLAIM_LEDGER
  C406 = COGNITIVE-OPS-LEARNER; the commit hashes above are
  authoritative).
* Domain-blindness of U: node-relabeling lane (commit `545b288fd`:
  ORIG/OPAQUE/PERMUTED arms byte-identical) and domain-blindness lane
  (commit `7f5087997`: sha `1f3bbad0` across arms).
* This lane: `docs/lab/research-lead/overnight-20260928/u_retirement/`
  (NAMECHECK.md, ur_genr.zag, ur_main.zag, ur_full_genr.zag,
  ur_genr_run1/2/3.txt + .err, ur_uni_run1/2/3.txt + .err,
  ur_gsu_run1/2/3.txt + .err, ur_diamond_run1/2/3.txt + .err,
  RETIREMENT.md).

## 12. What this does not establish

* Try-efficiency parity (out of scope by design; GEN trades tries for
  generality).
* Behavior on non-pipeline shapes beyond the established diamond.
* The side-effecting-MAP open question (all MAPs in every battery here
  are pure).
* Multi-query reuse beyond one sequential growth step.
* That no future problem will ever want the restricted form as a
  performance optimization; if it does, it should be a parameterized
  GEN configuration (Section 9), not a second mechanism.

## 13. Recommendation (carried from C406, executed here)

U is retired as a separate mechanism, effective this document. GEN is
the single composition mechanism. Future composition work builds on,
restricts, or red-teams GEN. The two-mechanism era (U vs GEN) is over.
