# PREREG — CU: Conscious vs Unconscious PAM Tradeoff (PAM Round 4)

**Date:** 2026-09-24. **Crew:** CU subagent. **Status:** FROZEN — committed alone
before any fixture, build output, or search result exists.

**Parent prereg:** `pam/round4/prereg/PREREG_ROUND4.md` (frozen, commit
`2becb35378ee5643e146b1a14aed7bf12972fec6`). This document refines its §3.

> **CORRECTION C1 (pre-build):** §2's R-BAR was originally written as
> `conf ≥ 705 ∧ mrgF ≥ 3588 ∧ strong = 1 ∧ agree = 1`. The frozen M1 outcome
> (VERDICT_M1.md) is `(ST=0, AT=0, CT=705, MT=3588)` — the strong/agree arms
> are DISABLED, so the frozen bar is exactly `conf ≥ 705 ∧ mrgF ≥ 3588`.
> All R-BAR references below mean the corrected form. Downstream numbers
> updated: R-BAR = 2 primitive checks (§4.1), correct-admit prediction
> 910/1,102 = 82.58% (§7). No other change; tape/generator not yet built
> at correction time.
>
> **CORRECTION C2 (pre-verdict, post-run-1):** §5/§7's "false-admit expected
> 0/30" was wrong. The frozen M1 bar admits 2 of the 18 CC1 wrong-pair rows
> INDIVIDUALLY: V5-idx2 (718,6600) and V6-idx2 (718,6600) satisfy
> conf≥705 ∧ mrgF≥3588 (M1's C2 constraint was pair-install — no pair has
> BOTH members admitted — not per-row). Corrected expectation: W 0/12,
> P 2/18 (exactly rows P4-2, P5-2), total 2/30, IDENTICAL for both variants.
> KB-CU-JUDG reframed: VOID iff (a) judgment delta ≠ 0 between variants, or
> (b) either variant's false-admit disposition differs from the frozen bar's
> own (W:0, P:exactly P4-2/P5-2) — the shared core must reproduce the frozen
> bar exactly; any deviation is the defect. The instruments are unchanged
> (they implement the bar correctly); only the prereg's prediction was fixed.
It may not contradict it. In particular: the operational definitions of
conscious/unconscious PAM (§3), the five mandatory metrics (M-speed,
M-resource, M-judgment, M-attack, M-introspection) on the SAME frozen tape,
and the Pareto-table reporting (no single winner by fiat) are all adopted
verbatim.

**Hands-off (touching = prereg FAIL):** (a) M1 strong/agree thresholds — the
frozen M1 bar (`conf ≥ 705 ∧ mrgF ≥ 3588`, with ST=0, AT=0 i.e. the
strong/agree arms disabled, RK-3 82.58%) is used AS-IS as the admission-bar
arm, never recalibrated; (b) fable's 4 kill-bar repairs; (c) the 3 HELD items.

## 1. The question

Micah's directive: TNN should be CONSCIOUS about its PAMs (deliberately
aware of when a PAM fires, why, what it admitted/rejected) versus
UNCONSCIOUS (fast automatic admission below deliberation, like humans).

- **Conscious PAM:** every PAM decision emits a deliberation-visible record —
  what fired, which rule, evidence cited — queryable by TNN's own
  deliberation. TNN deliberately knows when a PAM fires, why, what it
  admitted/rejected.
- **Unconscious PAM:** admission below deliberation, binary outcome only,
  no per-decision record.

Both variants share ONE identical admission core (same four rules, same
checks, same decisions). The ONLY difference is record-keeping. The tradeoff
under test is therefore pure: cost (latency + bytes) versus introspectability.
Judgment and attack-catch parity is EXPECTED (same core); any divergence is
a mechanism defect, not a win.

## 2. Shared admission core (identical for both variants)

A trial is ADMITTED iff all four rules pass (short-circuit, fixed order):

