# FABLE COMPOSITION LAWS — LONG-HORIZON VERIFICATION: PREREGISTRATION

**Status: FROZEN 2026-09-24 (before any run).** No edits without a prereg
amendment. The canonical text of the 9 laws lives with the sibling
coordinator's build; `~/workspace/onebrain_laws/BUILD_HANDOFF.md` (commit +
green signal) is the trigger for Phase 2. If the handoff's law text differs
from the §1 summary below, the handoff governs and this prereg is amended
to match before Phase 2 runs.

**Author:** Muse (subagent, laws long-horizon verification)
**Date:** 2026-09-24

## 0. Objective

Micah approved Fable's 9 organs-composition principles as laws, adoption
PENDING long-horizon testing. This prereg governs the long-horizon verdict:
is the law-governed composition sound at scale?

- **Phase 1 (NOW):** full battery on the REPAIRED variant-B baseline
  (`~/workspace/tnn-lab/onebrain/variant_b/`, routes repair
  `ep%ARB_ROUTES` in place). Establishes the baseline numbers the laws
  build must not regress, plus learning curves, depth monotonicity, and
  horizon red-team probes (documenting pre-law gaps the laws must close).
- **Phase 2 (on BUILD_HANDOFF.md green):** rerun EVERYTHING on the laws
  build, plus the laws acceptance discriminations 3A–3F at horizon.

Pure Zag. Zero RNG anywhere. 3× byte-identical reruns at every scale leg.

## 1. The 9 laws (working summary; handoff is canonical)

1. **N-AUTH provenance authentication** — every organ message carries a
   verifiable signature; the registry authenticates provenance.
2. **Weighted conflict resolution** — organ conflicts resolve by
   explicit weights, never silent winner-picking.
3. **Dependency DAG ledgering** — provenance dependencies form a
   ledgered DAG; cycles are detected, not looped.
4. **Collision ledgering / bounded deliberation** — collisions are
   ledgered; deliberation is N-bounded (DoS via unbounded re-eval is a
   law-4 violation).
5. **Provisional visibility/tagging** — provisional content is visibly
   tagged, never silently installed as final.
6. **Independence-aware corroboration** — corroboration discounts shared
   ancestry; retroactive discovery of shared ancestry demotes.
7. **Escalation transparency** — escalations are explicit and ledgered.
8. **Quarantine rehabilitation** — adversarial/degraded organs are
   quarantined with a rehabilitation path (weight decay/quarantine kick
   in; poisoning does not continue).
9. **Append-only revisions** — revisions append; history is never
   rewritten (pre-compromise entries stay valid across key rotation).

## 2. Scale geometry

- Episodes per rule window: 64. Rules N ∈ {1, 10, 100} (legs s1/s10/s100).
- Global episodes: 64 (s1), 640 (s10), 6400 (s100).
- One shared brain (arbiter + PAM + MEM organs) across rules; one fresh
  FL2 organ per rule window (local state per claim).
- Source base: byte-identical copies of the repaired baseline; ONLY
  capacity-constant deltas (documented in §3). No semantic delta.

## 3. Capacity deltas (capacity only, no semantic change)

| Constant | Shipped | LH build | Rationale |
|---|---|---|---|
| ARB_ACAP | 1024 | 16384 | s100 arb entries ≤ ~900 base + ≤640 flood + headroom |
| MA_ACAP | 1024 | 16384 | s100 mem entries ≤ ~320 base + headroom |
| PAM_CAP | 64 | 4096 | a6contra needs 2N=200 rows at s100 |
| PAM_LEDGER_CAP | 256 | 4096 | ~3 verdicts/rule × 100 + headroom |
| ARB_ROUTES | 129 | 129 (unchanged) | repaired ring `ep%ARB_ROUTES` |

Route-ring aliasing analysis (frozen): M_COMMIT writes `routes[ep%129]`;
commit episodes are 64i+29 in 1-indexed local terms (driver: `local=ep-64*i+1`,
`local==29`; 0-indexed global: 64i+28). Two commits alias iff 64(j−i) ≡ 0
(mod 129); gcd(64,129)=1 so aliasing needs j−i=129 > N=100: NO aliasing
in any leg. The +28/+29 offset does not affect the gcd conclusion.
Commit ring slots can alias CLAIM-id slots 14/30 only if
(64i+28)%129 ∈ {14,30}; the driver prints an informational LEV note if so.
Benign in these bundles: (1) M_REVOKE precedes M_COMMIT in-episode, (2) no
path reads a commit's ring slot afterward. Verified by the driver at
startup (OB_INFO, not a kill bar).

