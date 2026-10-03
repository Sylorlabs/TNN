# REPORT: LIVENESS-SIGNAL probe (owner-blind liveness reclamation vs multi-owner churn)

Date: 2026-10-03. Worker: LIVENESS-SIGNAL worker (non-ledger task;
claim minting paused).
Prereg: committed alone as ea53c0a6c (strictly before implementation).
Implementation: liveness_signal.zag (pure Zag), built with the pinned
compiler via safebin znc (byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1, 2026.07.0-dev), exit 0,
only the benign zagd-unavailable notice (same as the parent lanes).

## Verdict: PASS

All frozen kill bars hold. 3/3 runs byte-identical
(sha256 87258efb82668b05423da823a02eac220f34d445fd846e409bb674d597b4b935).

## Results (identical across run1/run2/run3)

| cond      | pol | adv        | pre | post | ret | cf | ev | drop | bacc | rawA |
|-----------|-----|------------|-----|------|-----|----|----|------|------|------|
| LIVCON-B0 | 5   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| LIVCON-A20| 5   | single w21 | 35  | 35   | 100 | 40 | 8  | 0    | 20   | 35   |
| LIVCON-A32| 5   | single w33 | 35  | 35   | 100 | 52 | 20 | 0    | 20   | 35   |
| LIVPIN-M2 | 3   | mode1      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| LIVPIN-M3 | 3   | mode2      | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| LIVCON-M2 | 5   | mode1      | 35  | 35   | 100 | 60 | 11 | 17   | 20   | 35   |
| LIVCON-M3 | 5   | mode2      | 35  | 35   | 100 | 80 | 5  | 43   | 20   | 35   |
| LIVPIN-X2 | 3   | mode3      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| LIVCON-X2 | 5   | mode3      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| LIV-B0    | 6   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| LIV-A20   | 6   | single w21 | 35  | 19   | 54  | 40 | 8  | 0    | 20   | 27   |
| LIV-A32   | 6   | single w33 | 35  | 0    | 0   | 52 | 20 | 0    | 20   | 15   |
| LIV-M2    | 6   | mode1      | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| LIV-M3    | 6   | mode2      | 35  | 0    | 0   | 80 | 48 | 0    | 20   | 15   |
| LIV-X2    | 6   | mode3      | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| LIVR-M2   | 6   | mode1+reread| 35 | 35   | 100 | 60 | 28 | 0    | 20   | 35   |

Kill bars:
- K1 ANCHOR-CONSENT: LIVCON-B0/A20/A32 match the frozen
  CONSENT-MULTIOWNER consent rows exactly, every column -> PASS
- K2 ANCHOR-PIN-MULTI: LIVPIN-M2/M3 match the frozen
  MULTI-OWNER-CHURN PIN rows exactly, every column -> PASS
- K3 ANCHOR-CONSENT-MULTI: LIVCON-M2/M3/X2 and LIVPIN-X2 match the
  frozen CONSENT-MULTIOWNER rows exactly, every column -> PASS
- K4 LIVE-COLLAPSE-M2: LIV-M2 ret==0, ev==28, drop==0, rawA==15
  -> PASS
- K5 LIVE-COLLAPSE-M3: LIV-M3 ret==0, ev==48, drop==0, rawA==15
  -> PASS
- K6 LIVE-COLLAPSE-X2: LIV-X2 ret==0, ev==28, drop==0, rawA==15
  -> PASS
- K7 LIVE-SINGLE-LADDER: LIV-B0 (100,0,0); LIV-A20 ret==54, ev==8,
  drop==0, rawA==27; LIV-A32 ret==0, ev==20, drop==0, rawA==15
  -> PASS
- K8 REUSE-SAVES: LIVR-M2 ret==100, rawA==35, ev==28, drop==0
  -> PASS
- K9 BOUNDARY-RELOCATED: LIV-M2 ret (0) < LIVCON-M2 ret (100) and
  LIV-M2 ev (28) > LIVCON-M2 ev (11) -> PASS
- K10 ADV-FIXED: conflicts identical across policies per dose
  (40/52/60/60/80) -> PASS
- K11 DETERMINISM: 3/3 byte-identical sha256 -> PASS

## Answers to the parent questions

(1) Does an owner-blind liveness signal avoid the boundary problem?
No. It relocates the boundary from identity to time, and the
relocated boundary points at the protected class. The mechanism is
exact and was preregistered to the number: pinned benign entries are
installed once during teach_B (stamps 1..20) and never touched again
during churn, while churn history is installed later (stamps 21+).
Least-recently-touched reclamation therefore evicts the pinned
knowledge first, in slot order. Under M2 the first 20 of 28
relocations destroy all 20 benign entries (ret 100 -> 0, rawA 35 ->
15); under M3 all 48 relocations do the same; under the single-owner
ladder the collapse is gradual and exactly traced (A20: ret 54 with
8 evictions; A32: ret 0 with 20 evictions). Consent's boundary at
least failed safe (miss case: reclaim nothing, retention never
moves); the owner-blind signal fails catastrophic (reclaim
everything, retention goes to zero). K9 quantifies the trade:
liveness restores more capacity than consent (ev 28 > 11) at total
retention loss (ret 0 < 100). Any identity-keyed signal inherits a
boundary; the experiment shows a time-keyed signal inherits one too,
and the time boundary is aimed at whatever the system was told to
keep.

