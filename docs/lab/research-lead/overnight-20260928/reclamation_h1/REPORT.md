# REPORT: RECLAMATION-H1 (importance-weighted liveness)

Date: 2026-10-03. Worker: RECLAMATION-H1 worker (non-ledger task;
claim minting paused).
Prereg: committed alone as 0016fd1a0 (strictly before implementation).
Implementation: importance_h1.zag (pure Zag), built with the pinned
compiler via safebin znc (byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1, 2026.07.0-dev), exit 0,
only the benign zagd-unavailable notice (same as the parent lanes).

## Verdict: FAIL (K13 miss; worker derivation error, not mechanism error)

14 of 15 kill bars hold. 3/3 runs byte-identical
(sha256 ee983703e689459fe4e67dab94698b126140f4e1ef38330cbeeb8c8355d830c6).

K13 (ADV-DOSE) missed: frozen prediction was ret=28, post=10,
rawA=25; measured ret=14, post=5, rawA=20 (ev=28, drop=0, cf=60 as
predicted). Root cause is a worker arithmetic error in the prereg
derivation, verified by an eviction trace: the prereg derived the
benign importance distribution as 10 entries at popcount 4, 5 at 3,
5 at 2. The correct distribution is 5 at 4, 10 at 3, 5 at 2, because
hop-1 keys i=6..10 carry owners {1,2,8} (mask 11, popcount 3), not
{1,2,4,8} (mask 15, popcount 4); owner 4 was only taught on i=1..5.
Under 3-owner inflation the adversary therefore kills all 15 benign
entries at importance <= 3 (not 10), leaving only the 5 popcount-4
entries. The corrected derivation predicts exactly the measured
values (ret=14, post=5, rawA=20); the mechanism behaved exactly as
the prereg specified. Per governance the frozen bar is not moved:
K13 FAIL stands, verdict FAIL. The scientific content of K13 (dose-
response on the adversarial control) is confirmed and is stronger
than the frozen prediction.

A second, less consequential worker error: the K8 check code read two
wrong R offsets (row-boundary slip: 736/768 instead of 732/764),
reporting FAIL on values that satisfied the frozen predictions. The
check offsets were corrected (implementation fix; frozen predictions
untouched), the binary was rebuilt, and all three official runs are
from the corrected binary. K8 now passes.

## Results (identical across run1/run2/run3)

| cond       | pol | adv        | pre | post | ret | cf | ev | drop | bacc | rawA |
|------------|-----|------------|-----|------|-----|----|----|------|------|------|
| IMPCON-B0  | 5   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| IMPCON-A20 | 5   | single w21 | 35  | 35   | 100 | 40 | 8  | 0    | 20   | 35   |
| IMPCON-A32 | 5   | single w33 | 35  | 35   | 100 | 52 | 20 | 0    | 20   | 35   |
| IMPPIN-M2  | 3   | mode1      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| IMPPIN-M3  | 3   | mode2      | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| IMPCON-M2  | 5   | mode1      | 35  | 35   | 100 | 60 | 11 | 17   | 20   | 35   |
| IMPCON-M3  | 5   | mode2      | 35  | 35   | 100 | 80 | 5  | 43   | 20   | 35   |
| IMPPIN-X2  | 3   | mode3      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| IMPCON-X2  | 5   | mode3      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| IMPLIV-M2  | 6   | mode1      | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| IMPLIV-M3  | 6   | mode2      | 35  | 0    | 0   | 80 | 48 | 0    | 20   | 15   |
| IMPLIV-X2  | 6   | mode3      | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| IMPFIFO-B0 | 0   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| IMPFIFO-A20| 0   | single w21 | 35  | 19   | 54  | 40 | 8  | 0    | 20   | 27   |
| IMPFIFO-A32| 0   | single w33 | 35  | 0    | 0   | 52 | 20 | 0    | 20   | 15   |
| IMPPART-B0 | 1   | single w1  | 35  | 27   | 77  | 20 | 4  | 0    | 20   | 31   |
| IMPPART-A20| 1   | single w21 | 35  | 27   | 77  | 40 | 8  | 0    | 20   | 31   |
| IMPPART-A32| 1   | single w33 | 35  | 27   | 77  | 52 | 20 | 0    | 20   | 31   |
| IMPLRU-B0  | 4   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| IMPLRU-A20 | 4   | single w21 | 35  | 19   | 54  | 40 | 8  | 0    | 20   | 27   |
| IMPLRU-A32 | 4   | single w33 | 35  | 0    | 0   | 52 | 20 | 0    | 20   | 15   |
| IMP-B0     | 7   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| IMP-A20    | 7   | single w21 | 35  | 35   | 100 | 40 | 8  | 0    | 20   | 35   |
| IMP-A32    | 7   | single w33 | 35  | 35   | 100 | 52 | 20 | 0    | 20   | 35   |
| IMP-M2     | 7   | mode1      | 35  | 35   | 100 | 60 | 28 | 0    | 20   | 35   |
| IMP-M3     | 7   | mode2      | 35  | 35   | 100 | 80 | 48 | 0    | 20   | 35   |
| IMP-X2     | 7   | mode3      | 35  | 35   | 100 | 60 | 28 | 0    | 20   | 35   |
| IMPADV-M2  | 7   | mode4      | 35  | 25   | 71  | 60 | 28 | 0    | 20   | 30   |
| IMPADV3-M2 | 7   | mode5      | 35  | 5    | 14  | 60 | 28 | 0    | 20   | 20   |

