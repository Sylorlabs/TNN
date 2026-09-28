# REDTEAM_R4.md — Blind red team vs the R4-hardened strength checker

**Date:** 2026-09-25 · **Target:** `ck_verify_overwrite` in `r4val/trial/strength_checker.zag` (called from `ck_verify`), hardening the R4 ruling *"overwriting a strong memory must cost the full erase price, paid BEFORE the overwrite lands."*
**Role:** blind red team attacking the CHECKER, not the mechanism. The checker was not modified.
**Driver:** `~/workspace/strength-round4/r4val/rt_redteam.zag` → binary `rt_redteam_bin` (do NOT commit the binary per workspace rules).
**Build:** `cd ~/workspace/strength-round4/r4val && ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 rt_redteam.zag -o rt_redteam_bin`
**Run:** `./rt_redteam_bin` — pure Zag, zero RNG, two runs byte-identical (`diff` clean).
**Baseline re-confirmed:** position (a) → `checker_failures=2` (flagged); positions (b)/(c) per brief pass — **with one anomaly, see §6.**

## Results table

| Attack | Mechanism rcs | Full `ck_verify` failures | Effort-logic verdict | Assessment |
|---|---|---|---|---|
| A1 weaken(0)→fused ow | wk=0, ow=0 (0 cites) | 1 | **PASS (0 flags)** | **DEFEATED — F1** |
| A2 weaken(10)→fused ow | wk=0, ow=0 (1 cite) | 1 | **PASS** | **DEFEATED — F1** |
| A3 weaken(10)→DIRECT ow | ow=0 (1 cite) | 1 | **PASS** | **DEFEATED — F2** |
| A4 double overwrite | ow1=0, ow2(no cites)=109, ow2(1 cite)=0 | 1 | held | HELD |
| A5 kill→rollback→ow | kill=0, rb=0, ow=0 (0 new cites); effort-direct=0; replay=302 | 1 | **PASS** | **DEFEATED — F4** |
| A6 cite recycling | ow1=0, recite(11)=0, ow2=0 | 1 | PASS | observation — F6 |
| A7 counterfeit cites (999991–4) | ow=0 | 1 | PASS | **gap — F5** |
| A8i forged code | justify(99)=2001, 0 ledger entries | n/a (test bug, see §5) | — | HELD (by mechanism) |
| A8ii wrong-slot justify | ow=110 (NOJUSTIFY) | 0 | — | HELD |
| A9 no prior write | fused=103, direct=103 | n/a | — | HELD (vacuous) |
| A11 P3 baseline (genuine) | pexp=0, ow=0 | 1 | held | HELD (intended path) |
| A11b P3 ep desync | pexp=0, ow=0 | 2 | — | false positive — F7 |

(The uniform `checker_failures=1` on overwrite trails is the F3 replay/step_ep divergence, **not** the effort logic — verified by calling `ck_verify_overwrite` directly in A5 → 0.)

## F1 — CRITICAL: weaken-then-overwrite defeats the full-erase-price law; checker passes

`st_weaken` (via `st_redeclare`) is **free**: it requires only stage≥MANAGE, live, non-core — no cites, no justify, no effort gate (`cite_ep=-1` pure-judgment path). `ck_verify_overwrite` prices effort as `n(strength_before)` read from the overwrite's **immediate** before-word. So:
- **A1:** memory admitted at s=90 → `st_weaken(x,0)` (rc=0, free) → `st_justify` (free) → `st_overwrite` → **rc=0 with 0 cites paid** for an s=90 memory. Before-word strength=0, need=0, 0 cites, justify present → effort logic clean.
- **A2:** weaken to 10 → 1 cite + justify → overwrite rc=0. Paid 1/4 of the lawful price.

The ruling's "no cheap-edit path" is not closed: the fused overwrite closed the *direct* path, but the *weaken* path discounts the price arbitrarily, and the checker blesses it because it never looks past the immediate before-word. Note the mechanism shares the pricing (`st_kill_effort_check` uses current strength), so the fix belongs at the law level (e.g., price on pre-weaken/high-water strength, or put an effort gate on weaken) — but as specified, **the checker's verification is defeated**: a law-violating overwrite passes.

