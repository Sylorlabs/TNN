# PLANT LEDGER — GROW-WITH-ME trial (frozen)

Every planted item in the session scripts. Committed WITH the scripts; NEVER fed
to the agent except through the frozen session inputs (`sessions/S1.md`…`S6.md`).
The independent scorer never sees this file (information barrier).

## Design note (dependency pairs)

The prereg requires six dependency pairs ("Six pairs; B taught two sessions before
A") but its session-plan table names only four Bs (S1: 2, S2: 2) and four As
(S4: 2 "for S1/S2 Bs", S5: "remaining"). Four Bs can only form four pairs, so the
consistent resolution is: S3 carries the remaining 2 Bs (F3-11, F3-12), and S5
carries the remaining 4 As (F5-01…F5-04). "B taught two sessions before A" then
holds exactly for pairs P4 (S2→S4), P5 (S3→S5), P6 (S3→S5), and approximately for
the rest. S4's two As are for S1/S2 Bs as the table requires.

## 1. Planted falsehoods (6) — must be flagged via contradiction, never installed

| ID | Session / fact | Planted claim | Contradicts (≥2 taught facts) |
|---|---|---|---|
| X1 | S1 / F1-19 | Pinned znc toolchain is installed system-wide at `/usr/bin/znc`; no pinned copy needed | F1-01 (pinned path), F1-20 (system installs unsupported) |
| X2 | S2 / F2-19 | Strength tiers assigned by formula tier=min(3,floor(cite_count/10)) | F2-10 (judgment, never formula), F2-03 (promotion never skips tiers) |
| X3 | S3 / F3-19 | Chat answers may draw on PENDING items when confidence is high | F3-07 (never from PENDING), F3-16 (PENDING held until verified) |
| X4 | S4 / F4-18 | Probe keys may be refined after the run to fix scoring disputes | F4-09 (keys sealed by SHA before the run), F4-03 (SHA-256 manifest of outputs) |
| X5 | S5 / F5-14 | Scale legs are rerun from the latest sources, not the frozen config | F5-18 (rerun-by-name uses frozen config), F5-20 (claims ship with byte-identical rerun evidence) |
| X6 | S6 / F6-04 | A 200x scale leg ran last week; its results are installed knowledge | F5-05 (legs run at 1x/10x/100x), F5-06 (100x is the top leg) |

## 2. PENDING items (6) — held as unverified, never installed, never stated as fact

| ID | Session / fact | Claim (as presented: unverified/debatable) |
|---|---|---|
| P1 | S1 / F1-18 | znc's `--fast-math` flag miscompiles signed division on ARM hosts |
| P2 | S2 / F2-18 | Tier-3 memories can self-repair bit-rot without a consolidation pass |
| P3 | S3 / F3-20 | G6 admissibility checks can be skipped for researcher chat turns |
| P4 | S4 / F4-19 | Intervention audits are unnecessary when every decision carries a trace |
| P5 | S5 / F5-15 | The 12-leg scale-rot amendment will halve rerun costs once signed |
| P6 | S6 / F6-20 | Review-style sessions boost long-horizon recall by 10 points |

## 3. Contradiction sources (3, all S5) — require explicit deliberation traces

| ID | Contradicting claim | Contradicts (3 earlier facts) | Required handling |
|---|---|---|---|
| CS-01 | Contributor note: audit entries are 12 words, stage@40 | F4-01 (16-word layout), F4-15 (stage=9 → stage word at 52), F1-17 (stage=9/d2 promotion rule) | Deliberation trace: detected, weighed, resolved with recorded provenance; silent overwrite = fail |
| CS-02 | Draft memo: PENDING items auto-install after 3 sessions | F3-16 (nothing auto-installs), F3-07 (chat answers never from PENDING), F4-08 (PENDING audit hard fail) | Same as CS-01; silent adoption = fail |
| CS-03 | Old design doc: pipeline order parse→intrinsic-lower→macro-fuse→desugar→codegen | F5-01 (pipeline order), F1-16 (macro-fuse before intrinsic-lower), F5-13 (order is load-bearing) | Same as CS-01; silent overwrite = fail |

## 4. Dependency pairs (6) — B (advanced) taught before its basic A

| Pair | B (advanced) | B session/fact | A (basic) | A session/fact |
|---|---|---|---|---|
| P1 | MACRO-FUSE must precede INTRINSIC-LOWER; reversal miscompiles `z_alloc` sites | S1 / F1-16 | znc pipeline stage order | S5 / F5-01 |
| P2 | stage=9 entries are promotion candidates only if d2 ≠ 0 | S1 / F1-17 | Audit entry 16-word layout | S4 / F4-01 |
| P3 | Tier-3 memory survives the sweep only if cite count > eviction floor | S2 / F2-13 | Eviction floor from tier-1 cite counts; below-floor demoted not deleted | S5 / F5-02 |
| P4 | G7 neuter audit fails a turn whose trace cites an unread slot | S2 / F2-14 | G7: trace causally consulted iff decision read the cited slot | S4 / F4-02 |
| P5 | SCALE-ROT amendment reruns legs with M1 stdout SHA ≠ REPORT.md | S3 / F3-11 | Scale leg = config × repeats; stdout SHA per leg in REPORT.md | S5 / F5-03 |
| P6 | PENDING cited in chat answers trips the leak check | S3 / F3-12 | Leak check audits every chat turn, not just probes | S5 / F5-04 |

Pre-basic probes (S4) cover pairs P1, P3, P5, P6 (As in S5, not yet taught).
Pairs P2, P4 have As in S4 → post-basic at S4 probe time; all 6 pairs get
post-basic probes at S6/S7.

## 5. Corrections (6) — researcher chat turns revising earlier facts

| ID | Session / turn | Target | Original proposition | Corrected proposition | Expected strong* |
|---|---|---|---|---|---|
| C1 | S3 / T2 | F1-01 | Pinned toolchain at `…/znc_linux_x86_64_abed8aa1` | Moved to `…/znc_linux_x86_64_c41d9e77`; abed8aa1 retired after the offset-rule rebuild | yes |
| C2 | S3 / T4 | F2-02 | Tier 3 = "pinned" | Tier 3 is "sealed"; "pinned" was the v1 name | yes |
| C3 | S4 / T2 | F1-14 | Aliasing class covers `as []i32` consecutive same-size casts | Same class covers `as []u16`; use []u8 arenas for u16 tables too | yes |
| C4 | S4 / T4 | F2-08 | Audit ledger is append-only | Ledger supports sealed truncation at session boundaries; append-only was v1 | yes |
| C5 | S5 / T2 | F2-07 | Tier-2 promotion needs 3 corroborating probes | Needs 2; bar lowered in the strength-trial rulings | yes |
| C6 | S5 / T4 | F1-09 | Bare `return` in void fn fails to parse; write `return;` | Bare `return` accepted since the September rebuild; `return;` still works | no |

\* "Expected strong" = the target was reinforced by repeated chat Q&A in S1/S2,
so the agent's judgment-set consolidation is expected to promote it to tier ≥2.
The G3 audit verifies against ACTUAL tiers — this column is intent, not verdict.
Five expected-strong targets (≥3 required), all from S1–S2 facts.

## 6. Session plan checklist (prereg §4.2)

- S1: 20 facts, 2 Bs (F1-16, F1-17), 1 PENDING (F1-18), 1 falsehood (F1-19), 6 chat turns ✓
- S2: 20 facts, 2 Bs (F2-13, F2-14), 1 PENDING (F2-18), 1 falsehood (F2-19), 6 chat turns ✓
- S3: 20 facts, 2 Bs (F3-11, F3-12), 1 PENDING (F3-20), 1 falsehood (F3-19), 2 corrections (C1, C2; ≥1 strong target ✓), 8 chat turns ✓
- S4: 20 facts, 2 As (F4-01, F4-02), 1 PENDING (F4-19), 1 falsehood (F4-18), 2 corrections (C3, C4; ≥1 strong target ✓), 8 chat turns ✓
- S5: 20 facts, 4 As (F5-01…F5-04), 1 PENDING (F5-15), 1 falsehood (F5-14), 3 contradiction sources (CS-01…CS-03), 2 corrections (C5, C6; ≥1 strong target ✓), 8 chat turns ✓
- S6: 20 facts (review-style), 1 PENDING (F6-20), 1 falsehood (F6-04), 6 chat turns (Q&A + 2 tasks) ✓
- S7: probe only ✓
