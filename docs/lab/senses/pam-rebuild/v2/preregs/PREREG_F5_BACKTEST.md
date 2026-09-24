# PREREG — F5 counter-corroboration trap, offline backtest

Frozen 2026-09-23. Committed ALONE before any code. Builder: F5 arm crew.

## 1. Hypothesis under test

F5 (counsel synthesis §F5, champion_B_corridor.md §4): percepts installed then
reversed by deliberate re-inspection become negative exemplars in a bank. Any
new candidate within defined distance of any exemplar is BLOCKED regardless of
evidence score, until three deliberate re-inspections from three temporal crops
confirm it — then the exemplar is removed (explicit re-judgment). Blocking is
the safe direction: a delayed correct percept is recoverable, an installed
wrong corrupts the system.

**Scope of THIS battery:** the pre-confirmation block predicate ONLY, replayed
over committed logs. The "three deliberate re-inspections from three temporal
crops" confirmation machinery is not exercised here (no temporal crops in the
committed logs); the kill bars are written on the pre-confirmation predicate
("blocked pre-confirmation", "within exemplar distance"). The confirmation
path is separate future work.

## 2. Data (all committed logs, verified before freezing)

### 2a. The 43 candidate trials
Source: `senses/pam-rebuild/v2/redteam/evidence/ledger_d_withhold.txt`
(lines containing `DISP=ACCEPT_INSTALL`).

Line format (verified from `v2/redteam/src/rt_records.zag`):
`prev_hash|link_hash|seq|tcode|fixture|prog|jcode|judgment|confidence|pred|measure|phash|truth|jG|confG|DISP=...|DETAIL=...`
(field indices 0..16; judgment=7, confidence=8, measure=10, truth=12, DISP=15).

Re-verified counts (2026-09-23, from the file, awk field split on `|`):
- 43 lines contain `DISP=ACCEPT_INSTALL`.
- 9 false (judgment != truth): 8× fixture `rt4_TMB-5_*.r24` (judg=RICH,
  truth=DARK), 1× fixture `rt4_COL-4_0000.r24` (judg=DIFFERENT, truth=SAME).
- 34 true (judgment == truth).

Family×truth table: PTC-5: 12 true; COL-4: 12 true, 1 false; TMB-5: 6 true,
8 false; PTC-4: 4 true. (12+12+6+4 = 34 true; 8+1 = 9 false; total 43.)

### 2b. The 6 exemplar wrongs (the frozen bank)
Source: `senses/pam-rebuild/round2/forks/R2-4/evidence/clean/sweep.jsonl`
(11,840 rows).

Filter (re-derived independently, 2026-09-23 — yields exactly the 6 seqs):
`10983 ≤ seq ≤ 11192 AND judgment=="RICH" AND truth=="BRIGHT"
AND 701 ≤ conf ≤ 718 AND 353 ≤ mrgF ≤ 382`.

| seq   | task       | fam   | judg | truth  | conf | mrgF | measure |
|-------|------------|-------|------|--------|------|------|---------|
| 10983 | timbredisc | TMB-1 | RICH | BRIGHT | 718  | 382  | 2618    |
| 10992 | timbredisc | TMB-1 | RICH | BRIGHT | 704  | 358  | 2642    |
| 11024 | timbredisc | TMB-1 | RICH | BRIGHT | 713  | 374  | 2626    |
| 11049 | timbredisc | TMB-1 | RICH | BRIGHT | 701  | 353  | 2647    |
| 11126 | timbredisc | TMB-1 | RICH | BRIGHT | 710  | 368  | 2632    |
| 11192 | timbredisc | TMB-1 | RICH | BRIGHT | 713  | 373  | 2627    |

The extraction script is committed at `v2/f5_backtest/mk_exemplars.py` (frozen
filter, deterministic) and writes the frozen bank as `v2/f5_backtest/exemplars.tsv`.

## 3. Frozen distance predicate (the mechanism under test)

Candidate is BLOCKED iff there EXISTS an exemplar in the bank such that ALL
three hold:

1. **Same family:** family stems match. Exemplar family = sweep.jsonl `fam`
   field (`TMB-1` → stem `TMB`). Candidate family = the `<STEM>-<N>` segment of
   the ledger `fixture` field (`rt4_TMB-5_0000.r24` → stem `TMB`). Rule:
   stems equal. Rationale: counsel's mechanical reading "timbredisc ≡ TMB-* by
   task tag"; no post-hoc exceptions, no outcome-driven carve-outs.
