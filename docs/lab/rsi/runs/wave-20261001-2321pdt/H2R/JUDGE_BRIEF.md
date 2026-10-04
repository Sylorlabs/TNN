# JUDGE_BRIEF: H2R (inversion) re-attempt

RENDER_SHA: 5a3e815c5
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE: TNN3H2 SUBSTRATE-ABSENT (wave-20261001-2021pdt) ;
  TNN3-SUBSTRATE DESIGN-COMPLETE with KB-H2R (this wave, unblocks H2)
NEW_KNOWLEDGE_CLAIM: A learner-authored BUILD ticket discovered the
  inversion (BRANCHEQ guard on slot 1, a slot researcher assemblers never
  guard) by trial on the prototype construction substrate, answering 36/36
  sealed inversion queries with the inverse content living only in the
  ticket, not in source.

## Verdict

BUILD-PASS. All frozen KB-H2R kill bars met unweakened; G-TRIAL, G-DET,
K-C0A satisfied. Full numbers in EVAL_RESULTS.md.

## What was tested

H2 (inversion): can a learner, given only the generic construction service
(BUILD tickets over the frozen 4-op ISA), author an executable graph that
inverts a taught relation chain (query answer <- given) when the frozen
forward path cannot? The H2 prereg was never frozen in wave-20261001-2021pdt
(SUBSTRATE-ABSENT: no learner-reachable construction path). The
TNN3-SUBSTRATE lane's prototype (verified BUILD tickets, fail-closed,
content-neutral) unblocked the re-attempt.

## How it passed

- Fresh prereg PREREG_H2R frozen alone (bded89be0), KB-H2R unweakened.
- Learner h2_trial: reverse-gather paths, author one BUILD ticket per
  (path, guard-orientation), execute, verify against expected as post-hoc
  feedback only. Guard slot always computed 1000+g; no 1001/1002 literal.
- Fresh sealed worlds (e3f7375d1, seed 20261002): 9 worlds x 4 rules,
  36 queries, no direct-query facts, query relation never taught.
- 36/36 correct (bar 29); TRIAL_ENTERED=2 every query (anti-triviality);
  ablation destroys all 36 answers; baseline 0/36; 3/3 byte-identical runs.
- White-box: verifying ticket cell tag=102 f4=1001 (guard slot 1),
  SET cells f4=1000. The inversion is in the ticket.

## Honest limitations

- Family C distractors were present but never executed (gather order put
  the true path first); distractor *rejection* was not observed, though the
  verify-reject mechanism is the same code path exercised via g=0/g=1.
- Masked control 36/36 is informative, not a bar.
- The substrate prototype is a dev harness (verbatim copy + appended
  code), not a lineage change to frozen tnn2.zag.

## Provenance

Prereg bded89be0 < impl 6f7c08e20 < worlds e3f7375d1 < eval 5a3e815c5.
Pure Zag throughout (safebin, no Python). Local commits only, never pushed.
