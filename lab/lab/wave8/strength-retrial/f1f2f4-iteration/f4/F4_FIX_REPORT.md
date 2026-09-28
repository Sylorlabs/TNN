# F4 FIX REPORT — cite-consumption (F4b) vs lss-reset (F4a)

Date: 2026-09-26. Crew: F4 iteration, continuation (crew 2).
Workdir: `~/workspace/strength-f1f2f4/f4/`. Forks: `f4a/`, `f4b/`.
Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Standing rules kept: pure Zag, zero RNG in decision paths, every attack 2×
byte-identical, real mechanisms not stubs. No git commits made; no binaries
committed; sibling `f1/`/`f2/` untouched; pristine `f4/` root copies untouched.

## 1. Bisection outcome — the F4b "miscompile" was a BASE bug, not a miscompile

Crew 1 was blocked: FA_V2 panicked (`panic: slice index out of bounds`) during
the second cite round under F4b, and stubbing the new functions to `return 0`
did not remove it, suggesting a compile-level miscompile.

Crew 2 re-ran the bisection from the PRISTINE core
(`f4/r4val/trial/strength_core.zag`, md5-verified unmodified) in a clean
scratch dir with a minimal probe (cite4 → `st_kill_evidenced` → `st_rollback_last`
→ cite4 → …). **The pristine core panics identically**, at the second
`st_evidence` call of round 2 (ep 22). The miscompile theory is retracted.

**Root cause** (base defect, both `st_evidence` and `st_collect_cites`):
`st_evidence`'s dup check allocated a 16-byte buffer, `st_collect_cites`
writes at most 4 i32s into it (`if(n<4)` guard), but the dup-read loop ran
`while(k<n)` with `n` = the TRUE distinct count. After kill→rollback the
effort window accumulates 8 distinct cites (4 + 4); at the 5th distinct cite
the loop reads `st_i32_get(buf,16)` — past the buffer → panic.
`st_collect_cites`' internal seen-scan has the same latent read-past-4 hazard
(one step later, at the 6th distinct cite). This is reachable on the pristine
core by any kill→rollback→recite shape; it never fired in R4 because no R4
trail put >4 distinct cites in one window.

**Fix applied inside the F4b fork only** (both core copies,
`f4b/strength_core.zag` and `f4b/r4val/trial/strength_core.zag`; checkers need
no change — they never read the buffer):
- `st_collect_cites`: distinctness ("seen") decided by a direct ledger scan
  instead of re-reading `out`; the 4-write cap stays; the returned distinct
  count is unchanged.
- `st_evidence` dup check: direct ledger scan over `(lss, audit_n)`; the
  16-byte alloc/free is gone.
Both rewrites are **provably identical to the old code on every input where
the old code did not panic** (for ≤4 distinct cites the old scans were exact,
and the new scans compute the same predicate). Proof: 45/45 honest cells
byte-identical (§3) and all control drivers byte-identical to pristine (§4).
F4a was left untouched (its lss-reset only shrinks windows; the hazard is
unreachable there). Whether the pristine base copy gets the same repair is
Micah's call (noted in §7).

## 2. Per-fork diff summary (vs pristine)

**F4a — lss-reset** (10 changed lines per core copy, checker untouched):
`st_last_strength_idx` also returns on `ST_OP_KILL` / `ST_OP_KILL_EVIDENCED`
with rc OK. A kill is a destruction, so it becomes an effort-window boundary:
after kill→rollback the pre-kill cites fall outside the next destruction's
window. Rule in effect: *4 fresh ledger entries per destruction*.

**F4b — cite-consumption** (96 changed lines per core copy, 35 in checker):
- New `ST_REFUSED_CONSUMED:i32=121`.
- New `st_cite_consumed(s,slot,cite_ep,after_idx,upto)`: 1 iff `cite_ep` sits in
  the effort window of an OK `KILL_EVIDENCED`/`OVERWRITE` on the same slot
  with index in `(after_idx, upto)`. Ledger-derived, no new state, no new
  entries — the checker recomputes the identical predicate.
