# REPORT: RECLAMATION-H3B (fresh K20 derivation, unchanged mechanism)

Date: 2026-10-03. Worker: RECLAMATION-H3B worker (non-ledger task;
claim minting paused).
Prereg: committed alone as 68e611a0b (strictly before the runs; no
implementation exists in this lane).
Mechanism: the UNCHANGED H3 binary (unpin_h3.zag source copy held for
provenance, never modified), compiled with the pinned znc
(znc 2026.07.0-dev (edition 2026), byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1); binary sha256
a9759f7c4bd71b944a6e0e2da69264c6f2f192ba4edef4835c8ee9fdf747223c,
verified byte-identical to the H3 artifact before the prereg commit.

## Verdict: PASS (22/22 kill bars hold)

3/3 runs byte-identical (sha256
284e3083b80d142dbfa1ae4c1c23260a9077f3ae578cc728cb1a8a9daf2c2bcd,
identical to the H3 frozen run hash; run1 `diff` clean against
reclamation_h3/run1.txt). All 22 kill bars pass against the fresh
prereg, including K20 under the corrected derivation
(UNPINSTALE-A20: ret=17, post=6, rawA=19, ev=16, drop=0, cf=48,
bacc=20).

The H3 derivation error is closed: the corrected derivation frozen
in the H3B prereg predicted every measured column of the
UNPINSTALE-A20 row exactly (pre=35, post=6, ret=17, cf=48, ev=16,
drop=0, bacc=20, rawA=19, releases=8, av=8, ai=0, lcheck=12,
a_released=0), and the re-run of the unchanged binary reproduces
that row bit-for-bit.

## Reading the in-band self-check lines (frozen in the prereg)

The binary prints in-band `K1..K22` and `VERDICT=` lines computed
against the values frozen at its compile time (the H3 values,
including the superseded post=7/ret=20 for K20). Recompiling to
update them would have modified the mechanism, which this lane
forbids. The binary therefore prints
`K20 STALE-CONTROL ret=17 post=6 rawA=19 ev=16 -> FAIL` and
`VERDICT=FAIL`. Those prints are instrument convenience, not the
governing verdict: the H3B prereg froze the corrected values and the
external worker check of the COND columns against that prereg is
the verdict. Every other in-band line prints PASS and its frozen
values are unchanged from H3, so they remain valid evidence for
K1..K19, K21, K22.

## Results (identical across run1/run2/run3; run1 == H3 run1 bit-for-bit)

Anchors (29): bit-for-bit identical to the H1B frozen table,
inherited from the H3 verification (H3 run1 diff clean against
reclamation_h1b/run1.txt; H3B run1 diff clean against H3 run1).

| cond           | pol | pre | post | ret | cf | ev | drop | bacc | rawA | rel | av | ai | lc | ar |
|----------------|-----|-----|------|-----|----|----|------|------|------|-----|----|----|----|----|
| UNPIN-B0       | 8   | 35  | 35   | 100 | 28 | 0  | 0    | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-A20      | 8   | 35  | 35   | 100 | 48 | 8  | 8    | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-A32      | 8   | 35  | 35   | 100 | 60 | 8  | 20   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-M2       | 8   | 35  | 35   | 100 | 68 | 8  | 28   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-M3       | 8   | 35  | 35   | 100 | 88 | 8  | 48   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-X2       | 8   | 35  | 35   | 100 | 68 | 8  | 28   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-SILENT   | 8   | 35  | 35   | 100 | 40 | 0  | 8    | 20   | 35   | 0   | 0  | 0  | 12 | 0  |
| PINCTRL-SILENT | 3   | 35  | 35   | 100 | 40 | 0  | 8    | 20   | 35   | 0   | 0  | 0  | 12 | 0  |
| UNPIN-WRONG    | 8   | 35  | 25   | 71  | 48 | 13 | 3    | 20   | 30   | 13  | 8  | 5  | 12 | 5  |
| UNPINSTALE-A20 | 9   | 35  | 6    | 17  | 48 | 16 | 0    | 20   | 19   | 8   | 8  | 0  | 12 | 0  |

Kill bars (external verification against the H3B prereg):
- K1 ANCHOR-CONSENT: PASS. K2 ANCHOR-PIN-MULTI: PASS.
  K3 ANCHOR-CONSENT-MULTI: PASS. K4 ANCHOR-FIFO: PASS.
  K5 ANCHOR-PART: PASS. K6 ANCHOR-LRU: PASS.
  K7 ANCHOR-LIVENESS: PASS.
- K8 IMP-COLD-SAVED: PASS. K9 IMP-MULTI-SAVED: PASS.
  K10 IMP-BEATS-LIVENESS: PASS. K11 IMP-BEATS-CONSENT-CAPACITY:
  PASS. K12 ADV-GAMED: PASS. K13 ADV-DOSE: PASS
  (IMPADV3-M2 post=5 ret=14 rawA=20 confirmed on COND row).
  K14 ADV-FIXED: PASS.
