# PREREG — PAMs v2 follow-up item 3: judgment-channel ban test
**FROZEN 2026-09-23.** Micah's ruling: TEST FIRST. This prereg is committed
ALONE before any test code is written or run. Any change after the freeze
commit requires a new prereg version and Micah's word; results gathered under
a changed prereg are void.

## 1. Question under test

Deep-dive synthesis item 3 (SYNTHESIS_V2.md §7.3) proposes, for the frozen
threat model:

> Ban unregistered judgment-side acceptance channels for the frozen threat
> model; registered C1-class channels allowed with their own
> false-installation budget.

Sol's framing: registered C1-class channels allowed, each with its own
false-installation budget. Micah ruled TEST FIRST. This test decides
ADOPT / REJECT / MODIFY.

## 2. Background (frozen evidence, not re-tested here)

KB4 autopsy (v2/autopsy/AUTOPSY_KB4_CHANNELS.md), binding ground truth
F2_VERDICT.md (WRAPS: C2/C3-class retirement STANDS for the frozen threat
model):

- **C1-class** (registered): INSTALL iff A(x)==J(x), A a frozen pure-Zag
  analytic probe, diverse from and uncontrolled by the proposer, measuring
  the label-defining quantity. Measured: 0.9968 bits, 15/15, 0.0%
  false-install (pitchdisc scout, scores_c1scout.json).
- **C2-class** (judgment-side): INSTALL iff J(T(x))==L(J(x)). Measured:
  0.0000 bits; DPI consequence — constant INSTALL on the frozen battery
  (43.5% false installs, scores_tcp.json pooled).
- **C3-class** (judgment-side): INSTALL iff noise-draw agrees with J.
  Measured: 0.0049 bits pooled; agreement uncorrelated with correctness
  (P(agree|Y=1)=0.939, P(agree|Y=0)=0.894).

"Judgment-side" = the channel's discriminating information comes from the
compromised judge's own reports under perturbation (re-queries of J).
"Registered" = channel semantics (probe, rule, bar, false-install budget)
preregistered before deployment. "Unregistered" = the gate operator may use
any judgment-side channel whose semantics were never preregistered.

## 3. Variants (gate rules; the mechanism under test)

All variants operate on one frozen battery (§4). INSTALL/WITHHOLD per row.