## F2 — CRITICAL: position-(a) bypass via one free weaken

The R4 headline result was "(a) direct write FLAGGED with 2 failures." **A3:** `st_weaken(x,10)` → 1 cite → justify → `st_overwrite_direct` → rc=0, before=10/after=50, effort logic clean. The confirmed kill evaporates: any attacker pre-weakens once (free) and the "flagged" position passes. (The direct-write hook is test-only, but the checker contract is "every OK ST_OP_OVERWRITE" — and the same weaken trick works on the fused path per F1.)

## F3 — HIGH: `ck_replay` step_ep divergence — the hardened checker fails lawful overwrite trails not followed by a kill (false positive)

Code trace: `st_overwrite`'s OK branch calls `st_kill_clear` (sets `step_ep←-1`) then re-adds **inline without restoring `step_ep←aux_ep`** (unlike `st_add_into_slot`, which sets it). `st_replay_check`'s OVERWRITE branch sets shadow `step_ep←aux_ep`. Real (−1) vs shadow (aux_ep) → `ck_replay` returns `300+slot` → full `ck_verify` fails on any trail with an OK overwrite not followed by a kill (the kill's `st_kill_clear` re-syncs both to −1, which is why position (a)'s trail shows exactly its 2 effort/justify failures and nothing else). `st_overwrite_direct` diverges the same way (leaves the ADD's `step_ep`, replay expects `aux_ep`). The checker's own P3 tracking (`ck_adm←aux` on OVERWRITE) agrees with the replay, not the mechanism — so this is a **mechanism bug (missing `step_ep` restore in both overwrite writers) manifesting as a checker false positive**. Practical impact: as committed, the hardened checker **cannot pass a trail containing an OK overwrite not followed by a kill** — completeness is broken on that trail shape. (Coordinator note 2026-09-25: the standing "(c) PASS with 0 failures" claim RE-VERIFIED — position (c)'s trail has a kill after the overwrite, which re-syncs step_ep; `./r4_attack_r4 c` prints `R4_T4 pos=2 ... checker_failures=0`. The §6 anomaly was a measurement error — the R4_T4 line is present. F3's conditional form stands.)

## F4 — HIGH: effort double-spend via kill → rollback → overwrite

**A5:** 4 cites + justify → `st_kill_evidenced` rc=0 → `st_rollback_last` rc=0 (slot live, str=90) → `st_overwrite` rc=0 **with zero new cites**. `ck_verify_overwrite` called directly on the overwrite → **0** (effort logic passes: KILL/KILL_EVIDENCED are not strength-writes, so `lss` stays at the ADD and the pre-kill cites still sit in `(lss, ow)`). One payment (4 cites + 1 justify) bought **two** full-price destructions of an s=90 memory. Sub-finding: `st_replay_check` cannot replay OK ROLLBACK entries either — it restores the ROLLBACK entry's own (zero) after-words instead of the rolled-back entry's before-words (observed `replay_rc=302`; the A5 trail fails full `ck_verify` on replay, masking the effort-logic pass).

## F5 — MEDIUM: counterfeit cites accepted as "effort"

**A7:** cites `999991–999994` (impossible episodes, far beyond any horizon) + justify → overwrite rc=0, effort logic clean. Neither mechanism nor checker validates `cite_ep` semantics on the overwrite path — the kill path has `ck_cite_genuine` (gate_mode 0); the overwrite path has **no genuineness check in any mode**. Effort can be paid in meaningless tokens. (Whether this violates the *letter* of the law is debatable — the law counts cites — but it hollows out the *meaning* of "effort"; at minimum the checker should mirror the kill path's genuineness check.)

## F6 — MEDIUM (observation): cite recycling across strength-writes

**A6:** after ow#1, re-citing `cite_ep=11` → rc=0 (accepted), ow#2 → rc=0, effort logic clean. The DUPCITE window is "since last strength-set," so the same episode can be cited again after every overwrite. Each overwrite nominally paid its price — **held per the letter** — but the effort is not fresh. Flagging for the law, not a checker-logic bug (checker faithfully mirrors).

## F7 — LOW: P3 `aux_ep` vs `s.*.ep` desync (false positive, arm-3 only)

**A11** (genuine expiry, old `cite_ep=5`, arm=3): held — the baseline path works as designed (`pexp_rc=0, ow_rc=0`; the 1 failure is F3). **A11b:** `st_set_episode(1000)` but `st_protection_expired(x, 5)` — the mechanism gates on the **unaudited** `s.*.ep` (→ OK), while the checker's `bad_pexp` re-verifies on the caller-supplied `aux` ep (5 − 0 ≤ 50 → `ck_no_bad_pexp` fails). Result: `checker_failures=2` (F3 + bad_pexp) on a mechanism-OK, genuinely-expired trail. No discount gaming is possible (a checker-accepted baseline requires a mechanism-OK PEXPIRED, which requires genuine expiry under the mechanism's K), but the dual-episode-source is a real desync: **fix by auditing a single episode value in the PEXPIRED entry and verifying that.**

## §5 Held attacks (checker + mechanism agree)

- **A8 justify forgery:** `st_justify(x,99)` → **2001** (`cl_bad`), **0 ledger entries** (`audit_delta=0`) — out-of-range codes can't even be recorded. Wrong-slot justify → overwrite refused **110** (`REFUSED_NOJUSTIFY`); trail `checker_failures=0`. *Caveat: my A8i sub-case mistakenly used `rt_cite4` (which includes a justify), so its `ow=0` is a test bug, not evidence — the valid forgery evidence is the 2001/no-entry result and A8ii.*
- **A9 no-prior-write (lss=−1):** overwrite on a never-added slot → **103** both paths. Unreachable for OK overwrites: the fused path refuses `lss<0` with 109, and liveness implies a prior OK ADD. Vacuous hold.
- **A4 double overwrite:** ow#2 with 0 new cites → **109** — the `(lss,i)` window correctly starts after ow#1 (pre-ow#1 cites don't leak); with 1 fresh cite + justify → OK. No off-by-one.

## §6 Anomaly — RESOLVED by coordinator re-verification

The red team reported `./r4_attack_r4 c` printed no `R4_T4` line. Coordinator re-ran 2026-09-25: the line IS present — `R4_T4 pos=2 attack_cites=5 checker_failures=0 ow_entries=1 ow_effort_flags=0` (the earlier `head -20` truncated it). The "(c) PASS with 0 failures" claim STANDS. Position (c)'s trail has a kill after the overwrite, which re-syncs step_ep per F3's conditional form.

## Recommended fixes (for the fixer, not this red team)

1. **F1/F2:** price overwrite effort on the high-water/pre-weaken strength (e.g., max strength since the previous strength-write, or carry a `max_strength` per slot), or put an effort gate on `st_weaken`; checker mirrors whichever the law chooses.
2. **F3:** restore `step_ep←aux_ep` (and keep `last_cite←-1`) in `st_overwrite`'s and `st_overwrite_direct`'s OK branches — matching `st_add_into_slot` semantics that the checker/replay assume.
3. **F4:** treat KILL/KILL_EVIDENCED as effort-window resets for `st_last_strength_idx` (or mark cites consumed); fix `st_replay_check`'s ROLLBACK branch to restore the rolled-back entry's before-words (index `i-1` at replay time).
4. **F5:** apply `ck_cite_genuine`-style validation to overwrite cites (or bound `cite_ep`: admission-ep ≤ cite_ep ≤ h).
5. **F7:** single audited episode source for PEXPIRED.

## Files

- Attack driver: `~/workspace/strength-round4/r4val/rt_redteam.zag` (source — commit it; `rt_redteam_bin` is built in the same dir, **do not commit the binary**)
- This report: `~/workspace/strength-round4/redteam_R4/REDTEAM_R4.md`

**Bottom line:** the R4 hardening does not hold as specified. The checker's effort logic is defeated two ways at the law level (F1 weaken-discount, F2 position-(a) bypass — both require a law decision, not just a checker fix), accepts counterfeit effort (F5 — checker gap, fixable), and — via F3 — false-positives on lawful overwrite trails not followed by a kill (mechanism bug, fixable). F4's double-spend and F7's desync are real. The "(c) PASS" claim re-verified and stands.
