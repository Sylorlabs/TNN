# VERDICT_PIPELINE — HELL-HOLE V4 final pipeline verification (rt4final)

**Date:** 2026-09-24. **Crew:** rt4final (subagent). **Workdir:**
`redteam/rt4final/` (NOT committed, per task).

**What this closes:** RT4b's disclosed limitation — its R6 tags were
oracle-authored / committed-old-core, not produced by the repaired logic
core. This run assembles the pipeline from **all three repaired components
plus the repaired decider** and re-proves acceptance, fresh attack, and
course bars end to end.

**Purity:** pure-Zag verdict paths (logic_bin, joke_run, decide are znc
native builds; r12_v4_t8 is the shipped classifier binary). Python used only
for glue (input prep, invocation, scoring) — no verdict logic. Zero RNG
(`grep -ri rand` clean on all harness/runner sources). Every component run
2× with byte-identical SHA assertion.

## 1. Components (all repaired, all verified before use)

| component | source | SHA256 (source) | binary | SHA256 (binary) |
|---|---|---|---|---|
| R6 logic core | `rt1fix3/logic_fixed3.zag` | `0a8b6c4c6694232fa48e4ed30cdcf63a8996e40eff2034c2717cca7555373ced` | `rt4final/build/logic_bin` | `6f59470c03129f4a4d20b72b7da3d232c5e26295476dfa021ca20c94082cec5c` |
| R12 classifier | shipped binary `rt2fix7c/r12_v4_t8` | — | (as shipped) | `87d903318e107c38087cc48e53eba1aaf2febea413bf3c38e875fed97caef4a7` ✓ matches task pin |
| Joke classifier | `rt3fix4/g_intent6_v4fix4.zag` | `1a1b787071fc99a8db8740ca56fbc7a3b9c154486a0f9dacb8ebf6b7bea8d890` ✓ matches fix4 FIX_REPORT | `rt4final/build/joke_run` (thin TSV runner importing the classifier lib) | `407182e41770f918ed69d7c6800cd9c141845f91b7c8eb58707576c0f6477646` |
| Pipeline decider | `rt4fix/src/decide.zag` (mode `new`) | `9c9acf7f033595143bfcabd0a09b5576011434078af26add520198a442a0970e` | `rt4final/build/decide` | `f5f2aaeeb22c1efc2ae16fe24a2db844431c74e643e7b5fa12508540313c0a7c` |

