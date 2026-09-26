# CONTROL_BOUNDARY.md — chunking battery fix (2026-09-26)

## What this document is

A precise, honest account of what TNN controls versus what the crew
scaffolded in this fix. Nothing here is faked: where the crew did the work,
it says so.

## What TNN controls (knowledge-driven, proven by the noseed control)

1. **Word meanings.** The registry holds, at runtime: granularity delimiters
   (`sentence`→`.`, `line`→newline), ordinal words (`first`→1 … `twelfth`→12),
   relation words (`after`→+1, `before`→−1). Every probe and parser builds its
   match strings from these bindings at runtime — no relation, ordinal, or
   granularity literal appears in the parser machinery.
2. **Address resolution.** `rel_probe_pos`, `parse_ordinal`, `gran_named`,
   and `parse_ord_before_name` read the registry; the machinery only executes
   the resolved address (split here, count that, reverse this word).
3. **Dependence is proven, not asserted.** The noseed control (seed block
   mechanically emptied, everything else identical) drops the wall from 26/26
   to 16/26: W00–W08 (minus W09), W17-survives, W19 fail without the seed,
   and they fail *in the specific ways* the legacy machinery fails (whole-text
   count "6" for W04, confident wrong "f" for W03). The machinery cannot
   reconstruct the knowledge on its own.

## What the crew scaffolded (honest)

1. **The seed itself is crew-authored.** `tnn_place_knowledge`'s KNOW-SEED
   block was written by the crew, not by a live TNN deliberation. It uses
   only the generic placement primitives (`tnn_bind_granularity`,
   `tnn_bind_ordinal`, `tnn_bind_relation`) — the same primitives a live TNN
   would call — and it contains no trap-specific knowledge (no answers, no
   question templates, only generic word→meaning bindings). But the *act* of
   placing was crew work. The task's bar — "if TNN has the knowledge then it
   should be able to place it" — is met at the **mechanism** level (the
   placement path exists and the machinery reads nothing else), not at the
   **agency** level (no live deliberation placed these bindings in this run).
2. **The candidate machinery is crew-designed.** `cand_delim`'s arms,
   `gran_split`, `rel_anchor_idx`, the two-hop resolver, the nesting
   detector — these are the hands. TNN supplies what the words mean; the crew
   built the hands that act on the meanings.
3. **The policy table is frozen crew measurement.** `policy_winner` is the
   learned policy from the derivation phase. The new cells (kinds 18/19/20/21
   → 10, kind 22 → 10) were added by the crew, with honest `policy_why`
   strings that say what they are (no invented "N examples" claims — those
   strings are reserved for genuinely measured cells).
4. **The kind taxonomy is frozen crew taxonomy.** Kind numbers 18–22
   (`GRAN_COUNT`, `GRAN_SELECT`, `GRAN_WORD`, `TWO_HOP`, `NESTED`) extend the
   existing numbering; they are labels, not knowledge.

## What full TNN control would look like (not present)

A live TNN deliberation that, when taught "after means one forward", itself
calls `tnn_bind_relation(know,"after",1)` — the seed block replaced by a
deliberation trace, with the crew able to delete the seed and watch TNN
re-place it. That installation path does not exist in this build. The seed
is a stand-in, delimited by KNOW-SEED markers so it can be mechanically
stubbed (as the noseed control does).

## Limits (load-bearing vs arbitrary)

- **Caller-supplied, not TNN-designed:** the 2048-byte knowledge arena, the
  256-byte word/segment scratch tables, and the output buffers are allocated
  by the battery harness. TNN's machinery takes them as parameters and works
  with any size; the capacities live in the fixture, not in TNN.
- **Remediated in stage C0:** the registry was rewritten from fixed
  per-kind slots (8/16/8, 15-byte word cap) to an append log whose capacity
  is purely the arena length. No per-kind item cap remains.
- **Physical encoding:** binding names use a u8 length prefix (255-byte max
  name). This is a physical encoding limit like the znc slice ceiling, not a
  semantic cap; no bound name approaches it.

## Bottom line

TNN's knowledge does the discriminating work (proven: remove it and 10 traps
fail in exactly the legacy ways); the crew built the machinery that honors
it and hand-placed the seed through TNN's own placement primitives. The
remaining gap to full TNN control is the installation act itself.
