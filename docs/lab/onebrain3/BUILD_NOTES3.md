# BUILD_NOTES3.md — One-brain round 3, v6 problem set (Worker A2)

## What was built
`v6.tsv`: 44 items, columns `id query expected_bid readings rationale`.
`spec_validate3.py`: structural + trigger validator (dynamic item count).
`run_single_v6.txt`: v2 binary `single`-mode output on v6 (spec/fork validation only).
`FREEZE3.txt`: SHA-256 + UTC timestamp (written before any prohibited mode).

## Category plan (44 items)
| Cat | Ids | n | Design |
|-----|-----|---|--------|
| A (duel helps, q15-like) | q01–q06 | 6 | rd7 (corr 2) kills a spurious substantive reading (corr 0); survivor's bid is the judged bid |
| B (duel annihilates, q06-like) | q07–q12 | 6 | rd7 (corr 2) kills ALL substantive readings (corr 0); old duel → NO_VERDICT; new guard must abstain |
| C (§9a denial binds) | q13–q24 | 12 | 4× α (forget+joke), 4× β (correction+challenge), 4× γ (forget+challenge); denial removes winner's support fact → winner flips |
| D (reintegration room) | q25–q36 | 12 | Close bids, contestable winners, differing ledger support |
| E (anchors, non-fork) | q37–q40 | 4 | Large margins (27/27/27/18); single-mode gets them right |
| F (withhold/challenge) | q41–q44 | 4 | Untaught predicates → 23 (3 unreachable, 1 reachable); false taught claim → 19 |

## §9 property counts (a/b/c)
- **(a) 12/44** — fact invalidation binds (q13–q24). Each has ≥2 alive fact candidates, a genuine r6/r0 denial deliberation, the denied fact has dependent bids (dep 1–2), and the denial flips the single-mode winner (α: 13→15; β: 16→19; γ: 15→19). Denial direction vs expected: α helps (4, toward), β/γ hurt (8, away) — honest mix.
- **(b) 12/44** — determinative reading duels. 6 duel-helps (q01–q06): old duel moves single→expected (16→18, 17→18, 19→20, 13→14, 16→17, 14→15). 6 duel-annihilations (q07–q12): old duel → NO_VERDICT; the new guard must detect the would-be-empty field and abstain.
- **(c) 40/44** fork-firable (≥2 ev=1 readings, top-two fired-bid margin ≤12); of these, **24/44** have expected ≠ mechanical single-mode winner, requiring a justified non-lowest-hid choice.

## Verbatim output-space cross-check
Single-mode accuracy: **20/44 = 45.5%** (target <70% — the set is hard, not solvable by argmax).
Fork-likely: **40/44** (target ≥30 — the audits actually run).
Per-item table: see `spec_validate3.py` output (all spec checks passed).

## Human-judgment method
Expected bids were set by human judgment from the query's operative speech act
(e.g. "the final self-correction is the operative act", "negation-blindness:
do not forget is an emphatic remember", "genuine either-or with no priority"),
each recorded with a written rationale in the TSV. A deterministic design aid
(`design_calc.py`, a source-mirror of the frozen v2 GEN + audit phases) was used
ONLY to hand-check trigger windows, corr values, denial binding, and duel
outcomes — never to set or adjust expected bids. Two design bugs were caught by
hand-checking (B1's rd4 topic caught the entities; B6's rd8>rd7 gated bid22 on
rd7); both were redesigned, not tuned.

## Single-only attestation
The v2 binary was run on v6 in **`single` mode only** (`run_single_v6.txt`).
No `onebrain`, `ablate`, `poison`, or `min` scoring was run on v6 before
freezing. No query or expected bid was changed based on any score. The audit
simulations above are hand-checks from the frozen source, not scoring runs.

## Disk note
Home disk is tight; all artifacts are small (TSV ~6KB, validator ~4KB,
single output ~70KB). `design_calc.py` (~15KB) is a working aid, not prereg.
