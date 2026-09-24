# PREREG — D1 Defense-Stack Battery (G1 + MG6 + H6)

**Date:** 2026-09-24. **Crew:** D1 defense-stack battery crew (subagent).
**Branch:** `tnn-native-lab` (sylorlabs/TNN). **Status:** FROZEN — committed alone
before any build output. This document is the single source of truth; the
generator (`gen_d1.py`), the Zag battery (`stack_main.zag`), and the scorer
(`score_d1.py`) all derive from it. No transcription.

## 0. F5 exclusion (forced, not silent)

R3-4 as ranked assumed F5 (negative-bank block) in the stack. The
300-percept red-team KILLED the frozen F5 predicate (94/300 = 31.3% delayed
>50 trials vs the 25% bar; `round2/f5_redteam300/VERDICT_F5_REDTEAM300.md`).
A killed mechanism is not composed into the stack. The battery therefore
tests the **surviving** defense stack **G1 + MG6 + H6**, and reports honestly
how it handles the 8 TMB-5 false accepts that F5 used to block (Leg 1 §4).

## 1. Stack composition (frozen order: gate → guard → hardening)

A trial stream is processed per task-code (tcode) through three ordered
stages. A candidate installs **only if it survives all three**. Truth is
passed through to disposition output for scoring and is NEVER read by any
stage (static check: `truth` appears only in field-copy/output code).

### Stage 1 — GATE = G1 (cf1 historical-corroboration)

Exact port of `v2/contradiction_matrix/src/cm_main.zag::g1_step`
(AUTOPSY_R2-4 §4). Per-tcode state: provisional slot, permanent slot,
challenger slot. Input per trial: `(tcode, prog, jcode, conf, pred, meas)`.
Output: gate event per trial.

- `prog != 0` or `pred != 1` → `WITHHELD` (no state change).
- perm exists, same jcode, `|Δmeas| ≤ tol(tcode)` → `CORROBORATED`.
- prov exists, no perm, same jcode, `|Δmeas| ≤ tol`, `conf ≥ 700` →
  **PROPOSE `PERMANENT_INSTALL`** (corroborator pair = stored prov + incoming).
- incumbent (perm, else prov) exists, jcode differs (conflict):
  - `conf ≥ 700` and challenger slot matches (same jcode, `|Δmeas| ≤ tol`) →
    **PROPOSE `REVISED_INSTALL`** (corroborator pair = stored chal + incoming).
  - `conf ≥ 700`, no match → store challenger → `CHALLENGER_PROV`.
  - `conf < 700` → `CONFLICT_WITHHELD`.
- incumbent exists, same jcode, outside tol → re-anchor prov → `PROVISIONAL`.
- no incumbent → store prov → `PROVISIONAL`.

Tolerances (frozen): colordisc 8, colorconst 40, shapetrans 60,
pitchdisc 4000, timbredisc 120, motiondir 0.

### Stage 2 — GUARD = MG6 (three-fold independence)

Applied to **every** install proposal (first-install corroborated pair AND
revision pair — the corroborated-install point, of which G1's revision point
is the verified instance). Input: the corroborator pair's
`(mrgF, seq, span_a, span_b)` for stored + incoming. Output: ALLOW or VETO.

**Exact frozen rule** (from `round2/cc1_guard/VERDICT_CC1_GUARD.md`):
allow `REVISED_INSTALL`/`PERMANENT_INSTALL` iff **all three** hold, else veto:
1. `min(mrgF_stored, mrgF_incoming) ≥ 400`;
2. spans disjoint: NOT (`sa_stored < sb_incoming` AND `sa_incoming < sb_stored`)
   (touching counts as disjoint);
3. `|seq_stored − seq_incoming| ≥ 20`.

Veto → proposal demoted, **no install**, gate state reverts to pre-proposal
(stored corroborator retained): vetoed `REVISED_INSTALL` → incoming
`CHALLENGER_PROV`; vetoed `PERMANENT_INSTALL` → incoming `PROVISIONAL`
(candidate retained). The veto arm that fired is recorded
(`guard-veto:margin|span|temporal`).

### Stage 3 — HARDENING = H6 (install-path rules)

Applied to every guard-allowed proposal. Exact port of the install-path
checks in `v2/hardening/H6/src/vgate_h6.zag` (R1–R4, no-provisional):
- **R1** prog gate: proposal's trials must be `prog = PASS`.
- **R2** channel attestation: both corroborators' channel tags verify —
  `hex(sha256("PAMV2-REG-CHANNEL-2026-09-23"|seq|fixture|jG|confG))` equals the
  gatt sidecar entry (the 8 spoofed decoy records carry the all-zero tag and
  fail here, as committed).