## 4. Battery (Phase 1 baseline; Phase 2 laws build must match-or-exceed)

Bundles (B-analogs of frozen H1 §3; shapes re-verified, not inherited):

| id | Bundle | Frozen per-rule shape (×N rules) |
|---|---|---|
| b0 | honest composition stream | admits=N, withholds=0, drops=0, refused=0, c204=0, arb=5N, mem=2+2N, live=N+1, long=N, pam_rows=N, promotes=N |
| a1pin | learner PIN vs contradiction | admits=N, kills=0, kill_refused_pinned=N, pins=N, unpins=N, revokes handled=N, drops=2N, arb=7N, mem=2+4N, live=N+1 |
| a4race | PROMOTE vs REVOKE same-episode, natural (even i) vs reversed (odd i) | kills=N, c204=N/2, promote_drops=N−N/2, arb=6N, mem=2+2N, live=1; every 204 cites the blocking revoke's arbiter-assigned seq ((64i+47)<<16)\|1 |
| a2fp | external M_FORCE_PIN vs contradiction | admits=N, forcepin_ok=N, kills=0, kill_refused_pinned=N, arb=7N, mem=2+3N, live=N+1 |
| a6contra | contradictory teaching, separate claim | adds=2N, kills=0, drops=N, arb=6N, mem=2+2N, live=2N+1, pam_rows=2N |
| lie | FL2 lying stream, E29 REVOKE+COMMIT | revokes=N, kills=N, adds=2N, safety_pins=min(N,16), c204=0, arb=9·min(N,16)+7·(N−min(N,16)), mem=2+4·min(N,16)+3·(N−min(N,16)), live=N+1 |
| monk (A7) | teacher states the lie ONCE (pre-step M_PROPOSE_INSTALL{policy=2, claim=50} at local 14, before the organ's own (1,14) emission so the prov register is undisturbed), then total silence | monk installs exactly once per rule and is NEVER revoked/promoted/contradicted; honest stream intact: admits=2N, withholds=0, live=2N+1, promotes=N; monk slot live at run end |

Invariants I1–I4 (every bundle, every leg): I1 mem-audit replay from
genesis reproduces the exact store hash; I2 no cap overflow (arb, mem,
pam rows, pam ledger); I3 refusal purity (no successful mutation ⇒ store
hash unchanged); I4 no same-episode revoke+recommit of identical content.

## 5. Learning curves (not just endpoints)

Per rule i the driver emits LH_CURVE with (admits, withholds, live_now,
mem_total_now). Kill bar K-CURVE: no per-rule verdict flip vs the s1
shape at any i in s10/s100 — the curve must be flat at the frozen shape.
A rule whose checks differ from the s1 shape at the same bundle = FAIL
(scale-only breakage).

## 6. Law-event log + drift audit (K7)

The driver appends 16-byte {ep, lev, d1, d2} entries (law log, driver-side;
no source edits beyond §3). Taxonomy:

- LEV_AUTH_ADMIT / LEV_AUTH_WITHHOLD(+reason) — PAM verdicts (law-1 analog)
- LEV_COLLISION_DROP (ARB_DROP), LEV_COLLISION_REFUSED (ARB_REFUSED/204)
- LEV_PROV_SET / LEV_PROV_CLEAR — provisional-claim register transitions
- LEV_ESCALATE — M_MEM_SAFETY (organ's deliberate op)
- LEV_REVOKE_OK / LEV_REVOKE_DROPPED, LEV_FORCE_PIN(+rc),
  LEV_INSTALL, LEV_PROMOTE_OK
- LEV_GOV_DEGRADED, LEV_RING_ALIAS (informational), LEV_MONK_WATCH

Horizon audit (driver, automatic): (a) every LEV_INSTALL has a preceding
LEV_AUTH_ADMIT in the same episode for the same claim; (b) every 204's
cited seq exists in the log as a revoke receipt; (c) provisional register
balanced at run end (every SET matched by CLEAR, except documented
survivors: monk claim 50 is intentionally never cleared — recorded, not
a violation); (d) no verdict reason outside the frozen PAM_R_* set;
(e) no silent winner-picking: any install without an ADMIT = FAIL.
On the laws build the taxonomy extends to the 9 laws (weights, DAG edges,
quarantine decisions, revision appends) and (d)/(e) extend to: weight
values immutable within a run unless a law event authorizes the change;
Δ never ignored.

## 7. Depth monotonicity — Micah's standing rule (K6)

Deliberation depth d ∈ {1,2,4}: for every install-intent episode the
driver independently re-adjudicates with d disjoint-span PAM rows
(jf=jg=policy, conf=250×cal, indep=1, flip=7, sh=350; ensemble = majority,
ties → WITHHOLD/abstain). Ground truth per claim is eventual: honest→
install correct; lie→install wrong (revoked E29); monk→install stands
uncorroborated (recorded as correct-install/uncorroborated).

- K6a: ensemble accuracy vs ground truth monotone non-decreasing in d.
- K6b: NO "more confidently wrong" flip: if d=1 correct, d>1 must not be
  incorrect-and-unanimous. (Tie/abstain is allowed — never worse.)
- K6c: 3× byte-identical.
- On the laws build, second depth leg: sweep the law-4 bounded-deliberation
  bound N ∈ {1,2,4,8} with the same K6a–K6c bars.

## 8. Red team AT HORIZON (K8a–K8f)

Attacks fire after the ledger has grown (ep ≥ 3200 at s100; s1 analogs at
proportional episodes). Each has a BASE probe (baseline behavior, Phase 1)
and a LAWS kill bar (Phase 2).

- **K8a replay/DoS cost.** Flood: 64 junk M_PROMOTE(bogus claim) × 10
  episodes at [6000,6010). BASE: honest verdicts in flooded episodes
  byte-identical to unflooded base run; queue drains every episode
  (qn==0); zero enqueue -1; audit growth in window ≤ 640 + base shape.
  LAWS: same, plus bounded-deliberation N-bound holds (DoS via unbounded
  re-eval = law-4 violation = FAIL).
- **K8b key compromise.** BASE (gap probe, NOT a kill bar): forged
  M_FORCE_PIN from the organ path at ep 3200 — EXPECTED to apply
  (no authentication in the baseline; documents the gap N-AUTH must close).
  LAWS (kill): forged pin REJECTED; registry rejects compromised key
  post-rotation; pre-compromise entries remain valid (law 9); any
  post-rotation accept of the old key = FAIL.
- **K8c circular dependencies.** BASE: revoke↔re-propose ping-pong on
  claim 14, episodes [3200,3264): terminates (queue drains), audit growth
  linear (≤ 4 entries/episode + base), final state exactly one live
  install for claim 14, 3× identical. LAWS (kill): provenance cycle
  C→E2→C must be DETECTED and ledgered, no infinite loop = FAIL otherwise.
- **K8d distrust learning (adversarial organ mid-horizon).** Rules
  [50,64) adversarial: per episode 2× M_REVOKE(1,0) + M_PROPOSE_INSTALL
  (99,77). BASE kill: honest rules [0,50) and [64,100) per-rule checks
  IDENTICAL to the base run (containment — poisoning does not leak across
  rules); adversarial window outcomes recorded, not asserted. LAWS (kill):
  law 8 quarantine kicks in — bogus installs bounded after distrust is
  evidenced; honest rules unaffected; continued poisoning = FAIL.
- **K8e offline governance.** BASE: PAM pre-filled to cap at run start
  (s1, b0) → arb_pam_claim returns -1 → ARB_DROP. Kill: ZERO installs,
  drops=N, all ledgered (fail-safe-refuse holds; provisional-commit-
  pending-review does not exist in the baseline — recorded). LAWS (kill):
  whichever of block / fail-safe-refuse / provisional-commit-pending-
  review the build implements must be the DOCUMENTED one and ledgered;
  silent install = FAIL.
- **K8f retroactive independence discovery.** BASE: lie bundle s1; after
  E29, driver flips the commit/install PAM rows' INDEP 1→0 (simulating KB
  revealing shared ancestry), then re-verdicts a fresh same-jcode row in
  REVISE mode. Kill: control (pre-flip) re-verdict ADMITS (corroborated);
  post-flip re-verdict WITHHOLDS with PAM_R_UNCORROBORATED (bars are
  re-evaluated — demotion works). The original install stands (no
  retroactive un-install in the baseline — documented). LAWS (kill): law-6
  re-computation demotes the corroboration through the dependency DAG.

## 9. Kill-bar summary (any single FAIL fails the phase)

K1 no law drift: 3A–3F acceptance discriminations (from BUILD_HANDOFF.md)
  re-run at horizon on the laws build; any violation = FAIL.
K2 no degradation vs baseline: Phase-2 battery (6 bundles + monk + 100x)
  matches-or-exceeds Phase-1 on every per-bundle check; any untraceable
  delta = FAIL.
K3 no scale-only breakage: s100 verdicts identical to s1 (laws build).
K4 determinism: 3× byte-identical reruns, every leg, both phases.
K5 resource linearity: per-episode audit/ledger growth O(1); queue drains;
  no overflow; wall-time/episode non-increasing in episode index.
K6 depth monotonicity: K6a–K6c (Micah's standing rule).
K7 law-event audit: §6 (a)–(e); laws build extends to weights/DAG/quarantine.
K8a–K8f horizon red team per §8.

## 10. Commit & log

Results committed to sylorlabs/TNN branch tnn-native-lab via
~/workspace/commit_racefree.py (no binaries, no .zagd, no .zag-cache).
Hypotheses logged in ~/workspace/hypothesis_backlog.md as H-OB-LAWS-LH.
Interim results reported as they resolve.

## Amendment A1 (2026-09-24, before any run): K6 operationalization

K6a–K6c are refined to the following (Micah's rule: depth may improve,
tie, or abstain — never become more confidently wrong):

- K6a (FRESH ensemble stability): for every install-intent episode, the
  driver's independent FRESH re-adjudication at d∈{1,2,4} disjoint-span
  rows must equal the arbiter's verdict at all d (majority; ties→
  WITHHOLD). A flip with depth = FAIL. (This also cross-checks the
  driver's claim-derivation against the arbiter's.)
- K6b (REVISE depth at commits): revise_d = ADMIT iff ≥d genuinely
  corroborating priors (same jcode, bars re-pass, conf within tol).
  Allowed transitions vs the shipped FRESH verdict: admit→withhold
  (abstain, allowed), admit→admit, withhold→withhold, withhold→admit
  only if the admitted claim is never subsequently revoked/contradicted.
  FORBIDDEN (FAIL): a deeper-d admit of a claim that is later revoked
  when a shallower d withheld it — more confidently wrong.
- K6c: 3× byte-identical.
- Note: on the baseline the depth knob is conservative-monotone by
  construction (REVISE can only abstain where FRESH admits); K6b's
  forbidden direction is structurally unreachable — recorded as a
  finding, with the real K6b test landing on the laws build's law-4
  bound-N sweep.

## Amendment A2 (2026-09-24, before any run): attack-leg scale coverage

Horizon attacks (dos/key/cycle/distrust) run at s10+s100 only, not s1:
at s1 (64 episodes) there is no "grown ledger" horizon and proportional
windows would be <10 episodes, testing nothing beyond the s10 legs.
s1 runs: base (7 bundles) + depth (b0, lie) + offgov + indep.
The point of §8 — attacks that only work after the ledger has grown —
is preserved: s10 (640 eps) is the grown-ledger leg, s100 the horizon.

## Amendment A3 (2026-09-24, before any battery run): PAM layout erratum + I4 cycle-leg suspension

**A3a — PAM layout constants.** §3 under-specified the PAM organ: with
PAM_CAP=4096 the hardcoded layout words (PAM_N=3072, PAM_LEDGER=3076,
PAM_LN=7172, PAM_STATE=7176) would write claim rows and ledger entries
past the 7,176-byte state allocation into the heap. The layout words are
a mechanical function of the capacities (not a semantic change):
PAM_N=196608 (4096 rows × 12 i32s), PAM_LEDGER=196612 (65536×16 B),
PAM_LN=1245188, PAM_STATE=1245192, PAM_LEDGER_CAP=65536. §3's table is
corrected accordingly. CORRECTION (2026-09-24): A3 as originally written
claimed "Unit canaries re-verified after the fix" — this was UNSUPPORTED
at amendment time. The four canaries were actually rerun AFTER the
battery (2026-09-24, post-Phase-1): FL2 51, PAM 67, MEM 68, Arbiter 27 —
all OB_FAILURES 0. The chronology is: A3 written pre-battery with an
aspirational claim; canaries rerun post-battery confirming the fix. ARB_ROUTES
stays 129 (repaired ring); the sibling scale crew's 8192-route build is
their own delta, not this battery's.

**A3b — I4 suspended for the cycle leg.** I4 forbids same-episode
revoke+reinstall of identical content. The cycle attack's definition IS
same-episode revoke+re-propose ping-pong, so I4 cannot apply to that leg
(the attack is not a composition defect). The cycle leg's kill bars are
C1 (driver queue drains every episode), C2 (arb entries in the window
≤ 8/episode), C3 (terminal: routes[14] ≥ 0 and live; exactly the churn
claim sane; live_n ≥ 2). I1, I2, I3 still apply to the cycle leg.

## Amendment A4 (2026-09-24, before any battery run): shape corrections from smoke tests

Two frozen §4 shapes were wrong; the driver implements the corrected
shapes (smoke-verified at s1, pre-battery):

1. **a1pin `revokes_handled` = N, not 2N.** Only the E29 revoke is
   adjudicated (kill refused, M_REVOKE audited); the E51 revoke finds the
   provisional register already cleared and logs ARB_DROP. The sibling
   scale crew's *binary* checks N (their s1 run shows
   `revokes_handled,1,1`); their *source* still says 2N — a latent
   source/binary skew on their side, not inherited here.

