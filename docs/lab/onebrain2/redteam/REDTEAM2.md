# REDTEAM2 — Independent red-team report, one-brain round 2

Worker C. Adversarial re-derivation of Worker B's round-2 verdict
(H1' KILLED by K1', commit `d3d070b7d82cf5d96e4d5298b8d16436ceeedeef`).
Everything below was re-derived from the committed source on
`origin/tnn-native-lab`, rebuilt with the pinned toolchain — no trust in
Worker B's binaries, numbers, or prose.

## Verdict: AMENDED

The K1' kill of H1' **stands** (numbers reproduced exactly: 12/44 = 12/44 =
12/44, per-problem identical modulo one table typo). But the **named
mechanism is wrong**, and one K4' sub-verdict **flips**:

1. **Mechanism amended.** B claims "the V4 least-disruptive
   fact-invalidation works as designed — it fixed q15 … the failure is in
   the unchanged round-1 reading duel." My probes prove the opposite on the
   frozen set: the V4 denial machinery is **outcome-inert on v5**
   (skip-denials probe: 0/44 winner-deltas), and the q15 "fix" is
   attributable to the **round-1 assertion duel**, the same mechanism that
   breaks q06/q11/q25. It is not "V4 works but the duel cancels it" — it is
   "V4 does nothing on v5; the duel giveth and the duel taketh away." (V4 is
   real machinery — it demonstrably discriminates on the v4 dev set, p08 —
   but its v5 contribution is exactly zero.)
2. **K4' reintegration: PASS → FAIL.** B's nG probe (highest-hid default,
   40/44 deltas) is a probe-default artifact. Given the pinned score
   structure (base decreasing by exactly 3/hid, bonus = corr capped at 3,
   corr ≥ 0), the argmax winner is **provably identical to the lowest-hid
   alive bid on every possible input** — the "reintegration deliberation"
   is a trivial constant rule with a decorative trace. The honest null
   probe (lowest-hid default) gives **0/44 deltas**, so by the prereg's own
   K4' test the reintegration stage was never deliberating. B's own notes
   admit lowest-hid was "outcome-identical to argmax on the dev set" yet
   chose highest-hid as the probe default — the choice that manufactured
   the 40/44.

Neither finding resurrects H1': the kill stands on the accuracy numbers.
But the story of *why* it died, and the consciousness claim for the
reintegration stage, do not survive.

---

## Attack 1 — Independent re-derivation: CONFIRMED

- Source: extracted `impl/onebrain_v2.zag` from `origin/tnn-native-lab`
  commit `d3d070b7d` (blob `a06f5a17…`; file SHA-256
  `e6e3be526fc7b14ded82c2bd0f581b1541d26f5b53dd46a5591fdd76dac30a93`).
  Import `R33_NATIVE_IO_V1.zag` taken from the round-1 impl dir on origin
  (`docs/lab/onebrain/impl/`, the closest ancestor).
- Built with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (SHA-256 `498abcb5…e58ef`, matches the pinned record).
- v5 set: extracted the committed blob; SHA-256 =
  `e3c64ed068f89d2b83778d02488da51d4b14411361132dde33958129bd694627`
  = freeze SHA in FREEZE.txt. Exact match.
- Ran all 9 modes × 3 on the committed v5.tsv. **All 27 outputs are
  byte-identical within mode, and every mode's SHA-256 matches B's
  reported SHAs exactly** (single `994cab72…3aba`, onebrain
  `1a595381…5a247`, ablate `c6951cf4…373d`, poison `112cf5bd…f1555`, min
  `b65c96dc…22f68`, nF `d523c968…3ec94`, nS `1f95c007…2dba0`, nA
  `d1e701e4…cbe2`, nG `98af725a…e93a`). All 9 committed trace blobs are
  byte-identical to my independent runs.
