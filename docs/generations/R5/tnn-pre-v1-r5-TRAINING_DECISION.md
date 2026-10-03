# Current Goldilocks training decision

## Decision

For the current controlled substrate, use:

```text
one persistent shared brain
+ recurrent visual PAMs
+ global-identity/local-temporal hybrid audio PAMs
+ action/effect grounding
+ raw UTF-8 Adaptive Motifs
+ all modalities available during language development
+ moderate variation/corruption first
+ clean correction and consolidation second
+ motif-gated temporal discourse workspace
```

## What “video works best” means after testing

Video is important because temporal continuity and action consequences expose
objects, identity, causality, and procedures. However, the tournament did not
support this stronger claim:

```text
video first, language much later = best language development
```

That schedule underperformed. Video provided the most useful grounding when
language and the other modalities were available closely enough in development
for the same persistent state to connect them.

## Budget dependence

- At small/medium budgets, order matters materially. `noisy_then_clean` is the
  most reliable integrated history tested.
- At 1,024 exposures, `mixed_all_from_birth` is almost tied. With sufficient
  experience, architecture and coverage dominate fine schedule ordering.
- Text-first can be efficient and competitive, but it is weaker as a grounding
  philosophy and risks building symbols before stable causes.
- Sensory-first with only sparse later language repeatedly underperforms.

## Not a universal optimum

This is the best schedule **for the generated four-factor world and current
substrate**. A universal or “perfect” developmental curriculum cannot be claimed
until the same frozen learner is tested on continuous natural video, real speech,
open interaction, unrestricted text, and hidden domains.
