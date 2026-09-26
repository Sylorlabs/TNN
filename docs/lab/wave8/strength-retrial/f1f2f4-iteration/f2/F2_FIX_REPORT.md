# F2 FIX REPORT — closing the position-(a) weaken bypass

**Crew:** F2 iteration (strength trial) — 2026-09-25/26
**Workdir:** `~/workspace/strength-f1f2f4/f2/` (sibling `f1/`, `f4/` untouched; nothing committed)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned, all builds)
**Current tree state:** FORK A applied (both `strength_checker.zag` copies carry it; both
`strength_core.zag` copies pristine — the two cores differ only by `st_overwrite_direct`
as required; the two checkers are byte-identical). Pristine backups: `pristine_backup/`;
fork-B reference cores: `logs/ref/`. All attack logs under `logs/` (`baseline/`, `forkA/`, `forkB/`).
Binaries in workdir are build artifacts — do NOT commit.

## The finding (recap)

R4 red team A3: `st_weaken(x,10)` → 1 cite → justify → `st_overwrite_direct` → `rc=0`,
`before=10/after=50`, checker 0 failures. One free weaken erased the R4 position-(a) kill
("flagged with 2 failures"). The direct-write hook is test-only, but the checker contract is
"every OK ST_OP_OVERWRITE" — and the same weaken trick works on the fused path.

## Fork designs (as implemented and measured)

### FORK A — checker-side high-water pricing (45 changed lines, checker only, mechanism untouched)

`ck_verify_overwrite` and `ck_verify_kill` now price erasure at `n(HW)` instead of
`n(before-strength)`, where **HW = max after-strength (word 14 & 255) over OK strength-writes
(ADD/STRENGTHEN/WEAKEN/TRAINER_DECLARE/OVERWRITE) for the slot in `[birth, idx)`**,
`birth` = most recent OK ADD or OVERWRITE before the checked op (a fresh judgment resets the
water mark). New helpers `ck_birth_idx` / `ck_high_water` in `strength_checker.zag`
(root + `r4val/trial/` copy, byte-identical). P3-baseline branch (`need >= 1 cite`) unchanged.

Design note: the task sketch said "scan in `[lss, ow_idx)`" with `lss` = last strength write.
Read literally that window is a singleton (the weaken itself) and the fork would do nothing —
the scan must extend past the discount move to the judgment's birth. The birth-window reading
is also what makes the fix uniform across discount vehicles (weaken, downward-strengthen,
trainer-declare-downward): any of them leaves the pre-discount high value inside the window.

### FORK B — mechanism-side effort gate on downward redeclare (22 changed lines, core only, checker untouched)

`st_redeclare` (both `strength_core.zag` copies): when `op` is WEAKEN — or STRENGTHEN with
`strength < current` (a strengthen below current *is* a weaken; the gate covers it, stated
precisely here) — and the move crosses an effort bucket (`st_n(cur) - st_n(strength) > 0`),
it requires that many **distinct cites in `(lss, now)`** under the existing DUPCITE rules,
else `ST_REFUSED_EFFORT` (audited, before==after, refusals-clean). Upward/level redeclares
stay free; TRAINER_DECLARE (trainer origin) stays outside the gate. The landed redeclare
becomes the new `lss`, so a later overwrite/kill still costs `n(s2)` on top — telescoping:
sum of discounts + `n(final)` = `n(s1)` always, regardless of step count.

## Honest-regression table (byte-identical vs reference evidence)

Build sanity first: unmodified sources rebuilt → 4/4 honest cells byte-identical to
`evidence_r4f/` (binary arg mapping confirmed).

| Suite | Reference | Fork A | Fork B |
|---|---|---|---|
| S1: B/C/C-P3 × VUP/WBS/JI × var 0–2 (27 cells) | `evidence_r4f/` | **27/27 identical** | **27/27 identical** |
| S10 spot: B_JI_0, B_VUP_2 | `evidence_r4/` | identical | identical |
| S100 spot: B_JI_0, B_WBS_1 | `evidence_r4/` | identical | identical |

(Evidence S10/S100 covers arm B only; all existing B scale logs matched. Every attack binary
run 2×, diff clean — zero RNG, deterministic.)

Why honest-vacuous (not assumed — verified by the table, mechanism sketch here):
- Fork A: honest trails contain no WEAKEN; the only honest downward moves are
  `st_strengthen(·,80)` after 90 and land in the same `n()` bucket (4), so
  `n(HW) == n(before-strength)` on every honest kill/overwrite.
- Fork B: the honest learner never calls `st_weaken`; its downward strengthens
  (90→80) have discount `n(90)-n(80) = 0`, so the gate never fires.

## Attack battery kill table

