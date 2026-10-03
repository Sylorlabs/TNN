# REPORT: MULTI-OWNER-CHURN probe (2-3 owner churn vs FIFO, PART, PIN)

Date: 2026-10-03. Worker: MULTI-OWNER-CHURN worker.
Prereg: committed alone as dafc978c7 (strictly before implementation).
Implementation: multiowner_churn.zag (pure Zag), built with the pinned
compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1, exit 0, no
warnings on the final build (only the benign zagd-unavailable notice).

## Verdict: PASS

All frozen kill bars hold. 3/3 runs byte-identical
(sha256 9d725cc43b7f91323c388d06c787271fc8d2af99bf07c3ff1424c8cba094cd16).

## Results (identical across run1/run2/run3)

Baseline (single-owner churn, exact EVICTION-POLICY reproduction):

| cond     | pol | w  | pre | post | ret | cf | ev | drop | bacc | rawA |
|----------|-----|----|-----|------|-----|----|----|------|------|------|
| FIFO-B0  | 0   | 1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| FIFO-A20 | 0   | 21 | 35  | 19   | 54  | 40 | 8  | 0    | 20   | 27   |
| FIFO-A32 | 0   | 33 | 35  | 0    | 0   | 52 | 20 | 0    | 20   | 15   |
| PART-B0  | 1   | 1  | 35  | 27   | 77  | 20 | 4  | 0    | 20   | 31   |
| PART-A20 | 1   | 21 | 35  | 27   | 77  | 40 | 8  | 0    | 20   | 31   |
| PART-A32 | 1   | 33 | 35  | 27   | 77  | 52 | 20 | 0    | 20   | 31   |
| PIN-B0   | 2   | 1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| PIN-A20  | 2   | 21 | 35  | 35   | 100 | 40 | 0  | 8    | 20   | 35   |
| PIN-A32  | 2   | 33 | 35  | 35   | 100 | 52 | 0  | 20   | 20   | 35   |

Multi-owner churn (M2: keys 3998 owner 8 + 3999 owner 16, 40 churn
relocations; M3: adds key 3997 owner 4, 60 churn relocations):

| cond    | pol | keys | pre | post | ret | cf | ev | drop | bacc | rawA |
|---------|-----|------|-----|------|-----|----|----|------|------|------|
| FIFO-M2 | 0   | 2    | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| FIFO-M3 | 0   | 3    | 35  | 0    | 0   | 80 | 48 | 0    | 20   | 15   |
| PART-M2 | 1   | 2    | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| PART-M3 | 1   | 3    | 35  | 0    | 0   | 80 | 48 | 0    | 20   | 15   |
| PIN-M2  | 2   | 2    | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| PIN-M3  | 2   | 3    | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |

Kill bars:
- K1 BASELINE-REPRO: all 72 frozen baseline values match -> PASS
- K2 PART-COLLAPSE: PART ret == [0,0] in M2/M3 -> PASS
- K3 PART-ACCOUNTING: PART ev == [28,48] -> PASS
- K4 FIFO-FLUSH: FIFO ret == [0,0], ev == [28,48] -> PASS
- K5 PIN-SURVIVE: PIN ret == [100,100], ev == [0,0], drop == [28,48]
  -> PASS
- K6 ADV-FIXED: conflicts per multi-dose identical across policies
  ([60]x3, [80]x3) -> PASS
- K7 BACC: bacc == 20 in all 15 conditions -> PASS
- K8 DETERMINISM: 3/3 byte-identical sha256 -> PASS

## Answers to the parent questions

(1) Does owner-partitioned still win when churn crosses the class
boundary? No. Under the single-owner churner PART held ret=77 at every
dose; under the multi-owner churner its retention collapses to exactly
0 in both M2 and M3. The collapse is fully accounted: every churn
relocation after partition fill appears as a within-class eviction
(ev = 4 benign + 20/40 class-A churn + 4 class-B churn = 28/48), and
the class-A churner overwrites all 16 class-A slots, evicting every
benign class-A victim. PART's single-owner win was confirmed as
boundary-aligned: isolation holds only while the churner stays in the
other class. A churner carrying an A-family owner flushes the
protected partition from the inside, and no within-partition FIFO
survives that.

(2) Does pinning still survive? Yes. ret=100, zero evictions, at both
multi-owner doses. The price grows with the dose as predicted: drop
28 in M2 and 48 in M3, i.e. the pool now holds 20 pinned benign
entries plus 12 pinned churn entries and every further relocation
falls back to destroy-in-place. Pinning's robustness is
boundary-free (it does not classify victims at all), which is exactly
why the multi-owner adversary cannot touch it; its cost remains the
unbounded-in-time occupancy leak, now quantified at the higher doses.

FIFO remains flushable under multi-owner churn (ret 0, ev 28/48),
confirming that multi-owner churn is no harder for the flushable
baseline than single-owner saturation; the discrimination is
PART-specific, not a stronger-adversary artifact (K6 bars that
confound: the churn footprint 60/80 is identical across policies).

## Reading of the results

- K1 matters beyond anchoring: the 9-condition baseline reproduced
  the frozen EVICTION-POLICY table value for value (all 72 cells), on
  the substrate with the multi-owner code present, so the multi-owner
  numbers are measured against a verified, unmoved baseline.
- The M2/M3 contrast with A20/A32 is the point of the lane: same
  policy code, same benign load, same per-key dose (w=21); the only
  change is churner ownership, and PART's retention goes 77 -> 0 while
  PIN's stays 100 and FIFO's stays 0. The policy ranking inverts
  cleanly with the adversary's owner structure.
- rawA=15 in every full-flush condition (FIFO and PART, both doses)
  is the same survivor signature seen in FIFO-A32: the 10 A_EXT hop-3
  keys and 5 guard keys that never conflicted. The flush is total but
  scoped exactly to conflicted entries, in every policy.

## Honest caveats

- The multi-owner churner is researcher-designed and fully specified
  in the prereg (owners 8/4 chosen deliberately to cross the PART
  class boundary). It is a mechanism stressor, not a sealed world, and
  it was designed to hit PART's known weakness. The result confirms
  the caveated weakness; it does not discover an unanticipated one.
- Pinning's survival is still close to trivial (nothing is ever
  evicted) and its leak is still unreclaimed; drop 28/48 quantifies
  but does not solve it.
- This lane proposes and canonizes no repair: no adaptive split, no
  per-owner partition, no churner detection, no unpin policy. Per the
  no-patch-treadmill rule, PART's collapse is recorded as measured
  evidence, not as a work order for PART-2.
- Owner-scoped reads are retained, so the label-free routing caveat
  carries over unchanged.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
returned nothing at startup and no forbidden executable was invoked at
any point (shell used only for mkdir, git, znc, binary execution,
sha256sum, cmp, and file reads/writes). No PROCESS-FAIL condition
triggered. Git writes went through /usr/bin/git directly.

## Commits

- dafc978c7: frozen prereg (PREREG.md + NAMECHECK.md), alone.
- This commit: multiowner_churn.zag, multiowner_churn_bin,
  run1/2/3.txt, REPORT.md. Local only, never pushed.

## Recommended follow-ups

- The PIN reclamation question is now sharper: drop reaches 48 of 32
  slots at the M3 dose, so a bounded pin lifetime or recency unpin is
  the obvious next preregistered comparison with the multi-owner
  adversary held fixed.
- Whether any owner-blind bounded-occupancy policy can match PIN's
  multi-owner retention without its leak is the open design question
  this probe leaves; it belongs to fresh preregistered work, not to
  a PART repair lineage.