- New `st_count_spent_cites(s,slot,after_idx,upto)`: distinct OK cites in the
  window consumed by an earlier destruction (own ledger-based distinctness
  scan, no buffer).
- `st_kill_effort_check`: `cnt = total − spent`; only FRESH cites count.
  `cnt≠need` with `spent>0` → `ST_REFUSED_CONSUMED` (121), else
  `ST_REFUSED_EFFORT` (109).
- Checker mirrors in `ck_verify_kill` / `ck_verify_overwrite` (fresh-count +
  genuineness only on unconsumed cites). Both checker copies byte-identical.
- Plus the §1 bufferless fix (2 comment-tagged hunks per core copy).
Rule in effect: *episodes are single-use tokens within an effort window*.

## 3. Honest regression — both forks 45/45 byte-identical

Trial binary rebuilt per fork (`trial_bin_f4a`, `trial_bin_f4b`).
S1: all 27 cells (B/C/C-P3 × VUP/WBS/JI × var 0–2) vs `evidence_r4f/`.
S10/S100: B × VUP/WBS/JI × var 0–2 (18 cells) vs `evidence_r4/` r1 logs.
Logs: `f4/logs/reg_f4a/`, `f4/logs/reg_f4b/`.

| fork | S1 (27) | S10/S100 (18) | total |
|------|---------|---------------|-------|
| F4a  | 27/27   | 18/18         | 45/45 |
| F4b  | 27/27   | 18/18         | 45/45 |

## 4. Attack kill table (2× byte-identical per fork)

Logs: `f4/logs/fa_f4a_r3.log`/`r4` (re-run by crew 2, matches crew 1's
r1/r2 exactly), `f4/logs/fa_f4b_r3.log`/`r4`.
rc codes: 0=OK, 108=REFUSED_NOROLLBACK, 109=REFUSED_EFFORT,
111=REFUSED_DUPCITE, 121=REFUSED_CONSUMED (new, F4b only).

| attack | shape | F4a | F4b |
|--------|-------|-----|-----|
| A5 | pay 4 → KILL_EVIDENCED → ROLLBACK → OVERWRITE, 0 new | ow=109 CLOSED | ow=121 CLOSED |
| V1 | FREE kill → rb → KILL_EVIDENCED, 0 new cites | ke=109 refused | ke=0 PASSES (legitimate — §5) |
| V1B | ke → rb → ke, 0 new cites | ke2=109 CLOSED | ke2=121 CLOSED |
| V2 | ke → rb → ke (4 fresh) → rb → ow, 0 new | ke1=0,ke2=0,ow=109 CLOSED | ke1=0,ke2=0,ow=121 CLOSED |
| V2B | ke → rb → rb (of ROLLBACK → 108) → ow | ow=109 CLOSED | ow=121 CLOSED |
| V3 | ke → rb → strengthen(95) → ow, 0 new cites | ow=109 CLOSED | ow=109 CLOSED |
| V4 | ke → rb → RE-CITE same 4 eps → justify → ow | recite=0×4, ow=0 **PASSES (hole — §5)** | recite=111×4, ow=121 CLOSED |
| V5 | ke → rb → `st_overwrite_direct` (test-only force) | direct=0, checker_flags=2 (flagged) | direct=0, checker_flags=1 (flagged) |
| C1 | ke → rb → ow with 4 fresh cites | ow=0 pass | ow=0 pass |
| C2 | ke with 4 fresh cites | ke=0 pass | ke=0 pass |
| C3 | ow with 4 fresh cites | ow=0 pass | ow=0 pass |

All attacks `checker_failures=0` except V5 (flagged by design, ≥1 on both).

