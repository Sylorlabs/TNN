# F1 Fix Report — weaken-then-overwrite discount (law-level red-team finding F1)

Date: 2026-09-26. Toolchain (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Scope: `f1/` only. No commits; no binaries left for the coordinator.

## The hole (baseline, measured)

`st_kill_effort_check` priced destruction at `st_n(current strength)`. A TNN-role attacker
could `st_weaken(90→0)` for free (WEAKEN is a free judgment re-declaration), then
`st_overwrite`/`st_kill_evidenced` for 0 cites, because `n(0)=0`. The R4 checker was
equally blind (`cf=0`). Baseline attack battery (`logs/baseline/f1_attack_r1.log`):

| attack | baseline result |
|---|---|
| A1: weaken 90→0, justify, fused overwrite | **ow_rc=0 — OPEN** |
| A2: weaken 90→10, 1 cite, justify, overwrite | **ow_rc=0 — OPEN** |
| double weaken 90→50→0 | **ow_rc=0 — OPEN** |
| weaken→kill_evidenced | **kill_rc=0 — OPEN** |
| downward via `st_strengthen(x,0)` (op relabel) | **ow_rc=0 — OPEN** |
| weaken→0, then test-only direct overwrite (A3) | executes, checker blind (cf=0) |

(Boundary weakens to 1/25/50 were already refused on baseline — residual `n(s)>0` with 0 cites.)

## The two forks

**Fork A — high-water erase pricing (WINNER).** `st_kill_effort_check` now prices
`st_n(HW)` where HW = high-water mark: the maximum strength *written* to the slot since
its most recent successful ADD or OVERWRITE (the judgment epoch), floored by current
strength. New shared helper `st_epoch_highwater()` in `strength_core.zag`; the checker
(`ck_verify_kill`, `ck_verify_overwrite`) calls the *same function* — mechanism and
checker are lockstep by construction. The FULL-stage gate follows the same mark
(`HW>50 ⇒ FULL`). WEAKEN itself stays a free judgment re-declaration; only destruction
is priced. One refusal-precedence fix during testing: no-epoch slots fall back to
current strength so the pre-existing NOTLIVE refusal fires before the effort check
(A9 control restored to `fused_rc=103 direct_rc=103`).

**Fork B — effort gate on downward weakening (LOSER, preserved as `logs/patches/forkB_vs_baseline.patch`).**
Any downward re-declaration (direction-gated, not op-gated — the `st_strengthen(x,0)`
bypass forced this) from s1 to s2<s1 requires `st_n(s1)−st_n(s2)` distinct cites since
the last strength-write (new refusal `ST_REFUSED_WEAKENGATE=121`); upward/level stays
free. New checker `ck_verify_weaken`. Total cites to destroy a 90-judgment still
telescope to exactly 4 (e.g. 3 at weaken + 1 fresh at overwrite).

## Window correctness (F2 crew's singleton-bug finding — checked, not present)

The F2 crew found that a high-water scan over `[lss, ow_idx)` is a singleton: WEAKEN is
itself a strength-write, so `st_last_strength_idx` at overwrite time returns the weaken
index and HW computes as 0. **My fork-A implementation never used that window.**
`st_epoch_highwater` scans `[birth, upto)` where birth = last OK ADD/OVERWRITE:

```
HW_BIRTH=90   (my st_epoch_highwater, birth-based)
HW_LSS=0      (literal [lss, upto) scan — the F2 singleton bug, reproduced for contrast)
CUR_STR=0
OW_RC=109     (overwrite refused: need=st_n(90)=4, 0 cites)
```

(`logs/forkA/hw_probe.log`; deterministic 2×.) Word indices verified against `st_snap`:
before-strength = b4&255 (word 8), after-strength = a4&255 (word 14). The cite-counting
window is unchanged (`(lss, now)`, exact-count `cnt==need` preserved); only the *pricing*
window is birth-based. A1/A2 closure below is the end-to-end proof: with the singleton
bug, `need` would be `st_n(0)=0` and both overwrites would succeed.

## Attack kill table (each attack run 2×, byte-identical; checker in gate_mode=1)

| attack | baseline | Fork A | Fork B |
|---|---|---|---|
| F1_A1 (weaken 90→0 → overwrite) | ow 0 OPEN | **ow 109** cf 0 | wk 121, ow 109 |
| F1_A2 (weaken 90→10, 1 cite → ow) | ow 0 OPEN | **ow 109** cf 0 | wk 121, ow 109 |
| weaken →1 / →25 / →50 | ow 109 | ow 109 | wk 121, ow 109 |
| double weaken 90→50→0 | ow 0 OPEN | **ow 109** | wk 121 |
| weaken→strengthen→weaken | ow 109 | ow 109 | wk 121 (down-strengthen 90→80 free, same band) |
| weaken → kill_evidenced | kill 0 OPEN | **kill 109** | wk 121, kill 109 |
| cited weaken (`st_redeclare`, cite_ep=21) | ow 109 | ow 109 | wk 121 (own cite_ep doesn't count) |
| downward `st_strengthen(x,0)` relabel | ow 0 OPEN | **ow 109** | wk 121 |
| **legitimate A-path**: free weaken, pay full HW price (4 cites+justify) | ow 109 (overpay refused by exact-count rule) | **ow 0, cf 0 PASS** | wk 121; overwrite at full price still passes (ow 0) |
| **legitimate B-path**: 3 cites, weaken, 1 cite+justify | ow 0 | ow 109 (A rejects partial payment) | **ow 0, cf 0 PASS** (total 4 cites = full price) |
| control: overwrite, no weaken, full price | ow 0 | ow 0 | ow 0 |
| upward / level re-declares | free | free | free (down 20→5 free: same price band, discount 0) |
| A3-style: weaken + test-only direct write | executes, checker blind | executes, **checker now flags 1 failure** | weaken refused; direct write still executes (test-only), checker flags |

Full logs: `logs/baseline/`, `logs/forkA/`, `logs/forkB/` (r1+r2 runs each).

## Honest regression (both forks)

- 27/27 S1 cells byte-identical vs `evidence_r4f` (all arms × curricula × variants).
- 6/6 B-arm S10/S100 spot checks byte-identical vs `evidence_r4`.
- GATE: all 4 arms `ST_GATE f=0` on both forks.
- r4_overwrite T1–T4 (positions a/b/c): byte-identical to baseline on both forks.
- Original red-team drivers (`rt_redteam`, `r4_attack`): all control lines (A5/A7/A9/A11B)
  byte-identical to baseline on both forks (A9 restored after the precedence fix; A11B's
  one pre-existing checker mismatch unchanged).
- Vacuity argument: the honest learner never calls `st_weaken`/`st_overwrite` (static
  grep of `strength_learner.zag`) and the regression diff is the empirical proof.

## Winner: FORK A

Both forks close every attack and every fresh variant, and both are honest-vacuous.
Fork A wins on:

1. **Smaller, more surgical change** — one pricing function, not a new gate + new refusal
   code + new checker function + two-payment telescoping.
2. **Relabel-immune** — fork B's first build was bypassed by the downward-`st_strengthen`
   variant and needed a second patch (direction-gating). Fork A reads the ledger's
   strength history, so no op renaming can evade it.
3. **Preserves free judgment** — weakening stays a free re-declaration; only destruction
   is priced. Fork B taxes downward revision itself (and its legitimate path costs an
   extra justify vs the no-weaken path).
4. **Mechanism and checker share one function** (`st_epoch_highwater`) — lockstep by
   construction; fork B carries parallel window logic in two places.

Fork B lost for those reasons, not for a missed attack — its evidence is preserved as
`logs/patches/forkB_vs_baseline.patch` plus its full attack logs.

## Exact law-change proposal (for Micah's signature — NOT adopted unilaterally)

> **Amendment to the full-erase-price law (R-strength-pricing):** the effort price of
> destroying a memory (`st_kill_evidenced`, `st_overwrite`) is `n(HW)`, where HW is the
> **high-water mark**: the maximum strength written to the slot since its most recent
> successful ADD or OVERWRITE (the judgment epoch), including the current strength.
> Citation windows, the exact-count rule (`cnt==need`), and justification requirements
> are unchanged; the FULL-stage requirement follows the same mark (HW>50 ⇒ FULL stage).
> WEAKEN/STRENGTHEN remain free judgment re-declarations. Rationale: the price must
> attach to the strongest judgment destroyed, not to whatever strength the slot happens
> to hold after free re-declaration.

Residual notes: a rolled-back strengthen still contributes its written peak to HW
(conservative — the strong judgment existed in the epoch); trainer_declare downward is
trainer-role-gated and out of scope. **Adoption of this amendment is Micah's call.**

## Files changed

- `strength_core.zag`: added `st_epoch_highwater()`; `st_kill_effort_check` prices
  `st_n(HW)` and stages on HW (test-only `st_overwrite_direct` untouched).
- `strength_checker.zag`: `ck_verify_kill` / `ck_verify_overwrite` price `ck_n(HW)`
  via the same helper (checkers byte-identical across copies).
- `r4val/trial/strength_core.zag`, `r4val/trial/strength_checker.zag`: synchronized;
  differ from root only by the test-only `st_overwrite_direct` hunk (verified by diff).
- Verified: rebuilt trial + attack battery from these exact sources reproduce the fork-A
  logs byte-identically (`F1A-IDENTICAL-TO-FORKA`, 3/3 honest cells OK).
