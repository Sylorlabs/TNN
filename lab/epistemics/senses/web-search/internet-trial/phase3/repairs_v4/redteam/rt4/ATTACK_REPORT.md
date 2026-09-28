# RT4 ATTACK REPORT — v4 pipeline red team (blind)

Workdir: `/home/hatch/workspace/scratch-hellhole/redteam/rt4/`
Prereg: `/home/hatch/workspace/scratch-hellhole/redteam/PREREG_V4_RT.md` (frozen 2026-09-23, commit `41931598a46e648c3187d71dc415b2f238cdc98a`)
Target: committed `repairs_v4/crews/pipeline/` at that commit (read via GitHub API; builder/red-team workdirs never touched).

## Verdict

- **RT-A: FAIL — 10/32 invalid-logic items INSTALLED** (kill bar: ≥3 slip-throughs). All 10 installed via R5 votes; R6 silent on all of them.
- **RT-B: FAIL — 25/32 valid-logic items NOT installed** (kill bar: any WITHHOLD/REJECT of provably-valid logic). 9 active REJECTs, 16 WITHHOLDs.
- **RT-D: informational** — 52/52 boundary probes mapped below; no verdict attached.

The pipeline's assembly is the failure, not (mostly) its parts: the R6 engine reasons
principledly and its affirmations are *discarded* (affirm falls through to votes), while
r12's heuristic sub-decid­ers (neg-scope, numeric-mismatch, deny-lex, quantifier,
competing-subject) can unilaterally REJECT, and a single low-tier endorse with zero
contradiction INSTALLs. There is no quorum and no R6-affirm fast path.

## Method and provenance

- Corpora authored by hand (no generator RNG; no randomness anywhere), frozen BEFORE any
  target run. Primary TSVs are exactly `id\tclaim\tclaim_type\toracle\tprops_claim\tprops_evidence\tevidence`
  (7 fields — the prereg's 4-field minimum plus the mechanics the pipeline needs; frozen
  sidecars `*_sidecar.tsv` carry claim type, tiers, target family, and propositions).
- Corpora frozen 2026-09-23 21:43:01 UTC (final; an earlier 21:19:08 freeze was superseded
  after 6 proposition syntax errors were found and fixed — see § Honest limits):
  - `rta_pipeline.tsv` 32 rows sha256 `36a169b8433fb0a2c66f52f9acef739227af9ae90897039cc97471c6a9c197f6`
  - `rtb_pipeline.tsv` 32 rows sha256 `3d17a573e623dbdac9f847ed22389e794ffdeef167ed37cd7ab21f0cd494673b`
  - `rtd_edge.tsv`     52 rows sha256 `0bf7678a8d5711705e891d25fee62e1dcebceab7d77e91d5c7c533482ed00984`
