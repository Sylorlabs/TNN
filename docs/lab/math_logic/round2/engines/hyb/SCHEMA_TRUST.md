# SCHEMA_TRUST.md — HYB schema-trust ledger: frozen arithmetic and provenance

Math R2 engine (a) HYB. This document freezes the exact trust/scoring
arithmetic and how to read license provenance in HYB outputs. Any change
to these rules is a spec change, not a tuning knob.

## 1. What a "license" is

Every derivation step in HYB consumes inference licenses — the
authorities the step appeals to. There are exactly three kinds:

1. **Committed schema licenses.** `S_MP`, `S_PBC`, `S_UI` — identified by
   their `COMMIT_SCHEMAS.md` canonical hashes:
   - `S_MP`  = `62cc41ffd582e687`
   - `S_PBC` = `369efe53016bbe1a` (the frozen doc prints a spurious leading
     zero; the engine asserts the true 16-digit hash at startup)
   - `S_UI`  = `b2f909c7d7b67f55`
2. **Rule-premise licenses.** When a step consumes a store claim as a rule
   (the `imp(...)` claim in MP, the `forall(...)` claim in UI, the
   `imp(not(?0),false)` claim in direct PBC), the license is
   FNV-1a-64 of that claim's canonical bytes. This is how a *false injected
   rule* enters the ledger: not as a schema, but as a rule-premise license
   with a hash that no committed schema has.
3. **Structural license.** `CONTRA` = FNV-1a-64 of the ASCII string
   `"CONTRA"` — the structural contradiction rule (a claim and its byte-
   complement derive `false`). It is not a schema and carries no content.

A derivation step's license set is `{schema license, rule-premise license}`
(one or both may be absent: premises have none; the structural step has
only `CONTRA`). A derivation PATH's license set is the union over its
steps, sorted, deduplicated, capped at 40 (largest hashes dropped first —
deterministic).

## 2. Trust ledger

- One entry per license hash ever observed, created on first sight.
- **Initial trust is uniform: 1000** (fixed-point, ×1000). There is no
  prior ranking of schemas; the committed schemas start exactly where an
  unknown rule-premise hash starts.
- **Learned updates only.** Trust moves exclusively as the outcome of a
  contradiction weighing (Section 5). No license is listed as distrusted in
  advance — distrust of a false rule's license is learned from losing.
- On a strict win: licenses distinctive of the *losing* side (present in
  the loser's path-license union, absent from the winner's) lose
  `200 / |distinctive_loser_licenses|` trust each; licenses distinctive of
  the *winning* side gain `100 / |distinctive_winner_licenses|` each.
- Clamped to `[0, 2000]`. Ties move nothing.
- The ledger is printed in the `TRUST:` output section, sorted by hash
  ascending, as `<16-hex-digits>=<trust>`.

## 3. Derivation paths

A path of claim X is a triple `(premise leaves, license set, depth)`:

- A premise (no derivation event) has one path: leaves `{X}`, licenses
  `{}`, depth `0`.
- A derived claim's paths come from the ledger's derivation events:
  for event `{pa, pb}` with direct licenses `{sh, rh}`, every combination
  of a path of `pa` and a path of `pb` forms a path whose leaves are the
  union of premise leaves, licenses the union plus `{sh, rh}`, depth
  `1 + max(depth_a, depth_b)`. Single-premise steps use one side.
- PBC discharges carry a synthetic event pointing at the subproof
  snapshot: each snapshot path of `false` becomes a path of the discharged
  claim with depth+1 and licenses plus the `S_PBC` hash.
- `false` derived structurally additionally expands via contradiction
  records (license `CONTRA`).
- Caps (all deterministic, all load-bearing, none semantic): 64 paths per
  claim, 256 premise leaves per path, 40 licenses per path, snapshot depth
  40. Reaching a cap sets no flag in the verdict; caps are documented here.

## 4. Evidence score

For one path: **premise quality** `Q = mean trust of its licenses`
(`1000` if the path is licenseless — i.e. a bare premise).

For a claim: paths are ordered by `(depth, premise-count, ledger order)`
and scanned greedily; a path contributes iff its premise leaves are
disjoint from all previously kept paths'. Contribution:
`Q * 1000 / (1 + depth)`. The claim score is the sum.

This prices what the spec asks for: premise quality (trust-weighted),
derivation depth (discounted), corroboration (independent paths add up),
and premise-disjoint independence (shared premises are priced once).

## 5. Contradiction weighing

For each contradictory pair `H` / `not(H)` observed (contradiction
records, plus the final target pair):

- Score both sides (Section 4). **Strictly better wins.**
- The losing derivation is marked `REFUTED-BY-WEIGHING` in the audit
  trail — kept visible, not hidden.
- **Equal evidence withholds only that claim** (verdict `WITHHELD`,
  confidence 0). Nothing global is withheld; every other claim keeps the
  verdict its own derivation earned.
- Trust updates (Section 2) apply on strict wins only.

Final target pair: `DERIVED-WEIGHED` / `REFUTED-WEIGHED` (confidence 1 —
a licensed derivation stands as the weighed-best), or `WITHHELD`
(confidence 0) on a tie.

## 6. Reading provenance in outputs

- `AUDIT:` lists every claim with its ONE-identical audit text; a trailing
  `REFUTED-BY-WEIGHING` marks a weighing loser.
- `WEIGHINGS:` lists `W<i>: C<a> vs C<b> : <score_a> vs <score_b> ->
  <A|B|TIE> [FINAL]`.
- `TRUST:` shows the learned ledger. A false injected rule's
  rule-premise hash appears here with trust below 1000 only after it has
  *lost* a weighing — the distrust is learned, never listed in advance.

## 7. Worked reading (B2_03 smoke)

Premises `imp(p,r)`, `imp(r,s)`, `p`; target `s`. Derivation: `r` by MP
(licenses `{S_MP, fnv("imp(p,r)")}`), `s` by MP (licenses
`{S_MP, fnv("imp(r,s)")}`); path of `s`: leaves `{imp(p,r), imp(r,s), p}`,
depth 2, score `1000*1000/3 = 333333` per path (all trusts start 1000).
`not(s)` is underivable, so no weighing fires; verdict `DERIVED`.