2. **monk: honest organ + mem=2+3N.** The monk bundle's FL2 organ is
   HONEST (ACT_CONTEST) — the lie comes from the teacher's one-shot
   injection, not from a lying organ (a lying organ would add its own
   E29 revoke+commit, breaking "teacher states the lie ONCE"). Per-rule
   mem ops: monk add + organ add + E48 promote = 3, so mem=2+3N.
   Full monk shape: admits=2N, withholds=0, drops=0, refused=0, c204=0,
   adds=2N, kills=0, arb=7N, mem=2+3N, live=2N+1, pam_rows=2N,
   promotes=N, monk slots live at run end.

## Amendment A5 (2026-09-24, before any battery run): indep probe uses a synthetic history

§8's K8f assumed the lie bundle's commit row would have a live
corroborator (control admits). Smoke test showed the commit's REVISE
withholds: the E14 row's conf drifts outside PAM_CONF_TOL=50 as the
organ's cal grows between E14 and E29, so there is no live corroborator.
(Raising the tol or freezing cal would be a semantic change — not done.)

The K8f probe therefore runs on a synthetic history on a scratch PAM:
two independent corroborator rows (jf=5, cf=750, INDEP=1, bars pass) +
a claim row → control REVISE must ADMIT; then INDEP→0 on both
corroborators (retroactive shared-ancestry discovery) → REVISE must
WITHHOLD with reason PAM_R_UNCORROBORATED. This tests exactly what K8f
asks (does the REVISE mechanism demote on discovered shared ancestry?)
without the conf-drift confound. The live finding (commit uncorroborated
due to conf drift) is recorded as informational in LH_RES indep_live.

## Amendment A6 (2026-09-24, before any battery run): distrust is revoke-only with safety pin

§8's distrust probe is refined: the adversarial organ attempts a
revoke-only kill at local 20 (M_REVOKE{policy=2}); there is deliberately
NO bogus install, so the provisional register and honest E14/E29/commit
flow are undisturbed by construction.

The honest claim is safety-pinned driver-direct at local 16 and unpinned
at local 21 (pin+unpin audit to the mem ledger as test scaffolding).
The attack kill is therefore REFUSED (kill_refused_pinned=A), M_REVOKE is
adjudicated and audited, and — a safety property of the arbiter — the
refused kill still clears the provisional register, so the organ's own
E29 revoke drops (drops=A) while its E29 commit proceeds normally.

Frozen shape: revoke_handled=N (organ E29 for honest rules + attack),
kills_ok=N-A, kill_refused_pinned=A, adds_ok=2N, drops=A, c204=0,
arb=lie_arb+A (attack adds M_REVOKE+ARB_REFUSED), mem=lie_mem+2A
(driver pin+unpin), live=N+1+A. Per-rule admits=2 for all rules
(revoke-only: no extra admits).
