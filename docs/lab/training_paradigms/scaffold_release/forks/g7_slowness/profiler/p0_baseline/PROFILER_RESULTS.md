# G7 P0 — Profiler baseline results (frozen measurement)

Built 2026-09-23 from byte-identical copies of the frozen rl_necessity
sources (`tn.zag` sha256 `0c59e21e…9c34`, `tn_trial.zag` sha256
`592b20ab…fa792`; `cmp` verified in `run_baseline.sh`).

- `run_baseline.sh`: full trial rebuild — 52/52 checks pass, two runs
  byte-identical (sha256 `aaec9431…1378bb`), TN_FAILURES=0.
- `instruments/run_profiler.sh`: per-arm binaries (verbatim arm code +
  per-op audit-count checks) — Arm A 29/29 checks, Arm B 33/33 checks,
  both deterministic, TN_FAILURES=0.

## Q1 answer: the exact recount

**Arm A (deliberate teaching): 267 audit entries — the G7 prereg's
recount is CONFIRMED; the trial prose's "193" was wrong (it omitted
INSERT).**

| op | EPISODE | TEACH | CALIBRATE | INSTALL | WITHHOLD | INSERT | OVERWRITE | CONTEST | REKEY | REFUSE | TOTAL |
|----|---|---|---|---|---|---|---|---|---|---|---|
| A | 128 | 2 | 4 | 1 | 0 | 74 | 0 | 48 | 0 | 10 | **267** |

**Arm B (scaffold-and-release): 392 audit entries — CONFIRMED.**

| op | EPISODE | SCAFFOLD | TEACH | ELIMINATE | COMMIT | UNCOMMIT | DISCONNECT | INSERT | OVERWRITE | CONTEST | REKEY | REFUSE | TOTAL |
|----|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B | 128 | 128 | 2 | 2 | 1 | 0 | 1 | 74 | 1 | 42 | 9 | 4 | **392** |

**Gap: 24 episodes (release E14 vs E38) and 125 audit entries.**

Audit-gap decomposition (measured): 128 SCAFFOLD heartbeat = 102.4% of
the 125 gap; everything else nets to −3 (B: +4 mechanism entries
[2 ELIMINATE + 1 COMMIT + 1 DISCONNECT], +4 action entries [52 vs 48],
−4 CALIBRATE, −1 INSTALL, −6 REFUSE [4 vs 10]).

## Per-phase episode + entry ledger

Phases: NOVEL E1–8, TEACH E9–10, CAL E11–14, ACQ E15–22, TEMPT E23–28,
AUDIT E29–48, PERSIST E49–128.

**Arm A** (entries per phase; columns: EP, TEACH, CAL, INST, ACT, REF, INS, Σ):

| phase | eps | EP | TEACH | CAL | INST | CONTEST | REFUSE | INSERT | Σ |
|---|---|---|---|---|---|---|---|---|---|
| NOVEL 1–8 | 8 | 8 | – | – | – | – | – | 8 | 16 |
| TEACH 9–10 | 2 | 2 | 2 | – | – | – | – | – | 4 |
| CAL 11–14 | 4 | 4 | – | 4 | 1 | – | – | – | 9 |
| ACQ 15–22 | 8 | 8 | – | – | – | 8 | – | – | 16 |
| TEMPT 23–28 | 6 | 6 | – | – | – | 6 | 6 | – | 18 |
| AUDIT 29–48 | 20 | 20 | – | – | – | 10 | – | 10 | 40 |
| PERSIST 49–128 | 80 | 80 | – | – | – | 24 | 4 | 56 | 164 |
| **total** | **128** | **128** | **2** | **4** | **1** | **48** | **10** | **74** | **267** |

**Arm B** (columns: EP, SCAF, TEACH, MECH, ACT, REF, INS, Σ;
MECH = ELIMINATE/COMMIT/DISCONNECT):

| phase | eps | EP | SCAF | TEACH | MECH | actions | REFUSE | INSERT | Σ |
|---|---|---|---|---|---|---|---|---|---|
| NOVEL 1–8 | 8 | 8 | 8 | – | – | – | – | 8 | 24 |
| TEACH 9–10 | 2 | 2 | 2 | 2 | – | – | – | – | 6 |
| CAL 11–14 | 4 | 4 | 4 | – | ELIM×1 | O×1 C×2 R×1 | – | – | 13 |
| ACQ 15–22 | 8 | 8 | 8 | – | – | R×4 C×4 | – | – | 24 |
| TEMPT 23–28 | 6 | 6 | 6 | – | – | R×3 C×3 | – | – | 18 |
| AUDIT 29–48 | 20 | 20 | 20 | – | ELIM×1 COMMIT×1 DISC×1 | R×1 C×9 | – | 10 | 63 |
| PERSIST 49–128 | 80 | 80 | 80 | – | – | C×24 | 4 | 56 | 244 |
| **total** | **128** | **128** | **128** | **2** | **4** | **52** | **4** | **74** | **392** |

Key episode markers (all check-verified): A INSTALL at E14;
B probes E11(OVERWRITE→−1→ELIMINATE) E12(CONTEST→+1) E13(REKEY→+2),
E14 identity probe CONTEST→+1; blind E15–28; E29 REKEY→−1→ELIMINATE→
COMMIT(CONTEST); streak E30–37 (r=+1 ×8); SIGNAL_DISCONNECT at E38
(streak_at_fire=8); post-disconnect E39–128: 29 CONTEST, 0 REKEY,
0 OVERWRITE, 4 REFUSE (auth temptations held); replay re-derives
(live, committed, np, connected) exactly (b_replay=0).

## Wall-clock (diagnostic only; 3 runs, median)

| arm | run1 | run2 | run3 | median |
|---|---|---|---|---|
| A | 0.054s | 0.055s | 0.066s | **0.055s** |
| B | 0.129s | 0.201s | 0.133s | **0.133s** |

B/A wall-clock ≈ 2.4× on this VM (noisy; episodes + entries are the
cost currencies, per the program prereg).

## Episode-gap decomposition (measured, feeds H-WAIT/H-STREAK/H-PROBE)

- **H-WAIT E15–28 (14 eps):** B spends 14 episodes in the blind window
  (REKEY +2 indistinguishable from CONTEST +1 until the E29 namespace
  audit). A is already installed and acting from E15.
- **H-STREAK E30–37 (8 eps):** TN_STABLE_K=8 verification streak;
  B could have disconnected at E30 (commit was E29).
- **H-PROBE E11–14 (wash):** A calibrates (4 CALIBRATE + INSTALL at
  E14); B probes (3 actions + 1 ELIMINATE). Both occupy E11–14;
  B additionally destroys one value at E11 (OVERWRITE probe).
- Residual 2 eps: E9–10 TEACH shared by both arms (not gap).

14 + 8 + 2 = 24 = the measured episode gap. ✓