`r4val/f2_attack.zag` (new, 12 variants) + original `rt_redteam.zag` (A1–A11b) +
`r4_overwrite.zag` (positions a/b/c). `checker_failures` = `ck_verify` failures;
`rc 109` = `ST_REFUSED_EFFORT`, `110` = `ST_REFUSED_NOJUSTIFY`.

### Fresh F2 battery (direct path + variants)

| # | Variant | Fork A | Fork B |
|---|---|---|---|
| F2A1 | **Original A3**: weaken 90→10, 1 cite, justify, DIRECT | wk 0, ow 0 → **flagged (ck_ow_effort 1 vs 4)** | wk **refused 109**, ow 0 → **flagged (1)** |
| F2A2 | weaken→0, DIRECT, 0 cites | **flagged** | wk refused 109 → **flagged** |
| F2A3 | double weaken 90→50→10, 3 cites split | **flagged** | wk1 ok, wk2 refused 109 → **flagged** |
| F2A4 | **control**: DIRECT, NO weaken, 1 cite (orig. R4 kill) | **flagged (1)** — kill preserved | **flagged (1)** — preserved |
| F2A5 | **legit**: weaken, full HW price (4 cites) in-window, DIRECT | **PASS (0)** | wk refused 109, DIRECT **PASS (0)** at full price |
| F2A6 | strengthen 20→90, weaken→10, DIRECT, 1 cite | **flagged** | wk refused 109 → **flagged** |
| F2A7 | downward **STRENGTHEN** 90→10 (no weaken), DIRECT | **flagged** | **refused 109** → **flagged** |
| F2A8 | weaken→**FUSED** overwrite (F1 cross-check) | mech ok, **flagged** | wk refused, ow **refused 109** |
| F2A9 | weaken→KILL_EVIDENCED (kill mirror) | mech ok, **flagged (ck_cite_count 1 vs 4)** | wk refused, kill **refused 109** |
| F2A10 | discount pre-paid (3 cites), weaken, 1 cite, DIRECT | **flagged**¹ | **PASS (0)** — telescoping |
| F2A11 | gen2: full-price DIRECT, then cheap DIRECT on new judgment | **PASS (0)** — birth reset correct | **PASS (0)** |
| F2A12 | TRAINER_DECLARE 90→50 (trainer role), 2 cites, DIRECT | **flagged** | **PASS (0)** — vehicle unpriced² |

¹ Fork-accounting difference (both preserve total price = n(90) = 4): under A, cites must sit
in the `(lss, ow)` window — pre-weaken cites don't count toward the overwrite, so the
attacker must repay `n(HW)` in-window. Under B they telescope through the weaken.
² Requires trainer role (unavailable to a TNN-role attacker via the channel-bound console);
a defense-in-depth gap in B, not a live hole. Demonstrates A's uniformity: **any**
discount vehicle is priced at high-water from the ledger, with no per-op gating.

### Original rt_redteam (regression controls — must not move)

| Case | Baseline (R4) | Fork A | Fork B |
|---|---|---|---|
| A1 weaken0+fused | 0 failures (HOLE) | **1** | wk 109, ow 109 → 0 (refused at mech) |
| A2 weaken10+fused | 0 failures (HOLE) | **1** | wk 109, ow 109 → 0 (refused at mech) |
| A3 weaken10+direct | 0 failures (**THE HOLE**) | **1** | wk refused, **1** |
| A4 dbl-overwrite | 0 (109/0 as expected) | unchanged | unchanged |
| A5 dbl-spend+rollback (F4-replay) | 0 | unchanged | unchanged |
| A6 cite recycle | 0 | unchanged | unchanged |
| A7 fake cites (F5) | 0 | unchanged | unchanged |
| A8i/A8ii | 2001/0; 110/0 | unchanged | unchanged |
| A9 no-prior-write | 103/103 | unchanged | unchanged |
| A11 P3 baseline | 0 | unchanged | unchanged |
| A11b desync (F7) | 1 | unchanged | unchanged |

### r4_overwrite positions a/b/c (R4 ruling-4 regression)

Both forks, all positions byte-identical behavior to baseline: (a) `attack_cites=1
checker_failures=2 ow_effort_flags=1` — the original position-(a) kill stands;
(b)/(c) 0 failures — lawful paths (incl. fused) untouched.

## Kill-criteria verdict

(a) A3 + every fresh variant closed on the direct path — **both forks pass**
(discount directs flagged/refused; legitimate full-price directs pass: F2A5, F2A11).
(b) Every honest trail byte-identical — **both pass** (27 S1 + 4 scale checks each).
(c) Zero RNG, 2× deterministic — **both pass**. (d) R4 fused-overwrite ruling and the
full-erase-price law intact — **both pass** (no price was ever lowered; r4_overwrite a/b/c
identical). (e) F3/F4-replay/F5/F7 controls (A5/A7/A11b) unmoved — **both pass**.