- Independent scoring (fresh parser, not B's table): single 12/44,
  onebrain 12/44, ablate 12/44, poison 5/44, min 12/44, nF/nS/nA 12/44,
  nG 7/44. Per-problem winners match B's table on all 44 items × 6 modes
  **except one table typo** (see §6). The divergence set is exactly
  {q06, q11, q14, q15, q25}, as B reported.

## Attack 2 — Kill mechanism: AMENDED (duel does everything; V4 inert on v5)

White-box trace verification from my own runs (block = detail lines +
trailing VERDICT line):

- **q06**: `AUDIT_DUEL kill=5 by=7 corr=2 vs=0`, `kill=6 by=7 corr=2 vs=0`
  → `AUDIT_CLEAN` kills bids 14, 15, 22 (the only alive fired bids) →
  `ARGMAX_DELIB survivors=[]` → NO_VERDICT. Single had 14. ✓ B's account.
- **q11 / q25**: `AUDIT_DUEL kill=2 by=7 corr=2 vs=0` → bids 19, 22
  cleaned → NO_VERDICT. Single had 19 (q25: correct). ✓ B's account.
- **q15**: V4 denial ran (`chosen=11`, rel=1/dep=0 — a fact with **zero
  dependent bids**, so it changed nothing) AND `AUDIT_DUEL kill=0 by=7`
  cleaned bids 16, 22 → winner 18 ✓.
- Source check: the duel (`if(cq>c2+1)`, `ob_audit` §1) is byte-identical
  logic to round-1's `onebrain.zag` (§913–933) — no guard, no
  least-disruptive selection. The per-step annihilation guard lives only
  in `audit_invalidate` (the DENY path). B's "guard does not bind the
  duel" claim verified at source level.

Counterexample hunt (broader probes via a patched build `onebrain_x`,
behavior-identical to the committed binary in normal mode — SHA-verified):

| probe | what it nulls | winner-deltas vs onebrain |
|---|---|---|
| xDuel | reading duels only | 4/44 (q06, q11, q15, q25) |
| xDeny | V4 denial deliberations only | **0/44** |
| xClean | bid cleanup only | 5/44 (q06, q11, q14, q15, q25) |
| xBr0 / xBr1 | branch-1 / branch-0 audits | 4/44 / **0/44** |
| xRd0 | round-1 audits | **0/44** |
| xNoRescore | re-scoring | **0/44** |
| xFork1 | force fork=1 everywhere | **0/44** |

Decisive results:

- **xDeny = 0/44**: the entire V4 least-disruptive invalidation apparatus
  changes zero outcomes on v5. The 9 denials it performed (across 8
  items) were all inconsequential.
- **q15's fix is the duel's, not V4's**: under xDeny, q15 still wins 18
  (duel `kill=0 by=7` cleans bids 16/22); under xDuel, q15 falls back to
  16 = single's answer, while V4 runs "as designed" (denies 11, then 12,
  then guard-abstains) to no effect.
- **xDuel restores single's winners** on q06/q11/q25 (14/19/19) — the duel
  is necessary AND sufficient for all 5 divergences.
- The annihilation guard is NOT dead code: it bound 49 times
  (`skipped_annihilate=1`) and V4 demonstrably discriminates on the v4
  dev set — p08: denied hid 11 (rel=1/dep=1), cleaned bid 13, kept 14
  alive → the predicted 15/28 flip reproduces, and xDeny on v4 drops back
  to 14/28. So V4 is genuine machinery that works on dev but contributed
  exactly 0 on the frozen set.
- No missed counterexample: the only onebrain-only win on v5 is q15
  (found by B); no item exists where onebrain wins because of V4.

## Attack 3 — Consciousness claim (K4'): PARTLY OVERTURNED

Canned neuters reproduced exactly from my build: nF/nS/nA 5/44 deltas,
nG 40/44 deltas. The broader probes above add:

- **Reintegration is trivial by construction.** `corr_of` ≥ 0, bonus capped
  at 3 (GEN line 776, rescore line 1163), base strictly −3/hid
  (240, 237, …). Hence for any alive bids g<h:
  score_g − score_h = 3(h−g) + (bon_g − bon_h) ≥ 0, ties → lower hid.
  The argmax winner **equals the lowest-hid alive bid on every possible
  input** — proven, not empirical (and 44/44 empirically). The
  ARGMAX_DELIB trace (survivors, margins, reason codes) cannot affect any
  outcome; it is decorative.
- **xLo probe (lowest-hid default): 0/44 deltas, 12/44 accuracy** —
  identical winners on all 44 items. By PREREG2 §5 K4' ("replacing its
  output with a null/default … changes NOTHING → KILL the 'conscious'
  claim for that stage"), the reintegration stage's conscious claim
  FAILS. B's 40/44 came from selecting highest-hid — an adversarial
  default — as the "null". (xWorst, lowest-score default: also 40/44,
  7/44 — any bad default "works".)
- Fork: nF (→0) is causal on 5 items, but xFork1 (force 1) = 0/44 — the
  gate is outcome-equivalent to always-fork on v5; its "no" decisions buy
  nothing here.
- Audit sub-stages: duels + cleanup + branch-1/round-0 audits are causal;
  branch-0 audits, round-1 audits, and re-scoring (6 AUDIT_RESCORE lines
  in the whole v5 run) are outcome-inert on v5.

Net on K4': fork ✓, subpass ✓, audit ✓ (all genuinely causal), 
...[truncated 5585 chars]