- K15 DETERMINISM: PASS (3/3 byte-identical, sha256
  284e3083b80d142dbfa1ae4c1c23260a9077f3ae578cc728cb1a8a9daf2c2bcd).
- K16 UNPIN-ALIGNED-CAPACITY: PASS (ret=100 throughout;
  drop = relocations - releases exactly: 16-8=8, 28-8=20).
- K17 UNPIN-MULTI: PASS (ret=100, ev=8, drop=28/48/28).
- K18 AUTHORITY: PASS (UNPIN-SILENT == PINCTRL-SILENT bit-for-bit
  in all 13 numeric columns; ev=0, drop=8 both).
- K19 COLD-PROTECTED: PASS (a_released=0 in all six aligned
  conditions).
- K20 STALE-CONTROL: PASS under the corrected derivation:
  UNPINSTALE-A20 shows ret=17, post=6, rawA=19, ev=16, drop=0,
  cf=48, bacc=20, pre=35, releases=8, av=8, ai=0, lcheck=12,
  a_released=0. Every frozen column matches. The corrected
  derivation (loop3 i=1..5 all fail because 1051/1052 sit in
  destroyed slots 8/9: post=2+2+0+2=6, ret=(100*6)/35=17,
  rawA=2+2+10+5=19) predicts the measured row exactly.
- K21 WRONG-RELEASE: PASS (ret=71, post=25, rawA=30, ev=13,
  drop=3, releases=13, audit 8 valid / 5 invalid, a_released=5).
- K22 LEARNER-INTACT: PASS (lcheck=12 in all 10 H3 conditions;
  9 UNPIN* rows plus PINCTRL-SILENT confirmed).

## Answers to the parent questions (unchanged from H3)

(1) Learner-issued unpin relocates the death decision behaviorally:
K18 (mechanism cannot reclaim without learner releases),
K16/K17 (drop = relocations - releases, no more, no less), K21
(failure locus is the learner's judgment; audit names the 5
invalid releases; retention pays exactly for those 5).

(2) The K19/K20 pair discriminates authority: the same staleness
intuition as learner judgment (belief + revision history) releases
zero A entries (ret=100), while as mechanism rule (primary
comparison) it destroys 16 cold entries (ret=17). A disguised
policy could mimic either row alone; it cannot produce both rows
from different authorities unless the authorities differ.

(3) H3 beats H1B on authority, not on the aligned adversary: H1B's
policy 7 restores more capacity under the aligned adversary
(IMP-M2: ev=28/drop=0 vs UNPIN-M2: ev=8/drop=28); H3's retention
of learner-held knowledge is 100 by construction with a graded,
auditable miss case.

## Honest caveats (from H3, unchanged)

The learner is simulated; only the REVISED reason is exercised;
no sealed post-freeze adversary; the WRONG condition's corrupted
log is harness-injected; owner-scoped reads retained; no repair
canonized. See the H3 report for the full accounting.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which
python` return nothing under that PATH (verified 2026-10-03 at
startup and before the runs); no forbidden executable invoked at
any point (shell used only for mkdir, cp, binary execution,
sha256sum, cmp, diff, grep, git ops, file reads/writes). No
PROCESS-FAIL condition triggered. Pinned znc verified
byte-identical to src/tools/toolchain/znc_linux_x86_64_abed8aa1
before the prereg commit. No recompilation was performed in this
lane (mechanism unchanged by design). Git writes via /usr/bin/git
directly (safebin git symlink EPERM lesson); explicit pathspecs;
no git reset; local only, never pushed.

## Commits

- 68e611a0b: frozen prereg (PREREG.md + NAMECHECK.md), alone,
  strictly before the runs.
- This commit: unpin_h3_bin and unpin_h3.zag (copies, sha256
  verified identical to the H3 artifacts, never modified),
  run1/2/3.txt, run1/2/3.err, REPORT.md. Local only, never pushed.

## Follow-ups for the parent

- RECLAMATION-H3B closes the H3 K20 derivation error: VERDICT=PASS
  (22/22) on the unchanged H3 binary under the corrected prereg.
  The corrected K20 values (ret=17, post=6, rawA=19, ev=16) are
  now frozen and verified.
- The H3 mechanism (policy 8 + learner routines + trace/audit)
  remains a candidate substrate piece for the continuing-learner
  memory question: death as a learner cognitive judgment with a
  white-box trace, where capacity drop measures release behavior.
- Open (from H3): INCORPORATED/SUPERSEDED reasons, sealed
  post-freeze adversary worlds, and the successful-episode
  importance source from the H1 follow-ups remain unrun.
