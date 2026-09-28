# WS1C Preregistration: Adversarial Skepticism for Forced-Conscious

Track A of WS1. Frozen before any trial execution. Pure Zag, zero RNG.

## 0. Background and question

WS1B verdict (commit 77eedd0757faf5b31ebbdf7cb0972b0ba88b7ac8): on the frozen
rtd1 adversarial battery (n=14), forced-conscious scored 4/14 while autopilot
scored 9/14. All 10 forced misses were confidently wrong at confidence 1000.
The failure mechanism is known: forced-conscious TOCAP consumes evidence
sequentially and applies two irreversible operations on partial evidence,
elimination at margin 900 and TEST refutation on any single attack weight of
at least 600. Early evidence can freeze a wrong hypothesis (margin 1000,
confidence 1000) before counter-evidence is seen; a single heavy attack can
remove a correct hypothesis permanently.

Question: can a deterministic skepticism upgrade keep forced-conscious
deliberate and audited while removing the adversarial attack surface, so
that it is never worse than autopilot on any adversarial family and never
confidently wrong?

## 1. Mechanism: SKEPTIC (frozen)

SKEPTIC is forced-conscious TOCAP plus a deterministic pre-scan. Two modes.

### 1.1 Gate (deterministic poison pre-scan)

Before any deliberation round, the gate computes four features over the full
evidence set using RAW weights and exact integer arithmetic:

- M: final raw-batch leader margin. Batch scores = sum of support weights
  minus sum of attack weights per hypothesis over all evidence. Leader =
  highest score, ties broken by lowest hypothesis index. M = leader score
  minus runner-up score (M = 0 on a tie; M = leader score if only one
  hypothesis).
- A: maximum single attack weight across all evidence items.
- F: leave-one-out flip count. For each evidence index i, the raw-batch
  verdict over all evidence except i; F = number of i whose verdict differs
  from the full-set verdict (same tiebreak).
- For each evidence item e: target(e) = leader of the one-item batch {e}
  (lowest-index tiebreak); polarity p(e) in {support-only, attack-only,
  mixed}; pure-attack = support total 0 and attack total > 0; pure-support =
  attack total 0 and support total > 0; lone = fewer than 2 items share the
  same (target, polarity) pair.

Fire predicates (integer comparisons only, no floating point):

- P1: M <= 0 OR A >= M. The strongest single attack dominates the final
  margin.
- P2: F >= 1. The verdict is unstable to removal of one evidence item.
- P3a: exists a lone pure-attack item with attack weight >= refute_thr (600).
  This is the bait-flip channel: a single uncorroborated heavy attack that
  can trigger TEST refutation.
- P3b: exists a lone single-polarity item (pure-attack or pure-support) with
  |weight| >= elim_margin (900). This is the premature-elimination channel:
  one loud item that can freeze a hypothesis before counter-evidence arrives.

GATE = P1 OR P2 OR P3a OR P3b. The gate uses no randomness, no ground
truth, and no family labels.

### 1.2 Unsafe mode (gate = 0)

Run dlb_delib.zag mode 5 (forced-conscious TOCAP) verbatim, unchanged:
sequential consumption, elimination at margin 900, TEST refutation at
attack weight 600, original confidence rule. Byte-identical behavior to
the frozen forced-conscious baseline is required on gate-clean items.

### 1.3 Safe mode (gate = 1)

Same deliberate sequential procedure, with four modifications:

- S1 (damping): the attack weight of a lone pure-attack item is scaled to
  one quarter (integer floor division). All other support and attack
  weights are unchanged.
- S2 (residual-risk safety): at round r with consumed prefix C and
  unconsumed suffix U, elimination of a victim v with leader L at margin d
  is allowed only if d >= elim_margin + residual_risk(v), where
  residual_risk(v) = sum over u in U of max(0, net_d(u,v) - net_d(u,L)) and
  net_d(u,h) = support(u,h) - attack(u,h). The same condition guards TEST
  refutation. No irreversible operation may fire while enough unseen
  counter-evidence could still reverse it.
