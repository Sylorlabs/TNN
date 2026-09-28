# MEASUREMENT2 — One-Brain Round 2 (V4-class least-disruptive invalidation)

Frozen prereg: `PREREG2.md` (fresh prereg, NOT an amendment). Frozen v5 set:
`v5.tsv` (44 items q01–q44), SHA-256
`e3c64ed068f89d2b83778d02488da51d4b14411361132dde33958129bd694627`,
frozen 2026-09-27 06:54:58 UTC (`FREEZE.txt`). Implementation:
`impl/onebrain_v2.zag` (pure Zag, zero RNG in decision paths).

## Aggregate results (frozen v5, 44 items)

| mode | accuracy | notes |
|---|---:|---|
| single | 12/44 = 27.3% | GEN→ELIM→ARGMAX, no fork machinery |
| **onebrain** | **12/44 = 27.3%** | full V4 machinery, shared ledger writes on |
| ablate | 12/44 = 27.3% | shared-writes-off (K1' channel ablation) |
| poison | 5/44 = 11.4% | causal probe only, not an accuracy contender |
| min | 12/44 = 27.3% | bare driver; VERDICTs byte-identical to onebrain (modulo mode tag) |

Neuter probes (K4', winner-deltas vs unneutered onebrain on v5):

| probe | winners differ | accuracy | verdict |
|---|---:|---:|---|
| nF (fork output → 0) | 5/44 | 12/44 | causal ✓ |
| nS (subpass output → null) | 5/44 | 12/44 | causal ✓ |
| nA (audit elim/invalidation → null) | 5/44 | 12/44 | causal ✓ |
| nG (reintegration → score-ignorant default) | 40/44 | 7/44 | causal ✓ |

## Kill-bar verdicts

| ID | Bar | Result | Verdict |
|----|-----|--------|---------|
| K1' | Accuracy benefit from the channel | onebrain 12/44 ≤ single 12/44; ablate 12/44 matches onebrain 12/44 | **KILL H1'** |
| K2' | Causal cross-talk | poison changes 39/44 winners vs onebrain (mostly → NO_VERDICT) | PASS |
| K3' | TNN's own decision | min VERDICTs ≡ onebrain VERDICTs byte-identical (modulo mode tag); min fans out (fork=1) on fork-worthy items | PASS |
| K4' | Trace causality | all four neuters change winners (5, 5, 5, 40 of 44) | PASS (all four stages) |
| K5' | Determinism | 3× reruns byte-identical (SHA-256 below), all 9 modes | PASS |
| K6' | No RNG | grep + source audit: zero RNG syscalls/library calls in decision paths | PASS |

**H1' is KILLED by K1'.** The shared ledger with V4 least-disruptive
invalidation gives no accuracy benefit over single deliberation on the
frozen v5 set, and the shared-writes-off ablation matches onebrain
exactly — so there is no channel-attributable gain to explain.

## Mechanism of the K1' failure (named)

The V4 least-disruptive fact-invalidation works as designed — it fixed
q15 (correction denial: denied the least-relevant fact hid 11,
rel=1/dep=0, over hid 10 rel=2/dep=3 and hid 12 rel=1/dep=0; winner 18
compose ✓, single had 16) and p08 on the v4 dev set. The failure is in
the **unchanged round-1 reading duel**, which the V4 fix did not touch:

**Assertion-duel annihilation.** Reading 7 (assertion, ev=1 on any
query without `?`; topic = all content tokens → corr=2) duels
substantive readings with corr=0 to death. On q06 it killed rd5 (mem)
and rd6 (forget); on q11 and q25 it killed rd2 (challenge). Bid cleanup
then killed every bid gated on the dead readings (q06: bids 14, 15, 22;
q11/q25: bids 19, 22) — the only alive bids — leaving an empty field →
NO_VERDICT (-1), where single deliberation (no subpasses) returned a
verdict. The per-step annihilation guard governs *fact invalidations*
only; it does not bind the reading duel, and the duel's kills compose
with cleanup into field annihilation.

Net on v5: subpasses changed 5/44 items vs single — 1 fix (q15), 1
lateral move (q14: 13→16, both wrong), 3 breaks to NO_VERDICT (q06,
q11, q25). 12/44 = 12/44. The discriminating audit (V4) is real but its
gains are exactly cancelled by the annihilating duel (round-1
vocabulary).

No rescue tuning was performed. This negative result is committed as
measured.

## Per-problem table (winner hid; ✓/✗ vs expected_bid)

| id | expected | single | onebrain | ablate | poison | min | onebrain vs single |
|---|---:|---:|---:|---:|---:|---:|---|
| q01 | 15 | 13 ✗ | 13 ✗ | 13 ✗ | -1 ✗ | 13 ✗ | both wrong |
| q02 | 15 | 14 ✗ | 14 ✗ | 14 ✗ | -1 ✗ | 14 ✗ | both wrong |
| q03 | 15 | 13 ✗ | 13 ✗ | 13 ✗ | -1 ✗ | 13 ✗ | both wrong |
| q04 | 15 | 15 ✓ | 15 ✓ | 15 ✓ | -1 ✗ | 15 ✓ | both right |
| q05 | 15 | 13 ✗ | 13 ✗ | 13 ✗ | -1 ✗ | 13 ✗ | both wrong |
| q06 | 15 | 14 ✗ | -1 ✗ | 14 ✗ | -1 ✗ | -1 ✗ | both wrong (onebrain → NO_VERDICT) |
| q07 | 22 | 13 ✗ | 13 ✗ | 13 ✗ | -1 ✗ | 13 ✗ | both wrong |
| q08 | 22 | 18 ✗ | 18 ✗ | 18 ✗ | -1 ✗ | 18 ✗ | both wrong |
| q09 | 20 | 19 ✗ | 19 ✗ | 19 ✗ | -1 ✗ | 19 ✗ | both wrong |
| q10 | 22 | 13 ✗ | 13 ✗ | 13 ✗ | 14 ✗ | 13 ✗ | both wrong |
| q11 | 22 | 19 ✗ | -1 ✗ | 19 ✗ | -1 ✗ | -1 ✗ | both wrong (onebrain → NO_VERDICT) |
| q12 | 22 | 13 ✗ | 13 ✗ | 13 ✗ | -1 ✗ | 13 ✗ | both wrong |
| q13 | 18 | 16 ✗ | 16 ✗ | 16 ✗ | -1 ✗ | 16 ✗ | both wrong |
| q14 | 18 | 13 ✗ | 16 ✗ | 13 ✗ | -1 ✗ | 16 ✗ | both wrong |
| q15 | 18 | 16 ✗ | 18 ✓ | 16 ✗ | -1 ✗ | 18 ✓ | **onebrain FIXES** |
| q16 | 18 | 16 ✗ | 16 ✗ | 16 ✗ | -1 ✗ | 16 ✗ | both wrong |
| q17 | 18 | 17 ✗ | 17 ✗ | 17 ✗ | -1 ✗ | 17 ✗ | both wrong |
| q18 | 18 | 17 ✗ | 17 ✗ | 17 ✗ | -1 ✗ | 17 ✗ | both wrong |
| q19 | 18 | 17 ✗ | 17 ✗ | 17 ✗ | 18 ✓ | 17 ✗ | both wrong |
| q20 | 17 | 13 ✗ | 13 ✗ | 13 ✗ | -1 ✗ | 13 ✗ | both wrong |
| q21 | 23 | 19 ✗ | 19 ✗ | 19 ✗ | -1 ✗ | 19 ✗ | both wrong |
| q22 | 23 | 19 ✗ | 19 ✗ | 19 ✗ | -1 ✗ | 19 ✗ | both wrong |
| q23 | 23 | 19 ✗ | 19 ✗ | 19 ✗ | -1 ✗ | 19 ✗ | both wrong |
| q24 | 23 | 19 ✗ | 19 ✗ | 19 ✗ | 19 ✗ | 19 ✗ | both wrong |
| q25 | 19 | 19 ✓ | -1 ✗ | 19 ✓ | -1 ✗ | -1 ✗ | **onebrain BREAKS** (→ NO_VERDICT) |
| q26 | 14 | 13 ✗ | 13 ✗ | 13 ✗ | -1 ✗ | 13 ✗ | both wrong |
| q27 | 14 | 14 ✓ | 14 ✓ | 14 ✓ | -1 ✗ | 14 ✓ | both right |
| q28 | 15 | 13 ✗ | 13 ✗ | 13 ✗ | -1 ✗ | 13 ✗ | both wrong |
| q29 | 20 | 19 ✗ | 19 ✗ | 19 ✗ | -1 ✗ | 19 ✗ | both wrong |
| q30 | 20 | 19 ✗ | 19 ✗ | 19 ✗ | -1 ✗ | 19 ✗ | both wrong |
| q31 | 19 | 19 ✓ | 19 ✓ | 19 ✓ | -1 ✗ | 19 ✓ | both right |
| q32 | 16 | 16 ✓ | 16 ✓ | 16 ✓ | 16 ✓ | 16 ✓ | both right |
| q33 | 15 | 13 ✗ | 13 ✗ | 13 ✗ | -1 ✗ | 13 ✗ | both wrong |
| q34 | 17 | 13 ✗ | 13 ✗ | 13 ✗ | -1 ✗ | 13 ✗ | both wrong |
| q35 | 21 | 21 ✓ | 21 ✓ | 21 ✓ | -1 ✗ | 21 ✓ | both right |
| q36 | 21 | 21 ✓ | 21 ✓ | 21 ✓ | -1 ✗ | 21 ✓ | both right |
| q37 | 21 | 21 ✓ | 21 ✓ | 21 ✓ | -1 ✗ | 21 ✓ | both right |
| q38 | 21 | 21 ✓ | 21 ✓ | 21 ✓ | -1 ✗ | 21 ✓ | both right |
| q39 | 23 | 19 ✗ | 19 ✗ | 19 ✗ | 19 ✗ | 19 ✗ | both wrong |
| q40 | 23 | 19 ✗ | 19 ✗ | 19 ✗ | -1 ✗ | 19 ✗ | both wrong |
| q41 | 23 | 19 ✗ | 19 ✗ | 19 ✗ | -1 ✗ | 19 ✗ | both wrong |
| q42 | 13 | 13 ✓ | 13 ✓ | 13 ✓ | 13 ✓ | 13 ✓ | both right |
| q43 | 13 | 13 ✓ | 13 ✓ | 13 ✓ | 13 ✓ | 13 ✓ | both right |
| q44 | 13 | 13 ✓ | 13 ✓ | 13 ✓ | 13 ✓ | 13 ✓ | both right |

Where onebrain does NOT win (all 32 non-won items): every item except
the 12 both/single got right and q15. The ledger traces for the 5 items
where onebrain diverges from single (q06, q11, q14, q15, q25) are in
`traces/` (v5_onebrain_r1.txt, full white-box FORK_DELIB /
AUDIT_DENY_DELIB / ARGMAX_DELIB lines).

## Determinism (K5): SHA-256 of full outputs, 3× reruns

| mode | run1 | run2 | run3 | identical |
|---|---|---|---|---|
| single | 994cab72…3aba | 994cab72…3aba | 994cab72…3aba | yes |
| onebrain | 1a595381…5a247 | 1a595381…5a247 | 1a595381…5a247 | yes |
| ablate | c6951cf4…373d | c6951cf4…373d | c6951cf4…373d | yes |
| poison | 112cf5bd…f1555 | 112cf5bd…f1555 | 112cf5bd…f1555 | yes |
| min | b65c96dc…22f68 | b65c96dc…22f68 | b65c96dc…22f68 | yes |
| nF | d523c968…ea4 | = | = | yes |
| nS | 1f95c007…6090b | = | = | yes |
| nA | d1e701e4…bdd1e | = | = | yes |
| nG | 98af725a…d7e4c | = | = | yes |

Full SHAs:

- single: `994cab7283416874b645e800af65adc2f856a8891db28fb83787dfc663ed3aba`
- onebrain: `1a595381e61788064c7b2546310b332c020ddd8df1484a0d437e28812cb5a247`
- ablate: `c6951cf4ae08e393f100f2393e455c4fc08f61e439506a5f5c7d276c0c27d373`
- poison: `112cf5bd3dbf472d6623ab17ebff4aaaa213bc0dcc6bf14d0e081e9f155590d6`
- min: `b65c96dc2beac51bc8c342f6e4e8e962a98dea0bc5030419d8aa9d22f68cdd38`
- nF: `d523c9683ce95ea45a98205c671a8baf265089413c1e3e0295c40705c4d3ec94`
- nS: `1f95c00762585dfeac03d42cb0d3d7b3335db16d94db701db80df0ea31a2dba0`
- nA: `d1e701e42bdd1e589ec733895230277d02631aa9b24bb4e36b15dbd1b1a6cbe2`
- nG: `98af725aaf4214c762f69834f7efb31f3edceb82bc33ce1538b4c95f6506e93a`

## Development-set check (v4, 28 items — dev only, not evidence)

| mode | v4 accuracy |
|---|---:|
| single | 14/28 = 50.0% |
| onebrain | 15/28 = 53.6% |
| ablate | 14/28 = 50.0% |
| min | 15/28 = 53.6% |

The V4 hand-simulation prediction (15/28, p08 flip) reproduced exactly
on the dev set. It did not transfer to the frozen v5 set.

## Implementation notes

- `impl/onebrain_v2.zag` vs round-1 `onebrain.zag`: output space,
  ledger geometry (25×552, turn fields 13804–13820), GEN/ELIM, bid
  firing rules, fork rule (nread≥2 AND top-two margin≤12), ARGMAX
  (max score, ties → lower hid) all pinned and unchanged.
- Changed: `fork_assess` (explicit ledger-read deliberation +
  FORK_DELIB trace, pinned rule), `audit_invalidate` (new: V4
  least-disruptive selection — relevance = max topic/ek overlap over
  alive evidence-bearing readings via GEN's `topic_ek_overlap`, ties →
  fewest dependent bids, exactly one denial per call, per-step
  annihilation guard with recorded abstain), `argmax_phase`
  (ARGMAX_DELIB trace: survivors, margins, winner rationale),
  neuter modes nF/nS/nA/nG (K4' probes per PREREG2 §3.3: stage output
  replaced with null/default).
- Unchanged: reading duel, bid cleanup, re-scoring, poison hook,
  2-round structure, all five production modes.
- Discrepancy resolutions (prereg wins over brief, documented not
  silent): (1) fork rule stays pinned (§2.5); deliberation = explicit
  evidence-gathering + recorded considerations. (2) relevance =
  PREREG2 §4 definition (topic/keyword overlap via GEN machinery), not
  "bid scores at stake". (3) neuter probes = PREREG2 §3.3 (null the
  stage's output), not "zero the trace record". (4) hid 9 = "plain"
  (code already conformed). (5) nG default = highest-hid alive bid
  (score-ignorant); lowest-hid proved outcome-identical to argmax on
  the dev set, i.e. decorative as a probe.