**Controls vs pristine base** (drivers rebuilt per fork against fork trial
sources; pristine baseline built in scratch for comparison):
- `rt_redteam` 2× identical per fork (`f4/logs/rt_f4a_r1/r2.log`,
  `rt_f4b_r1/r2.log`). Vs pristine, the ONLY delta on either fork is RT_A5
  (double-spend): base `ow_rc=0` (vulnerability) → F4a `ow_rc=109`,
  F4b `ow_rc=121`. A1/A2/A3/A4/A6/A7/A8/A9/A11/A11B byte-identical to base —
  F1/F5/F7 no-regress holds (A1 fused path, A7 fakecite, A11B desync all
  unchanged).
- `r4_overwrite` positions a/b/c: byte-identical to pristine base, 2× each,
  per fork (`f4/logs/ow_f4a_*.log`, `ow_f4b_*.log` run from bisect against
  base). Fused-overwrite ruling (c) and full-erase-price enforcement
  (`R4_T3B: kill_0new_rc=109 kill_1new_rc=0`) intact.

## 5. The two judgment calls

**V1 — F4a's refusal is over-strict; F4b's pass is legitimate.**
FA_V1: a FREE kill (arm-B law: plain `st_kill` costs nothing) → rollback →
`st_kill_evidenced` reusing the original 4 cites. Net-destruction accounting:
paid destruction ops = 1 (the ke; the free kill is free by signed law),
payments = 1 (cites 11–14 + justify — the free kill consumed nothing),
net standing destructions = 1. 1 payment → 1 destruction: legitimate.
F4a refuses (109) because the free kill reset the window — it charges twice
for one net destruction when a free kill intervenes. No exploit exists under
F4b's pass: the next evidenced kill needs 4 fresh cites (V1B: ke2=121), so the
free kill buys nothing beyond the arm-B-law freebie.

**V4 — F4b's refusal is correct; F4a's pass is a genuine hole.**
FA_V4: cite4 → ke1 (pays) → rb → re-cite the SAME 4 episode numbers →
justify → overwrite. Two destruction OPERATIONS occur (ke1 cleared the slot —
a real, observable state transition; the overwrite destroys again) but only
one payment of evidentiary work was ever performed; re-entering the same 4
numbers is not new work. F4a passes (recite=0×4, ow=0) because its rule is
"fresh ledger entries", not "fresh episodes" — an attacker can loop
destroy→rollback→re-cite paying once. F4b refuses (recite=111, ow=121):
episodes are single-use tokens. The law prices destruction operations, not
net standing state; F4b is the tighter, correct reading.

## 6. F4b-blocks-F6 note — accurately scoped

Round 4's F6 (REDTEAM_R4.md): "the same episode can be cited again after every
overwrite… held per the letter — but the effort is not fresh. Flagging for
the law." Crew 1's note said F4b "additionally closes F6". Crew 2 tested it:
**F4b does NOT close the F6-A6 pattern** — probe (`ow#1` → re-cite same
11–14 → `ow#2`, equal strengths) gives `ow2=0, checker_failures=0` under F4b.
`st_cite_consumed` is window-bounded (destructions at/below `after_idx` are
excluded), so cites "refresh" across every strength-write/overwrite boundary,
exactly as in R4. What F4b changes beyond the strict F4 mandate is the
**window-scoped single-use-token principle** itself (plus the new 121 code):
within one effort window, a cite that paid for an OK destruction can never
pay again — this is what closes the rollback-mediated recycling (F4) and the
FA_V4 re-cite. Extending single-use GLOBALLY (which would close F6-A6) is a
further law change and remains Micah's explicit call.

## 7. WINNING fork: F4b

- Closes A5 and every variant (V1B, V2, V2B, V3, V4). F4a leaves V4 passing —
  2 destruction ops for 1 payment — the F4 mandate not fully closed.
- V1: F4b's pass is legitimate (net-destruction accounting, §5); F4a's
  refusal is a false positive that would block coherent TNN behavior (free
  kill → reconsider → deliberate evidenced destroy).
