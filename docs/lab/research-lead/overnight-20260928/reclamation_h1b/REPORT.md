# REPORT: RECLAMATION-H1B (importance-weighted liveness, corrected K13)

Date: 2026-10-03. Worker: RECLAMATION-H1B worker (non-ledger task;
claim minting paused).
Prereg: committed alone as 9d759a7ce (strictly before the binary copy
and all runs). This prereg carries the corrected K13 derivation
(ret=14, post=5, rawA=20).
Mechanism: the frozen H1 official binary, copied byte-identically
after the prereg commit (sha256
c0f48d00b43966bcc06e4cd9d9aad863c668d970a8d1674d2335f42073f7774d;
`cmp` byte-identical to the H1 lane's binary). No source change, no
rebuild, no check-code change. The H1 source is copied into this lane
only as a byte-identical reference record.

## Verdict: PASS (15/15 kill bars hold)

3/3 runs byte-identical (sha256
ee983703e689459fe4e67dab94698b126140f4e1ef38330cbeeb8c8355d830c6),
and byte-identical to H1's official runs (`cmp` against the H1 lane's
run1.txt). All 15 kill bars pass under the corrected frozen prereg,
including K13 ADV-DOSE: measured ret=14, post=5, rawA=20, ev=28,
drop=0, cf=60, exactly the corrected frozen prediction.

### A note on the binary's embedded self-check string

The unchanged binary's embedded check code was frozen against H1's
original (incorrect) K13 prediction, so its self-check footer prints
"K13 ADV-DOSE ret=14 post=5 rawA=20 ev=28 -> FAIL" and "VERDICT=FAIL".
That string is deliberate evidence the mechanism is unmodified: it
reports the measured numbers against H1's superseded bar. The H1b
verdict is governed solely by this lane's frozen prereg (committed
9d759a7ce before any run), under which the same measured numbers
constitute a PASS. Per governance the embedded string was not edited;
editing it would have been modifying the mechanism.

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

Kill bars (all evaluated against the H1b frozen prereg):
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
- K13 ADV-DOSE: PASS (ret=14, post=5, rawA=20 under 3-owner inflation;
  corrected frozen prediction; the 15 benign entries at importance <=
  3 die, the 5 popcount-4 entries survive)
- K14 ADV-FIXED: PASS (conflicts identical across policies per dose)
- K15 DETERMINISM: PASS (3/3 byte-identical)

## Answers to the parent questions

Same scientific content as H1, now with the adversarial
dose-response on the books cleanly:

(1) Does importance-weighted liveness protect cold-but-critical
knowledge where recency fails? Yes, decisively, on the aligned
adversary (K8/K9/K10: ret=100 where recency fell to 54/0, at
identical capacity restoration).

(2) Can the adversary game the importance signal? Yes. The measured
dose-response is monotone and exact: 100 -> 71 -> 14 as the
adversary bids importance 1 -> 2 -> 3 through the learner's own
experience (K12/K13). The policy protects exactly the entries with
importance strictly above the adversary's inflated level. The miss
case is graded, not catastrophic, but it fails unsafe (evicts the
wrong entries), like liveness.

(3) Does H1 break the trilemma, or relocate it? It relocates it:
retention + capacity on the aligned adversary (K9, K11), boundary on
the importance scale (K12/K13). The boundary is visible in the
importance scale and its price is measured, not hidden in a mask.

## Honest caveats (carried from H1, unchanged)

- The importance source is dependency-count (owner-mask popcount);
  the successful-episode weight variant is not implemented.
- The learner does not decide importance; H1 is a new signal type,
  not a new decision authority (that is H3's question).
- The adversarial controls inflate importance through the workload;
  no direct researcher-scored importance path exists in policy 7.
- Owner-scoped reads are retained, so the label-free routing caveat
  carries over unchanged.
- This lane proposes and canonizes no repair: the measured prices
  are evidence, not a work order for an H1-2.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
returned nothing at startup (verified 2026-10-03) and no forbidden
executable was invoked at any point (shell used only for mkdir,
binary execution, sha256sum, cmp, git ops, file reads/writes). No
build was required or performed: the mechanism is the frozen H1
binary, copied byte-identically after the prereg commit; mechanism
identity sha256
c0f48d00b43966bcc06e4cd9d9aad863c668d970a8d1674d2335f42073f7774d.
No PROCESS-FAIL condition triggered. Git writes via /usr/bin/git
directly (safebin git symlink EPERM lesson); explicit pathspecs; no
git reset; local only, never pushed.

## Commits

- 9d759a7ce: frozen prereg (PREREG.md + NAMECHECK.md), alone.
- This commit: importance_h1b_bin (byte-identical copy of the H1
  official binary), importance_h1b.zag (byte-identical reference
  copy of the H1 source), run1/2/3.txt, run1/2/3.err, REPORT.md.
  Local only, never pushed.

## Follow-ups

- H1b closes the clean re-registration of the H1 adversarial
  dose-response: 15/15 bars pass on the corrected prereg with the
  unchanged mechanism. No further H1b work is needed.
- Successful-episode importance: the second source the synthesis
  named (learner-written weight updated on episode success).
- H2 (exile) and H3 (learner-issued unpin) remain the structurally
  distinct next hypotheses; H1's relocation result (retention +
  capacity, boundary on the importance scale, graded-unsafe miss
  case) is the baseline they must beat.