## WINNING FORK: A (checker-side high-water pricing)

Both forks satisfy every preregistered kill criterion. A wins on design merit:

1. **Smallest blast radius.** Checker-only; the mechanism — TNN's action space — is
   completely untouched. `st_weaken` stays free (TNN can still change its mind about
   importance without friction); only *erasure* is priced at high-water.
2. **Uniform across discount vehicles.** Weaken, downward-strengthen, trainer-declare-downward
   are all priced at HW from the ledger (F2A7, F2A12 measured). Fork B needed a
   beyond-spec extension (downward-strengthen) and still leaves the trainer-declare vehicle
   unpriced (F2A12 passes under B).
3. **No new behavioral law.** Fork B makes weakening cost cites — a TNN that deliberates an
   importance-downgrade with no counter-evidence on record would now be *refused*. That is a
   bigger law change than the F2 finding requires, and its desirability is genuinely open.
4. **Matches the program's architecture.** The finding is framed as checker blindness
   ("the checker contract is 'every OK ST_OP_OVERWRITE'"); the R4 hardening already placed
   overwrite verification in the checker. A repairs exactly the blind instrument.

## LAW-CHANGE PROPOSAL (proposed — NOT enacted)

**Proposed amendment to the full-erase-price law** (add one paragraph; everything else stays):

> *High-water erase pricing.* The lawful effort to erase a judgment — by overwrite
> (`ST_OP_OVERWRITE`) or evidenced kill — is `n(HW)`, where `HW` is the maximum strength
> the judgment held at any point during its current lifetime, i.e. since the most recent
> `ADD` or `OVERWRITE` of that slot. A `WEAKEN` or any other downward redeclare does not
> reduce the erase price; it is priced as if the judgment still held its high-water
> strength. `n(s) = ceil(s/25)` is unchanged.

**What changes:** `ck_verify_overwrite` / `ck_verify_kill` compute `need = ck_n(HW)` via
`ck_birth_idx` + `ck_high_water` (non-baseline branch only).
**What stays:** the `n(s)` schedule; the `(lss, idx)` cite window; the JUSTIFY requirement;
P3-baseline uniform tier (`≥1 cite`); `st_weaken` free and mechanism-unchanged; the R4
fused-overwrite ruling; cite genuineness (F5); rollback/replay semantics (F4).

**Why the losing fork (B) lost:** larger behavioral change (weakening now costs cites —
a new law about when strength may decrease, with the open normative question of
deliberative downgrades without counter-evidence); per-op gating burden (needed the
downward-strengthen extension; trainer-declare still unpriced); no advantage on any kill
criterion. B remains a coherent defense-in-depth option if fail-closed at the mechanism
is wanted *in addition* — but not instead.

**What remains Micah's call:**
1. Sign (or amend) the high-water law text above — the only law change proposed.
2. Detection-vs-prevention: under A, a discount direct/fused overwrite still returns
   `rc=0` at the mechanism; only the checker flags it. Acceptable under the standing
   "checker-verified trails" contract, but if any consumer trusts un-checked ledgers,
   say so and B (or A+B) can be deployed.
3. F2A10 accounting: under A, pre-weaken cites don't count toward the overwrite
   (repay `n(HW)` in-window); under B they telescope. Both preserve total price.
   If telescoping is preferred, that's an argument for B's accounting — speak now.
4. Whether `st_weaken` *should* cost effort as a matter of law (B's premise) — I recommend
   no, but it's a real design question, not settled by this fix.
5. The F1 crew's fused-path mechanism fix is orthogonal and still theirs; my F2A8
   cross-check only confirms A flags the weaken→fused shape at the checker.

## Files

- Report: `~/workspace/strength-f1f2f4/f2/F2_FIX_REPORT.md` (this file)
- Fork-A checker (applied): `strength_checker.zag`, `r4val/trial/strength_checker.zag`
  (byte-identical); reference copy `logs/ref/strength_checker_forkA.zag`
- Fork-B cores (reference): `logs/ref/strength_core_forkB.zag`,
  `logs/ref/r4val_strength_core_forkB.zag` (differ from pristine only in `st_redeclare`)
- Pristine backups: `pristine_backup/` (SHAs match `EVIDENCE_MANIFEST.md`)
- Attack driver: `r4val/f2_attack.zag` (12 variants, F2A1–F2A12)
- Logs: `logs/baseline/` (pre-fix), `logs/forkA/`, `logs/forkB/` (honest/ + attack logs)
- Binaries (`*_forkA`, `*_forkB`, `*_base`) are workdir artifacts — do not commit.
