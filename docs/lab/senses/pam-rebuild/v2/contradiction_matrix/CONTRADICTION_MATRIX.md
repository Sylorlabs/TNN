# CONTRADICTION MATRIX — results and verdict (PAMs v2 follow-up item 6)

**Settling experiment for Sol debate Round 4, disagreement #4 (FS-G completeness):**
"FS-G bars do not, by themselves, specify what happens when evidence conflicts,
when a corroborator is wrong, or when a stronger signal contradicts an incumbent."
**Status: EXECUTED 2026-09-23.** Prereg frozen alone at
`5bd979f2a15de0933623ed43dbaa98b8af4e2599` before any build output existed.

**Method:** pure-Zag battery (`src/cm_main.zag` + generated `src/cm_records.zag`)
runs 10 cells × 3 candidate gates (31 trials × 3 = 93 disposition lines per run).
Three runs byte-identical
(sha256 `fe6ad1dbc4173146472274e9f5bc9785fb6761a7c012c512ccddc07b7f7bd8b2` ×3).
Python scorer vs frozen EXPECT.tsv / EXPECT_CELL.tsv. Zero RNG.

**Gates:** G0 = frozen R2-4/H2 gate (negative control); G1 = cf1
historical-corroboration (AUTOPSY_R2-4 §4, pure-Zag implementation from spec —
no cf1 Zag had landed on the branch); G2 = V2-D-hardened (detector spec
REDTEAM_V2 §4 + PREREG_V2-D §2, hardening: **prog-required** + **conflict
adjudication**).

## Per-cell results (expected vs actual; PASS = emitted == preregistered)

| cell | G0 expected → actual | G1 expected → actual | G2 expected → actual |
|---|---|---|---|
| C1 correct challenger | PROV,PERM,CONF,CONF → same ✅ | PROV,PERM,CHAL,REV → same ✅ (revises, correct) | PROV,PERM,CHAL,REV → same ✅ (revises, correct) |
| C2 wrong challenger | PROV,PERM,CONF → same ✅ | PROV,PERM,CHAL → same ✅ (withholds) | PROV,PERM,CHAL → same ✅ (withholds) |
| C3 1145 dominator | PROV,PERM,CONF → same ✅ | PROV,PERM,CHAL → same ✅ (withholds despite domination) | PROV,PERM,CHAL → same ✅ (withholds despite domination) |
| R1 high→low conf | PROV,PERM,CONF → same ✅ | PROV,PERM,CONF → same ✅ | PROV,PERM,CONF → same ✅ |
| R2 low→high conf | PROV,PERM,CONF → same ✅ | PROV,PROV,CHAL → same ✅ (conf bar keeps incumbent provisional) | PROV,PERM,CHAL → same ✅ |
| CC1 two WRONG agreeing | PROV,PERM,CONF,CONF → same ✅ | PROV,PERM,CHAL,REV → same ✅ **FALSE INSTALL (preregistered known-unsafe)** | PROV,PERM,CHAL,REV → same ✅ **FALSE INSTALL (preregistered known-unsafe)** |
| CC2 two CORRECT agreeing | PROV,PERM,CONF,CONF → same ✅ | PROV,PERM,CHAL,REV → same ✅ (revises, correct) | PROV,PERM,CHAL,REV → same ✅ (revises, correct) |
| H1 missing history | CONF → same ✅ | CONF → same ✅ (fallback) | CONF → same ✅ (fallback) |
| T1 tie | PROV,PERM,CONF → same ✅ | PROV,PERM,CHAL → same ✅ | PROV,PERM,CHAL → same ✅ |
| W1 UNRESOLVED stream | WITH×3 → same ✅ (0 installs) | WITH×3 → same ✅ (0 installs) | WITH×3 → same ✅ (0 installs; prog-required holds) |

**30/30 gate-cells PASS.** Full machine table: `evidence/score.txt`.
No trial hit an unspecified or defensive branch; every emitted disposition came
from a named preregistered rule.

## What each cell demonstrated

- **C1 / CC2:** historical corroboration revises correctly under G1 and G2
  (two agreeing correct high-conf PASSes → REVISED_INSTALL; final permanent =
  the correct judgment). G0 withholds both — the 9.4% RK-3 failure mode in
  miniature (negative control behaving as preregistered).
- **C2 / C3:** singleton challengers never revise under G1/G2 — including the
  1145-class dominator (wrong, conf 874 > incumbent 605, mrgF 10410 > 2300,
  strong=1/agree=1, D-fired under G2). Pointwise adjudication stays banned;
  the cf2 failure mode (naive single-shot revision installs 1145) is not
  reproduced by either corroboration gate.
