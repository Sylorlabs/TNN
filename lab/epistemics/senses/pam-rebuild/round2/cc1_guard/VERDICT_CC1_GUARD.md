# VERDICT — CC1 margin-guard experiment (PAMs Round 2)

**Date:** 2026-09-24 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Prereg:** `a673da8aa9481194992a38963eb7b99074fe1f5e` (frozen alone before any build output)
**Runs:** sha256 `14fc017a4a0dddf9a8dc3cea1db647a8759c363b46095f79516bca0ae67ae12f` ×3 (byte-identical, zero RNG)
**Fidelity:** 154/154 (cell, config) dispositions match the preregistered EXPECT tables exactly.

## Question

The contradiction matrix left a preregistered known-unsafe cell: **CC1** —
two wrong high-conf PASSes agreeing within tolerance install a false
permanent under both corroboration gates (G1/G2). Five candidate
margin-guard rules (vetoes on G1's corroborated-revision step) were tested
head-to-head against the G1/G2 baselines on 22 cells (8 carried, 9 scored
CC1 variants, 4 throughput variants, 1 unscored ceiling probe).

## Per-candidate results

| candidate | exact rule (frozen) | K1 CC1-family 0 false installs | K2 throughput 5/5 | K3 C3 stays withhold | K4 regression | K5 byte-identical ×3 | verdict |
|---|---|---|---|---|---|---|---|
| MG1 margin floor | allow iff min(mrgF₁,mrgF₂) ≥ 400 | **FAIL** — V5 false-installs (high-margin wrong pair, mrgF 6600/6603, clears the floor) | PASS | PASS | PASS | PASS | **KILL** |
| MG2 margin asymmetry | allow iff min(mrgF₁,mrgF₂) ≥ 2 × perm-mrgF | **FAIL** — V5 false-installs (6600 ≥ 2×510) | **FAIL** — vetoes W1/W2/W3 (correct challengers at 500/3000/6600 vs incumbents 2400/8100) | PASS | PASS | PASS | **KILL** |
| MG3 disjoint spans | allow iff corroborator spans disjoint | **FAIL** — V7 false-installs (disjoint-span wrong pair) | PASS | PASS | PASS | PASS | **KILL** |
| MG4 temporal separation | allow iff \|seq₁−seq₂\| ≥ 20 | **FAIL** — V8 false-installs (Δseq=427 wrong pair) | PASS | PASS | PASS | PASS | **KILL** |
| MG6 three-fold independence | allow iff MG1 ∧ MG3 ∧ MG4 | **PASS** — 0/9 false installs | **PASS** — 5/5 correct revisions | PASS | PASS | PASS | **SURVIVE** |

**Baselines (reported):** G1/G2 false-install on 8/9 scored CC1-family cells
(everything except V3, where |Δmeas|=121 > tol 120 means no corroboration
forms at all) — the frozen known-unsafe result reproduced on the expanded
geometry. Both revise 5/5 throughput cells correctly.

**V9 ceiling probe (unscored, preregistered):** all 7 configs false-install.
A wrong pair that is strong on every guard-visible axis (high margins,
disjoint spans, separated windows) is observationally identical to a correct
pair — no evidence-side guard in this family can separate them.

## Why each single-mechanism guard dies (mechanism, not just numbers)

- **MG1** dies on V5: the margin floor's safety is evidence-contingent. The
  frozen six wrong trials sat at mrgF ≤ 382, but nothing in the machinery
  stops a wrong pair from carrying correct-like margins (the 1145 singleton
  already proved wrong percepts can reach mrgF 10410). A floor is a
  distribution bet, not a mechanism.
- **MG2** dies twice, structurally: within the tested geometry **no factor
  K works** — vetoing the base wrong pair needs K > 358/510 ≈ 0.70, while
  sparing the W1 correct pair needs K ≤ 500/2400 ≈ 0.21. Relative-to-
  incumbent dominance punishes correct challengers whenever the incumbent
  is strong. Do not try to tune K; the rule form is wrong.
- **MG3** dies on V7: span-disjointness stops same-span correlation but not
  the correlated cross-span attack (REDTEAM_V2 §4's "fool F and G identically"
  surface, realized here as a wrong pair on disjoint spans).
- **MG4** dies on V8: temporal separation stops same-burst correlation but
  not a persistent correlated error (e.g. a stuck/wrong calibration) that
  re-emits across windows.

## The winner: MG6 — three-fold independence

**Exact frozen rule.** At G1's corroborated-revision point (stored challenger
+ incoming same-jcode PASS within tolerance, both conf ≥ 700), allow
REVISED_INSTALL iff **all three** hold, else veto → CHALLENGER_PROV
(challenger slot retained, no install):

1. `min(mrgF_stored, mrgF_incoming) ≥ 400` (challengers are strong);
2. spans disjoint: NOT (`sa_stored < sb_incoming` AND `sa_incoming < sb_stored`)
   (challengers are evidence-independent; touching counts as disjoint);
3. `|seq_stored − seq_incoming| ≥ 20` (challengers are temporally independent).

Guards read only `(mrgF, seq, span_a, span_b)` of the two corroborators and
the incumbent's install-time `mrgF` — never `truth`, never judgment-side
channels (`jG`/`confG`). Guards never authorize a revision; C3 (1145
dominator) stays `PROV,PERM,CHAL` under every candidate — no pointwise
adjudication reintroduced.

## Deployment statement

**The CC1 deployment block is LIFTED for G1+MG6 with the exact rule above**
— the first corroboration gate with a Zag-verified guard against correlated
wrong corroborators: 0 false installs across the 9-cell scored CC1 family,
5/5 correct revisions preserved, C3 withholds, full regression clean,
byte-identical ×3.

**Scope and honest limits** (the unblock is conditional, not blanket):

1. **Tested geometry only:** single-task cells, tcode 0/4 (tol 8/120),
   two-tier corroborated sequences. Cross-task interference untested.
2. **V9 ceiling:** a wrong pair strong on all three axes defeats MG6 and is
   observationally identical to a correct pair on every guard-visible axis.
   Closing V9 needs information not in the current record format (the
   correctness bit is genuinely absent — AUTOPSY_R2-4 §2.2). The residual
   risk is located precisely, not hidden.
3. **MG1's 400 floor recall cost** on the full frozen stream (correct trials
   below 400) was not measured here; the floor was frozen from the six wrong
   trials' max (382).
4. **G1 only:** G2's D-fired path carries the same structural caveat; the
   veto ports mechanically to the same revision point but is untested here.
5. **Frozen-input note for the follow-up:** the autopsy's "mrgF ≥ task T3"
   candidate is ambiguous as written — `deliberate.zag`'s `thr_of(4)` is 80,
   which does NOT exclude the CC1 pair (382/358). This prereg froze an
   explicit 400 instead; any adoption of the autopsy candidate must cite the
   explicit floor, not `thr_of`.

## Artifacts

- Prereg (frozen alone): `PREREG_CC1_GUARD.md`, `gen_guard.py`,
  `EXPECT_GUARD.tsv`, `EXPECT_GUARD_CELL.tsv` — commit `a673da8a`.
- This commit: `src/guard_main.zag`, `src/guard_records.zag` (generated),
  `src/R33_NATIVE_IO_V1.zag` (byte-identical copy), `score_guard.py`,
  `evidence/run{1,2,3}.txt`, `evidence/DIGESTS.txt`, `evidence/score.txt`,
  `RUNLOG_CC1_GUARD.md`, `VERDICT_CC1_GUARD.md`.
- Pure Zag mechanisms; Python glue only (generator + scorer). Zero RNG.
