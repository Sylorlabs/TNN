# INTERPRETATION.md — Crew B protocol interpretations of frozen PREREG §§1–8

Crew B ran the D1 full battery against the real TNN learner under the frozen
`~/workspace/comp_b4/ref/PREREG.md` §§1–8 exactly. Nothing from
`AMENDMENT_PROPOSAL.md` was enacted. D2 was excluded (no buildable D2
instrument in the frozen prereg).

Every ambiguity below is documented as a crew interpretation, never silently
resolved. Numbered I1–I12 for reference from RESULTS.md / BARS.md.

## Frozen-text anchors (verbatim)

- §1: "P0 probes each part with 8 held-out inputs (no overlap with any
  training token); a part counts as mastered at ≥7/8."
- §1: "Unmastered parts are excluded from the composition phases."
- §4: "The battery presents every pair (i,j) i≠j (single-rule→pair
  'chains') and every triple (i,j,k) i,j,k distinct (three-hop chains)".
- §5: "C is produced by the deterministic generator (§4), is absent from
  the training mass ..., and the learner must produce C from parts alone."

## Crew interpretations

**I1 — Rule names in prompts.** The frozen text names the rule semantics
(reverse, duplicate-first, rotate-left, drop-last, upper-first, sort-chars)
but does not fix the English word used to invoke them. The crew used the
frozen hyphen-stripped names: `reverse`, `dupfirst`, `rotleft`, `droplast`,
`upperfirst`, `sortchars`. Teaching: "`<name>` turns a word backwards."
(etc.) + six worked examples per rule on tok(0..5). P0 probe:
"what is the `<name>` of `<token>`?"

**I2 — Chain prompt phrasing.** Frozen §4 says the learner must produce C
"from parts alone" but does not fix the chain prompt. The crew used:
"what is the `<a>` then `<b>` of `<t>`?" (pairs) and
"what is the `<a>` then `<b>` then `<c>` of `<t>`?" (triples).
This names both parts in application order — the only phrasing that makes
the two-/three-hop task well-defined without hinting at the expected string.

**I3 — P1 retrieval prompt.** Frozen P1 does not name rule semantics in the
prompt. The crew's prompt was: "which two rules, in which order, turn `<s>`
into `<exp>`?" — no part names, no indices, no hint of the answer. P1 was
not administered to the learner (see I7); six sample prompts were run in a
separate qualitative session (RESULTS.md §samples).

**I4 — Pair/triple enumeration (major).** Frozen §4 names "every pair (i,j)
i≠j" and "every triple (i,j,k) i,j,k distinct" but does not state: whether
repeated parts are allowed (it says i≠j / distinct — read as excluding
repeats), how many inputs per combination, or how the tok counter continues
past the frozen P2 index range `14–61` (inherited verbatim from the 48-item
pilot, which is not allocable to 30 pairs + 120 triples). The crew adopted:
- all 30 ordered distinct pairs (6×5), 4 inputs each → tok 14–133;
- all 120 ordered distinct triples (6×5×4), 4 inputs each → tok 134–613;
- counter continues deterministically from the frozen formula (§4), no phase salt.
The crew judged this the minimal faithful reading: it honors "every pair"
and "every triple ... distinct" while reusing the frozen tok formula and
continuing the frozen counter. The pilot's `14–61` range cannot accommodate
the six-rule full battery under any reading; the continuation is recorded
here as interpretation, not amendment.

**I5 — P3 placement and format.** Frozen phases are sequential; distractors
are a P3 phase. The crew presented the 8 P3 probes after P2, one session:
"what is `<t>`?" for tok 614–621. A3's interleaving was not enacted (it is a
proposed amendment).

**I6 — Case and the learner intake (UPPER-FIRST).** The frozen rule is
"upper-first: capitalizes the first letter". The crew taught the canonical
form ("the upperfirst of ao is Ao."). The real learner's chat intake
lowercases input (its positive control echoes "the upperfirst of ao is ao."
— it cannot even retain the taught capital A). This is an intake limitation
of the real learner, not a battery defect; it is documented here rather than
scored against either side. (This is exactly why D2 was excluded: the frozen
prereg supplies no D2 instrument that survives this intake.)

**I7 — No mastery → no substantive P1/P2.** The learner scored 0/8 on all
six P0 parts (48/48 "I don't know."). Per frozen §1, "unmastered parts are
excluded from the composition phases": all 600 proposed composition items
(pair + triple applications) were classified (a) — "learner lacks at least
one part" — and no substantive P1/P2 outputs were elicited. The 18 sample
prompts (6 P1 + 10 pair + 2 triple) were administered in one extra session
for qualitative evidence only; they do not enter scoring.

**I8 — Honest-broker scoring.** Scoring is mechanical and label-blind: the
Zag scorer (`battery.zag`, mode `learner`) matches each verbatim learner
response against the generator's expected output by exact string equality.
No human reads or judges responses; rule identities and pair identities are
fixed generator mappings, invisible to any judgment call. P0 probe (r,t)
records include the response text for audit.

**I9 — Chance arms.** Frozen: NULL and SINGLE-RULE only, "never anything
else". Scripted in the same Zag binary from the same generator: NULL always
outputs the input; SINGLE-RULE applies a fixed single part (cycling the six
rules by pair index) and is marked correct only against the true composed
output. No wrong-order or other arms (A1 not enacted).

**I10 — K6 scope.** Frozen K6 runs "over all pairs" (K6 adjudicated under
the frozen bar). With zero learner successes it is vacuous; the crew did not
extend it to triples. The bigram audit (§5 of audit.py) covers all 30 pairs.

**I11 — Determinism.** Pure Zag, zero RNG, pinned compiler. Two byte-identical
reruns of every arm; learner sessions additionally rerun under
`MALLOC_PERTURB_=165` — byte-identical. Allocator perturbation is supported
and was exercised (frozen text is silent on it; recorded here as crew
interpretation of "at least two byte-identical reruns").

**I12 — Real learner, genuine intake.** The real workbuddy-round-2 learner
(commit 3cd24f11d119a17d14d9637e43ebdc8918b41e92, chat mode) was used, not a
scripted learner, LLM, or hardcoded answers. All teaching and probes went
through its genuine text intake (see I6 for the intake's case handling). The
learner was given a fair chance: one fresh session per rule for P0
(7 teaching lines each: 1 definition + 6 examples), one all-rules session
for P3 (42 lines), one all-rules session for samples (42 lines).
No per-response adaptation, no tuning, no re-prompting.
