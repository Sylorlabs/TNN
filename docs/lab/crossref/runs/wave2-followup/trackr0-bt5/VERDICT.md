# B-T5 — VERDICT: **FAIL STANDS (evidence now supplied)**

**Crew:** TRACKR0 B-T5 evidence crew (Wave-2 crossref follow-up). **Date:** 2026-09-24 PDT.
**Task:** Micah undecided on B-T5 — "test more of it first, bring evidence."
**Deliverables:** this file + `RUNLOG.md`, in `~/workspace/scratch-crossref/T2/TRACKR0/bt5/`.
**Authority:** frozen prereg `7b2100d09911c5c10252c5756c7def288e70bd1f` (only authority; prereg-named pins only — brief pins `ce1e3b0b`/`bcd39f4b` confirmed non-existent, never used).

## Bottom line

**B-T5's split-to-merge FAIL stands — and the missing evidence is now supplied.**
The committed round-trip FAIL evidence (`d74b481df26aaa1d6c77f5ca825a499a69b3a42f`) re-executes
**byte-identically** from pinned source with the pinned toolchain; the FAIL is a genuine,
measured dynamics gap in the recovered mechanism, not a harness artifact. The fork probes
pin down exactly which two gates block the composition, and prove a minimal two-part core
change would compose byte-identically — which is the amendment case for Micah.

## 1. Provenance trace — where the B-T5 FAIL claim comes from

| Step | Date | What happened | Artifact |
|---|---|---|---|
| 1 | 2026-09-21 | Prereg freeze (`units/PREREG_FREEZE.md` §2, Micah-signed). B-T5 bar: "split/merge fire under recovered conditions and are auditable; … boundaries shown mutable (**a recruited chunk split then re-merged on the record**)." | frozen prereg |
| 2 | 2026-09-21 | Crew B-DYNSG (`dyn_b5.zag`) claims B-T5 **PASS** — but split fired on `"splitchk"` (id 0) while merge fired on **different** material (`"AAAA"+"BBBB"`, ids 1+2). Self-flags FINDING B5-F1: same-material split→re-merge is unachievable in the frozen core (prefix shadow); refers to Micah. | `VERDICT_B5_DYNAMICS.md` |
| 3 | 2026-09-21 ~06:05 | Coordinator flags it (`MORNING_BRIEF_2026-09-21.md`): "the crew claimed pass but the coordinator flags it — split and merge fired on *separate* contexts, the literal 'same material re-merge' was not demonstrated. **FAIL or BLOCKED pending your reading.**" | morning brief |
| 4 | 2026-09-21 ~09:40 | **Marathon Crew 5**, commit `d74b481df26aaa1d6c77f5ca825a499a69b3a42f`: `bt5_roundtrip.zag` — literal round-trip against the frozen core (`r0_maybe_split`/`r0_maybe_merge`). **Verdict: FAIL**, explicitly supersedes the B-DYNSG PASS for B-T5. | `VERDICT_BT5_ROUNDTRIP.md`, `rt_leg0.log`, `rt_leg1.log`, `BT5_FROZEN_SPEC_EXTRACT.md`, `bt5_roundtrip.zag` |
| 5 | 2026-09-23 | Frozen T2-TRACKR0 prereg (`7b2100d…`) records the claim: "B-T5 split-to-merge FAIL." | `PREREG_TIER2.md` §T2-TRACKR0 |
| 6 | 2026-09-22/23 | T2-TRACKR0 crew: no B-T5 evidence in its inherited set (b_t1/closeout/repair only); prereg Method/Rule don't cover B-T5 → recorded open. | crew VERDICT.md §3 cl.8 |
| 7 | 2026-09-24 | This crew: supplies the missing evidence (below). | this file |

**Integrity of the committed evidence:** branch-head blobs are byte-identical to the
`d74b481df` commit blobs (API-verified git blob SHAs):
`VERDICT_BT5_ROUNDTRIP.md` `fa35c4bfd01715cb203c030ba0fc5a0bc9493012`,
`rt_leg0.log` `d133c000e35749ec2ab87b059b4cf256bcc0ef3d`,
`rt_leg1.log` `c546102c7798afe64ada420e7088d67d52742256`,
`bt5_roundtrip.zag` `97f03fdd3ea37de08c1458872b29a4e22ab4e4c9`.
(The `308bf365`/`3b011ef1` branch-surgery incident touched these paths; the repair
restored them exactly — no silent substitution.)

