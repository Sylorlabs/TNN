# REPORT: PINNING-RECLAMATION comparison (no-reclaim vs LRU vs owner-consent)

Date: 2026-10-03. Worker: PINNING-RECLAMATION worker (non-ledger task).
Prereg: committed alone as 95f9cdab5d (strictly before implementation).
Implementation: pinning_reclamation.zag (pure Zag), built with the pinned
compiler via safebin znc (byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1, 2026.07.0-dev), exit 0,
no code warnings.

## Verdict: PASS

All frozen kill bars hold. 3/3 runs byte-identical
(sha256 7bb4827624fef32ada6e636451638b47db58fcbd90a9ec1b53efc4e538f32738).

## Results (identical across run1/run2/run3)

| cond       | pol | w  | pre | post | ret | cf | ev | drop | bacc | rawA |
|------------|-----|----|-----|------|-----|----|----|------|------|------|
| PINR-B0    | 3   | 1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| PINR-A20   | 3   | 21 | 35  | 35   | 100 | 40 | 0  | 8    | 20   | 35   |
| PINR-A32   | 3   | 33 | 35  | 35   | 100 | 52 | 0  | 20   | 20   | 35   |
| PINLRU-B0  | 4   | 1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| PINLRU-A20 | 4   | 21 | 35  | 19   | 54  | 40 | 8  | 0    | 20   | 27   |
| PINLRU-A32 | 4   | 33 | 35  | 0    | 0   | 52 | 20 | 0    | 20   | 15   |
| PINCON-B0  | 5   | 1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| PINCON-A20 | 5   | 21 | 35  | 35   | 100 | 40 | 8  | 0    | 20   | 35   |
| PINCON-A32 | 5   | 33 | 35  | 35   | 100 | 52 | 20 | 0    | 20   | 35   |

Kill bars:
- K1 BASELINE: pre==35 and bacc==20 in all 9 conditions -> PASS
- K2 NORECLAIM-REPRO: PINR ret==[100,100,100], cf==[20,40,52],
  ev==[0,0,0], drop==[0,8,20] -> PASS (exact parent PIN replica on the
  modified substrate)
- K3 LRU-CAPACITY: PINLRU drop==[0,0,0] -> PASS
- K4 LRU-FIFO-EQUIV: PINLRU ret==[100,54,0], ev==[0,8,20] -> PASS
  (exact parent FIFO dose-response)
- K5 CONSENT-HOLDS: PINCON ret==[100,100,100], ev==[0,8,20],
  drop==[0,0,0] -> PASS
- K6 ADVERSARY-FIXED: conflicts per dose identical across policies
  ([20]x3, [40]x3, [52]x3) -> PASS
- K7 DETERMINISM: 3/3 byte-identical sha256 -> PASS

## Answer to the experimental question

Does reclamation restore capacity without losing robustness?

- No-reclaim pinning (policy 3): perfect robustness (ret=100 at every
  dose, zero evictions) but the leak is confirmed on the new substrate:
  drop=[0,8,20], i.e. 8 then 20 relocations fall back to
  destroy-in-place at r=20 and r=32. K2 reproduces the parent PIN row
  bit-for-bit, so the baseline is anchored.
- LRU reclamation (policy 4): restores capacity completely (drop=0 at
  every dose, K3) but loses the robustness pinning was bought for.
  Retention falls to exactly the flushable FIFO dose-response,
  ret=[100,54,0] with ev=[0,8,20] (K4): the LRU row is bit-for-bit the
  parent FIFO row. This is not a coincidence the experiment stumbled
  into; it was the preregistered sharp prediction. Under an adversary
  that churns never-re-read keys after benign teaching, recency cannot
  separate dead churn history from live benign entries: last-touch
  order equals placement order equals the FIFO bump order, so
  minimum-last-touch eviction strikes the same entries FIFO would.
  The genuine-LRU machinery (last-touch stamped on placement and on
  pool read hits) is implemented, but no pool reads occur during the
  churn phase, so recency degenerates to arrival. The price of LRU
  reclamation here is total: it converts pinning back into FIFO.
