# H7 Broader-Fix Swarm — Coordinator Synthesis

**Date:** 2026-09-24
**Directive:** Micah refuses the 3/10 hypothetical-SINC-lookalike score and bets a broader fix exists. Go broader — architectural, curriculum, representation-level.
**Status of the bet after this swarm:** the strongest representation-level candidate is a **verified negative**. The bet is not yet lost — one legitimate route remains (new data, per the 2b proof's own §10 option 2) — but it needs Micah's signature and it is an experiment, not a guaranteed fix.

## What the swarm did

- **Outside investigation:** grok-4.7 delivered a ranked 5-proposal analysis (`outside/grok47_analysis.md`). gpt-5.6-sol was attempted 6 times; every attempt returned `choices: null` with 0 completion tokens (UnoRouter provider-side outage, not a prompt problem). claude-opus-5.5 / claude-fable-5.1 were NOT used (reserved for stumped problems per directive; this swarm produced concrete results without them).
- **Crew 1 (mechanism):** separation audit of scope-indexed markers against the real crew2 learner + curriculum, with a faithful Python simulation reproducing the committed baseline (33 hypothetical / 52 joke markers, exact 7 misses, joke NO 16/20, tr3 20/20). Build gate was 5/7 misses separated.
- **Crew 2 (curriculum/amendments):** concrete 48-item sincere-discourse calibration corpus, exact amendment texts (H7-A2/A3/A5), missing-bit sanity check against every frozen source, final ranking.

## The headline: scope-indexed markers are DEAD (verified negative)

grok-4.7's top proposal — install `(scope, bigram)` instead of bare 2-grams — rested on a premise that is **factually wrong for this corpus**: it claimed genuine exemplars installed `(MATRIX, "if the")`. Empirically, `"if the"` was installed by ex3_03 *"What if the harvest fails this season?"* — embedded at word index 1, **structurally identical to the sincere lookalikes** ("Ask if the shop is open" — also embedded, word index 1, one-word governor at index 0, complement-clause role). No MATRIX-installed `"if the"` key exists.

Audit results:
- Honest embedding depth fixes **2/7** misses. Most generous positional reading fixes **4/7**. Both < 5/7 build gate → **no fork was built** (correct stop).
- si3_14/16/18 ("Ask/See/Check if the …") are **structurally isomorphic** to the install exemplar on every generic feature. Only lexical-governor or length differences exist — both inadmissible (banned by HARD0 / collapse joke NO 16/20 → 6/20, the exact 2b trade-off replayed).
- The 2b impossibility proof stands **unrefuted and now strengthened**: the isomorphism runs deeper than the proof's own §5 check — even the finer structural feature the proof didn't examine fails, because the install exemplar itself is embedded.

This is evidence about the bet: the missing bit ("does marker m occur in sincere discourse?") is not hiding in utterance structure. It is genuinely absent from the frozen information structure.

## Ranked fix proposals (all evidence in)

| Rank | Proposal | Verdict | Label |
|---|---|---|---|
| 1 | **Sincere-discourse calibration corpus** (48 FL2 episodes, Phase 2c; 8 endorse + 8 withhold × 3 marker families: `if`/`do we`/`it is`; anti-confound controls; exact prereg replacement text in `crew2/CALIBRATION_CORPUS_PROPOSAL.md`) | Only route the 2b proof itself leaves open (proof §10 option 2: "supply the missing information legitimately"). Concrete, designed, deterministic. HONEST DOWNGRADE after Crew 1: projected 6–9/10, not certain 9/10 — the corpus was designed assuming scope keys; under bare keys FL2 revocation of `if the` may cost tr3 items that depend solely on it. Run as an experiment with full bar measurement, not a guaranteed fix. | **NEEDS MICAH'S SIGNATURE** (Phase 2c insertion) |
| 2 | **H7-A3: redefine "content"** (one paragraph: content-only = any feature computable from the utterance's concept graph incl. anonymous syntactic roles and scope-indexed n-grams; speaker/item-id/lexical type lists stay banned) | Zero-risk audit shield. Fixes nothing alone; protects any future representation work from being re-banned as if-specific. | **NEEDS MICAH'S SIGNATURE** |
| 3 | **H7-A2: factored decision** (Head A illocution / Head B overlay modality; joke bar re-anchored to Head B content-only, hypothetical-SINC bar to Head A structure-allowed; HARD0 applies to both heads) | Fixes the joint-bar contradiction architecturally (the 2b corollary). Big amendment surface; low standalone fix power for sinc_lk_3. The 10/10 path only via Head B per Crew 2. | **NEEDS MICAH'S SIGNATURE** |
| 4 | **H7-A5: eval admissibility** (§4 rule: speaker-only/item-id-only contrasts unscored; si3_15 "It is as if winter came early" — concept JOKE — as preregistered fallback candidate) | Honest eval-side fallback. Admits the proof for the items it truly covers. | **NEEDS MICAH'S SIGNATURE** |
| 5 | Scope-indexed markers (standalone) | **VERIFIED NEGATIVE.** Do not build. | — (dead) |
| 6 | Sincere-compatibility counter (HARD0-clean unsupervised mechanism) | Provably mode-3-equivalent: fixes sinc_lk_3, regresses joke NO to 15/20. A tradeoff, not a fix. | fits frozen, not recommended |
| 7 | Contrastive endorse pool alone (grok #4) | Predicted bar-neutral at best; ablation only. | fits frozen, not recommended |

Full texts: `crew2/RANKING.md`, `crew2/AMENDMENT_TEXTS.md` (exact H7-A2/A3/A5 wording with frozen-section quotes), `crew2/MISSING_BIT_CHECK.md` (proof §7 claim CONFIRMED across every frozen source — `sincere_count` = 0 for all three markers everywhere a teaching signal exists), `crew1/SEPARATION_AUDIT.md`, `crew1/FORK_VERDICT.md`.

## Single strongest recommendation

**Run the calibration corpus as a proper experiment — it is the only remaining legitimate move, and Micah's bet is not disproven, only narrowed.**

The 2b proof proves no mechanism can *manufacture* the missing bit from the frozen structure. It does not prove the bit is unlearnable — only that it must arrive as **new legitimate information**. The corpus supplies exactly that: sincere `if`/`do we`/`it is` constructions as FL2 teaching episodes, letting eliminative revocation observe the contradiction it has never seen. Pair it with H7-A3 (one paragraph, zero risk) so the audit trail is clean.

Concretely: sign Phase 2c (48 items, `crew2/calibration_corpus_items.txt`), run the full frozen battery with 3 byte-identical reps, and read the bar table honestly — if sinc_lk_3 moves to ≥9/10 with no regressions, the bet pays off; if it trades against tr3 or joke NO, we will have mapped the exact price of the missing bit, which is itself the answer to "how much does sincerity-compatibility cost."

What NOT to do: do not build scope-indexed markers (dead), do not accept 3/10 as a ceiling before the corpus experiment runs (the proof's option 2 is untested), and do not touch the frozen bars without a signature.

## Provenance

- grok-4.7 analysis: `outside/grok47_analysis.md` (6,854 chars, 2026-09-24)
- gpt-5.6-sol: 6 attempts, all provider-side `choices: null` — no output obtained
- Crew 1: `crew1/` (audit, verdict, faithful sim `sim_learn.py`, `audit_scope.py`, reference `src/h7_main_crew2.zag`, curriculum evidence copies)
- Crew 2: `crew2/` (corpus proposal + 48 exact items, amendment texts, missing-bit check, ranking)
- Zero RNG anywhere. No binaries, no `.zagd`. Nothing committed by crews; this commit is the coordinator's.
