# H2R sealed worlds: seed record

Seed: 20261002 (fixed post-prereg-freeze; one seed, one generation).
Generator: gen_worlds.zag (LCG state = (state * 1103515245 + 12345) mod 2^31).
Output: worlds_sealed.zag, 9 worlds (families A/B/C x 3), 4 rules each,
36 hidden queries. Values 1..999, pairwise distinct within each world.
Relation per world: 701 + world index. Query relation: R + 5000 (never taught).

Pre-seal refinement (transparent, documented here, not a prereg bar change):
the generator excludes 23 integers from draws (1-8, 12, 16, 20, 24, 28, 32,
36, 41, 64, 96, 101, 102, 104, 902, 999) so that no sealed world value
textually collides with any numeric literal in h2r_impl.zag (node field
offsets, ISA tags, loop bounds). This makes the frozen K-C0A (iii) grep
exact with zero caveats. The draw remains PRNG 1..999 with rejection;
976 values remain; the exclusion is content-neutral for the hypothesis test.

Commit order: PREREG_H2R (bded89be0) strictly before implementation
(6f7c08e20) strictly before this sealed-worlds commit. The learner source
predates all sealed values.