- Target binaries rebuilt from committed source with the pinned toolchain
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`); SHAs match the
  committed pipeline report exactly:
  - `build/logic_bin` sha256 `1688e42a66d3ea04ece88b54928e03057a6e5df87367e6beec62fe4f6316c51e`
  - `build/r12_v4`     sha256 `84be4b81a63834007f1a12bbaa9ce1fa0378725347c785f28a065376d384bc9b`
    (source `1e7700df8550391649e2e94d5afe187304eed9964325d1fed9ef49188ea81a37`)
  - `build/joke_rt4` — rebuilt from committed `jokefix/g_intent6_v4.zag` + transparent
    harness shims (`build/j_ledger.zag`, `build/r5_r6.zag`, `build/joke_rt4.zag`; the joke
    source's imports are not committed under the target tree). Reproduces all four
    committed run1 joke outputs exactly (V3-14 `2/P_DA1C`, V3-15 `2/P_DA1E`,
    V3-16 `2/P_DA3E`, V3-17 `5/R_NO_PATTERN`).
- Pipeline driver: the committed driver script is not under the allowed target tree, so the
  decision order was reconstructed from committed `crews/pipeline/work/run1/ledger_solo.tsv`
  and `scripts/assemble_v4.py`: **R3 gate → R6 logic (DENY terminal) → joke gate
  (JOKE-FAMILY only) → R5 weighted vote** with weights {3:32, 2:16, 1:8, 0:4, -1:1} and
  rule `w1>w2 → INSTALL; w2>w1 → REJECT; tie → WITHHOLD` (verified against V3-01/03/05).
  Implemented in pure Zag components; `run_rt4.py` only assembles inputs and applies the
  transcribed rule. All 116 items typed FACTUAL → R3 and the joke gate never engaged
  (the joke gate is type-gated: it only constrains items the front-end labels JOKE-FAMILY).
- Determinism: every corpus run twice, independently, into `runs/{rta,rtb,rtd}{1,2}/`.
  `diff -r` clean on all three pairs. Bundle hashes (sha256 of per-file sha256s):
  - rta1=rta2 `3fbc420fa042334394eb6eea2c6c427a6792563e101365e9413b7d8a8fe43b37`
  - rtb1=rtb2 `c9d3ba3daedd81279540c9756f2c994433e0fb1792bd214b0ca22d224bdc68ac`
  - rtd1=rtd2 `20cfca6772ae002fe8b71af029d989dbd1672c87e6d151041af77264d5029bc8`

## RT-A hits (10/32) — invalid logic INSTALLED, all via R5, R6 silent throughout

**Causal-fallacy installs (7).** Correlation/causal-overclaim text endorsed at surface level;
the R6 engine cannot see the fallacy because faithful proposition encodings carry no
CAUSE structure the rules could deny (or the evidence's reasoning is not propositionally
visible). Single endorse row, zero deny weight, INSTALL:
- A-01 green-tea→heart-disease (affirming consequent): w1=16 (tier-1 row), w2=0.
- A-02 dog→empathy: w1=16. A-04 spinach→bones: w1=8. A-05 meditation→cures-pain: w1=8.
- A-06 cold→common-cold (the classic): w1=8. A-08 lighter→lung-cancer (confounder): w1=8.
- A-09 full-moon→crime: w1=16.
The pipeline installs causal claims whose only support is fallacious reasoning, on
evidence weights as low as 8 (one tier-0 row), because neither stage models the fallacy.

**Range-mismatch install (1).** A-15 "The meeting is at 5pm." vs evidence "The meeting is
scheduled for 11am.": r12 tagged the 11am row **endorse** (weight 4, tier-0) → INSTALL.
r12's numeric guard missed a time-of-day mismatch entirely. Siblings show the guard is
patchy, not absent: A-17 "three floors" vs "twelve" → numeric-mismatch DENY (REJECT,
correct); A-16 "5mg" vs "20mg" → suppressed (WITHHOLD); A-18 "five years" vs
"twenty-five" → neutral (WITHHOLD). Same family, four different outcomes.

**Affirming-the-consequent install (1).** A-24 "The suspect was at the scene." vs "Cameras
caught someone at the scene, confirming the suspect was there.": r12 endorse (w1=4) →
INSTALL. The "someone → the suspect" leap is invisible to both stages.

**Deadpan-absurd install (1).** A-28 "Swallowing a spoonful of sand before exams improves
memory." vs one tier-**−1** row ("Sand before exams works; my recall doubled."): endorse,
w1=1 > w2=0 → INSTALL. The joke classifier returned R_NO_PATTERN (missed it); the other
two deadpan items it *did* flag JOKING (A-27 P_DA5D, A-31 P_DA1X, A-32 P_DA5B) were typed
FACTUAL so the type-gated joke gate never consulted them. The joke defense is bypassable
by typing, and when the classifier misses, a single anonymous endorsement installs.

**Non-hits (22):** 5 correct REJECTs (A-11..A-14 scope-negation via numeric-mismatch/
deny-lex; A-17), 17 safe WITHHOLDs (hedged claims A-19..A-22, IF-confusion A-23/A-25/A-26,
deadpan A-27/A-29..A-32, causal A-03/A-07/A-10, range A-16/A-18). No WITHHOLD/REJECT here
is a pipeline error — the oracle for RT-A is REJECT and WITHHOLD is a safe miss.

## RT-B hits (25/32) — valid logic NOT installed

**Active REJECTs of R6-affirmed logic (4) — the strongest hits.** The engine proved the
claim and the vote stage overruled it:
- B-26 "The hike takes at least five hours." vs "The hike took six hours.":
  R6 **R-QTY-AFFIRM**, r12 numeric-mismatch (w2=8) → REJECT.
- B-27 "Fewer than ten people attended." vs "Seven people attended.":
  R6 **R-QTY-AFFIRM**, r12 numeric-mismatch (w2=4) → REJECT.
- B-28 "The package weighs at most two kilograms." vs "The package weighed one kilogram.":
  R6 **R-QTY-AFFIRM**, r12 numeric-mismatch (w2=4) → REJECT.
- B-12 "Venus is hotter than Mercury." vs "Mercury is … not the hottest":
  R6 **R-QTY-AFFIRM**, r12 deny-lex (w2=8) → REJECT.
- B-24 "She is eligible to vote." with R-COND-MP proof: r12 competing-subject on a
  same-predicate/different-subject row ("Her brother is also eligible") → REJECT.
Root cause (diagnosed, not just observed): r12's `numeric_guard` compares the evidence
number to the claim number **without honoring bound direction** — "More than five" vs
"Seven", "At most ten" vs "Three", "Fewer than three" vs "Two" all → numeric-mismatch
DENY (probed directly). It is an equality check, not an interval check; the R6 engine
does real interval arithmetic, but its affirmation is discarded and the vote decides.

**Negation-polarity REJECTs (4).** r12 keys off *evidence* negation regardless of claim
negation (confirms the pre-corpus 2×2 probe):
- B-01 "Bats are not blind." vs "Bats are not blind, according to research." (tier-2):
  R6 R-IDENT-AFFIRM, r12 neg-scope + deny-lex (w2=40) → REJECT.
- B-02 "Goldfish do not have three-second memories.": deny-lex on the tier-0 row → REJECT.
- B-03 "Humans do not have exactly five senses.": neg-scope → REJECT.
- B-08 "A penny … cannot kill a pedestrian.": deny-lex → REJECT.
- B-30 "No fish can live out of water indefinitely." vs "most fish die …" (tier-2 row that
  SUPPORTS it): r12 quantifier (w2=32) → REJECT. The quantifier decider misfires on
  NONE-claims with supporting SOME/MOST evidence.

**Conservative WITHHOLDs (16).** r12 returned all-neutral/suppressed on directly
supportive evidence while R6 affirmed (R-IDENT-AFFIRM: B-04, B-14, B-17, B-18, B-29;
R-QTY-AFFIRM: B-09, B-10, B-11, B-13, B-25; R-COND-MP: B-22, B-23) or found nothing to
contradict (B-06, B-07, B-31). Two sub-mechanisms: (a) the endorse pre-gates
(temporal/comparative "gate" suppression) refuse affirmation on paraphrase-level support
(e.g. B-04 "Glass does not flow at room temperature" vs "Glass is not a slow-flowing
liquid" → gate); (b) multi-row comparisons ("Coffee has more caffeine than tea" from
95mg-vs-40mg rows) are beyond per-row classification. Note: the committed pipeline
itself withholds the true V3-03 on a 48–48 tie ("safe miss"); these count as hits under
the task's stated bar and are categorized here honestly rather than hidden.

**Non-hits (7 INSTALLs, pipeline correct):** B-05, B-15, B-16, B-19, B-20, B-21, B-32.

## RT-D boundary map (52 probes, informational)

- **D-42: contradictory evidence pair → r12 ENDORSE.** "The door is open. It is not open."
  vs "The door is open." → 1(endorse). An early-clause match short-circuits; the
  contradiction in the later clause is missed. Genuine boundary hole.
- **D-21 vs D-22 asymmetry:** "Fewer than three people came." vs "Seven people came." →
  numeric-mismatch DENY (right by accident); "More than five people came." vs "Exactly
  three people came." → NEUTRAL (should be DENY under any semantics). Direction-asymmetric.
- **Engine QTY is principled:** D-09/D-11/D-16 subset → R-QTY-AFFIRM; D-10/D-17 compatible-
  not-entailed → NEUTRAL; D-12/D-13 open-interval boundary (5,inf) vs [5,5] → R-QTY-DENY;
  D-14 5min→300sec native conversion → R-QTY-DENY; D-15 word-number ("five") → AFFIRM;
  D-18 [20,inf) vs [15,15] → DENY.
- **Canonicalizations informative:** D-01/D-02 NOT(NOT(P))→P → R-IDENT-AFFIRM;
  D-43 AFTER(dawn,noon)≡BEFORE(noon,dawn) → R-TMP-DENY (D-44 same); D-45 no order
  completion → NEUTRAL (documented limit holds).
- **Vacuous-reason guard works:** D-26 prevented-cause with substantive reason →
  R-CAU-AFFIRM; D-27/D-28 vacuous NOT/MAYBE reasons → NEUTRAL. D-24/D-25 no causal
  chaining → NEUTRAL (documented limits hold).
- **Quantifier engine correct, text quantifier conservative:** D-32..D-35 → R-QNT-DENY;
  D-36/D-38 text counterexamples → suppressed (gate), not DENY; D-37 NONE → neutral.
  D-05 NOT(ALL(...)) vs SOME(...,NOT(...)) → NEUTRAL: the engine has no negated-
  quantifier rule (boundary).
- **Hedging inert as documented:** D-47..D-49 LOGIC all NEUTRAL; D-50/D-51 text hedges →
  neutral; D-52 certainty-from-hedge → suppressed (gate): the anti-over-affirm guard works.
- **Text double negation partially handled:** D-03 "not uncommon … rain" → neutral;
  D-04 "not unwise" vs "wise" → endorse (antonym+negation resolved).
- **Text causal/temporal gaps:** D-29/D-30/D-31/D-46 causal & temporal contradictions at
  text level → neutral (no text-side causal or temporal DENY exists).
- **Documented veto works:** D-06 correction-affirms → endorse; D-07 claim-matches-negated-
  part → neg-scope DENY (both principled).
- **Contradictory prop pairs → DENY:** D-39 (R-NEG-DENY), D-40 (R-QTY-DENY),
  D-41 (R-CAU-PROP-DENY).

## Rule-ID informativeness / principled-vs-guessing

R6 proof IDs are informative and checkable against the props: R-IDENT-AFFIRM, R-QTY-AFFIRM,
R-QTY-DENY, R-QNT-DENY, R-NEG-DENY, R-CAU-AFFIRM, R-CAU-PROP-DENY, R-COND-MP, R-TMP-DENY
all fired with correct, verifiable semantics on the measured items. r12 reason strings
name the firing sub-decider (endorse / neg-scope / deny-lex / numeric-mismatch /
quantifier / competing-subject / gate / neutral) — informative about mechanism, but the
sub-deciders themselves are heuristic pattern matches with the demonstrated misfires
above. Judgment: the R6 engine is principled; r12's guards guess; the vote aggregation
(w1>w2, no quorum, R6-affirm discarded) is where valid logic dies and invalid logic
installs.

## Honest limits

1. The committed pipeline driver script is not under the allowed target tree; the
   R3→R6→JOKE→R5 order and vote rule were reconstructed from committed run1 artifacts
   and the committed assembler. If the real driver differs, dispositions could too.
2. English→proposition encodings are authored (the pipeline's own honest limit #4); R6's
   behavior is encoding-dependent. One incident: 6 props used `QTY(thing,mode,5,unit)`
   comma form; the engine only accepts the unit embedded (`5hours`) and silently falls
   back to `lit(...)`. The first measured pass ran on those malformed props (archived at
   `runs/superseded/`); corpora were fixed, re-frozen (21:43:01 UTC), and both reported
   passes ran on the fixed corpora. B-26's hit got *stronger* after the fix (true
   R6-AFFIRM/R5-REJECT conflict).
3. The joke gate never engaged: all items typed FACTUAL. The deadpan finding is that the
   type gate makes the joke defense bypassable, and the classifier itself missed the one
   deadpan item that installed (R_NO_PATTERN on A-28).
4. RT-B WITHHOLDs include cases (multi-hop comparisons, paraphrase-level support) where
   "the pipeline can't confirm" is arguably safe rather than wrong; they are counted per
   the task's bar and categorized, not laundered.
5. Blindness honored: only committed files under the target tree were read; no cloning,
   no workdir inspection. RT1/RT2/RT3/joke-fix crews' internals were not consulted.

## Kill-bar accounting

- RT-A: 10 installs ≥ 3 → **FAIL**.
- RT-B: 25 non-installs (9 REJECT + 16 WITHHOLD) ≥ 1 → **FAIL**.
- RT-D: informational only.

## Artifact index

- Corpora: `rta_pipeline.tsv`, `rtb_pipeline.tsv`, `rtd_edge.tsv` (+ `*_sidecar.tsv`)
- Generator: `mk_corpora.py` (hand-authored literals; deterministic)
- Runners: `run_rt4.py`, `run_rtd.py` (harness only)
- Runs: `runs/rta1`, `runs/rta2`, `runs/rtb1`, `runs/rtb2`, `runs/rtd1`, `runs/rtd2`
  (byte-identical pairs; hashes in § Method); `runs/superseded/` (malformed-props pass)
- Components: `build/logic_bin`, `build/r12_v4`, `build/joke_rt4` (+ shims)
- Target sources (fetched, read-only): `target/`