**On "artifact-driven suspicion":** the T2-TRACKR0 prereg's overnight note about
artifact-driven suspicion concerns **B-T1** (XOR-collision relocations, perturbed-leg
boundary at L=7), not B-T5. For B-T5 the open question was whether the FAIL is a
harness artifact. It is not — three independent mechanism-level blockers (measured,
§2), and the fork probes prove exactly which gates block (§3).

## 2. Test: re-execution of the committed round-trip battery

**Setup.** Fetched at pin `d74b481df`: `bt5_roundtrip.zag` (sha256
`2462290f9887a08d78c595607f5bacc8d47151b16e4793b2a0e329ac6628083a`),
`r0_core.zag` (blob `8e631666e013c6eed99e26f476df10e6c2f19a83`),
`r0_probe.zag` (blob `9e4df2f194d68c4fe17f74ac13e1754dd0509573`),
`m8_armor.zag` (blob `053c1cff77bac1bd2c51aa80d54411e6810a8027`),
`harness_common.zag` (blob `87ebfdc5a059…`), `R33_NATIVE_SHA256_V2.zag` (blob
`5dd858fa1097`), `R33_NATIVE_IO_V1.zag` (blob `a6b440d25643`). Mirrored
`impl/{dynamics,core,harness}/` layout; built with the pinned toolchain
`znc_linux_x86_64_abed8aa1` (sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`,
matches the recorded pin), `--no-zagd --no-analyze --no-foreground-cache`. Pure Zag;
source canary clean (no RNG/clock/entropy in decision paths).

**Results (10/10 runs, rc=4):**

| Check | Committed | My re-run |
|---|---|---|
| leg 0 pert 0 vs committed `rt_leg0.log` | md5 `fc67fccf9fb59cc7b9f6137d54590054` | **byte-identical** (`cmp` clean) |
| leg 1 pert 0 vs committed `rt_leg1.log` | md5 `6c1099926b124fbd642349b4d3581b3b` | **byte-identical** (`cmp` clean) |
| pert 1–4 vs pert 0 (per leg) | only the 2 self-labeling lines differ | **confirmed** — diffs are exactly `RT_BATTERY,leg=,pert=` and `M8_PERTURB,` |
| M8 captures | leg0 store `7008d19c…0cc1eb22`, ledger `1547986639`; leg1 store `2698a3b7…20080bb3fb21`, ledger `952025763` | **all four match** |

**Measured FAIL evidence (both legs, identical):**

| # | Measurement | leg 0 | leg 1 |
|---|---|---|---|
| Split fired under recovered conditions (`use=3, conflict=500, util 5283→−717 ≤ 0`) | child id 1 | child id 1 (util 5163→−837) |
| Parent state after split | 2 (tombstoned), succ=1 | 2 (tombstoned), succ=1 |
| `r0_maybe_merge(parent,child)` rc | **−1** | **−1** |
| `r0_maybe_merge(child,parent)` rc | **−1** | **−1** |
| Ledger SPLIT(196)/MERGE(197) ops | **1 / 0** | **1 / 0** |
| Merge-alone control (RT-3: `"spli"+"tchk"`) | id 2, 8/8 bytes, byte-exact | id 2, 8/8 bytes, byte-exact |
| Halves' bytes concatenated vs original | 8/8 preserved | 8/8 preserved |
| `RT_VERDICT` | **FAIL** | **FAIL** |

## 3. Test more: fork probes — which gates actually block?

The committed verdict names three measured causes. Two are design-level gates in the
frozen core; I tested both with relaxed-merge forks (scratch-only, frozen core untouched):

- **Fork A** — merge accepts the tombstoned split-parent as an input (the both-live gate
  is an implementation extra, not in the prereg's recovered firing conditions), but keeps
  the prereg's exact gain arithmetic (parent regret counted).
- **Fork B** — as Fork A, plus the tombstoned parent's regret is forgiven (regret counted
  over live inputs only) — models a core where split halves/forgives regret the way it
  halves utility.

| Probe | leg 0 | leg 1 |
|---|---|---|
| frozen merge (reproduces committed FAIL) | −1 / −1 | −1 / −1 |
| Fork A (live-gate relaxed only) | **−1 / −1** | **−1 / −1** |
| Fork B (live-gate relaxed + regret forgiven) | merged id 2, **8/8 bytes byte-identical to snapshot** | merged id 2, **8/8 bytes byte-identical to snapshot** |
| Fork verdict | `FORKB_COMPOSES` | `FORKB_COMPOSES` |

**Reading.** Fork A proves the both-live gate is *not* the only blocker: with the parent's
6000 regret counted, the gain conjunct still refuses (`jgain − regret = 620 − 6000 < 0`).
Fork B proves the two gates are the *only* blockers: relax both and the composition works
byte-identically on both legs, ledger-audited (MERGE op emitted, marked fork in d2).

**Source-level confirmation (harness-independent).** In `r0_core.zag`:
- `r0_split_at` tombstones the parent (l.684); `r0_maybe_merge`/`r0_merge_ids` require
  both inputs live (ll.743, 771) → merge refuses the split's own halves in both orders.
- Utility on a live chunk sinks *only* via `r0_regret_update`, which increments regret by
  exactly the rate it decrements utility (ll.645–656, 1:1 coupling). The split's utility
  conjunct (`utility ≤ 0` from ~5283) therefore **requires parent regret ≥ ~5283**, while
  the merge's gain conjunct (`jgain − regret ≥ learned_gain`, jgain ≤ 1000 leg0 / 500 leg1,
  `learned_gain ≥ 0`) **requires parent regret ≤ 1000/500** on the same pair — arithmetically
  mutually exclusive regardless of harness choices. No regret level satisfies both.
- The prefix half can never be recruited live again (dedup matches the tombstoned prefix
  record — measured in RT-2: `RT2_FIND_LIVE_SPLI=−1`, re-observation re-issues the 8-span
  as a fresh dup instead).

## 4. Verdict on the open case

**B-T5's FAIL stands — evidence supplied.** The committed evidence is byte-reproducible
from pinned source; the FAIL is a genuine dynamics gap in the recovered mechanism
(split tombstones + shadows; split/merge regret arithmetic mutually exclusive), not a
harness artifact.

**Amendment case for Micah** (the crew does not decide this):
- **Option A — amend the prereg wording:** accept the B-DYNSG reading (split and merge
  both fire under recovered conditions and are ledger-auditable, on whatever contexts) and
  drop/soften the "same material" parenthetical.
- **Option B — approve a core change:** allow merge to consume tombstoned split-parents
  AND have split forgive/half regret the way it halves utility. Fork B proves this
  minimal two-part change composes byte-identically on both legs. Note both parts are
  needed — either one alone still refuses (Fork A).
- **Not available:** keeping the frozen core *and* the literal bar — they are jointly
  unsatisfiable (three independent blockers, §2–3).

## Files

- `bt5/VERDICT.md` — this file
- `bt5/RUNLOG.md` — full run log
- `bt5/build/impl/{dynamics,core,harness}/` — pinned-source rebuild tree (fetched blobs at `d74b481df`); `build/impl/dynamics/bt5_roundtrip` binary + `rt_leg{L}_p{P}.out` run outputs
- `bt5/fork/impl/{dynamics,core}/` — fork tree (`r0_core_fork_rx.zag`, `bt5_fork.zag`); `fork/impl/dynamics/bt5_fork` binary + `fk_leg{L}_r{R}.out`
- Nothing committed to any repo (coordinator does the single publication commit).

**Caveats.** Type C + re-execution: the `.seg`-scale corpora are not committed (hashes only),
unchanged from the T2-TRACKR0 scope. The fork is a what-if probe, not evidence for a verdict
change — the frozen core is untouched. Build artifacts (`.zag-cache/`, `.zagd.semantic-ready`,
binaries) remain in the scratch trees only.