2. **|conf_cand − conf_ex| ≤ 150** (battery's number, unchanged).
3. **|margin_cand − margin_ex| ≤ 2000** — see §4 for the frozen substitution.

Blocked = within exemplar distance (would need the three re-inspections to
confirm). Not blocked = proceeds. Note: all 43 trials are already
ACCEPT_INSTALL dispositions in the log; the predicate is replayed as a
pre-confirmation gate on top.

## 4. Frozen margin-field resolution (documented substitution)

**Finding: `mrgF` is genuinely unavailable for the 43 candidates.**

Evidence:
- `round2/forks/R2-4/src/sense_r24.zag`, `task_timbredisc`: the sense output
  emits TWO distinct keys — `ob_kint(ob, pos, "mrgF", mrg)` where
  `mrg = timbre_margin(r12, hh)` (classification margin to the timbre class
  boundary), and `ob_kint(ob, pos, "measure", r12)` where `r12` is the raw
  spectral centroid. They are different quantities by construction.
  `measure` is per-family task-specific (centroid for timbredisc, `dcm` for
  colorconst, `ravg` for shapetrans, etc.).
- `v2/redteam/src/rt_records.zag` (the record builder behind the 43-line
  ledger) parses only `judgment`, `confidence`, `prog`, `pred`, `measure`
  from the `.r24.sense` files; `mrgF` is never read into the ledger format.
- The `.r24.sense` files and the rt4 fixtures do not exist in this repo or
  anywhere on this VM (`find` for `rt4_TMB-5_0000.r24*` returns nothing), so
  `mrgF` cannot be recomputed from committed material.

**Frozen substitution (no silent substitution):** use the ledger's `measure`
field for candidates and sweep.jsonl's `measure` field for exemplars as the
second distance axis, with the battery's unchanged window ±2000:

`|measure_cand − measure_ex| ≤ 2000`.

Caveat recorded: `measure` is NOT the classification margin; it is the
task-specific raw quantity (for timbredisc: spectral centroid). The
predicate's semantics on this axis are therefore "near in raw measure", not
"near in margin". The kill bars stand as written against the frozen
predicate. If F5 survives, a follow-up with true-margin replay (regenerated
sense outputs, separate prereg) is the honest upgrade path.

## 5. Kill bars (both must pass; else KILL, no rescue)

- (a) **Block recall:** ≥ 8 of the 9 false accepts blocked pre-confirmation.
  The 6 exemplars are in the bank by construction; the test is whether the
  other 3 falses fall within exemplar distance — if the bank only catches its
  own members, F5 is a replay list, not a trap. Below 8/9 → KILL.
- (b) **Over-block cost:** ≤ 4 of the 34 true accepts within exemplar
  distance (would-be-delayed). Above 4/34 → KILL (redesign, not tune).

## 6. Conditional follow-up (red-team clause)

ONLY if both bars pass: red-team with 300 near-exemplar correct percepts;
KILL if > 25% are delayed > 50 trials. This is filed here as a conditional
clause and is NOT run under this prereg — generating 300 fresh percepts is
not an offline replay of committed logs and needs its own fixture-generation
prereg. Documented next step on SURVIVE.

## 7. Laws and method

- The block predicate is implemented in pure Zag (the predicate IS the
  mechanism under test). Deterministic; zero RNG. The binary reads the
  committed ledger path and the frozen `exemplars.tsv` from argv, parses the
  43 `DISP=ACCEPT_INSTALL` lines and the 6 bank rows, prints one decision
  line per trial plus summary counts.
- Run 3×; SHA-256 of stdout must be byte-identical across all three runs.
- Commit order: this prereg ALONE first; then build + run; then evidence
  (program source, exemplar extraction script, `exemplars.tsv`, three run
  outputs, SHA list) + verdict committed together.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- New work under `senses/pam-rebuild/v2/f5_backtest/`; message files under
  `~/workspace/tmp_commit/`; never `/tmp`; never commit binaries or
  `.zagd`/`.zag-cache` files.

## 8. Transparency note

Data ranges were visible during the pre-freeze format/count verification
(required by the battery: "re-verify these counts yourself from the file
before freezing"). All free choices follow the battery's mechanical form:
stems from the literal tags, thresholds exactly 150/2000 as specified, the
only available margin-equivalent field documented as a caveat. No threshold
tuning, no post-hoc family exceptions, no outcome-conditioned rules.

## 9. Deliverable

Verdict: SURVIVE or KILL with measured numbers (x/9 blocked, y/34
over-blocked), run SHAs, commit SHAs. If killed: say so plainly with the
numbers and stop — no rescue mission.
