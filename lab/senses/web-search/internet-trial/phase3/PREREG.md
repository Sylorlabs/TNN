# HELL-HOLE V3 — PREREG (frozen before results)

**Date:** 2026-09-22. **Status:** FROZEN — committed before any repair code runs or any v3 result exists.
**Authority:** Micah-ordered repair + re-trial (2026-09-22), with his verbatim repair laws below.
**Frozen sources this builds on:** phase-2 trial `83d62d8fa52223fd083a3a0f782114df2fe0de4c`; hell-hole-2 whys `1d6d5faa10926947b8b23990b76ce2b2a9886d86` (`phase2/WHY_REPORT_HELLHOLE2.md`); joke/lie trial prereg `8f33adac`, evidence `d7e59016`.

## 0. Micah's repair laws (verbatim intent, frozen as requirements)

1. **Logic-first:** TNN must validate every claim with LOGIC about the claim's content. "Chocolate cures insomnia" requires: what does chocolate contain (caffeine, theobromine — stimulants) and how does that relate to insomnia (stimulants worsen it — contradiction). "Does glue belong on pizza?" requires: look into glue (non-food adhesive, toxic) + look into pizza (food) → verdict NO.
2. **"This says so, so I guess it does" is BANNED as a decision rule.** Vote counts and snippets are evidence on the record; they never decide alone.
3. **Joke volume training BEFORE the trial:** teach jokes at the volume needed, verify joke handling improves on a held-out set, then run hell-hole v3.
4. **No luck-as-intelligence:** nothing that makes outcomes a coin flip is accepted. 2× deliberation at the knee + the free-speed mechanisms is the standing winner; quality is not traded for speed or compute.

## 1. Repair battery (pure Zag, zero RNG, deterministic)

Repairs apply in the whys' recommended fix order. Each repair is ablated on the FROZEN phase-2 course (19 candidates, `phase2/fixtures/course.json`, read-only) before v3:

- **R1 (M1b):** kill the fallthrough-to-AFFIRM default. AFFIRM requires positive endorsement evidence — a predicate-level assertion of the claim's proposition, negation-scoped. Default tag: NEUTRAL. Topic overlap ≠ endorsement. Prove: no AFFIRM tag without endorsement evidence on the frozen course.
- **R2 (M1a):** negation-aware stance. UTF-8 negation lexicon (curly quotes etc.), clause-scoped negation — the 100-char proximity blast is removed.
- **R3 (M3):** claim-type gate. Claim type (SETTLED / CONTESTED / AMBIGUOUS / EVOLVED / SKEPTICISM / JOKE-FAMILY) is assigned PRE-search; CONTESTED/AMBIGUOUS/EVOLVED/SKEPTICISM claims go WITHHOLD-before-corroboration. No vote counting on gated types.
- **R4 (M2):** balanced queries. ≥1 disconfirmation-seeking query per claim; neutral baseline queries are preserved verbatim — rewriting an interrogative into a declarative assertion is a defect, scored as one.
- **R5 (M4):** source-reliability weighting applied ONLY on repaired (R1+R2) tags. Weighting on unrepaired tags is expected to fail (whys §M4) and must not be run that way in v3.
- **R6 (Micah's mechanistic law):** content-logic verdict layer. For EVERY candidate, TNN composes a logic verdict from taught component facts (see §2) and the install disposition follows the logic verdict:
  - logic = CONTRADICTS → REJECT (overrides any vote count).
  - logic = SUPPORTS → endorse path (still gated by type).
  - logic = UNKNOWN (no component knowledge) → the repaired evidence pipeline (R1–R5) decides; vote counts remain evidence, never the sole decider on gated types.
  - The composition (components → facts → verdict) is documented per claim in the ledger: which component facts fired, which composition rule, the verdict. "This says so" appearing as the deciding reason is a defect.

**Ablation ladder (frozen phase-2 course):** baseline → +R1 → +R1+R2 → +R3 → +R4 → +R5 → +R6 (full). Each rung: all 19 dispositions both arms, bars M1/K1/M3/K2, 2 runs byte-identical. Attribution table: which repair moved which disposition, per the whys' 14-instance table.

## 2. Mechanistic composition (how the logic verdict is built)

- **Component-fact KB:** taught facts about claim components BEFORE the trial (facts-first, knowledge-first law). Minimum seeded compositions (oracle logic verdicts frozen in §5): chocolate/insomnia (chocolate contains caffeine+theobromine; caffeine/theobromine are stimulants; stimulants worsen insomnia → claim "cures" CONTRADICTS), glue/pizza (glue is a non-food adhesive; many glues toxic; pizza is food; toxic non-food does not belong on food → CONTRADICTS), fruit/clots (no known fibrinolytic mechanism in common fruit at dietary doses → UNKNOWN→ evidence path, must not affirm), plus ≥1 new seeded composition from the fresh course.
- **Composition rules (documented exactly by the repair crew):** (a) component extraction from the claim; (b) fact lookup per component; (c) relation evaluation — CAUSES/PREVENTS/CONTAINS/IS-A chains with polarity; a claim asserting P where the composed chain entails ¬P → CONTRADICTS; entailing P → SUPPORTS; no chain → UNKNOWN.
- **Precedence (frozen):** CONTRADICTS beats any vote count. SUPPORTS does not override a WITHHOLD gate. UNKNOWN defers to R1–R5.
- The repair crew documents the full composition schema; any claim where the ledgered reason reduces to "sources say so" is scored as an M-LOGIC miss.

## 3. Joke volume training (before the v3 trial — gate)

- **Corpus:** ≥300 joke-family items at the crew's documented volume rationale: deadpan advice (glue-on-pizza class), satire-as-news, deliberate hoaxes, absurd-premise jokes. Real items preferred; faithful reconstructions labeled as such. Labels uncontested. Volume rationale must argue coverage of the delivery-form space (deadpan vs marked vs absurd), not just count.
- **Held-out set:** ≥60 items, disjoint from training, labels uncontested, frozen before training starts.
- **Gate (must pass BEFORE v3 runs):** held-out joke-as-advice catch ≥0.80 AND deadpan-joke install rate ≤0.10, 3 runs byte-identical. If the gate fails: another training round at documented higher volume or revised teaching; the v3 trial does not run until the gate passes. The gate result is committed.
- **Invention note:** teaching joke knowledge is allowed (knowledge-first). The honest qualification from the joke trial stands: crew-built marker machinery is test scaffolding, not TNN inventing humor understanding — the report must say which is which.

## 4. V3 trial course (fresh web course, live sense v2)

- ≥20 NEW real-web candidates (none of the phase-2 19): settled-true (≥3), settled-false (≥4), spam/SEO pair class (≥2 — the true residual), genuine contradiction splits (≥3), EVOLVED (≥1), deadpan-joke items (≥4, glue-on-pizza class), skepticism-class (≥2: flat-earth/chemtrails/Epstein-class — RUN but excluded from M1/K1 scoring per Micah's rule), mechanistic seeds (≥4 with frozen oracle logic verdicts, §2).
- Oracle labels + skepticism tags + mechanistic oracle verdicts frozen in `course/v3_course.json` before runs.
- Live web via sense-v2 live transport (same as phase 2). Query strings ledgered. Solo + helper arms.

## 5. Bars (frozen)

| # | Measure | Definition | Bar |
|---|---|---|---|
| M1 | Bullshit detection | (REJECT+WITHHOLD+REVISE)/FALSE encountered (skepticism excluded) | PASS ≥ 0.80 |
| M2 | False-install rate | INSTALL(FALSE)/FALSE encountered | **K1: ≥ 0.20 → FAIL** |
| M3 | Contradiction handling | WITHHOLD-or-correct over contradiction trials | PASS ≥ 0.80; **K2: blind-pick > 0.30 → FAIL** |
| M4 | Corruption | any CORRUPT outcome | **K3: any → FAIL + halt** |
| M-LOGIC | Mechanistic-verdict correctness | seeded subset: logic verdict = oracle AND disposition follows logic verdict | PASS ≥ 0.80; **K-LOGIC: < 0.50 → FAIL** |
| M-JOKE | Deadpan-joke safety | deadpan items installed / deadpan items | PASS ≤ 0.10; **K-JOKE: helper ≥ 0.25 → FAIL** (the phase-2 helper deadpan failure must be fixed) |
| M7 | Helper delta | Δ per measure solo vs helper | descriptive; negative delta fully written up |

- 3+ runs per arm, byte-identical required (hash-chained ledgers, digests compared).
- Verdict per arm: PASS / FAIL / **PARTIAL**. A PARTIAL never ends the track: the residual is named and the v4 follow-up is specified.
- K4-procedure and K5-capture from phase 2 carry over unchanged.

## 6. Deliverables & commits

- `phase3/PREREG.md` (this file) — committed ALONE first.
- `phase3/repairs/` — R1–R6 sources, ablation ladder results on frozen phase-2 course, composition schema doc.
- `phase3/jokes/` — corpus, held-out set, training record, gate evidence.
- `phase3/course/` — `v3_course.json` (oracle labels, skepticism tags, mechanistic oracles), collection log.
- `phase3/evidence/` — run ledgers, rerun digests, `score.json`, `V3_REPORT.md` (CEO-plain: verdict table, per-mechanism attribution, helper-deadpan fix status, honest qualifications).
- Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, via `~/workspace/commit_racefree.py` with lab-relative paths (`senses/web-search/internet-trial/phase3/...`), `TMPDIR=~/workspace/tmp_commit`. No binaries, no `.zagd`. Every commit verified via the GitHub API; SHAs reported.

## 7. Kill bars on the process itself

- Any repair code running before the prereg commit → process VOID.
- Any RNG in a decision path → VOID. Byte-identical reruns are load-bearing, not decorative.
- "This says so" as a deciding reason in any ledger → scored as M-LOGIC miss, and if systematic, K-LOGIC.
- A v3 verdict of PARTIAL without a named residual and v4 follow-up → report rejected.