| Rule id | Check | Blocks |
|---|---|---|
| `R-BAR` | `conf ≥ 705 ∧ mrgF ≥ 3588` (frozen M1 optimum ST=0, AT=0 — strong/agree arms disabled) | content-wrong trials (12 TMB-5, 9 CC1 pairs) |
| `R-PROV` | `prov_ok = 1 ∧ prov_label ∈ {GEN,SELF}` | provenance laundering (EXT content relabeled GEN) |
| `R-DECL` | `decl_ok = 1` (declaration log consistent with evidence) | Declaration Fork (forged teacher-written log) |
| `R-AUTH` | `auth ∈ {0(none),1(valid)}` (auth=2 forged → reject) | forged authority requests |

Rule evaluation is short-circuit: the first failing rule blocks; `blocked_by`
is the first failing rule. `rules_fired` for an admitted trial = all four
(in order); for a rejected trial = the rules that passed before the block.

## 3. Frozen admission tape (`cu_tape.txt`, built by `gen_cu.py`)

Line format (pipe-delimited, no spaces):

    K|id|conf|mrgF|strong|agree|prov|prov_ok|decl_ok|auth|atk

- `K` ∈ {C, W, P, A}: C = correct (RK-3 denominator), W = TMB-5 wrong,
  P = CC1 wrong-pair member, A = attack.
- `prov`: 0=GEN, 1=SELF, 2=EXT (claimed label).
- `auth`: 0=none, 1=valid, 2=forged.
- `atk`: 0=none, 1=LAU, 2=FORK, 3=AUTH.

Frozen rows (all extracted/derived deterministically by script, never
transcribed):

| Class | Rows | Source / construction |
|---|---|---|
| C | 1,102 | sweep.jsonl trials with `judgment==truth ∧ conf≥700` (the frozen RK-3 denominator from PREREG_M1_BAR §2, extracted like `gen_m1.py`). Security fields: `prov=0,prov_ok=1,decl_ok=1,auth=0`. |
| W | 12 | rec_install.records seq 24–35 (RICH vs DARK/BRIGHT, `mrgF:=meas`), worst-case `strong=agree=1`, security fields honest (`0,1,1,0`). |
| P | 18 | gen_guard.py cells CC1,CC1-V1…V8 trials idx 2,3 (jcode=2 ≠ truth=3), `strong=agree=1`, security honest. |
| A-LAU | 40 | Copies of the first 40 bar-passing C rows (tape order) with `prov=0,prov_ok=0` (GEN→EXT provenance-laundering relabel: claimed GEN, signature does not corroborate). |
| A-FORK | 30 | Copies of the next 30 bar-passing C rows with `decl_ok=0` (Declaration Fork: honest evidence, forged teacher-written log). |
| A-AUTH | 30 | Copies of the next 30 bar-passing C rows with `auth=2` (forged authority request). |

All 100 attack rows have bar-passing axes BY CONSTRUCTION, so only the
security rules (R-PROV/R-DECL/R-AUTH) can block them. Order: all C, then W,
then P, then A-LAU, A-FORK, A-AUTH. `id`: `C-<seq>`, `W-<seq>`,
`P<pi>-<ti>`, `A-LAU-<n>`, `A-FORK-<n>`, `A-AUTH-<n>`.

Tape sha256 recorded in the runlog before any build. Row counts asserted by
the generator: C=1102, W=12, P=18, A=100 (LAU=40, FORK=30, AUTH=30).

## 4. Instruments (pure Zag, zero RNG)

### 4.1 `cu_pam.zag` — the PAM instrument

Usage: `cu_pam <c|u> <tape>` where `c` = conscious, `u` = unconscious.
Implements §2 verbatim; `admit()` is one function shared by both modes.

- **Conscious mode:** per row, after the decision, emits one deliberation
  record line to stdout:
  `REC|<id>|<K>|<outcome>|<fired csv>|<blocked_by>|<conf>|<mrgF>|<strong>|<agree>|<prov>|<prov_ok>|<decl_ok>|<auth>`
  and accumulates it into a deliberation-visible record store (a `[]u8`
  arena; each record also counted as 1 deliberation entry).
- **Unconscious mode:** per row writes exactly 1 outcome byte (1/0) to an
  outcome arena. No records, no entries.