- **R1:** sub-700 challengers are not revision candidates under any gate.
- **R2:** a single high-conf challenger does not revise even a low-conf
  incumbent; cf1's §4.2 permanence bar additionally keeps the sub-700 incumbent
  provisional (PROV,PROV,CHAL — the bar working as specified).
- **CC1:** the load-bearing negative result. Two wrong high-conf PASSes
  agreeing within tolerance (frozen seqs 10983/10992, |Δmeas|=24 ≤ tol 120)
  trigger REVISED_INSTALL under G1 **and** G2 → **false permanent install**,
  exactly as preregistered. This is AUTOPSY_R2-4 §2.3's caveat made concrete:
  cf1's replay 0% was evidence-contingent, not a theorem. Correlated wrong
  corroborators defeat historical corroboration, with or without the V2-D
  detector hardening.
- **H1:** with no history the corroboration path is inert; all three gates
  fall back to CONFLICT_WITHHELD — even for a correct challenger. Specified,
  safe, conservative.
- **T1:** equal evidence is not corroboration; the tied challenger is stored
  (G1/G2) or withheld (G0), never installed.
- **W1:** the REDTEAM_V2 §4 KILL regression. Unhardened V2-D installed 43
  ACCEPT_INSTALL on 288 UNRESOLVED trials (9 false). Hardened G2 emits
  WITHHELD ×3, zero installs: the prog-required hardening holds.

## Verdict

**Fully-specified contradiction behavior: all three gates.** No cell left any
trial to unspecified behavior — every disposition in all 93 lines × 3 runs
came from a named preregistered rule, and all 30 gate-cells matched their
preregistered expectations exactly.

**No false installs: G0 only** — at the cost of never revising (withholds the
correct revisions in C1/CC2).

**Specified + safe + revises: none.** G1 and G2 revise correctly on C1/CC2 and
withhold correctly on C2/C3/R1/R2/H1/T1, but both false-install on CC1
(preregistered known-unsafe). The V2-D hardening fixes the UNRESOLVED-install
regression (W1) but does not touch the correlated-corroborator weakness —
CC1 defeats G2 through the D-fired path itself.

**Answer to disagreement #4's settling experiment:** the contradiction behavior
is now fully specified and machine-checked for the three candidate gates, and
the residual gap is precisely located: **correlated wrong corroborators**.
Sol's new #1 architecture (historical-corroboration-only revision) is validated
on 9 of 10 cells but **must not deploy** without an additional guard for CC1.

**Preregistered follow-up (unchanged):** the `mrgF ≥ task T3` challenger margin
bar (AUTOPSY_R2-4 §4 step 3) is the candidate fix — it excludes the CC1 pair
(mrgF 382/358) while keeping the correct revisions (C1/CC2 mrgF ≥ 5949). It was
deliberately excluded from these gates as "verify in Zag before adopting"; it
needs its own Zag verification experiment before adoption.

## Honest limits
- G-span fields (jG, confG) are synthetic throughout (preregistered per trial);
  the matrix tests gate contradiction logic, not the sense front end.
- Single-task cells; cross-task interference untested.
- §4 step 4 (corroborated negative evidence) specified but vacuous here (no
  FAIL trials in any cell).
- G2's ACCEPT_INSTALL truth-acceptance path on a first install is unexercised
  (no cell pairs a D-fired trial with no incumbent).
- R2/G1's provisional-incumbent conflict handling (no single-observation
  reversal of provisionals) is a specified prereg choice, exercised and passing.
- Frozen trial provenance: seqs 721/1145/1262/1330/1689 (colordisc) and
  10983/10992 (timbredisc) from
  `senses/pam-rebuild/round2/forks/R2-4/evidence/clean/sweep.jsonl`; all other
  rows synthetic with values in frozen distribution ranges (provenance per
  trial in the prereg §3 tables).

## Artifacts
- Prereg (frozen, alone): `PREREG_CONTRADICTION_MATRIX.md`, `gen_cells.py`,
  `EXPECT.tsv`, `EXPECT_CELL.tsv` — commit `5bd979f2a15de0933623ed43dbaa98b8af4e2599`.
- This commit: `src/cm_main.zag`, `src/cm_records.zag` (generated),
  `src/R33_NATIVE_IO_V1.zag` (byte-identical copy), `score_cm.py`,
  `evidence/run{1,2,3}.txt`, `evidence/DIGESTS.txt`, `evidence/score.txt`,
  `RUNLOG.md`, `CONTRADICTION_MATRIX.md`.
