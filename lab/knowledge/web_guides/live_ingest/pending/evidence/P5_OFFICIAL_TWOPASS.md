# P5 official two-pass — 2026-09-25 (follow-up round)

## Why a second P5 run was needed

The coordinator's shakedown P5 (7/7 PASS) used a lazy-init budget of 22,704,448
bytes and exercised shedding (35,801 shed). The first official two-pass in this
round (passdirs `p5pass_a`/`p5pass_b`) used the frozen template budget
(PENDING_BUDGET_BYTES|25653632 = 25,653,632) with the as-generated 333,165 CAP
claims — and **no shedding occurred**: all 333,165 claims fit
(stored_bytes=25,320,390 ≤ 25,653,632). The shedding mechanism — the actual
subject of kill bar P5 — was not exercised.

Root cause: the CAP count came from `gen_cap.min_count_for_budget`, whose
`worst_line_cost` assumes every index has the full digit width (6 digits for
333,165 → 77 B/claim → 25,653,705 estimated). The true average is 76.0 B/claim
(most indices are shorter), so the set undershoots the budget by 333,242 bytes.

Prereg §8 is explicit: CAP "Count = enough to exceed the measured budget (§7)".
The count was therefore extended **in compliance with the prereg** (not a
deviation): 20,000 further claims from the frozen deterministic generator
(`The marker stone <i> stands <i> meters tall.`, indices continuing
333,166..353,165), appended as `cap_chunks/chunk_ax` (15,000 claims,
SHA-256 prefix `1c606ba5fe01c9ff`) and `cap_chunks/chunk_ay` (5,000 claims,
SHA-256 prefix `84f29c206619f35c`). Claim format, generator logic, index
continuity, and frozen budget are unchanged; chunks are regenerable from the
frozen `gen_cap.py` text pattern. (Incidental: `driver_p5.py`'s inline
accounting check double-counts shed claims as resolved — the committed
`verify_p5.py` excludes `|SHED|` resolutions correctly; the authoritative
verifier used here is `verify_p5_official.py`, which also computes the presented
count from the chunk files instead of the hardcoded 333165.)

## Official two-pass (passdirs `p5off_a`, `p5off_b`)

Binary: `bin/kbp`, SHA-256
`81b34ac86e8c53bed55bb2827f3cf0b09eec88f0027188af6b3e902b721f90bd`
(535,011 B — the authoritative rebuild, see REBUILD_RESOLUTION.md).
Budget: frozen template, 25,653,632 bytes. Presented: 353,165 CAP claims in
25 chunks. Verifier: `verify_p5_official.py` (parameterized passdir,
chunk-counted).

### Pass A (`p5off_a`) — 7/7 PASS

| Check | Result |
|---|---|
| p5-accounting | PASS — 353165 == 336407 + 16758 + 0 + 0 |
| p5-shed-res-match | PASS — shed resolutions 16758 == shed 16758 |
| p5-oldest-first | PASS — shed seqs exactly {1..16758} |
| p5-ledgered | PASS — 16758 ledgered == 16758 shed |
| p5-no-reuse | PASS — stored 336407 seqs exactly {16759..353165} |
| p5-kb-count | PASS — 12 KB lines, knowledge.txt SHA unchanged |
| p5-budget | PASS — stored 25653616 ≤ budget 25653632 |

### Pass B (`p5off_b`) — 7/7 PASS (identical numbers)

| Check | Result |
|---|---|
| p5-accounting | PASS — 353165 == 336407 + 16758 + 0 + 0 |
| p5-shed-res-match | PASS — 16758 == 16758 |
| p5-oldest-first | PASS — shed seqs exactly {1..16758} |
| p5-ledgered | PASS — 16758 == 16758 |
| p5-no-reuse | PASS — stored 336407 seqs exactly {16759..353165} |
| p5-kb-count | PASS — 12 KB lines, knowledge.txt SHA unchanged |
| p5-budget | PASS — stored 25653616 ≤ budget 25653632 |

### Cross-pass byte-identity (prereg §7: "two runs byte-identical")

| File | A vs B |
|---|---|
| pending.txt | IDENTICAL (SHA-256 `7265136730820648…` both) |
| knowledge.txt | IDENTICAL |
| resolutions.txt | IDENTICAL |
| shed_ledger.txt | IDENTICAL |
| pending_init.log | IDENTICAL |
| holdpolicy.txt / installed.txt / testproto.txt | IDENTICAL |
| rejections.txt | absent in both (zero refusals — consistent) |

## Verdict: P5 PASS (official)

Shedding exercised under the frozen production budget: 16,758 oldest claims
shed first, every shed ledgered, stored set exactly the newest 336,407 with no
gaps and no sequence reuse, knowledge base untouched, budget respected to
within 16 bytes, and both passes byte-identical. The prereg §8 CAP-count
requirement ("enough to exceed the measured budget") is now actually satisfied.
