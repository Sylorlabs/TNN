# SCALE EPISTEMIC corpus — build notes

Built 2026-09-26. Workdir: `~/workspace/epistemic_scale/corpus/`
Files: `corpus.tsv` (data), `CORPUS_NOTES.md` (this file). Nothing committed to git.

## Final counts (preregistered composition — hit exactly)

| class       | id range    | count |
|-------------|-------------|-------|
| fact        | F001–F240   | 240   |
| opinion     | O001–O200   | 200   |
| lie         | L001–L120   | 120   |
| skepticism  | S001–S080   | 80    |
| **total**   |             | **640** |

Format: TSV with header `id\ttext\tclass\tprovenance`. Every data line has
exactly 4 tab-separated fields; text is single-line, plain ASCII, no tabs or
newlines inside fields. IDs are contiguous with zero-padded numbering, no
duplicates. Validated mechanically after writing (field count, ASCII check,
duplicate-ID check, contiguity check — all pass).

## How facts were sourced and verified

- The bulk of facts are durable common knowledge (geography, history dates,
  basic science, everyday observations) with provenance `common knowledge`.
- Non-obvious / surprising facts were spot-verified via web search on
  2026-09-26 before inclusion, marked `verified: web search 2026-09-26`:
  - F006 honey edible after 3,000 years in Egyptian tombs
  - F007/F008 Venus retrograde rotation; Venusian day (243 d) longer than its year (225 d)
  - F017 sharks predate trees (~450M vs ~385M years)
  - F024 Cleopatra closer in time to the 1969 Moon landing than to the pyramids
  - F025 teaching at Oxford (1096) predates the Aztec capital Tenochtitlan (1325)
  - F034 fruit flies first animals in space (US V-2, Feb 1947), not Laika
  - F232 Pringles-can inventor Fredric Baur buried with ashes in a Pringles can
- Estimates and widely-repeated figures that lack a single authoritative value
  are marked `commonly cited` or `commonly cited estimate` (e.g. F020 Shannon
  number, F081 stars vs grains of sand, F205 lifetime walking distance).
- Every lie's provenance names the specific true claim it contradicts
  (`contradicts: ...`), so the falsehood is auditable item by item.
- Opinions carry provenance `subjective: <domain>` (taste, music, values, ...).
- Skepticism items carry provenance `public debate: <topic>`.

## Judgment calls

1. **Skepticism vs lie boundary.** Per the standing rule, skepticism =
   claims with two sides and real public disagreement, excluded from
   true/false scoring. This includes scientifically settled claims with a
   large dissenting public (flat earth S002, chemtrails S001, vaccines-autism
   S013, moon-landing hoax S005) — they test whether TNN forces a verdict or
   holds UNDETERMINED. Clear-cut myths with no live public debate went to
   `lie` instead (10%-of-brain L047, glass-flows L046, tongue map L057,
   lightning-never-strikes L048).
2. **Deliberately excluded as facts** (too disputed for a `fact` label):
   "the Nile is the longest river" (Amazon dispute — used the safe joint
   phrasing F075 instead), "France has the most time zones" (true only
   counting overseas territories — avoided the superlative), "Russia has the
   most time zones" (same reason — F065 states only the count, 11).
3. **Phrasing hedges inside facts.** Where the mechanism or number is debated
   but the core claim is solid, the text carries its own hedge rather than a
   stronger false claim: F014 "under certain conditions" (Mpemba),
   F140 "an estimated third" (Black Death), F200 "roughly ten million"
   (color discrimination), F203 "a 2014 study claimed" style attributions
   where a single study is the source.
4. **Pineapple on pizza** is classed `opinion` (O003), not skepticism — it is
   a taste preference with no factual dispute, per the brief.
5. **French fries origin** (S076) is classed `skepticism` — France vs Belgium
   is a genuine unresolved historical dispute, not a checkable fact.
6. **Anti-leak measures applied:**
   - Opinions mix first-person forms ("I think", "I feel", "I believe") with
     flat assertions stated as if factual ("Mornings are better than
     evenings", "The Beatles are overrated") — no uniform giveaway phrasing.
   - Lies mix blatant (L005 Moon made of cheese, L118 Shakespeare invented
     "internet") with subtle single-detail corruptions (wrong city L007/L014,
     wrong year L018/L040/L069, wrong number L004/L029, wrong person
     L013/L027, inversions L023/L079/L080).
   - Facts mix easy (F001, F170, F179) with obscure (F044, F056, F057, F232).
   - No label words ("this is a fact", "in my opinion") appear in any text.
   - Syntax was varied across items (declarative, hedged, parenthetical,
     inverted); no repeated template sentences.
7. **Near-miss pairs kept intentionally apart.** A few facts directly debunk
   common myths that also appear as lies (e.g. F235 tongue map vs L057,
   F236 Columbus vs L060, F237 Napoleon height vs L012, F239 fortune cookies
   vs L062, F240 carrots vs L098, F223 knuckles vs L053, F226 five-second rule
   vs L096, F227 gum vs L097). This is deliberate: it tests whether TNN can
   hold the true version while rejecting the false one, rather than pattern
   matching on topic.