- Both modes also emit `OUT|<id>|<K>|<outcome>` lines (evidence plumbing
  for the scorer; EXCLUDED from resource accounting).
- Summary block at end: admissions per class, total cycles (see cost model),
  total record bytes, total deliberation entries.

**Deterministic cycle cost model (frozen here, implemented verbatim):**

- Field parse of one row: 2 cycles (loop overhead), both modes.
- Each primitive check (`cmp1(a,b)`): 1 cycle. R-BAR = 2, R-PROV = 2,
  R-DECL = 1, R-AUTH = 1 (short-circuit: only checks up to the block).
- Decision assembly: 1 cycle.
- Conscious record emission: 1 cycle per emitted byte (byte count = record
  bytes; the resource and the cycle cost coincide by construction).
- Unconscious outcome byte: 1 cycle.
- No wall-clock anywhere in the binary (wall time measured externally and
  reported in the runlog only).

### 4.2 `cu_query.zag` — TNN's own deliberation answering "why admit X?"

Usage: `cu_query <run-stdout-file> <cu_questions.txt>`. This module is the
operationalization of "TNN's own deliberation querying its records": it
scans the run's REC lines and answers each `ASK|<id>`:

- If a REC for `id` exists: `ANS|<id>|<fired csv>|<blocked_by>|<conf>|<mrgF>|<strong>|<agree>|<prov>|<prov_ok>|<decl_ok>|<auth>`
- Else: `ANS|<id>|NO_RECORD`
- Cost: 1 cycle per record byte scanned + 1 per answer byte; reported in
  the summary block (introspection is a deliberation action — its cost is
  part of the tradeoff).

The module reads records ONLY (never the tape): its answers are
reconstructed from the deliberation-visible record store, exactly as TNN's
deliberation would.

### 4.3 `cu_questions.txt` (frozen, from `gen_cu.py`)

- 20 `ASK|<id>` rows = the first 20 C rows in tape order whose axes pass
  the frozen M1 bar (computed by the generator's Python mirror of §2 — all
  will be admitted since C security fields are honest).
- 5 `ASK|<id>` diagnostic rows = the first 5 W rows (all rejected by R-BAR).
  Diagnostic only: they probe whether the record store answers "rejected,
  blocked by R-BAR" rather than hallucinating an admission.

### 4.4 `score_cu.py` (glue, never the instrument)

Independently recomputes from the tape + evidence: bar-pass per row
(Python mirror of §2), the five metrics, the Pareto table, and the
introspection quality score vs ground truth extracted from the conscious
run's REC lines. Any number the scorer cannot reproduce from evidence is
reported as UNVERIFIED, never trusted.

## 5. Metrics (frozen definitions)

- **M-speed:** total cycles ÷ 1,232 rows (cycles/admission), per variant;
  ratio = conscious ÷ unconscious (deterministic). Wall-time ratio of the
  two binaries on the same tape reported as corroboration (runlog only,
  not a bar input — wall time is not deterministic).
- **M-resource:** deliberation-record bytes ÷ 1,232 rows (conscious);
  outcome bytes = 1/row (unconscious); deliberation entries per row
  (conscious 1, unconscious 0). Growth check: bytes in second half of the
  stream ÷ bytes in first half (must be ~1.0; >1.05× = superlinear growth,
  reported as a defect against the wild K4 schema).