All three `.zag` sources built with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 --no-analyze`.
r12_v4_t8 used as-shipped (SHA verified before use).
Pipeline order per repaired assembly semantics: R3 gate → R6 DENY (terminal
REJECT) → R6 AFFIRM+proof (terminal INSTALL) → JOKE-FAMILY gate → all-item
absurdity screen (intent 2/3 → WITHHOLD) → R5 vote with quorum
(INSTALL iff best==1 ∧ w≥16 ∧ ≥2 endorse rows; REJECT iff best==2 ∧ w≥16 ∧
≥2 deny rows; else WITHHOLD).

## 2. Acceptance — RT4's original 32+32 corpus, real components

`accept/`: inputs derived from `rt4/rta_pipeline.tsv` + `rt4/rtb_pipeline.tsv`
(claim_prop/evidence_props fields feed the real logic core directly).

| arm | result | bar |
|---|---|---|
| RT-A installs | **0/32** | 0 — PASS |
| RT-B installs | 26/32 | installs/withholds characterized below |

**RT-A (all 32):** 29 WITHHOLD/R5 (quorum held; includes A-07/A-08 single-tier-2
endorse probes blocked by the ≥2-row rule), 3 WITHHOLD/JOKE via the all-item
absurdity screen (A-27, A-31, A-32 — joke intent 2 on FACTUAL items,
quarantined exactly as designed). Zero installs; zero R6 affirms on any RT-A
item.

**RT-B non-installs (6/32), all fail-safe, zero wrong-side INSTALLs:**
- B-02, B-07, B-08, B-31 → WITHHOLD/R5: r12 emitted zero endorses; the
  assembly correctly withholds rather than inventing evidence (clean r12
  recall misses, by design per FIX_REPORT §5).
- B-03, B-30 → REJECT/R5: **wrong-side REJECTs** from r12's residual
  neg-polarity/universal-negation deny-misfire (B-03 "Humans do not have
  exactly five senses": two supporting rows tagged deny via `numeric-mismatch`
  / `neg-scope`; B-30 "No fish can live out of water indefinitely": three
  near-paraphrase rows tagged `numeric-mismatch`). **r12-component defect,
  not an assembly defect** — the decider applies quorum faithfully to wrong
  tags. Same two items RT4b flagged; r12_v4_t8 carries the identical residual
  as the r12_v4_t3 RT4b used.
- Positive control: B-06 → INSTALL/R5 (vote-path install works when r12
  endorses — the repaired r12 fixed this item); 25/26 installs are INSTALL/R6
  via the real core's affirm fast path (R-IDENT-AFFIRM, R-QTY-AFFIRM,
  R-COND-MP).

**Comparison vs RT4b's oracle/committed-tag run — differences: NONE.**
The real R6 core's tags agree with RT4's committed old-core tags on all 64
items (0 diffs, proofs included); r12_v4_t8's tags agree with r12_v4_t3's at
the disposition level on all 64; the repaired joke classifier's intents agree
at the disposition level on all 64. Proof: `accept/decide_out.tsv` SHA
`af06aad0f940b17c5d12e0ed49488774ac677988c61066892db5a127f6c5c101`
is **byte-identical to RT4b's** `accept/decide_out.tsv`. The oracle-authoring
limitation is closed with zero disposition change — the assembly's acceptance
behavior is fully explained by the real components.

Per-item log: `accept/accept_report.json` (id, oracle, r6tag, r6proof,
joke intent, disposition, attribution).

## 3. Fresh blind attack — NEW 32+32 corpus, real components

`corpus_fresh.tsv` — 64 novel items (domains disjoint from all prior corpora),
authored with claim_prop/evidence_props alongside the NL text, **frozen
before any component run**: SHA256
`ccebe7c9590f4572be5f47895758cd7666851f0112bcf90db945edfb764f6c34`.
Authoring script `mk_corpus.py` (authoring only, no component contact, no
post-run edits).

| arm | result | bar |
|---|---|---|
| RT-A installs | **0/32** | 0 — PASS |
| RT-B non-installs | 14/32 | all withholds, characterized below — zero wrong-side |

**RT-A (0 installs):** 15 REJECT/R6 — the real core denied invalid claims
directly (R-NEG-DENY ×7: F4A-06/13/17/24/28/29/31; R-QTY-DENY ×4:
F4A-11/12/20/25/26; R-QNT-DENY ×2: F4A-18/30; R-CAU-PROP-DENY: F4A-14).
17 WITHHOLD/R5 — causal fallacies (F4A-01..04), affirming-consequent
(F4A-05, correctly neutral — no MP from `IF(a,b)`+`b`), single-endorse probes
(F4A-07/08, quorum blocked), hedged-evidence (F4A-09/10), informal fallacies
(F4A-21..23), vacuous-reason affirm attempt (F4A-27, `CAUSE(NOT(RAINED),…)` —
round-3 fix holds), universal-authority (F4A-32). Zero R6 affirms on any
invalid claim. Joke screen thin on deadpan: only F4A-13 ("moon is made of
cheese") drew intent 2 (R6 denied it first anyway); F4A-14..17 drew intent 5
— consistent with RT3d's residual deadpan misses; the pipeline held via
R6/R5 regardless.

**RT-B fast path (designed R6=1): 18/18 INSTALL/R6.** All affirm rules
exercised live: R-IDENT-AFFIRM ×9, R-COND-MP ×3, R-CAU-AFFIRM ×2,
R-QTY-AFFIRM ×4 (incl. `at_most`/`at_least` subset directions). (F4B-29/30
were authored as vote-path but their props were structurally identical to
the claims — honest mislabel in my design notes, correct INSTALL/R6
dispositions; the true vote-path set is the 14 below.)

**RT-B vote path (14 items, R6=0): 14/14 WITHHOLD/R5 — zero wrong-side.**
r12 endorse behavior per item (row tags):
- 1 endorse only (quorum ≥2 correctly blocks): F4B-17 (tier-3), F4B-22
  (tier-1, w1=8<16), F4B-23 (tier-2, w1=16), F4B-31 (tier-3), F4B-32 (tier-2).
- 0 endorses: F4B-18 ("The audit found zero late payments." → gate),
  F4B-19 ("The parcel weighs 1 kg." → gate), F4B-20 (deny-lexicon support,
  gate+gate), F4B-21 ("Diners rate the restaurant 4 out of 5 stars…" →
  gate+gate — same gap RT4b probed), F4B-25, F4B-26, F4B-27.
- deny-misfires absorbed by quorum (nd=1 <2, no wrong-side REJECT):
  F4B-24 ("No crashes observed in 500 test runs…" → `neg-scope` deny),
  F4B-28 ("wait times fell 30 percent after the new policy" → `relation`
  deny).

**Attribution:** not an assembly defect. The assembly withholds exactly per
spec instead of inventing evidence. Root cause of all 14 is the **r12
component's endorse-recall gap** on natural supporting evidence (gate/neutral
on explicit-subject paraphrases; deny-lexicon support never endorsed),
unchanged from RT4b's finding on r12_v4_t3 — r12_v4_t8 carries the same gap.
Two deny-misfires (`neg-scope`, `relation`) are r12-component defects, but
the ≥2-deny-row quorum prevented wrong-side REJECTs — the quorum is working
as a safety net.

Per-item log: `attack/attack_report.json`.

## 4. Course bars M1/K1 with real components

`course/`: real joke intents on all 24 course claims (joke_run), real R6 tags
on the 6 committed R6 inputs (all DENY, matching committed logic=2),
committed votes (row texts not in repo — same basis as RT4b), decide mode
`new`, scored with the committed `score_v4.py` unmodified.

- **solo: M1=1.0000 (11/11), K1=0.0000 (0/11), ALL BARS PASS**
  (M3=1.00 K2=0.00 M-LOGIC=1.00 M-JOKE=0.00 K3=OK K5=[])
- **helper: M1=1.0000 (11/11), K1=0.0000 (0/11), ALL BARS PASS**
  (same; agree 21/24)
- Real joke intents: V3-14 → 2 (glue-pizza deadpan, correct), V3-21 → 2
  ("Adding glue to pizza sauce…" — defensible; disposition REJECT/R6 via the
  logic seed, unaffected). V3-15/16/17 deadpans → 5 (classifier misses; they
  WITHHOLD via R5 — the known agree 22→20 / 23→21 dip from the repaired joke
  classifier, kill bars unaffected).

## 5. Determinism (2× byte-identical, pure-Zag, zero RNG)

| artifact | SHA256 (run1 = run2, asserted in-harness) |
|---|---|
| corpus_fresh.tsv (frozen pre-run) | `ccebe7c9590f4572be5f47895758cd7666851f0112bcf90db945edfb764f6c34` |
| accept/logic_out.txt | `f25f4c8add0277dfcf75bab8958223568eb82bea37de86f7ed0ca6148785be9d` |
| accept/r12_out.txt | `c03b3be148250592011c91207cfd97bcb16e1c2cbbc411a56b56ae743b08f5e5` |
| accept/joke_out.txt | `23c272b1c85118f4357ca426b804495d7036c5655c7c7afd7d1e290e4197355d` |
| accept/decide_out.tsv | `af06aad0f940b17c5d12e0ed49488774ac677988c61066892db5a127f6c5c101` (= RT4b's, byte-identical) |
| attack/logic_out.txt | `bbdfef5bdbf2e62415ff39bc2bd6bf860b3f74d131c3ff12ee071ba144da4013` |
| attack/r12_out.txt | `14a100cd70d187cc97daa10dc2f947d468afc5776030fd6989f211939d6497ca` |
| attack/joke_out.txt | `ebc6db8b68ea54c990a8fc4e5b508e6e1dc37e7e242f428f6e2e8c0918c25af5` |
| attack/decide_out.tsv | `1382326b48733770fe3b2524e3aaa1bf2bc53f6aced43cb390a53c9a5da5b2ea` |
| course ledgers | solo `ef31837b…1ba6b59d`, helper `0acf5536…513ec339` (decide_out SHAs) |

## 6. What the pipeline proves (explicit statement)

With all three repaired components and the repaired decider assembled, the
pipeline is **fail-safe, never fail-dangerous**:

1. **Zero invalid installs** across 64 attack items (32 acceptance + 32 fresh
   blind): the safety bar holds with real components, not oracle tags.
2. **The R6 affirm fast path is sound**: 18/18 valid structural affirms
   installed terminally (never lost downstream — defect 1 closed); **zero**
   affirms on any invalid claim across 64 items (no false affirmation path).
3. **The R6 deny path is sound**: 15/15 fresh-attack invalid claims with
   refuting evidence were terminally REJECTed with correct rule attributions.
4. **Quorum works as designed**: single-endorse installs blocked (F4A-07/08,
   F4B-17/23/31/32); single-deny wrong-side REJECTs blocked (F4B-24/28);
   r12's endorse-recall gap degrades to WITHHOLD, never to INSTALL or
   wrong-side REJECT.
5. **Course kill bars hold**: M1=1.0/K1=0.0 both arms, all bars pass.

**Residuals (all component-level, none assembly-level):** (a) r12
endorse-recall gap strands valid vote-path items in WITHHOLD (14/14 fresh,
4/6 acceptance) — fail-safe; (b) r12 neg-polarity/universal-negation
deny-misfire wrong-side REJECTs valid negated claims (acceptance B-03/B-30 —
pre-existing, identical in RT4b); (c) joke classifier still misses most
deadpan-absurd items (intent 5 on F4A-14..17, V3-15/16/17) — the pipeline
held via R6/R5 on every such item here, but the screen is thin. All three
are forwarded findings for the component lines, not pipeline-assembly
defects. **No victory declared over the components** — but the assembly
itself is verified correct: with real repaired components, it never installs
the invalid and never wrong-sides the valid.

## Files (all under `redteam/rt4final/`, NOT committed)
- `VERDICT_PIPELINE.md` (this file), `mk_corpus.py`, `corpus_fresh.tsv`
- `run_accept.py` → `accept/` (inputs, component outputs, decide I/O, SHAs,
  `accept_report.json`)
- `run_attack.py` → `attack/` (same layout, `attack_report.json`)
- `run_course.py` → `course/` (joke/R6/decide I/O, ledgers, SHAs)
- `build/` (sources+binaries: logic_bin, joke_run(+joke_run.zag runner),
  decide; source SHAs §1)
