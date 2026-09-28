# Strength Round 4 Follow-up — F1/F2/F4 Iteration Synthesis (Coordinator)

Date: 2026-09-26. Ordered by Micah 2026-09-25 ~19:09 PDT: "for F1 iterate and test
more on top of this same for f2 for f4 same thing."
Toolchain (pinned for all builds): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Workdirs: `~/workspace/strength-f1f2f4/{f1,f2,f4}/`. Nothing here was committed by
the crews; this synthesis assembles their three fix reports and my independent
verification. **No law changes are enacted — the amendments below are proposed
for Micah's signature only.**

## Headline

| Finding | Hole | Winning fix | Loser |
|---|---|---|---|
| F1: weaken→fused-overwrite discount | `st_weaken(90→0)` free, then overwrite/kill at `n(0)=0` cites | **Fork A: high-water erase pricing** (`st_epoch_highwater`, mechanism + checker share one function) | Fork B: effort gate on downward weaken (patch preserved) |
| F2: weaken bypasses R4 position-(a) | test-only `st_overwrite_direct` + weaken looks properly priced to the checker | **Fork A: checker-side high-water pricing** (`ck_birth_idx`/`ck_high_water`, mechanism untouched) | Fork B: mechanism effort gate on downward redeclare (reference cores preserved) |
| F4: kill→rollback→overwrite double-spend | 4 cites pay for kill; rollback restores; same evidence pays overwrite again | **Fork F4b: single-use effort cites** (consumed cites can't pay twice in a window; new `ST_REFUSED_CONSUMED=121`) | Fork F4a: lss-reset (patch preserved; leaves V4 hole, false-positives V1) |

F1 and F2 converged independently on the same law concept (high-water pricing);
their fixes compose: F1's is mechanism+checker on the fused path, F2's is
checker-only covering every overwrite including the direct test hook. F4's fix is
orthogonal (cite single-use within an effort window).

## F1 — weaken→fused-overwrite discount (winner: high-water erase pricing)

**Baseline hole (measured):** A1 (weaken 90→0 → justify → fused overwrite):
`ow_rc=0` — open. A2 (weaken 90→10, 1 cite): `ow_rc=0` — open. Double-weaken,
weaken→kill_evidenced, and downward-`st_strengthen` relabel: all open on baseline.

**Winner — Fork A.** `st_kill_effort_check` prices `st_n(HW)` where HW = max
strength *written* since the judgment's most recent successful ADD/OVERWRITE
(birth-based window `[birth, upto)`), floored by current strength; FULL-stage
follows the same mark (HW>50 ⇒ FULL). New shared helper `st_epoch_highwater()`;
the checker calls the *same function* — lockstep by construction. WEAKEN stays a
free judgment re-declaration; only destruction is priced.

**Window correctness (cross-crew catch):** the F2 crew found a literal
`[lss, ow_idx)` scan is a singleton (WEAKEN is itself a strength-write, so
`st_last_strength_idx` returns the weaken index → HW=0 → no-op fix). The F1 crew
verified by direct probe (`logs/forkA/hw_probe.log`, 2×): `HW_BIRTH=90` vs
`HW_LSS=0`, `OW_RC=109`. Their implementation never had the bug.

**Kill table (2× byte-identical):** every baseline-open attack → `109` refused
under A (A1, A2, double-weaken, weaken→kill, strengthen-relabel); legitimate
paths pass (free weaken + 4 fresh cites + justify → `ow_rc=0, cf=0`).
**Honest regression:** 27/27 S1 vs `evidence_r4f` + 6/6 B-arm S10/S100 vs
`evidence_r4` byte-identical. r4_overwrite a/b/c and rt_redteam controls (A5/A7/A9/A11B)
byte-identical to baseline.

**Why B lost:** larger change (new gate + refusal code + checker fn + two-payment
telescoping); first build bypassed by the strengthen-relabel variant; taxes
judgment revision itself; the legitimate path costs an extra justify. Not a missed
attack — design grounds.

## F2 — free weaken bypasses position-(a) (winner: checker-side high-water pricing)

**Baseline hole:** A3 = `st_weaken(x,10)` → 1 cite → justify → `st_overwrite_direct`
→ `rc=0`, `before=10/after=50`, checker 0 failures. R4's position-(a) kill erased.

**Winner — Fork A (checker only, mechanism untouched).** `ck_verify_overwrite` /
`ck_verify_kill` price `n(HW)`, HW = max after-strength over OK strength-writes in
`[birth, idx)`, birth = most recent OK ADD/OVERWRITE. 45 changed lines; both checker
copies byte-identical; both core copies pristine (verified by diff against
`pristine_backup/`).

**Kill table (12 fresh variants, 2× byte-identical):** A3 + all variants (weaken→0,
double-weaken, strengthen-downward, weaken→fused, weaken→kill, pre-paid discount,
strengthen-then-weaken, trainer-declare-downward) → **flagged**; legitimate
full-price directs → **PASS (0)**; second-generation judgment (birth reset) → PASS.
Original R4 position-(a) kill preserved (still 2 failures); r4_overwrite a/b/c
byte-identical. F3/F4-replay/F5/F7 controls (A5/A7/A11b) unmoved.

**Why B lost:** weaker uniformity — needed a beyond-spec extension for
downward-strengthen and still leaves the trainer-declare vehicle unpriced
(F2A12: A flags, B passes); and B makes weakening cost cites, a bigger
behavioral law change with an open normative question (deliberative downgrades
with no counter-evidence would be refused).

## F4 — kill→rollback→overwrite double-spend (winner: cite-consumption F4b)

**Baseline hole:** A5 = 4 cites → KILL_EVIDENCED → ROLLBACK → OVERWRITE with 0 new
cites → `ow_rc=0` — the same evidence pays for two destructions.

**Winner — Fork F4b.** A `cite_ep` counted toward an OK destruction's effort price
is CONSUMED: it cannot count toward any later destruction on the same slot while
the consuming destruction is inside the later destruction's effort window.
New `ST_REFUSED_CONSUMED=121` (mechanism, mirrored in `ck_verify_kill` /
`ck_verify_overwrite`); ledger-derived consumed-sets, no new state; arm-B free
kills stay free (a free kill pays nothing, consumes nothing).

**Kill table (2× byte-identical):** A5 → `ow=121` closed; V1B/V2/V2B/V3 → closed;
**V4 (re-cite same 4 episodes after rollback)** → recites `111`×4, `ow=121` closed;
V5 (forced direct) → checker-flagged. **V1 (free kill→rb→ke, 0 new cites) passes
(`ke=0`) — judged legitimate:** 1 payment → 1 paid destruction; the free kill is
arm-B law and consumed nothing (net-destruction accounting). F4a over-strictly
refuses V1 (109, charges twice for 1 net destruction) and leaves V4 passing
(`ow=0` — 2 destruction ops, 1 payment: the actual hole).
**Honest regression:** 45/45 byte-identical per fork (27 S1 + 18 B-arm S10/S100).
Controls: only RT_A5 differs from pristine (by design); A1/A2/A3/A4/A6/A7/A8/A9/A11/A11B
identical; r4_overwrite a/b/c identical — fused-overwrite ruling and
full-erase-price law intact.

**F6 note (accurately scoped):** F4b does NOT close round-4's F6 (cite-recycling
across strength-write boundaries) — verified empirically (ow#1→re-cite→ow#2
still passes). Consumption is window-bounded; global single-use would be a
further law change (Micah's call).

## Independent coordinator verification (this turn, fresh builds from applied sources)

- **Builds:** rebuilt 6 binaries from the exact applied sources with the pinned
  toolchain (F1/F2 trials, F1/F2/F4b attack drivers). All built clean.
- **Honest cells:** freshly built F1/F2/F4b trial binaries each ran B×VUP×var0×S1
  **byte-identical** to the frozen `evidence_r4f/` reference. (`verify/` logs)
- **Attack spot-checks:** F1 A1/A2 → `ow_rc=109` closed ✓. F2 A3-shape →
  `checker_failures=1` flagged (ck_ow_effort 1 vs 4) ✓. F4b A5 → `ow_rc=121` ✓;
  F4b V4 → `ow_rc=121` ✓; F4b V1 → `ke=0` (legitimate per §5 analysis) ✓.
- **Source-structure checks:** F1 checkers byte-identical ✓; F2 cores pristine vs
  backup, checkers byte-identical ✓; F4b checkers byte-identical ✓; root↔trial core
  copies differ only by the test-only `st_overwrite_direct` hunk ✓; trial/learner
  sources unchanged by all forks ✓; F2's `[birth, idx)` window and F1's birth-based
  `st_epoch_highwater` confirmed in source ✓.
- **F4 §1 base defect — CONFIRMED INDEPENDENTLY:** built the F4 attack driver
  against the **pristine, md5-verified unmodified** `f4/r4val/trial/strength_core.zag`
  (`4c928c29b9a2d4fc79d153fecba1e381`) → `panic: slice index out of bounds` during
  the kill→rollback→recite shapes. Root cause in source: `st_evidence` allocates a
  16-byte cite buffer (4 i32 slots); `st_collect_cites` writes at most 4 but returns
  the *true* distinct count (unbounded); the dup-check then reads `buf[k*4]` for
  `k<n` — after kill→rollback the window holds 8 distinct cites, the 5th read runs
  past the buffer. `st_collect_cites`' own seen-scan carries the same latent
  read-past-4 hazard. This panic is reachable on the committed Round-4 code by any
  kill→rollback→recite trail; it never fired in R4 because no R4 trail put >4
  distinct cites in one window. It is fixed inside the F4b fork only (bufferless
  ledger scans, semantics-neutral on non-panicking inputs — proven by the 45/45
  regression). Repairing the pristine base copy is Micah's call.

## Proposed law amendments (FOR MICAH'S SIGNATURE — not adopted)

### Amendment H — high-water erase pricing (F1 + F2)

> The effort price of destroying a memory (`st_kill_evidenced`,
> `st_overwrite`) is `n(HW)`, where HW is the **high-water mark**: the maximum
> strength written to the slot since its most recent successful ADD or OVERWRITE
> (the judgment epoch), including the current strength. A `WEAKEN` or any other
> downward re-declaration does not reduce the erase price; destruction is priced
> as if the judgment still held its high-water strength. Citation windows, the
> exact-count rule (`cnt==need`), and justification requirements are unchanged;
> the FULL-stage requirement follows the same mark (HW>50 ⇒ FULL stage).
> `WEAKEN`/`STRENGTHEN` remain free judgment re-declarations. `n(s)=ceil(s/25)`
> is unchanged.

Rationale: the price must attach to the strongest judgment destroyed, not to
whatever strength the slot happens to hold after free re-declaration.

### Amendment F4 — single-use effort cites

> A citation episode (`cite_ep`) counted toward the effort price of an OK
> destruction (`ST_OP_KILL_EVIDENCED` or `ST_OP_OVERWRITE` with rc=`ST_OK`) on a
> slot is CONSUMED: it cannot count toward the effort price of any later
> destruction on the same slot while the consuming destruction remains inside
> the later destruction's effort window. A destruction following a rollback of
> an OK destruction must therefore bring fresh citation episodes;
> re-presenting consumed episodes is refused (`ST_REFUSED_CONSUMED`=121 at the
> mechanism, mirrored by `ck_verify_kill` / `ck_verify_overwrite` in the checker).

What stays: arm-B free kills remain free (a free kill pays no effort, consumes
nothing — the F4-V1 shape stays legitimate); strength-writes and OK destructions
still reset effort windows; the dup-cite rule, erase price `n(strength)`, and
justify requirement unchanged; fused-overwrite ruling, R4 hardening
(F3/F4-replay/F5/F7), and the F1/F2 findings untouched.

## What remains Micah's call

1. Sign (or amend/reject) Amendment H — high-water erase pricing.
2. Sign (or amend/reject) Amendment F4 — single-use effort cites (incl. the new
   121 refusal code).
3. F2 detection-vs-prevention: under F2's fork A, a discount *direct* overwrite
   still returns `rc=0` at the mechanism; only the checker flags it. F1's fork A
   closes the *fused* path at the mechanism. If any consumer trusts un-checked
   ledgers, F2's fork B (or A+B) is the defense-in-depth option.
4. F2A10 accounting: under A, pre-weaken cites don't count toward the overwrite
   (repay `n(HW)` in-window); under B they telescope. Both preserve total price.
5. Whether `st_weaken` *should* cost effort as a matter of law (the losing forks'
   premise) — both crews recommend no; open normative question.
6. F6 stays OPEN under F4b (verified). Global single-use cite tokens would close
   it — a further law change.
7. The §1 base defect: repair the pristine base copy (panic on
   kill→rollback→recite shapes), or leave the repair inside the F4b fork only.
8. The F4 V1/V4 readings are encoded in the proposed F4 text (net-destruction vs
   destruction-operation accounting); he may prefer F4a's stricter-window reading.

## Residual risks

- F4a's "fresh ledger entries per window" rule is strictly weaker than F4b; if the
  F4b amendment is rejected, V4 (same-episode replay after rollback) stays open.
- F2's checker-side fix does not prevent at the mechanism on the direct path; a
  consumer that never runs the checker sees `rc=0`.
- F1/F2 high-water pricing is conservative on rolled-back strengthens (a
  rolled-back strengthen's written peak still counts toward HW) — deliberate,
  flagged in the F1 report.
- The §1 buffer defect exists in the committed Round-4 code; any future trail
  that accumulates >4 distinct cites in one effort window panics the binary
  (uncontrolled crash, not a clean refusal).

## File inventory (this commit)

- `SYNTHESIS_F1F2F4.md` — this file.
- `f1/F1_FIX_REPORT.md`, `f1/patches/` (fork-A diffs vs pristine ×4 files),
  `f1/logs/` (baseline/forkA/forkB attack + honest logs), `f1/r4val/f1_attack.zag`.
- `f2/F2_FIX_REPORT.md`, `f2/patches/` (fork-A checker diffs vs pristine ×2),
  `f2/logs/` (baseline/forkA/forkB/sanity), `f2/r4val/f2_attack.zag`.
- `f4/F4_FIX_REPORT.md`, `f4/patches/` (F4b ×4, F4a core for the record),
  `f4/logs/` (attack r1–r4, regressions, controls), `f4/r4val/f4_attacks.zag`.
- `verify/` — coordinator verification log (fresh-build honest-cell diffs,
  attack spot-check outputs, pristine-panic reproduction log).
- No binaries, no `.zagd`, no cache files. All attack runs 2× byte-identical,
  zero RNG, pinned toolchain throughout.
