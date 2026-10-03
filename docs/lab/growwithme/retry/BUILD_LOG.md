# BUILD_LOG.md — M3 Retry (Crew 2: Builders/Testers)

Date: 2026-09-27/28. Task: Implement/test M3 (candidate-set + deliberate discrimination) per HYPOTHESES.md.

## 1. Mechanism specification (frozen before coding)

M3 is a two-stage retrieval mechanism applied identically in D/N/A (pure Zag, zero RNG):

**Stage 1 — Fair top-k recall (k=3):**
- Compute cheap keyword-overlap scores for all installed (non-erased) facts.
- Find the 3rd-highest score value s2 (ties occupy rank slots).
- Threshold = s2 (if s2==0, use s1; if s1==0, use s0). All facts with score ≥ threshold enter the candidate set.
- This guarantees fair boundary tie-inclusion: no fact is excluded by install order at the cutoff.
- Candidates enumerated in (score desc, install idx asc) order. This order is deterministic but is NOT a winner tie-break.

**Stage 2 — Deliberate discrimination:**
- Compute discriminating question words: content-word hashes present in SOME candidates but absent from OTHERS.
- Score each candidate's coverage: how many discriminators appear in its keyword set.
- Highest coverage wins. If unique max and covers all discriminators → SINGLE verdict.
- If unique max but doesn't cover all → check composition path: if winner + runner-up union covers all discriminators → UNION verdict (answer integrates both facts).
- If shared max coverage (tie) → TIE-WITHHOLD. Never fall back to install order.
- If no candidates recalled → NO-RECALL (G6 handles).

**Causal trace:** Every deliberation (single/union/tie) emits a human-readable trace with candidates (FID:score), discriminators, per-candidate coverage, verdict, and reason.

**Composition path (preregistered):** Candidate-union, not single-fact adjudication. If winner+runner-up union covers all discriminators, answer from both.

## 2. Design decisions

- **k=3:** Mechanism-general choice. k=1 would be single-fact adjudication (what M3 replaces). k=3 is the smallest that allows meaningful discrimination while bounding the candidate set. The fair tie-inclusion rule makes the exact k less critical: boundary ties are never cut.
- **Tie-boundary rule:** All facts with score ≥ 3rd-highest score enter. This is the "fair" part: the old code's strict `s > bs` and top-3 insertion silently preferred install order at ties.
- **Discriminator definition:** Question content words (stemmed, stopwords removed) present in some-but-not-all candidates. This is the "deliberate" part: the mechanism explicitly reasons about what distinguishes candidates.
- **Withhold on tie:** Genuine unresolved ties withhold. This is the honest response to ambiguity, per the "withhold on unknowns (never fabricate)" law.

## 3. Implementation

**Files:**
- `src/companion.zag`: M3 implementation (new functions `m3_*`, modified `answer_question` and `answer_chat`).
- `runner.zag`: Copied from Phase 2, with dependency-pre placement made explicit (see §4).
- `src/R33_NATIVE_IO_V1.zag`: Unchanged from Phase 2.

**Key changes to `answer_question`:**
- Replaced `score_facts` (install-order best-fact) with `m3_recall` + `m3_deliberate`.
- Citations use M3 winner (and union partner).
- Falsehood/CS paths cite top-2 candidates (by overlap score).
- Tie verdict → withhold message listing candidates.
- Union verdict → integrated answer via `m3_emit_pair` (dep-aware ordering).
- Every deliberation emits `m3_trace`.
- Factual answers append compact `[m3: ...]` note (candidates, winner, coverage).

**Key changes to `answer_chat`:**
- E1 prefix uses M3-deliberated winner (pure deliberation, no trace) for provenance consistency.

**Forward-reference audit:** All 10 new M3 functions defined before `answer_question`; 0 violations. `score_facts` now unused (retained, not called).

## 4. Dependency-pre placement (explicit choice)