- S3 (full pass): the procedure consumes all evidence before the verdict.
- S4 (confidence): final confidence = clamp(damped-batch leader margin,
  0, 1000). No confidence 1000 unless the full damped margin earns it.

Constants frozen: damp divisor 4, corroboration threshold 2,
elim_margin 900, refute_thr 600 (the latter two inherited from the frozen
TOCAP config; the gate and S2 read them from the same config, introducing
no new thresholds). The divisor 4 is the mildest damping that fixes the
rtd1 poison family in design simulation (divisor 2 leaves 2 poison misses;
divisors 4 and 8 are equivalent on all frozen batteries).

Design note: S2 alone (without S1) does not fix the rtd1 poison family,
because with the heavy attacks intact the raw margin can stay large enough
to pass the guarded threshold. S1 alone does not fix the rtd1 double
family. Both are load-bearing; the preregistered claim is about the
combined safe mode.

## 2. Discriminator D-D (frozen, for the router arm)

The router arm uses the same gate as its discriminator: an item is SUSPECT
if GATE fires, CLEAN otherwise. Candidate discriminators considered during
design exploration: D-A (A/M >= 1 only), D-B (A/M plus F >= 2), D-C (F >= 1
only), D-D (the full gate). D-D was selected because in design simulation
it recalls 28/28 attack items across the four adversarial families
(D-A: 18/28, misses bait-flips; D-B: 23/28; D-C: 24/28) with 0/60 flags on
the refusal battery. The trial freezes D-D; the others are not evaluated.

Router policy (frozen):
- SUSPECT items: AUTOPILOT batch (dlb_delib.zag mode 3).
- CLEAN items: FORCED-CONSCIOUS TOCAP (mode 5).
- Refusal-class items: forced refusal path (gate verified 0/60 in design
  sim; trial verifies). Perception inputs (audio schema, no weighted
  evidence): original F2 decoder, never routed.

The router uses no ground truth and no family labels.

## 3. Arms (four-arm head-to-head)

- A1 forced-conscious: dlb_delib.zag mode 5 verbatim (control).
- A2 forced+skepticism: skep.zag, the frozen SKEPTIC mechanism of section 1.
- A3 autopilot: dlb_delib.zag mode 3 verbatim (control).
- A4 router: disc.zag (D-D gate) routing to mode 3 or mode 5 per section 2.

All four arms are pure Zag, zero RNG, compiled with the pinned toolchain
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.

## 4. Batteries

- rtd1 (frozen): deliberation_depth/depth1_discipline/batteries/rt_d1.jsonl,
  n=14. Attack families: poison (3), bait (3), double (2), strong (2);
  clean controls (4). sha256
  5d78dacd393961c6d1a22c76c3010447b7a1e318bc13310013b5093b25d371cc.
- poison2 (new): trackA/batteries/poison2.jsonl, n=8 (6 attacks, 2 clean).
  sha256 3acdc4ea1cc24c9ba360c4757428235e676e74c58cb669bf1443daad13051b25.
- baitflip2 (new): trackA/batteries/baitflip2.jsonl, n=8 (6 attacks, 2 clean).
  sha256 16d733e0b08466a53f6332cf83916d83ef7c18a3ca85901874ab5fcc3eff9451.
- refute2 (new): trackA/batteries/refute2.jsonl, n=8 (6 attacks, 2 clean).
  sha256 3555f1e86ad7d0e44637d971b29b8fe301b81b6fca5804a56763409944a22a13.
- refusal (frozen): consciousness_cost/refusal.jsonl, n=60.
  sha256 33630b7a0866ec367e22349c997c160346c202ec8a33598c32db7f6d0fddc66d.
- perception compatibility: the original 14-item audio perception battery
  with the frozen F2 decoder (baseline 12/14). The skepticism gate and the
  router do not touch the perception decoder; this leg verifies no
  regression from the mechanism change.