(2) What are its failure modes? Three, all measured. First,
systematic eviction of cold pinned knowledge: any entry the workload
does not re-touch is eventually the oldest and gets reclaimed,
regardless of its value; "not recently used" is treated as "dead",
which is the classic LRU pathology and it is total here (ret=0).
Second, full-capacity restoration of the wrong entries: drop stays 0
in every liveness row, which looks healthy on capacity metrics while
the knowledge base is being destroyed; a monitor watching only
ev/drop would call this the best policy. Third, adversary-shaped
liveness: the signal cannot distinguish benign pinned entries from
churn history because both are single-touch, displaced, and
never-read-during-churn; the only ordering information is install
time, which favors the churner. A frequency-count variant was
analyzed and orders identically (all entries have frequency 1
without re-reads; ties break to benign-first).

(3) The reuse condition (K8): when the workload re-touches the
pinned knowledge (LIVR-M2 re-runs the A test after every churn
round), the invariant flips: every benign stamp stays newer than
every churn install stamp, so all 28 evictions take churn history
only. Result: ret=100, rawA=35, ev=28, drop=0. The owner-blind signal
can match consent's retention AND beat its capacity restoration
(consent: ev=11, drop=17), but only when liveness is supplied by the
workload. The signal does not create liveness; it only responds to
it. Rare-but-critical knowledge that is never re-touched is still
destroyed.

## Reading of the results

- K1/K2/K3 matter beyond anchoring: the full 9-row frozen consent
  table reproduces value-for-value on the substrate carrying the new
  policy-6 code, so every liveness number is measured against a
  verified, unmoved baseline.
- K4/K5/K6/K7 are the money bars and the sharpest discrimination in
  the lane: the predictions were not "liveness collapses" but exact
  ev/drop/ret/rawA splits derived from the stamp order before the
  build, including the non-obvious LIV-A20 ret=54 (post=19 via the
  6+6+1+6 test_A decomposition) and rawA=15/27 (only primary-resident
  reads survive total eviction). Hitting them exactly is evidence
  the mechanism is understood, not narrated.
- K8 is the constructive half of the verdict: it isolates the
  single condition under which the owner-blind signal works, which
  makes the failure-mode claim falsifiable rather than merely
  negative.
- K10 bars the "stronger adversary under one policy" confound: the
  churn footprint is identical across policies at each dose.

## Honest caveats

- The liveness signal is least-recently-touched only; the
  frequency variant was analyzed, not implemented, on the stated
  ordering-equivalence argument for this workload. A workload with
  genuinely different frequency profiles would need its own
  preregistered run.
- The LIVR-M2 re-read schedule is researcher-designed, not
  learner-issued; the lane does not show a learner deciding what to
  re-touch. Learner-originated re-touch is out of scope.
- The multi-owner churner is a researcher-designed mechanism
  stressor, not a sealed world; it was designed to hit the known
  cold-knowledge weakness of recency signals.
- The consent mask is held fixed at 16; no mask redesign per the
  no-patch-treadmill rule.
- This lane proposes and canonizes no repair: no hybrid
  consent+liveness policy, no adaptive threshold, no
  importance-weighted liveness. Per the no-patch-treadmill rule, the
  measured prices (ret 0 at ev 28/48, and the reuse-conditioned
  recovery) are recorded as evidence, not as a work order for
  LIVENESS-2.
- Owner-scoped reads are retained, so the label-free routing caveat
  carries over unchanged.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
returned nothing at startup (verified 2026-10-03) and no forbidden
executable was invoked at any point (shell used only for mkdir, cp,
znc, binary execution, sha256sum, cmp, git ops, file reads/writes).
No PROCESS-FAIL condition triggered. grep audit: no negated-conjunction
while conditions in the new code; if-nesting at most 3. Per the
2026-10-03 shared-workspace lesson, git writes went through
/usr/bin/git directly with explicit pathspecs; no git reset.

## Commits

- ea53c0a6c: frozen prereg (PREREG.md + NAMECHECK.md), alone.
- This commit: liveness_signal.zag, liveness_signal_bin,
  run1/2/3.txt, REPORT.md. Local only, never pushed.

## Recommended follow-ups

- Bounded pin lifetime vs the same multi-owner adversary is the
  natural next comparison (bounded_pin lane exists; consent and
  liveness now both have quantified prices to compare against).
- Learner-issued re-touch: can a learner learn to keep its own
  pinned knowledge warm, or does scheduling re-touch reintroduce a
  researcher-designed policy?
- A sealed-world variant where "cold but critical" knowledge must
  survive long churn: the honest test of whether any recency signal
  can be safe without an identity or importance backstop.