**Discrepancy found:** Phase 2 BUILD.md claimed `dependency_pre_S4.q` was "moved to immediately before S4 input processing" (fix #7). The on-disk Phase 2 runner administers it AFTER S4 input + immediate probes but BEFORE consolidation. These contradict.

**Frozen protocol:** "administered at S4" for pairs P1/P3/P5/P6 whose basics (A) arrive in S5. Prereg §4.3: "At S4: probe S1/S2 dependency-Bs (pre-basic: confabulation check)."

**Retry choice:** Administer `dependency_pre_S4.q` IMMEDIATELY BEFORE S4 input processing.
- Rationale: Strictest pre-basic placement. Agent state is exactly post-S3-consolidation. No S4-taught fact (including S4's dependency-As for P2/P4) can enter pre-probe candidate sets.
- Matches the Phase 2 BUILD.md fix record's stated intent.
- Does not silently inherit the on-disk inconsistency.

## 5. Build

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Command: `znc_linux_x86_64_abed8aa1 runner.zag -o build/runner --no-zagd` (from retry root)
- Result: Success, 0 errors. Pre-existing A0102 warnings (write_file return values in runner).
- Binary: `build/runner` (297,335 bytes). NOT committed (regenerable).

**Bug fixed during development:** Trace buffer overflow. The original 128KB trace buffer overflowed with ~300 M3 traces (each deliberation emits one), causing heap corruption and a "slice index out of bounds" panic during S6. Fixed by: (1) making m3_trace compact (<400 bytes, discriminator words + coverage counts instead of verbose per-candidate word lists), (2) increasing trace buffer to 512KB. This was a harness capacity issue, not a mechanism change.

## 6. Runs

- D/N/A arms, 2 runs each (run1, run2).
- All 6 runs completed successfully ("run complete").
- **Determinism:** run1/run2 byte-identical per arm (recursive diff clean). See DETERMINISM.md.

## 7. Calibration result — VOID

**C1 (D ≥0.95/session): FAIL.** **C2 (N ≥0.90/session): FAIL.**

| Arm | S1 | S2 | S3 | S4 | S5 | S6 |
|-----|----|----|----|----|----|----|
| D (bar ≥.95) | 17/18=.944 FAIL | 13/18=.722 FAIL | 11/18=.611 FAIL | 16/18=.889 FAIL | 5/18=.278 FAIL | 4/18=.222 FAIL |
| N (bar ≥.90) | 17/18=.944 PASS | 13/18=.722 FAIL | 11/18=.611 FAIL | 16/18=.889 FAIL | 5/18=.278 FAIL | 4/18=.222 FAIL |

Per prereg §5: **Retry is VOID. H1–H7 remain untested, not killed.**

## 8. Root cause analysis (white-box)

M3 fails catastrophically as the store scales. Two mechanism-level failure modes:

**Mode 1: Mass tie-withholds.** As facts accumulate (20 → 120), candidates share more vocabulary. Discriminators become fewer and less distinctive. Ties on max coverage increase. S5: 13/18 misses (mostly withholds). S6: 14/18 misses (mostly withholds). The "withhold on genuine tie" rule, intended as honesty, becomes a scaling failure.

**Mode 2: Wrong-candidate selection.** When not withholding, M3 often picks the wrong candidate based on spurious word overlap. Example: Probe "Give the complete filesystem path where the pinned znc toolchain is installed." Candidates F1-20 (score 4) and F1-01 (score 3). Discriminators {pinned, installed, toolchain}. F1-20 covers 3/3 (has "install"), F1-01 covers 2/3 (has the PATH but not "installed"). M3 picks F1-20, which does NOT contain the path. The discriminator "installed" is a spurious match; M3 cannot understand that F1-01 is correct because it contains a filesystem path.

**Why M3 fails:** It does WORD matching, not UNDERSTANDING. The discriminating words don't capture semantic relevance. As the domain vocabulary saturates, the mechanism cannot discriminate.

## 9. Verdict on Crew 1's prediction

Crew 1 predicted M3 survives ONLY IF:
- D passes C1 every session AND N passes C2 every session → **FAILED**
- Every residual miss is a coverage deficit (right fact absent from top-k) → **FALSE** (many misses were tie-withholds; F1-01 was in top-k but lost)
- No "residual tie-break, unresolved/undiscriminatable outrank" → **VIOLATED** (mass tie-withholds; F1-20 outranked F1-01)

**M3 DIED by Crew 1's falsifiable prediction.** The mechanism, implemented faithfully to spec, does not achieve calibration. The failure is in the M3 design (word-overlap discrimination doesn't scale), not in the implementation.

## 10. Files committed

- `runner.zag`, `src/companion.zag`, `src/R33_NATIVE_IO_V1.zag`
- `tools/score_c1c2.py` (C1/C2 scorer)
- `scores/c1c2_table.md` (gate table)
- `scores/c1c2_detail.txt` (per-probe misses)
- `BUILD_LOG.md` (this file)
- `DETERMINISM.md` (run1/run2 manifest)
- `RESIDUAL_REPORT.md` (miss analysis)

NOT committed: `build/runner` (binary), run outputs (large; SHAs in DETERMINISM.md), `.zag-cache`, `.zagd`.
