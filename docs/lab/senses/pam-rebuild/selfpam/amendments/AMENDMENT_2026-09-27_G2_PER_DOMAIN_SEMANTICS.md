# Amendment 2026-09-27-G2 — Per-domain admission semantics (ENACTED)

**Status:** ENACTED per Micah's word, 2026-09-27 ~18:18 PDT. This is a
governance decision, not a crew proposal. It supersedes the unsigned draft
`AMENDMENT_2026-09-27_G1_FIX1.md`'s single-variant recommendation.

## The ruling

The self-PAM admission gate uses **different equality semantics per domain**:

- **Text / intelligence → APPROXIMATE equality.** "Just because something is
  related doesn't mean it's wrong." A claim that is related-but-true must not
  be withheld for failing to be identical. The approximate comparator for text
  must be a genuine semantic architecture, not a byte-sum — the legacy sum
  (312/312 adversarial admits) and the weighted variant (104/312 adversarial
  misses, per NW-1) are both disqualified as text semantics.
- **Video / image / audio regeneration → EXACT identity.** Where the point is
  regenerating the thing itself, only exact holds: the FNV-1a exact variant
  (id4) is the only tested variant at 100% (1,200/1,200 frozen corpus,
  312/312 adversarial expansion, 20/20 must-admit). The weighted middle is
  dead (NW-1: misses 104/312 while being exactly as strict as exact on
  benign noise — all cost, no benefit).

## Consequences

1. **Fix the cost of exact's weirdness (media line).** Exact withholds on
   benign differences (re-encodings, re-captures, rounding) as hard as on
   adversarial ones. The media line must mitigate this architecturally —
   e.g. canonicalize-then-fingerprint — without reintroducing aggregation
   blind spots. The canonicalizer becomes the new attack surface; red-team
   it as such.
2. **Build genuine approximate equality (text line).** A native architecture
   for text/intelligence admission where paraphrase and related-but-true
   claims are admitted and genuine confabulations are withheld. Synonym
   lookup tables are rejected as disguised hardcodes.
3. The §8 draft's SPAN-SUM value remains untouched; these semantics govern
   the candidate-experimental gate ids, not the frozen draft.

## Evidence grounding

- NW-1 noise-response results: `selfpam/noise_response_2026-09-28/REPORT_NW1.md`
  (commit `b552c209d882370d17aeec339a3932d317926afa`).
- Fix1 + adversarial expansion: commits `794021e7`, `a5bba138f`, `b9173c3c`.
- z.ai consulted as advisor 2026-09-28 (key 403, grok-4.7 substituted);
  advisor does not decide semantics — Micah does, and did.
