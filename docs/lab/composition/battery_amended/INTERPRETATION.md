# INTERPRETATION — Crew D, D1 under the amended composition prereg (A1–A7)

Readings I1–I12 are Crew B's (frozen run, superseded). New readings I13+
below govern the amended run only. Honest-reading rule: every reading is
supported by a measured number in this directory; new ambiguities are
documented, not resolved by fiat.

## I13. The rich fair-teaching protocol generalizes to all six rules without loss.

Crew C's certified protocol (definition + procedure + 12 worked examples
with letter walkthroughs on tok 0..5 and 700..705, train salt C=13) was
extended verbatim to all 6 rules (228 teaching lines + 2 taught controls per
P0 session). Taught controls: 12/12 echoed verbatim (rules 0,1,2,3,5 exact;
rule 4 lowercased on intake per I6). Intake is received; the channel works.

## I14. Rich teaching changes nothing on held-out probes: 0/6 mastery again.

P0: 48/48 probes "I don't know." Mastery 0/6 — identical to Crew B's sparse
teaching and Crew C's rich teaching (single-rule arm). The failure is not a
teaching-sparsity artifact: 12 worked examples with walkthroughs per rule
buy zero generalization. This replicates Crew C's retrieval-echo finding on
all six rules: the learner echoes taught strings and cannot synthesize novel
strings.

## I15. The instrument's binding chance arm is WRONG-ORDER, not NULL.

Measured true-output-correct rates on the salted instrument: null 16/600
(0.0267), singlerule 38/600 (0.0633), wrongord 61/600 (0.1017). A1's rule
(chance = max of the three) selects WRONG-ORDER: K1 line = 0.2017. Note the
coincidence: wrong-order's 61/600 equals the "wrong-order" dumb-strategy rate
in the audit (61/600) — the scripted wrongord arm applies parts in descending
number order for pairs and reversed order for triples, close to the
reversed-order strategy. "Ascending number order" scores 212/600 (0.3533) as
a post-hoc strategy; it is not one of A1's three chance arms and does not
enter the bar, but it is instrument evidence that index-ordered application
is a strong non-compositional strategy on this item set.

## I16. A2's salt defeats every chain the frozen shift memorizer could use.

Gate results: 0 cross-phase single-step shift pairs across all 6 phase-pairs;
1080 chained/prefix intermediates, 0 shift-equivalent to any training token;
strict shift-memorizer P0 [0,0,0,0,0,2] — no rule reaches 7/8, so the chaining
attack the frozen bypass relied on is dead. The chained memorizer's 16/600
P2 hits are all input==expected identity coincidences (soft items), not
shift-chain successes. A2 holds: the composition battery is memorizer-proof
for the shift family.

## I17. K2 voids the battery; K1's kill is arithmetic alongside the void.

K1: 0/600 = 0.0000 <= 0.2017 -> composition claim KILLED. K2: 600/600 class
(a) -> battery VOID. Per Crew C's binding reporting rule the K1 kill is
presented WITH the K2 void; the void is the operative verdict: with parts
unmastered, P2/P3/P4 cannot discriminate composition from non-learning, so
no composition finding (positive or negative) is licensed beyond the P0
mastery failure.

## I18. P3 could not literally interleave with excluded P2 for the real learner.

The instrument's administered order interleaves P3 distractors through P2,
but the learner mastered 0/6 parts, so under frozen priority its P1/P2 items
are excluded (class (a)) and there was no P2 stream to interleave into.
Distractors were administered inside the P0 sessions (2,2,1,1,1,1 across the
6 sessions): 8/8 "I don't know.", reflex 0/8. The exclusion is the honest
form of the A3 requirement under the frozen priority rule.

## I19. A5's non-commutation expectation is falsified for P5 vs P4.

A5 asked to verify that P5/P6 do not commute with P1–P4. Measured on all
salted P2 inputs: (3,4) and (4,3) — i.e. upperfirst (P5) x droplast (P4) —
commute exactly (also (1,3),(3,1) as in Crew B). Algebraically:
upperfirst(droplast(s)) = droplast(upperfirst(s)) for all s, since
capitalizing the first character commutes with dropping the last. The
expectation holds for P6 (sortchars: commutes with nothing) but fails for
P5 vs P4. Documentation, not a bar change.

## I20. Soft items: 22/600, concentrated at short inputs.

A5 soft-item definition (this battery's choice, recorded here): P2 items
whose expected output equals >=2 of {identity, first-only, second-only,
wrong-order}. Count: 22/600; 19 at input length 2, 1 at length 3, 2 at
length 5. These are the items a non-composing agent can answer correctly;
they explain the chance arms' nonzero trueacc (e.g. null's 16/600 =
identity coincidences exactly).

## I21. A5 point-3 pick: per-condition P4 breakdown, not narrow pair-systematic (d).

The taxonomy is unchanged; what is recorded is the evidence format: the
battery keeps the per-pair P4 table (30 pairs, salted bigram data in the
audit) rather than collapsing to a narrow pair-systematic (d), because the
per-pair table preserves input-conditional interference evidence. Moot for
the real learner (all (a)); on file for reference arms (refinterfere's
(0,1) (d) demonstration; refnocombine's (0,5) behavioral misfire, I23).

## I22. Label blindness was honored.

Item IDs in `items.tsv` are salted token indices, not rule names; P1 records
carry neutral indices (0 audit lines with semantic labels); the learner
scorer is mechanical (final-word match) and never read a response; transcripts
were scored in hash-named workdirs with SCORES.md keyed by transcript hash
only. Blinding held through adjudication.

## I23. Instrument wrinkle: P4's asymmetry criterion is purely behavioral.

The (0,5) INTERF line on refnocombine (identity-output arm) is a misfire of
the frozen behavioral criterion: pair (5,0)'s 4 salted items happen to satisfy
reverse(sortchars(s)) == s (e.g. 'smig'), giving rev=4/4 identity coincidences
against acc=0/4. This is a soft-item artifact, not genuine interference.
K5 is moot for the real learner; the wrinkle is recorded so future (d)
findings are checked against identity-coincidence first.

## I24. Instrument wrinkle: 2 of 8 P3 distractors are palindromes under salt.

tok 614 ('iggi') and tok 618 ('kiik') are palindromes under the salted
generator, so the reverse-based reflex probe is insensitive on them (reflex
arm: 6/8, still above K4's 0.20). Frozen §4's k^2 anti-palindrome property
does not fully survive salting in the P3 index range. No tuning was done
(brief: do not tune the instrument); the insensitivity is documented.

## I25. K6 under salt: 30/30 pairs covered, none excluded.

Bigram-clean input counts (salted, train bigrams from all 72 teaching
examples): every pair has >=2 bigram-clean inputs; the excluded set is empty.
K6 is vacuous for the real learner (0 successes), but the covered-pair set is
computed and on file, so the bar is evaluable for any future claimant.