- **R3** attested-agreement bar: both corroborators `conf ≥ 700`,
  `jG == jcode`, `confG ≥ 700`, attested.
- **R4** revision margin: for `REVISED_INSTALL` against an installed
  permanent — historical corroboration (≥1 prior same-task same-jcode PASS
  trial within tol, from the trial history) AND
  `conf_incoming − conf_perm ≥ 100`.
- No-provisional: satisfied by construction (proposals are corroborated
  pairs; single observations never reach this stage).

Any check fails → `WITHHELD` (`harden-<reason>`), state reverts. All pass →
final `PERMANENT_INSTALL` / `REVISED_INSTALL`, state commits per G1.

### Input/output contracts

- Gate in: ordered trial stream `(seq,tcode,prog,jcode,conf,pred,meas,mrgF,
  truth,jG,confG,span_a,span_b,fixture)`. Gate out: per-trial gate event +
  install proposals with corroborator pairs.
- Guard in: each proposal + pair `(mrgF,seq,span)` ×2. Guard out:
  ALLOW → proposal; VETO → demoted disposition (above), state retained.
- Hardening in: each allowed proposal + gatt sidecar + trial history.
  Hardening out: final per-trial disposition
  `(leg,trial_idx,seq,disposition,detail,truth,judgment)`; INSTALL only if all
  three stages pass.

## 2. Fixture battery (frozen, all from the branch)

### Leg 1 — 43 V2-D ACCEPT_INSTALL candidates (KILL-BAR LEG)

The F5 backtest ledger (`v2/f5_backtest/run1.out`): 43 candidates =
9 false accepts (8 TMB-5 RICH/DARK + 1 COL-4 DIFFERENT/SAME) + 34 true
accepts. Replayed **as install candidates in ledger order** (which is
strict seq order), with **frozen replay framing**:
- `prog = PASS`, `pred = 1` for all 43. (The records carry `prog =
  UNRESOLVED`; the candidate set is DEFINED as V2-D's accepted installs and
  F5's candidate list, and F5's predicate never read prog. Replaying them as
  UNRESOLVED would make every stage withhold trivially and test nothing.
  The UNRESOLVED origin is documented as the V2-D regression context that
  the hardening already fixed.)
- All other fields verbatim from `v2/redteam/evidence/rec_withhold.records`
  (seq, tcode, jcode, judgment, conf, meas, phash, truth, jG, confG);
  original withhold-stream seqs kept (0–118) so the guard's `|Δseq|` sees
  true temporal geometry; attestation from committed
  `v2/hardening/gatt/withhold.gatt` (all 43 tags verified recomputed-clean
  2026-09-24).
- `mrgF := measure` (frozen substitution; the record format carries no
  margin — same substitution the F5 backtest documented for the same reason).
- `(span_a, span_b)` derived deterministically from the trial's `phash`:
  `span_a = u32be(phash[0:8]) mod 20000`,
  `span_b = span_a + 1 + (u32be(phash[8:16]) mod 4000)`.
  Documented synthetic (the record format has no spans); per-arm veto
  attribution is recorded so span-arm vetoes are identifiable as
  synthetic-geometry artifacts.

### Leg 2 — 12 sustained TMB-5 cross-span wrongs (KILL-BAR LEG)

`v2/redteam/evidence/rec_install.records` trials seq 24–35 (12 consecutive
RICH judgments, truth DARK/BRIGHT, conf 764–832, meas 1888–2373), fields
verbatim, original seqs, attestation from committed
`v2/hardening/gatt/install.gatt` (tags verified recomputed-clean),
same `mrgF`/`span` frozen rules as Leg 1. This is the sustained correlated
attack the guard must refuse.

### Leg 3 — 10 contradiction-matrix cells (GUARD-GEOMETRY LEG)

The 10 CM cells (C1, C2, C3, R1, R2, CC1, CC2, H1, T1, W1) with the EXACT
trial rows from `round2/cc1_guard/gen_guard.py` (frozen `(tcode, prog, jcode,
conf, pred, meas, mrgF, truth, jG, confG, seq, span_a, span_b)` literals —
the verified guard geometry, including the CC1 wrong pair
mrgF 382/358 and the C1/CC2 correct pairs). Attestation: gatt tags generated
with the frozen registered-channel key for fixture string `{cell}#{idx}`;
all cell trials are genuine (non-spoofed) by construction. Per-trial EXPECT
frozen in §5.

### Leg 4 — 288-fixture redteam streams (REGRESSION LEG)

The four committed gate record streams
(`v2/redteam/evidence/rec_{clean,withhold,install,decoy}.records`;
288+288+44+52 records over the 12 fixture families × 24) with committed
gatt sidecars, fields verbatim (real prog values — UNRESOLVED withholds),
same `mrgF`/`span` frozen rules. Aggregate bars only (§6): the kill-bar
false-install count runs over this leg too.

