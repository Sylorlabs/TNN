# VERDICT — Arm V (BPE enemy), Track A closeout

**Date:** 2026-09-21
**Arm:** V — BPE enemy, adversarial baseline (ENEMY family)
**Adjudicated by:** verdict gap-fill crew (Track A closeout)
**Verdict: UNADJUDICATED** — the arm was never built (missing items below)

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> **Runs both directions:** V is beaten (retired as control, thesis advances) iff ≥1 TNN-native arm passes ≥2 of VC1–VC4: VC1 use-alignment (B4 ≥2× V's post-warmup); VC2 revision (B5 ≥10× fewer re-keyed bytes per edit); VC3 partial recall (B2 ≥3× better on misaligned spans); VC4 composition (B9 ≥20 pp). **Intellectual-honesty clause [REV]:** if V meets/beats the best TNN-native arm on a majority of the scored battery under signed weights and VC1–VC4 all fail, the thesis retreats to "chunks compose over tokens" — no goalpost-moving.

Mechanism (frozen): fixed subword tokenizer — 16,384 merges, both
corpora, frozen tie-breaks, Zag build-time trainer. "The thing to beat."

## Why UNADJUDICATED

There is nothing to adjudicate:

- **No build.** `cl/` contains no `arm.zag` (only `.zag-cache`);
  `substrate/` has only the shared R33 substrates; `work/` contains only
  `b64_test_bin`. No BPE trainer, no merge table, no tokenizer binary.
- **No battery.** The VC1–VC4 battery (B4/B5/B2/B9 vs TNN-native arms)
  was never run — for V or against it.
- **No fairness review.** The A-42 fairness checklist + one-page review
  ("before numbers count") was never done.
- The tracka-closeout inventory independently records V as
  "MISSING — Barely started. No verdict found. No scorecards."

Both directions of the criterion are unevaluable: no TNN-native arm can
be shown to pass ≥2 of VC1–VC4 against a nonexistent V, and the [REV]
intellectual-honesty clause cannot trigger without V's scored battery.

## What's missing (to adjudicate)

1. The V build itself: Zag build-time BPE trainer → frozen 16,384-merge
   tables for both corpora with frozen tie-breaks.
2. A-42 fairness checklist + one-page review (prerequisite before
   numbers count).
3. The VC1–VC4 battery: V's B4/B5/B2/B9 numbers and the head-to-head
   comparisons vs TNN-native arms under signed weights.

**Result: V UNADJUDICATED — never built; the adversarial baseline the
thesis must beat does not exist yet.**