- Owner-consent reclamation (policy 5): gets both. Capacity is fully
  restored (drop=0 at every dose) and robustness is untouched
  (ret=[100,100,100], rawA=35 at every dose, K5). The 8 and 20 churn
  relocations that pinning dropped are instead reclaimed from the
  adversary's own pinned churn history (ev=[0,8,20]), because the
  consent mask (owner 16) admits only churn-owned entries and every
  benign victim carries an A-family bitmask that never intersects it.

Head to head: reclamation without a reliable liveness signal (LRU here)
is strictly worse than no reclamation at all against this adversary,
it pays pinning's implementation cost for FIFO's outcome. Reclamation
with an ownership signal restores capacity for free on retention, but
its consent boundary aligns with the single-owner churn adversary, the
same alignment caveat the parent lane recorded for PART.

## Reading of the results

- K2 matters beyond anchoring: the modified substrate (new header
  fields, touch side table, read-stamp logic) reproduces the parent PIN
  row exactly, so the LRU and CONSENT numbers are measured against a
  verified replica, not a re-derived baseline.
- K4 is the money result and the sharpest discrimination in the lane:
  the prediction was not "LRU loses some retention" but exact
  FIFO-equivalence, derived from the protocol timing (no pool reads
  during churn). Hitting it bit-for-bit is evidence the mechanism is
  understood, not just observed.
- K6 bars the natural confound: the adversary's footprint (conflict
  counts 20/40/52 per dose) is identical across all three reclamation
  regimes, so the retention differences are policy effects.
- The discrimination design worked as preregistered: K2 anchors;
  K3 vs K2 shows LRU kills the leak; K4 vs K2 shows LRU pays the full
  robustness price (exact FIFO collapse); K5 vs K3/K4 separates consent
  from LRU (both reclaim, only consent keeps ret=100).

## Honest caveats

- The consent mask (16) aligns with the churn adversary's owner, just
  as the parent PART class boundary did. Consent wins partly because
  the owner who can release entries is the owner doing the churning.
  A multi-owner churn adversary (owners who do not consent, or consent
  masks that do not cover the churner) would test whether consent
  generalizes; that probe needs its own prereg.
- LRU is tested with churn interleaved strictly after benign teaching
  and with no pool reads during churn. A protocol that re-reads benign
  entries during the churn phase would differentiate recency from
  arrival and could rescue LRU; not tested here.
- The churn adversary is a mechanism stressor on the reclamation rule,
  not a sealed world and not a claim about realistic learner behavior.
  Owner-scoped reads carry over the parent caveat unchanged.
- Per the no-patch-treadmill rule, this lane does NOT canonize a
  reclamation policy. Each regime carries a measured price; choosing
  between them (or designing liveness signals beyond owner consent)
  belongs to fresh preregistered work.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
returned nothing at startup and no forbidden executable was invoked at
any point (shell used only for mkdir, znc, binary execution, sha256sum,
cmp, and file reads/writes). No PROCESS-FAIL condition triggered.
grep audit: no negated-conjunction while conditions in the new code.
Per the 2026-10-03 shared-workspace lesson, git writes went through
/usr/bin/git directly with explicit pathspecs; no git reset.

## Commits

- 95f9cdab5d: frozen prereg (PREREG.md + NAMECHECK.md), alone.
- This commit: pinning_reclamation.zag, pinning_reclamation_bin,
  run1/2/3.txt, REPORT.md. Local only, never pushed.

## Recommended follow-ups

- Multi-owner churn adversary against PIN-CONSENT: the current K5 PASS
  rests on the consent mask aligning with the churner's owner.
- Benign re-reads interleaved during churn against PIN-LRU: the
  protocol timing that collapses LRU to FIFO is a stated condition,
  not a law; find the read pattern that rescues recency.
- Liveness signals beyond owner consent (e.g. read-recency with
  benign refresh, bounded pin lifetime, learner-issued unpin): the
  learner-owned version of "who decides an entry is dead" is the
  continuing-learner form of this question.