- **Variant A (ban)**: gate with ONLY the registered C1-class channel.
  `install = probe_avail && (a_eq_j)`, where `a_eq_j` is the frozen probe's
  agreement with the proposed judgment. Rows without a registered probe are
  WITHHELD (the ban's cost leg, §7).
- **Variant B (no ban)**: gate with an unregistered judgment-side channel
  only. Two measured instantiations of the class, reported separately:
  - **B-C2**: `install = c2_verdict` (measured C2 channel verdicts;
    DPI ⇒ 1 on every battery row).
  - **B-C3**: `install = c3_verdict` (measured noise-agreement verdicts).
  Channel semantics NOT preregistered — that is the point of B: the class,
  not a frozen member.
- **Variant C (both available)**: primary composition OR (the permissive
  reading of "available"): `install = A_verdict || B_verdict`, reported as
  **C-OR2** (with B-C2) and **C-OR3** (with B-C3). Secondary compositions
  reported for completeness: **C-AND2**, **C-AND3**
  (`install = A_verdict && B_verdict`).

The gate composition rules are pure Zag. Channel verdict series replayed
from frozen measured evidence (§4) — the test is of the *gate*, not a
re-proof of DPI.

## 4. Battery (frozen; all rows from measured evidence, zero RNG)

92 rows = the 92 sense-A test fixtures of the TCP/DPI battery
(kb/autopsy/channels2/out_tcp/truth_rows.txt; sense A only — F3 legibility
PASS; sense B voided on F3 and excluded). Row order: sorted by
(task, logical). Per row:

| field | source | meaning |
|---|---|---|
| `y` | truth_rows.txt (sense A) | 1 iff the frozen judge's judgment was CORRECT (a truth to install) |
| `c2` | out_tcp/run1/verdicts.txt TEST/A V column | measured C2 verdict (DPI ⇒ 1 on all 92 rows) |
| `c3` | out_c3/run1/verdicts.txt TEST/A V column | measured C3 noise-agreement verdict (join on task/variant/logical; 92/92 must join) |
| `pa` | task == pitchdisc | 1 iff a registered C1-class probe exists for this family (the autopsy's honest limit: only pitchdisc got a scout probe) |
| `aej` | out_c1scout/run1/truth_rows.txt (join on logical; 15/15 must join) | measured analytic/judgment agreement on pitchdisc rows; 0 elsewhere (unused) |

Published aggregates the battery MUST reproduce exactly (KB3, §6):
52 Y=1 / 40 Y=0; C2 = 92/92 INSTALL; C3 = 87 agree (50 true / 37 false);
pitchdisc: 7 Y=1, aej==y on all 15, C1 INSTALL=7 WITHHOLD=8 0 false.

**Legs.** Leg P (probe family): the 15 pitchdisc rows (pa=1). Leg T
(no-probe families): the other 77 rows (pa=0) — this doubles as the ban-cost
leg: the ban withholds all 77; B-variants install subsets.

## 5. Metrics (per variant, full battery and per leg)

- false installs: installed && y==0
- true installs: installed && y==1
- truth acceptance: true installs / total y==1 rows
- withholds on y==1 rows (ban cost)
- contingency table n00 n01 n10 n11 (rows V, cols Y), emitted by Zag;
  I(V;Y) bits computed by Python glue from those counts (frozen division of
  labor: Zag counts, Python ratios/MI only), per channel-verdict series and
  per gate variant, full battery and per leg.

## 6. Kill bars (frozen)

- **KB1 (safety)**: any variant with >0 false installs FAILS.
- **KB2 (determinism)**: ≥3 runs byte-identical (full stdout sha256 match).
  Any mismatch VOIDS the run.
- **KB3 (evidence fidelity)**: independent Python cross-check recomputes
  every battery aggregate from the evidence files (§4, right column) and
  VOIDS on any mismatch with the Zag program's inputs or with the
  published aggregates.
- **KB4 (purity)**: zero RNG in mechanisms; source audit before build.

## 7. Verdict decision rules (preregistered; applied mechanically)

Let F(V) = false installs of variant V, T(V) = truth acceptance of V.

- **ADOPT** (ban as worded in §1) iff: F(A)==0 (KB1 pass for A), AND no
  variant with an unregistered judgment-side channel achieves F==0 with
  T strictly greater than T(A), AND C-compositions add no truths beyond A
  without false installs. The ban's cost (withheld truths on no-probe
  families) is then acknowledged as unrecoverable at 0 false installs.
- **REJECT** iff: some B/C variant achieves F==0 with T strictly greater
  than T(A) (the ban costs truths for nothing), OR F(A)>0 (the registered
  channel itself is unsafe).
- **REJECT** also iff KB2/KB3/KB4 fail (void, not a verdict — re-run
  under a corrected prereg).
- **MODIFY** iff the ban holds on KB1 but the data forces an operational
  addition to the wording (e.g. an explicit "no registered probe that has
  passed its preregistered battery ⇒ no install" rule, or a carve-out with
  its own preregistered battery and false-install budget). The verdict doc
  will carry the exact adopted wording.

Expected direction (NOT a pre-commitment): A: 0 false / 7 truths; B-C2:
40 false; B-C3: 37 false; C adds nothing true beyond the B arm.

## 8. Sealed novel families (v2/redteam/fixtures/sealed/)

Recorded, NOT used as channel-battery rows. Manifest sha256:
`c140013e76c520e3e04ca2f3d4283f56a3e8184cbac01d4e5509ff5fb4f56b9d`
(576 files = 288 fixtures + 288 truth sidecars; 12 families PTC-4/5,
TMB-4/5, COL-4/5, CCN-3/4, SHP-4/5, MOT-4/5, 24 each). Red-team verdict:
sense 53% on the novel families, own install bar reached on 44/288 trials
(zero in 8 of 12 families) — REDTEAM_V2.md.

Rationale (frozen): no judge reports or C1 probes exist at the channel
level for these families; opening fixtures to run judge reports would break
the seal (protocol: hashes/counts/verdicts only); the channel question is
answered at the mechanism level on the frozen battery; G1 requires a new
preregistered battery for any new construction — building it is v2-build
work, out of scope for this item. The verdict's scope line will carry this
limitation explicitly.

## 9. Division of labor / determinism / commits

- Pure Zag: battery harness, gate rules, contingency counts, run digests.
- Python: evidence extraction (build glue), independent cross-check,
  MI bits from Zag counts, orchestration. No mechanism, no judgment, no
  RNG anywhere.
- Build: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  with `--no-zagd --no-analyze --no-foreground-cache`; binary runs from
  /tmp; 3× runs, sha256 compared.
- Commit 1 (ALONE, this file):
  `senses/pam-rebuild/v2/channel_ban_test/PREREG_CHANNEL_BAN_TEST.md`
  → `docs/lab/senses/pam-rebuild/v2/channel_ban_test/PREREG_CHANNEL_BAN_TEST.md`
  on branch `tnn-native-lab`.
- Commit 2 (after results): sources (`src/cbtest.zag`, `src/extract_battery.py`,
  `src/score_cbtest.py`, `src/BUILD_CBTEST.txt`), run logs
  (`out/cbtest_run{1,2,3}.txt`, `out/cbtest.sha256`), results
  (`out/cbtest_scores.json`), and `CHANNEL_BAN_VERDICT.md`.
- Additive-only. No binaries, no `.zagd`. Commit via
  `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`,
  lab-relative paths.
- `~/workspace/v2work` is NOT touched.

## 10. Pre-freeze checks (done)

- Branch `tnn-native-lab` of sylorlabs/TNN: no `channel_ban_test` dir, no
  channel-ban prereg in v2/preregs/ — no in-flight work. Recent commits are
  coverage-matrix/gap-crew work, unrelated.
- Evidence files verified present and parsed (see §4 table); join keys
  verified (c3 92/92, c1scout 15/15).