## 3. What the battery measures (frozen)

- **False installs** (kill bar a): any trial where the stack emits
  `PERMANENT_INSTALL` or `REVISED_INSTALL` with `judgment != truth`,
  over Legs 1–4.
- **True retention** (kill bar b): of the 34 TRUE candidates in Leg 1, how
  many the stack installs (final `PERMANENT_INSTALL`/`REVISED_INSTALL`).
- **Per-arm guard attribution**: for every veto, which arm(s) fired.
- **Honest F5-less report**: how the 8 TMB-5 false accepts (Leg 1 idx
  16,19,21,22,24,25,27,29) are handled with no F5 in the stack —
  per-trial dispositions.

## 4. Kill bars (R3-4, frozen)

- **KB-D1a:** ANY false install through the full stack on the frozen trials
  → **KILL** the stack as sufficient (return to per-layer analysis).
- **KB-D1b:** true-install retention < 26/34 → **KILL** the conjunction as
  too costly; layers must be re-tuned separately.

## 5. EXPECT derivation (frozen method)

`gen_d1.py` (deterministic Python glue, zero RNG) builds
`stack_records.zag` (all legs' trial tables), the cell/stream gatt files,
`EXPECT_D1.tsv` (leg, trial_idx, expected disposition code, expected
install flag), and `EXPECT_D1_CELL.tsv` (per-leg install/false-install
counts) from a Python mirror of the §1 rules. The mirror is
**hand-verified** on every kill-bar-critical trial:
- all 9 false candidates must not install (traced: 3 reach proposals and
  are guard-vetoed on the temporal arm; 6 never form proposals);
- the 4 true proposals and why each is vetoed (all temporal arm, `|Δseq|`
  1–5 < 20);
- the CC1 cell: wrong pair vetoed on the margin arm
  (min(382,358) < 400).
The Zag battery is an independent implementation; the scorer requires its
output to match EXPECT exactly. A shared misreading is guarded against by
the hand-verification, not by the mirror.

Disposition codes (frozen, same as the matrix): 0=PERM 1=PROV 2=CORR
3=CONF 4=CHAL 5=REV 6=ACC 7=WITH.

## 6. Leg 4 aggregate bars (frozen)

- 0 false installs across all four streams (kill bar (a) covers this leg).
- Install/withhold counts reported per stream; no per-trial assertions
  (regression sweep, not a kill-bar leg).

## 7. Determinism and toolchain

- Pure Zag battery (`stack_main.zag` + generated `stack_records.zag` +
  byte-identical copies of `R33_NATIVE_IO_V1.zag`,
  `R33_NATIVE_SHA256_V2.zag`); Python only for glue (generator + scorer).
- Zero RNG. Three runs per stream; byte-identical stdout required
  (sha256 match across run1/run2/run3).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Workdir: `~/workspace/pam_round2/d1_stack/` (NOT /tmp).
- znc gotchas honored: `[]u8` arenas with explicit LE accessors (no
  consecutive same-size `as []i32` casts); `.*` only on pointers; `@import`
  relative to cwd; no `};`; no identifier named `try`.

## 8. Honest limits (frozen, not post-hoc)

1. `mrgF := measure` and phash-derived spans on stream trials are
   substitutions; the guard's margin arm is calibrated on the CC1-family
   geometry, not on stream measures (colordisc measures 71–343 sit below
   the 400 floor by construction of the substitution, not by evidence).
2. The 43-candidate `prog = PASS` replay is a modeling choice (documented
   above); the UNRESOLVED origin is the V2-D regression context.
3. Cell gatt tags are generated (frozen key), not committed sidecars.
4. MG6's verified scope (single-task cells, tcode 0/4) carries over; the
   V9 ceiling (wrong pair strong on all three axes defeats the guard)
   is inherited by the stack. The stack adds H6's R4 margin (≥100), which
   is stricter than G1+MG6 alone (e.g. it withholds C1's correct revision,
   mrg 77 < 100).
5. Cross-task interference untested; G2's D-fired path not in the stack
   (G1 only, per the task).

## 9. Artifacts

- This prereg (committed ALONE).
- Then: `gen_d1.py`, `stack_main.zag`, `stack_records.zag` (generated),
  `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` (byte-identical copies),
  `gatt_leg{1,2,3}.txt` (leg3 generated), `score_d1.py`,
  `evidence/run{1,2,3}_*.txt`, `evidence/DIGESTS.txt`,
  `RUNLOG_D1_STACK.md`, `VERDICT_D1_STACK.md`.
