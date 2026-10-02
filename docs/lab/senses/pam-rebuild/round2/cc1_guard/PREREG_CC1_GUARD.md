# PREREG — PAMs Round 2: CC1 margin-guard experiment

**Status: FROZEN 2026-09-24. To be committed alone — before any build output exists.**
**Program:** PAMs v2 follow-up, CC1 guard verification (Micah's six prereg rulings, item 1/2/3/6 context).
**Crew:** CC1 margin-guard crew (PAMs Round 2).

## 1. Problem statement (frozen input)

The contradiction-matrix experiment
(`senses/pam-rebuild/v2/contradiction_matrix/`, 30/30 PASS, runs
sha256 `fe6ad1db…7bd8b2` ×3) exposed a preregistered known-unsafe cell:

- **CC1** — two WRONG high-conf PASSes agreeing within tolerance
  (frozen timbredisc seqs 10983/10992, |Δmeas|=24 ≤ tol 120) trigger
  REVISED_INSTALL → FALSE PERMANENT INSTALL under **both** corroboration
  gates (G1 cf1 historical-corroboration, G2 V2-D-hardened).

This blocks deployment of any corroboration gate until a guard is verified.
This experiment designs candidate margin-guard rules and tests them
head-to-head against the G1/G2 baselines on an expanded CC1-variant fixture
set.

## 2. Candidate guard rules (frozen, exact)

Guards are **vetoes on the corroborated-revision step** of G1 (cf1,
AUTOPSY_R2-4 §4 — the recommended mechanism). At the point where G1 would
emit REVISED_INSTALL (stored challenger + incoming same-jcode PASS within
tol, both conf ≥ 700), the guard is consulted:

- guard allows → REVISED_INSTALL (unchanged G1 behavior);
- guard vetoes → **CHALLENGER_PROV** (challenger slot retained, no install).

Guards NEVER authorize a revision; they only withhold one. Singleton
challengers, sub-700 challengers, no-history conflicts, and UNRESOLVED
trials never reach a guard (C3/R1/R2/H1/T1/W1/C2 paths untouched).

**Input contract.** Guards read only: the two corroborating trials'
`(mrgF, seq, span_a, span_b)` and the incumbent permanent slot's
install-time `mrgF`. Guards do NOT read `truth` (contractually off-limits),
and do NOT read judgment-side channels (`jG`/`confG`) — the judgment-channel
ban is adopted as written. `mrgF` (evidence margin), evidence spans, and
`seq` are evidence-side, not judgment-side.

**Frozen constants.**

| symbol | value | meaning |
|---|---|---|
| MG1_FLOOR | 400 | absolute margin floor (both challengers must clear) |
| MG2_FACTOR | 2 | asymmetry factor (min challenger mrgF ≥ 2 × incumbent perm mrgF) |
| MG4_SEQ_GAP | 20 | minimum \|seq₁ − seq₂\| for temporal independence |

**MG3 disjointness** (frozen): spans (sa₁,sb₁),(sa₂,sb₂) are disjoint iff
NOT (sa₁ < sb₂ AND sa₂ < sb₁). Touching spans count as disjoint.

**Rationale for MG1_FLOOR=400.** The autopsy's §4-step-3 candidate
("mrgF ≥ task T3", reusing `deliberate.zag`'s `thr_of`) is ambiguous as
written: `thr_of(4)` (timbredisc) = 80, which does NOT exclude the CC1 pair
(mrgF 382/358). This prereg freezes an explicit floor instead: 400 excludes
the six frozen corroborated-wrong RICH trials (mrgF 353–382, AUTOPSY §2.3)
with margin 18, and keeps every frozen correct challenger (min 6600) with
wide margin. Honest limit: correct timbredisc trials below 400 would be
excluded (recall cost on the full stream is not measured here).

### The five candidates

- **MG1 — margin-of-agreement floor.** Agreement within tolerance is
  insufficient when the challengers' absolute margins sit below the floor.
  Allow iff `min(mrgF₁, mrgF₂) ≥ 400`.
- **MG2 — margin-asymmetry.** The corroborators' margins must dominate the
  would-be-revised claim's margin by a frozen factor.
  Allow iff `min(mrgF₁, mrgF₂) ≥ 2 × mrgF_perm_incumbent`.
  (Requires the permanent slot to carry install-time mrgF — a pure-Zag
  gate-state extension, preregistered here.)
- **MG3 — disjoint-evidence guard.** The corroborators' evidence spans must
  be disjoint (M1 declared-disjoint-evidence, applied corroborator-vs-
  corroborator). Allow iff spans disjoint per the frozen definition.
- **MG4 — temporal-separation.** Corroborators must come from independent
  observation windows. Allow iff `|seq₁ − seq₂| ≥ 20`.
- **MG6 — three-fold independence (crew's own candidate).** Allow iff
  MG1 ∧ MG3 ∧ MG4 all pass. Rationale: corroboration requires challengers
  that are strong (margin), evidence-independent (disjoint spans), AND
  temporally independent (separate windows) — three distinct notions of
  corroborator independence from the frozen literature (autopsy §4 step 3;
  SURVIVOR_MECHANISMS M1; R2-8's independent-source protocol).

Each candidate is tested against its own identical kill bar (§4) — no
candidate is selected by argument.

## 3. Fixture set (frozen, deterministic, zero RNG)

Record format (13 × i64): `tcode|prog|jcode|conf|pred|meas|mrgF|truth|`
`jG|confG|seq|span_a|span_b`. `prog`: 0=PASS, 2=UNRESOLVED.
All values are literals in `gen_guard.py` (single source of truth; the
tables below are its human-readable form).

**Carried cells** (frozen matrix geometry + new `seq`/`span` fields;
provenance per the frozen prereg §3):

| cell | trials (tcode,prog,jcode,conf,pred,meas,mrgF,truth,jG,confG,seq,span_a,span_b) |
|---|---|
| C1 | S1 (0,0,0,605,1,0,2300,0,9,0,721,0,2000); S2 (0,0,0,750,1,3,2400,0,9,0,722,100,2100); T2 (0,0,1,814,1,89,6600,1,1,830,1262,0,2000); T3 (0,0,1,827,1,95,7212,1,1,840,1330,2100,4100) |
| C2 | S1 (4,0,3,760,1,2480,500,3,9,0,10967,0,2000); S2 (4,0,3,770,1,2490,510,3,9,0,10968,100,2100); T2 (4,0,2,718,1,2618,382,3,2,720,10983,0,2000) |
| C3 | S1 (0,0,0,605,1,0,2300,0,9,0,721,0,2000); S2 (0,0,0,750,1,3,2400,0,9,0,722,100,2100); T2 (0,0,1,874,1,127,10410,0,1,850,1145,0,2000) |
| R1 | S1 (0,0,0,900,1,0,8000,0,9,0,2001,0,2000); S2 (0,0,0,920,1,3,8100,0,9,0,2002,100,2100); T2 (0,0,1,650,1,90,5000,1,1,660,2003,0,2000) |
| R2 | S1 (0,0,0,500,1,0,2000,0,9,0,2011,0,2000); S2 (0,0,0,520,1,2,2100,0,9,0,2012,100,2100); T2 (0,0,1,850,1,90,7000,1,1,860,2013,0,2000) |
| H1 | preinstall perm=(j0,meas0,conf605,seq721), no_hist=1; T0 (0,0,1,814,1,89,6600,1,1,830,1262,0,2000) |
| T1 | S1 (0,0,0,800,1,0,5000,0,9,0,2021,0,2000); S2 (0,0,0,800,1,3,5000,0,9,0,2022,100,2100); T2 (0,0,1,800,1,90,5000,1,1,800,2023,0,2000) |
| W1 | T0 (0,2,1,850,0,90,0,1,1,850,2031,0,2000); T1 (0,2,1,850,0,90,0,0,1,850,2032,0,2000); T2 (0,2,1,850,0,90,0,1,1,850,2033,0,2000) |

**CC1 family** (incumbent S1/S2 = BRIGHT, conf 760/770, meas 2480/2490,
mrgF 500/510, truth 3; challengers = wrong RICH, truth 3):

| variant | T2 | T3 | mechanism stressed |
|---|---|---|---|
| CC1 (base) | (4,0,2,718,1,2618,382,3,2,720,10983,0,2000) | (4,0,2,704,1,2642,358,3,2,710,10992,100,2100) | frozen known-unsafe geometry |
| CC1-V1 | as base | meas 2737 (\|Δ\|=119) | near-miss inside tol |
| CC1-V2 | as base | meas 2738 (\|Δ\|=120) | tolerance boundary (inclusive) |
| CC1-V3 | as base | meas 2739 (\|Δ\|=121) | just outside tol — no corroboration at all |
| CC1-V4 | conf 850 | conf 840, else base | high-confidence wrong pair |
| CC1-V5 | mrgF 6600 | mrgF 6603, else base | HIGH-MARGIN wrong pair (margin-guard stress) |
| CC1-V6 | mrgF 6600 | mrgF 358, else base | asymmetric margins |
| CC1-V7 | span (0,2000) | span (2100,4100), else base | DISJOINT-SPAN wrong pair (span-guard stress) |
| CC1-V8 | seq 10983 | seq 11410 (\|Δseq\|=427), else base | TEMPORALLY-SEPARATED wrong pair (time-guard stress) |
| CC1-V9 | mrgF 6600, span (0,2000), seq 10983 | mrgF 6603, span (2100,4100), seq 11410 | PERFECT STORM: high margins + disjoint spans + separated — observationally identical to a correct pair on every guard-visible axis. **Unscored ceiling probe** (reported, not kill-barred). |

**Throughput family** (correct challengers; every guard must revise 5/5):

| variant | geometry |
|---|---|
| CC2 (base) | frozen: S1/S2 SAME (mrgF 2300/2400); T2 (0,0,1,814,1,89,6600,1,1,830,1262,0,2000); T3 (0,0,1,814,1,89,6603,1,1,835,1689,2100,4100) |
| CC2-W1 | as CC2, challengers mrgF 500/520 (just above the 400 floor), seqs 3001/3101 |
| CC2-W2 | as CC2, challengers mrgF 3000/3100 (below 2× incumbent 2400), seqs 3002/3102 |
| C1-W3 | strong incumbent S1/S2 (conf 900/920, mrgF 8000/8100, truth 0); correct challengers T2/T3 (mrgF 6600/7212, truth 1, seqs 4003/4071, spans disjoint) |

Correct-final-jcode per cell: C1/CC2/W1/W2/W3 → 1; C2/CC1-family → 3;
C3/R1/T1 → 0; R2 → none (G1/guards) / 0 (G2); H1 → 0; W1 → none.

## 4. Kill bars (frozen, per candidate)

For each candidate g ∈ {MG1, MG2, MG3, MG4, MG6}:

- **K1 — CC1-family safety.** False installs = 0 across the scored CC1
  family {CC1, V1…V8}. (V9 excluded from scoring: it is the unscored
  ceiling probe.) False install = REVISED_INSTALL/ACCEPT_INSTALL occurred
  AND final permanent jcode ≠ the cell's correct final jcode.
- **K2 — throughput preservation.** Correct REVISED_INSTALL in 5/5 of
  {C1, CC2, CC2-W1, CC2-W2, C1-W3}, final permanent jcode = correct.
  (A guard that withholds everything is withhold-everything, explicitly
  ruled out — throughput is a kill bar, not a nice-to-have.)
- **K3 — no pointwise reintroduction.** C3 (1145 dominator) → no
  REVISED_INSTALL and no ACCEPT_INSTALL; disposition sequence PROV,PERM,CHAL.
- **K4 — regression.** {C2, R1, R2, H1, T1, W1} disposition sequences
  identical to unguarded G1.
- **K5 — determinism.** Three full runs byte-identical (sha256 match).

**SURVIVE** iff K1 ∧ K2 ∧ K3 ∧ K4 ∧ K5. Otherwise **KILL**, with the
failing bar and the failing cell(s) named.

**Baselines (reported, not kill-barred):** G1 and G2 unguarded are expected
to false-install on every scored CC1-family cell except V3 (no
corroboration there) — reproducing the frozen known-unsafe result on the
expanded geometry.

## 5. Execution protocol (frozen)

- Pure-Zag battery `src/guard_main.zag` (+ generated `src/guard_records.zag`,
  + byte-identical `src/R33_NATIVE_IO_V1.zag`): runs every cell through 7
  configs {G1, G2, MG1, MG2, MG3, MG4, MG6} (553 lines/run), printing one
  `GUARD|<cell>|<cfg>|<trial>|<disp>|<perm_j>|<perm_seq>` line per trial.
- G1/G2 control flow verbatim from the frozen `cm_main.zag`; state extended
  with install-time perm mrgF and challenger (mrgF, seq, spans) — disposition
  behavior of unguarded G1/G2 unchanged (checked against the frozen
  EXPECT.tsv on the 8 carried cells).
- Guards apply ONLY at the G1 corroborated-revision point (§2).
- Three full runs; sha256 of each run's stdout must be byte-identical
  (zero RNG; all inputs literal).
- Python scorers (`score_guard.py`, glue only): fidelity check vs
  EXPECT_GUARD.tsv / EXPECT_GUARD_CELL.tsv (generated from this prereg),
  then kill-bar evaluation computed INDEPENDENTLY from run output +
  `gen_guard.py` cell metadata (correct jcodes, scored flags).
- Build: `znc_linux_x86_64_abed8aa1 src/guard_main.zag -o guard_bin`
  (toolchain `~/workspace/tnn-lab/toolchain/bin/`, cwd=`src/` for `@import`
  resolution). Workdir `~/workspace/pam_round2/cc1_guard/` (never /tmp).
  No binaries or `.zagd` committed.

## 6. Commit map

- This prereg (ALONE, before any build output):
  `senses/pam-rebuild/round2/cc1_guard/PREREG_CC1_GUARD.md`,
  `gen_guard.py`, `EXPECT_GUARD.tsv`, `EXPECT_GUARD_CELL.tsv`.
- Build + evidence + verdict:
  `src/guard_main.zag`, `src/guard_records.zag` (generated),
  `src/R33_NATIVE_IO_V1.zag` (byte-identical copy),
  `score_guard.py`, `evidence/run{1,2,3}.txt`, `evidence/DIGESTS.txt`,
  `evidence/score.txt`, `evidence/killbars.txt`,
  `RUNLOG_CC1_GUARD.md`, `VERDICT_CC1_GUARD.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`, via
  `~/workspace/commit_racefree.py`, TMPDIR=`~/workspace/tmp_commit`,
  lab-relative paths. No binaries, no `.zagd`. Additive-only.

## 7. Laws

Pure Zag for mechanisms/verification; Python only for glue/analysis
(generator + scorers). Zero RNG in any decision path. Byte-identical reruns
required. Judgment-channel ban adopted as written (guards read no jG/confG).
Pointwise-revision ban as modified (two-tier corroborated sequences only;
guards are vetoes, never single-pair adjudications — C3 proves it).

## 8. Honest limits (preregistered)

- G-span fields (jG, confG) synthetic throughout (as in the frozen matrix);
  the experiment tests guard contradiction logic, not the sense front end.
- Single-task cells; cross-task interference untested.
- MG1's 400 floor is frozen from the six wrong trials' max (382); its recall
  cost on the full frozen stream (correct trials below 400) is not measured.
- V9 is observationally identical to a correct pair on all guard-visible
  axes; no evidence-side guard in this family can pass it — it bounds the
  mechanism, it does not discriminate between candidates.
- Guards are verified on G1's corroborated-revision step only; G2's D-fired
  path carries the same structural caveat and needs the guard ported
  (mechanical — same veto point — but untested here).
