# RNG scan — merged tree

Date: 2026-09-25.

Grep backstop across all three merged src/ trees (build/, longhorizon/, redteam/),
including the vendored SHA-256 module:

Pattern: `rand|srand|random|lcg|entropy|/dev/urandom|getrandom`
Hits: 0.

Empirical backstop: all four batteries (smoke, red team, LH B-alone, LH integrated)
ran 3× with byte-identical outputs.

Result: zero RNG in any decision path. PASS.