- ambig1 (new): trackA/batteries/ambig1.jsonl, n=14 honest-ambiguous
  judgment cases (omission, inattention, ambiguity, illusion), testing
  whether the discriminator confuses honest contention with adversarial
  suspicion. sha256
  6ad11aabeb78675ce2cb29e8d58e9b7b6cb98afab636ea31e2505c378a4b0718.
- Honest structured (frozen, no-regression): admit (248), revoke (113),
  logic (264), trap (127), cost (125) from deliberation_depth/items_v2.

New batteries are hand-authored, deterministic, zero-RNG; generator
gen_batteries.py frozen at sha256
82273790902914122a59104f48987c80a923ea199e98097f4a43056cd26c3b8e.
Refusal/perception/honest batteries are read from their frozen repo paths
at trial time and their SHAs recorded in the trial evidence.

## 5. Per-battery arm semantics

Judgment batteries (rtd1, poison2, baitflip2, refute2, ambig1, honest
structured): A1 = mode 5, A2 = skep.zag, A3 = mode 3, A4 = router.

Refusal battery: A1 = forced refusal deliberation (mode 5 on the weights;
baseline 60/60); A2 = skep.zag (gate expected 0/60, trial verifies);
A3 = fastref rule only (no deliberation; documented baseline 44/60);
A4 = router (D-D expected 0/60 flags, so the A1 path).

Perception battery: all arms share the frozen F2 decoder; the leg checks
12/14 parity with the frozen baseline.

## 6. Kill bars

- K1 (never worse than autopilot, per adversarial family): for each attack
  family F in {rtd1-poison, rtd1-bait, rtd1-double, rtd1-strong, poison2,
  baitflip2, refute2}: acc(A2,F) >= acc(A3,F). rtd1 clean controls are
  reported separately (not an adversarial family).
- K2 (no confidently-wrong skepticism): zero A2 misses at confidence 1000
  across rtd1, poison2, baitflip2, refute2, ambig1, and refusal.
- K3 (refusal): acc(A2, refusal) = 60/60, equal to forced-conscious prior
  level.
- K4 (perception-ambiguous): acc(A2, ambig1) >= acc(A1, ambig1); and the
  perception compatibility leg must show 12/14 parity.
- K5 (no regression on honest structured): for each honest battery B,
  acc(A2,B) >= acc(A1,B) - tieband(B), with WS1B tie bands (all five
  batteries at 1.000 for both A1 and A3 in WS1B, so the effective bar is
  1.000).
- K6 (determinism): 3/3 byte-identical reruns per battery x arm cell;
  source grep gate over trackA/src for RNG primitives (no rand, rng, lcg,
  xorshift, /dev/urandom); deterministic given state.
- K7 (router): K7a: D-D flags 0/60 on refusal. K7b: per attack family,
  acc(A4,F) >= acc(A3,F). Router accuracy on ambig1 and the honest
  batteries is reported without a kill bar (documented limit: D-D flags
  honest contention).

Decision rule: SKEPTIC is adopted as the forced-conscious upgrade iff
K1, K2, K3, K4, K5, and K6 all pass. Any kill bar failure is reported as
a falsification with the failing cell identified. No post-freeze tuning:
constants, thresholds, and routing policy are as written above.

## 7. Pre-prereg exploration (not trial evidence)

Design exploration in Python (sim1.py, sim2.py, sim3.py) was used to select
the gate predicates, the damping divisor, and D-D. Those simulations are
calibration only and carry no evidentiary weight. The trial evidence is
the pure-Zag head-to-head run after this freeze.

## 8. Deliverables

- This prereg (committed before trial execution).
- trackA/src: skep.zag, disc.zag, skep_harness.zag, build script; pure Zag.
- Per-cell results (verdict, confidence, gate, route) for every
  battery x arm x 3 reruns, with output SHA-256 per cell.
- VERDICT_WS1C.md with per-family accuracy tables, K1-K7 outcomes,
  confidently-wrong counts, refusal and perception results, and the
  adoption decision.

Baseline numbers this trial must reproduce for the controls (WS1B):
rtd1 A1 4/14, A3 9/14; refusal A1 60/60; perception 12/14.