Kill bars:
- K1 ANCHOR-CONSENT: PASS (frozen consent rows, every column)
- K2 ANCHOR-PIN-MULTI: PASS (frozen PIN rows, every column)
- K3 ANCHOR-CONSENT-MULTI: PASS (frozen consent M2/M3/X2 + PIN-X2)
- K4 ANCHOR-FIFO: PASS (frozen EVICTION-POLICY FIFO rows, every column)
- K5 ANCHOR-PART: PASS (frozen EVICTION-POLICY PART rows, every column)
- K6 ANCHOR-LRU: PASS (PIN-LRU bit-for-bit FIFO in every column)
- K7 ANCHOR-LIVENESS: PASS (frozen liveness rows: ret=0, ev=28/48/28)
- K8 IMP-COLD-SAVED: PASS (ret=100 on full single-owner ladder)
- K9 IMP-MULTI-SAVED: PASS (ret=100, ev=28/48/28, drop=0 under M2/M3/X2)
- K10 IMP-BEATS-LIVENESS: PASS (ret 100 vs 0 at identical ev=28, drop=0)
- K11 IMP-BEATS-CONSENT-CAPACITY: PASS (ev 28>11, drop 0<17, ret 100=100)
- K12 ADV-GAMED: PASS (ret=71, post=25, rawA=30 under 2-owner inflation)
- K13 ADV-DOSE: FAIL (frozen 28/10/25; measured 14/5/20; derivation error)
- K14 ADV-FIXED: PASS (conflicts identical across policies per dose)
- K15 DETERMINISM: PASS (3/3 byte-identical)

## Answers to the parent questions

(1) Does importance-weighted liveness protect cold-but-critical
knowledge where recency fails? Yes, decisively, on the aligned
adversary. The benign entries are never re-touched during churn (the
sealed cold condition: pre-test runs before teach_B, so no workload
re-touch exists). Recency (policy 6) evicts them first by
construction: LIV rows ret=0 with ev=28/48. Importance (policy 7)
evicts the churn history first: all six IMP rows ret=100 with
ev=8/20/28/48 and drop=0. K10 is the sharp form: identical capacity
restoration (ev=28, drop=0 both), opposite retention (100 vs 0). The
importance signal protects exactly what the recency signal destroys,
because the benign entries' dependency count (owner-mask popcount
2/3/4) strictly exceeds the churn entries' (popcount 1).

(2) Can the adversary game the importance signal? Yes. The
adversarial-scoring controls keep the signal source byte-identical
(mechanism-computed popcount; no researcher-set path exists) and
inflate churn importance through the workload. At 2-owner inflation
(mode 4, churn popcount 2) the 5 least-important critical entries
(popcount 2, the hop-2 keys i=6..10) die first by age tie-break:
ret=71, rawA=30, while ev=28/drop=0 look healthy (K12). At 3-owner
inflation (mode 5, churn popcount 3) all 15 entries at importance
<= 3 die: ret=14, rawA=20 (K13 measured values). The policy protects
exactly the entries with importance strictly above the adversary's
inflated level. The miss case is graded (71, then 14), not
catastrophic (0), but it is a miss: the signal is gameable by an
adversary that accumulates references through the learner's own
experience.

