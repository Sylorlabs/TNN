# KBCONTROL — raw results (three-arm KB-control cost measurement)

**Prereg:** `../preregs/KBCONTROL_PREREG.md` (frozen 2026-09-24T05:53:27Z).
**Date:** 2026-09-24. **Toolchain (pinned):**
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
**Law compliance:** zero RNG in all new sources (`grep -iE 'rng|rand\('`
clean on `kb3/*.zag`); every arm 3/3 byte-identical (SHA256 below);
TMPDIR=~/workspace/tmp_commit; no /tmp batteries.

## What was run

| Arm | Binary | Source |
|---|---|---|
| A1 DELIBERATE-TRAINED (curriculum) | `build/kb_arm1` | `wave2/memoryagency/trial/kb3/kb_arm1.zag` + `kb3_common.zag` + `../memory_core.zag` |
| A3 DELIBERATE-UNTRAINED (curriculum) | `build/kb_arm3` | `wave2/memoryagency/trial/kb3/kb_arm3.zag` + `kb3_common.zag` + `../memory_core.zag` |
| A1 MA1 trial, prereg-faithful (8-slot) | `build/ma1_trial_cap8` | `buildsrc/` = committed `trial.zag`+`memory_core.zag`+`substrate/` with **one-line change** `const MA_CAP:i32=256;`→`const MA_CAP:i32=8;` (diff-verified identical otherwise; honors PREREG_MA1's "8-slot store") |
| A1 MA1 trial, as-committed | `build/ma1_trial` | committed `trial.zag`+`memory_core.zag` (MA_CAP=256) |
| A2 SILENT/AUTOPILOT | `build/r27auto` | `r27rerun/` symlinks → verbatim `evidence/scratch/trial_auto.zag` + `wave3/r27-consolidation/impl/psm.zag` |
| (ref) R27 deliberate | `build/r27delib` | symlinks → verbatim `evidence/scratch/trial_delib.zag` + `psm.zag` |

Shared curriculum: R27 frozen C1/C2/C3 episode sequences (848+640+3392 =
4880 episodes/arm), capacities 32/32/128. Probe: per true id ×4 contexts,
correct/wrong/abstain; spurious = live long-term slots not holding a true
skill's true form. Mid probe (A1/A3 only): after the last adversarial
block (C1:e=608, C2:e=320, C3:e=2432).

## Kill-bar verdicts

- **K1 — PARTIAL FAIL with root cause (finding, not a halt of the arms):**
  as-committed MA1 rerun = **54/58** (`MA_FAILURES,4`, exit 1). The 4
  failures: `kill_badslot_callerbug` (103 vs 2001), `add_full_refused`
  (0 vs 104), `add_full_slot` (8 vs -1), `audit_count` (29 vs 28).
  **Root cause:** `MA_CAP` was raised 8→256 after the 2026-09-19 evidence
  run (for MA2/MA3 scale); PREREG_MA1 specifies an **8-slot store** and
  `trial.zag` was never updated. With 256 slots the store never fills
  (ADD succeeds at slot 8) and slot 99 is a legal empty slot
  (REFUSED_NOTLIVE, not caller-bug). **The deliberate machinery is NOT
  broken:** the prereg-faithful MA_CAP=8 variant reproduces **58/58**
  (`MA_FAILURES,0`, 28 audit entries, replay+clean-refusals pass),
  3/3 byte-identical. The 4 failures are a capacity-constant drift in the
  committed tree — flagged for repair (either pin MA_CAP=8 for MA1 via
  `ma_add_lim`, or amend PREREG_MA1).
- **K2 — PASS** (load-bearing criteria): A2 probe counts and digests
  **byte-identical** to the committed 2026-09-23 `trial_auto_audit.log`
  (C1 32/32/16+16, C2 56/24/0+6, C3 128/128/64+64; digests 89820595,
  962579342, 670018724). Wall-clock 1.52s vs bill's 3.244s — machine
  variance (this VM ~2.1× faster); probe/digest identity is what matters.
- **K3 — PASS:** all 6 binaries 3/3 byte-identical (SHA256 in
  `logs/timing.json`).
- **K4 — PASS:** no rng/rand in new sources.

## Timing (mean of 3; python `resource` peak RSS of child)

| Arm | wall mean | 4880-ep ms/ep | peak RSS | SHA256 (run1) |
|---|---|---|---|---|
| A1 trained (curriculum) | 0.4192 s | **0.0859** | 15.8 MB | d2dce9beaea3e019… |
| A3 naive (curriculum) | 0.3900 s | **0.0799** | 15.9 MB | 50be9b8d207164af… |
| A2 autopilot (r27auto) | 1.5216 s | **0.3118** | 15.9 MB | c74c01da55aa671c… |
| R27 deliberate (ref) | 1.2806 s | 0.2624 | 16.1 MB | 6f5a638f722e9e34… |
| MA1 trial (cap8, 58 checks) | 0.0731 s | n/a | 15.9 MB | 244907dab4283dd7… |
| MA1 trial (as-committed) | 0.0965 s | n/a | 15.9 MB | 5f2489f7ae1101f8… (rc=1) |

RSS is runtime-baseline-dominated (~15.8 MB for every arm); the honest
memory differentiator is arena bytes (below).

## Probe accuracy (end probe = PRIMARY, frozen)

| Curriculum | A1 trained (c/w/a, spur) | A3 naive (c/w/a, spur) | A2 autopilot (c/w/a, spur) |
|---|---|---|---|
| C1 (80 probes) | **80/0/0**, 0 | **80/0/0**, 8 | 32/32/16, 16 |
| C2 (80 probes) | **80/0/0**, 0 | **80/0/0**, 0 | 56/24/0, 6 |
| C3 (320 probes) | **320/0/0**, 0 | **320/0/0**, 32 | 128/128/64, 64 |

## Mid probe (DIAGNOSTIC — judgment under adversarial pressure, before phase D heals)

| Curriculum | A1 trained (c/w/a, spur) | A3 naive (c/w/a, spur) | A2 |
|---|---|---|---|
| C1 | 68/0/12, 0 | 52/16/12, 12 | n/a (binary probes end-only) |
| C2 | 48/0/32, 0 | 40/16/24, 4 | n/a |
| C3 | 260/0/60, 0 | 148/112/60, 60 | n/a |

(Abstains at mid are correct: late-true ids not yet seen — e.g. C1 mid
runs after episode 608 installs id 16, so 3 late ids abstain. C2's
48/32: curriculum never shows ids 3,7,11,15 verified in phase A
(t%4==3 ⇒ e%4==3 ⇒ impostor slots); the trained arm correctly refuses
to install them from UNVERIFIED impostor episodes — abstain is the
honest answer. The naive arm installs them as impostors → wrong.)

## Instrumented op counts (per curriculum)

A1 trained — C1: add=20 kill=0 pin=20 promote=20 refused=0
suppressed_imp=192 suppressed_fab=96 anomaly=0 collateral=0 audit_n=61
replay=0 clean=0.
C2: add=20 kill=0 pin=20 promote=20 suppressed_imp=60 suppressed_fab=20
audit_n=61 replay=0 clean=0.
C3: add=80 kill=0 pin=80 promote=80 suppressed_imp=768 suppressed_fab=384
audit_n=241 replay=0 clean=0.
**Total: 363 audited ops / 4880 episodes = 0.074 ops/ep. Zero kills.**

A3 naive — C1: add=36 kill=8 pin=4 promote=24 refused_pinned=96
conflict_refused=96 collateral=**4** audit_n=169 replay=0 clean=0.
C2: add=62 kill=42 pin=4 promote=40 refused_pinned=40 conflict_refused=40
collateral=0 audit_n=189 replay=0 clean=0.
C3: add=168 kill=56 pin=4 promote=108 refused_pinned=96 conflict_refused=96
collateral=**28** audit_n=433 replay=0 clean=0.
**Total: 791 audited ops / 4880 = 0.162 ops/ep (2.2× the churn of A1).**

A2 autopilot — unaudited mutations: C1 consol=32 dropped=160; C2
consol=28; C3 consol=128 dropped=640. **Total 988 unaudited mutations /
4880 = 0.202/ep. Audit entries: 0 (no audit machinery by construction).**

## Structure vs judgment (D2 — the key question)

**STRUCTURE (identical for A1 and A3):**
- Audit completeness: 100% both arms — every `ma_*` call (success AND
  refusal) appends exactly one entry (A1 C1: 20+20+20+1=61=audit_n;
  A3 C1: 36+8+4+24+96+1=169=audit_n; likewise C2/C3).
- `ma_replay_check` = 0 (ledger replays to exact live state) and
  `ma_audit_clean_refusals` = 0 (refusals never mutate) on all 6 runs.
- **Silent overwrites: 0** for both arms (proven by replay-exactness: no
  state change without an audit entry). A2: 188 unaudited slow-tier
  last-wins installs (+800 fast-tier drops), 0 audit entries.

**JUDGMENT (A1 > A3 > A2):**
- Mid-probe under attack (C3): A1 260/0/60 → A3 148/112/60.
- Spurious installs (C3): A1 0 < A3 32 < A2 64.
- Collateral true-kills: A1 0 < A3 28 (C3) / 4 (C1).
- Churn: A1 363 ops < A3 791 ops (2.2×).
- End-probe true recall: A1 = A3 (320/320) > A2 (128/320).

**D1 decision bar:** did NOT fire — A3 matches A1 on end-probe BUT
spurious≠0 and collateral≠0, so trained judgment adds measurable value
(zero spurious, zero collateral, 2.2× less churn). Caveat: phase D
(return-to-true) heals A3's end-probe; on a curriculum without a healing
phase, A3's end-probe would look like its mid-probe. Follow-up: rerun
with phase D removed.

**Decomposition of MA1's 58/58:** the 58 checks test the STRUCTURE —
refusal gates (CORE/PINNED/NOTLIVE/STAGE/FULL), audit of every path,
replay-exactness, rollback. The "trained judgment" in MA1 is the
scripted choice of *what* to kill/pin. A3 proves the split: keep the
structure, swap in naive judgment → all structural properties hold
perfectly (audit 100%, replay exact, 0 silent overwrites) while judgment
failures (collateral kills, spurious installs, churn) show up
*in the ledger itself*. Structure buys safety+accountability; judgment
buys KB cleanliness.

## Where autopilot genuinely wins (explicit answer)

**Nowhere on outcome-per-cost.** Head-to-head on the same 4880 episodes:
- Accuracy: A2 loses everywhere (C3: 128/320 correct vs 320/320 for
  both deliberate arms; 64 spurious vs 0/32).
- Speed: A2 is **3.6× SLOWER per episode** than the trained deliberate
  arm (0.312 vs 0.086 ms/ep) — its every-10-episode full-tier scans and
  pollution management cost more than deliberation's early exits. (Same
  direction as the bill's C1: deliberate 2.2× cheaper.)
- A2's **only** win is arena bytes: 5,888 B (C1/C2) / 23,552 B (C3) vs
  A1/A3's 170,240 B — i.e. **not paying for the 160 KB audit ledger**
  (4096-entry × 10-word). That saving buys 128 wrong + 64 spurious
  probes on C3 and zero auditability. Verdict: no genuine win — same
  outcome at lower cost does not occur; the cheapest accurate arm is
  the deliberate one.
- Notable: even the NAIVE deliberate arm beats autopilot on accuracy
  (320 vs 128 correct on C3) AND speed (0.080 vs 0.312 ms/ep).
  Deliberate structure alone outperforms autopilot; training the
  judgment adds the rest.

## Memory footprint (arena bytes, deterministic)

- A1/A3 per run: MaStore 167,168 B (of which the audit ledger is
  163,840 B = 97.9%) + side arrays (kid/ver/ctx) 3,072 B = **170,240 B**;
  `ma_replay_check` transiently allocates a shadow store (+167,168 B) →
  peak arena **337,408 B**.
- A2 per curriculum: fast 1152/4608 B + slow 640/2560 B + hist 4096/16384
  B = **5,888 B** (C1/C2) / **23,552 B** (C3).
- Peak RSS ~15.8 MB for all arms (runtime baseline; does not
  differentiate).

## Logs

`logs/kb_arm1_run{1,2,3}.log`, `logs/kb_arm3_run{1,2,3}.log`,
`logs/ma1_trial_cap8_run{1,2,3}.log`, `logs/ma1_trial_run{1,2,3}.log`
(as-committed, 4 failures visible), `logs/r27auto_run{1,2,3}.log`,
`logs/r27delib_run{1,2,3}.log`, `logs/timing.json` (wall/RSS/SHA256 per
rep). Binaries removed after measurement (not committed).
`measure.py` = the timing/RSS/SHA256 battery (Python glue).
`r27rerun/` = 3 symlinks documenting the verbatim A2 rerun setup.