- **M-judgment:** correct-admit rate = admits/1,102 on C (RK-3 style;
  expected 910/1,102 = 82.58% for BOTH — the frozen M1 bar); false-admit
  disposition on the 30 frozen wrong rows (expected W 0/12, P exactly the
  2 rows P4-2/P5-2 that pass the frozen bar individually — Correction C2;
  M1's C2 pair-install constraint still holds: no pair fully admitted).
- **M-attack:** catch rate = rejected-attacks/100 overall and per type
  (LAU/40, FORK/30, AUTH/30). Expected 100% BOTH (same core).
- **M-introspection:** per ASK row, 2 points — 1 for exact rule-set match
  (`fired csv` + `blocked_by`) vs ground truth, 1 for exact evidence match
  (all 10 evidence fields). Quality = total/40. Conscious is "yes by
  construction" — this tests QUALITY. Unconscious answers NO_RECORD →
  0/40 by construction (head-to-head reported).

## 6. Bars (frozen)

- **KB-CU-WORTH (the preregistered "conscious is worth its cost" claim):**
  PASS iff ALL hold: (i) introspection quality ≥ 0.85 (34/40);
  (ii) total-cycle speed ratio ≤ 12.0 (the record-keeping overhead is
  inherently ~10× the trivial core; the bar has teeth against blowup,
  not against the inherent cost); (iii) judgment delta = 0
  (correct-admit rate AND false-admit count identical across variants);
  (iv) attack-catch delta ≥ 0 pts (conscious not worse). Sub-outcomes
  reported individually regardless.
- **KB-CU-ATTACKWIN:** conscious "wins on M-attack" iff attack-catch
  delta (conscious − unconscious) ≥ +15 pts. Expected: 0 → FAIL (records
  buy introspection, not attack-catch — report it honestly).
- **KB-CU-JUDG:** the shared core must reproduce the frozen bar exactly:
  VOID iff judgment delta ≠ 0 between variants, or either variant's
  false-admit disposition differs from the frozen bar's own (W: 0/12;
  P: exactly rows P4-2 and P5-2, which pass the frozen bar individually —
  Correction C2; M1's C2 pair-install constraint is unaffected). Any
  deviation = core defect, not a variant win.
- **KB-CU-REPLAY:** any of the ≥2× byte-identical reruns diverge →
  that battery VOID (defect, not noise).
- **KB-CU-INTROFLOOR:** conscious introspection quality < 0.85 →
  conscious FAILS its headline claim regardless of the composite.
- **KB-CU-LINEAR:** conscious bytes/admission growth (2nd half ÷ 1st
  half) > 1.05 → resource-growth defect, reported; verdict downgraded.

## 7. Expected numbers (frozen predictions, not bars)

| Metric | Conscious | Unconscious |
|---|---|---|
| Correct-admit (C) | 910/1,102 = 82.58% | same (shared core) |
| False-admit (W+P=30) | W 0/12, P 2/18 (P4-2, P5-2 pass the frozen bar individually; no pair fully admitted) | same |
| Attack catch (100) | 100% | 100% |
| Cycles/row | ~109 (6 checks + 2 parse + 1 decision + ~100 record bytes) | ~10 (6 checks + 2 parse + 1 decision + 1 outcome byte) |
| Speed ratio | ~10.9× | 1× |
| Record bytes/row | ~100 | 0 (1 outcome byte) |
| Deliberation entries/row | 1 | 0 |
| Introspection quality | ≥ 0.95 | 0/40 |

## 8. Determinism & toolchain (frozen)

- Pure Zag for both instruments; zero RNG anywhere (no seeds, no clock).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- `R33_NATIVE_IO_V1.zag`: byte-identical copy (same sha as the M1 crew's,
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`).
- znc build notes honored: `[]u8` arenas + explicit LE accessors for all
  indexed tables (never `as []i32/u32/u16`); no slice > 2^25 bytes;
  i32 struct fields avoided (arena layout instead); bare `@import`;
  `_zag_arg` read unconditionally (argc=0 per ZNC-2026-09-21-007).
- Batteries: `cu_pam c` 2×, `cu_pam u` 2×, `cu_query` on conscious output
  2×, `cu_query` on unconscious output 2× — sha256(stdout) must match
  within each pair, else VOID.

## 9. Commit plan (frozen)

1. This prereg — committed ALONE, before any fixture/build/output exists.
2. `gen_cu.py` + `cu_tape.txt` + `cu_questions.txt` (+ sha) + `cu_pam.zag`
   + `cu_query.zag` + `R33_NATIVE_IO_V1.zag` + build + `evidence/` +
   `RUNLOG_CU.md` + `score_cu.py` — committed after the runs.
3. `VERDICT_CU.md` — Pareto table, bar outcomes, commit SHAs.
Never: binaries, `.zagd` files.