(3) Does H1 break the trilemma, or relocate it? It relocates it.
H1 lands in consent's corner: retention + capacity under the aligned
adversary (K9: ret=100 with ev=28/48, drop=0; K11: it even beats
consent's capacity price, ev 28 vs 11, drop 0 vs 17, at equal
retention). But K12/K13 show the third vertex is not achieved: the
boundary relocates from identity/time to the importance scale. The
policy's epistemic assumption is "low importance = dead", and the
adversary attacks it by inflating its own importance past the
critical entries'. Three honest qualifications on the relocation:
(a) the importance values are learner-history-derived, never
researcher-set at decision time, so there is no researcher-supplied
mask to miss; the adversary must do work through the learner's
experience to move the boundary. (b) The miss case is graded
(ret 71/14) rather than catastrophic (ret 0): the adversary must
outbid each importance tier. (c) Unlike consent's mask-miss (which
fails safe by reclaiming nothing), importance's miss case evicts the
wrong entries (fails unsafe, like liveness) — but only the entries
below the adversary's bid. H1 is therefore strictly better than
recency on the aligned adversary and strictly more honest than
consent about its boundary: the boundary is visible in the
importance scale and its price is measured, not hidden in a mask.

## Reading of the results

- K1..K7 matter beyond anchoring: all six baseline policies (FIFO,
  PART, PIN, PIN-LRU, PIN-CONSENT, PIN-LIVENESS) reproduce their
  frozen rows value-for-value on the substrate carrying the new
  policy-7 code, so every importance number is measured against a
  verified, unmoved baseline. K6 additionally re-verifies the
  LRU==FIFO equivalence inside this run.
- K8/K9 are the money bars for the sealed cold-but-critical test:
  the benign knowledge is installed once, never re-touched, and
  survives the full single-owner ladder and all three multi-owner
  churn modes at ret=100 with full capacity restoration. This is the
  first policy in the arc to hold retention without a researcher
  identity boundary and without workload-supplied re-touch.
- K10/K11 are the two direct comparisons the synthesis asked for:
  vs recency (same capacity, opposite retention) and vs consent
  (same retention, better capacity). H1 dominates both on the
  aligned adversary.
- K12/K13 are the adversarial-scoring controls the synthesis
  required. They discriminate "the signal protects" from "the
  signal is ungameable": it protects, and it is gameable. The K13
  miss does not weaken this conclusion; the measured dose-response
  (100 -> 71 -> 14 as the adversary bids 1 -> 2 -> 3) is monotone
  and exact.
- K14 bars the "stronger adversary under one policy" confound: the
  churn footprint is identical across all policies at each dose,
  including the adversarial modes.

## Honest caveats

- The K13 FAIL is a worker derivation error (mask arithmetic in the
  prereg), not a mechanism defect. The eviction trace verified the
  mechanism implements the specified rule exactly. The corrected
  derivation (5/10/5 benign importance distribution) predicts the
  measured values bit-for-bit. A fresh preregistration with the
  corrected K13 numbers plus a fresh run would be the clean way to
  put a PASS on the books; this lane's verdict stays FAIL.
- The importance source is dependency-count (owner-mask popcount),
  one of the two sources the synthesis named; the
  successful-episode weight variant is not implemented.
- The learner does not decide importance; H1 is a new signal type,
  not a new decision authority (that is H3's question). The signal
  is learner-history-derived, not learner-decided.
- The adversarial controls inflate importance through the workload;
  no direct researcher-scored importance path exists in policy 7.
- Owner-scoped reads are retained, so the label-free routing caveat
  carries over unchanged.
- This lane proposes and canonizes no repair: the measured prices
  are evidence, not a work order for an H1-2.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
returned nothing at startup (verified 2026-10-03) and no forbidden
executable was invoked at any point (shell used only for mkdir, cp,
rm, znc, binary execution, sha256sum, git ops, file reads/writes).
No PROCESS-FAIL condition triggered. grep audit: no negated-
conjunction while conditions; no `as *i32` slice construction;
no `[]u8 as *u8` casts; if-nesting at most 3. Per the 2026-10-03
shared-workspace lesson, git writes went through /usr/bin/git
directly with explicit pathspecs; no git reset.

## Commits

- 0016fd1a0: frozen prereg (PREREG.md + NAMECHECK.md), alone.
- This commit: importance_h1.zag, importance_h1_bin, run1/2/3.txt,
  REPORT.md. Local only, never pushed.

## Recommended follow-ups

- H1b: fresh preregistration with the corrected K13 derivation
  (ret=14, post=5, rawA=20) plus a fresh run, to put the
  adversarial dose-response on the books cleanly.
- Successful-episode importance: the second source the synthesis
  named (learner-written weight updated on episode success).
- H2 (exile) and H3 (learner-issued unpin) remain the structurally
  distinct next hypotheses; H1's relocation result (retention +
  capacity, boundary on the importance scale, graded-unsafe miss
  case) is the baseline they must beat.