- Honest trails byte-identical (45/45); controls clean (only A5 differs from
  base, by design); zero RNG; deterministic 2× throughout.
- The §1 bufferless fix is semantics-neutral (proven by the regression) and
  was REQUIRED for F4b's scenarios to run at all — cite accumulation across
  rollback is inherent to the F4 fix domain.

## 8. LAW-CHANGE PROPOSAL (for Micah's signature — NOT adopted by this crew)

**What changes:** add Amendment F4 to the full-erase-price law
(Micah's 2026-09-20 ruling: "overwriting a strong memory costs the full erase
price, with no cheap-edit path"):

> *Amendment F4 — single-use effort cites.* A citation episode (`cite_ep`)
> counted toward the effort price of an OK destruction (`ST_OP_KILL_EVIDENCED`
> or `ST_OP_OVERWRITE` with rc=`ST_OK`) on a slot is CONSUMED: it cannot count
> toward the effort price of any later destruction on the same slot while the
> consuming destruction remains inside the later destruction's effort window.
> A destruction following a rollback of an OK destruction must therefore bring
> fresh citation episodes; re-presenting consumed episodes is refused
> (`ST_REFUSED_CONSUMED`=121 at the mechanism, mirrored by `ck_verify_kill` /
> `ck_verify_overwrite` in the checker).

**What stays:** arm-B free kills remain free (a free kill pays no effort, so it
consumes nothing — FA_V1 stays legitimate); strength-writes
(`STRENGTHEN`/`WEAKEN`/`TRAINER_DECLARE`) and OK destructions still reset the
effort window; the dup-cite rule is unchanged; the erase price `n(strength)`
and the justify requirement are unchanged; the fused-overwrite ruling
(position c), the R4 hardening (F3/F4-replay/F5/F7), and the F1/F2 law-level
findings are untouched.

**Why F4a lost:** its "fresh ledger entries per window" rule (1) leaves the V4
same-episode replay hole — 2 destruction ops, 1 payment — and (2) false-positives
on V1, double-charging when a free kill intervenes.

**What remains Micah's call:**
1. Sign the F4 amendment above (or reject / amend it).
2. F6 stays OPEN under F4b (verified: ow→re-cite→ow passes). Global
   single-use tokens would close it — a further law change, his call.
3. The §1 base defect (16-byte cite buffer read-past-end → panic on any
   kill→rollback→recite shape) is fixed inside the F4b fork only; repairing
   the pristine base copy is his call.
4. The V1/V4 analyses (§5) are encoded in the proposed text; he may prefer
   F4a's stricter-window reading instead.

## 9. File inventory (new/changed by crew 2)

- Modified: `f4b/strength_core.zag`, `f4b/r4val/trial/strength_core.zag`
  (§1 bufferless fix; F4b design itself is crew 1's, verified here).
- Rebuilt (not committed): `f4b/trial_bin_f4b`, `f4b/r4val/f4_attacks_f4b`,
  `f4b/r4val/rt_redteam_f4b`, `f4b/r4val/r4_overwrite_f4b`,
  `f4a/r4val/rt_redteam_f4a`, `f4a/r4val/r4_overwrite_f4a`.
- Logs: `f4/logs/fa_f4b_r3.log`, `fa_f4b_r4.log`, `fa_f4a_r3.log`,
  `fa_f4a_r4.log`, `rt_f4b_r1/r2.log`, `rt_f4a_r1/r2.log`,
  `ow_f4a_{a,b,c}.log`, `reg_f4a/` (45), `reg_f4b/` (45).
- Scratch removed: `f4/bisect/` (bisection fully documented in §1),
  `f4b/r4val/probe_a6*` (F6 finding documented in §6).
- Untouched: `f4/f1/`, `f4/f2/`, all pristine `f4/` root and `f4/r4val/` sources,
  all `f4a/` sources, `f4b` checkers (crew 1's, verified byte-identical).
