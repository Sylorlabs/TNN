# CORRECTION (owed, 2026-09-22): the lie catcher was not fully native

## What we told Micah
That the falsehood-leg / lie-catcher harness was fully native.

## What was actually true
The deliberation binaries (delib_b2.zag, delib_b3.zag, delib_cnt.zag,
delib_f2.zag, delib_f3.zag, delib_vol.zag, delib_sa.zag, delib_sarc.zag)
contain three helpers — `is_known_false`, `is_known_true`, `is_absurd` —
whose bodies are lists of strings authored against the leg-b falsehood
items and the c70 battery ("triangle has 4 sides", "goldfish filed", ...).
That is test-derived world knowledge baked into the binary, not learned
or deliberated knowledge. The "constant across all rungs, so it cannot
bias the volume curve" comment in delib_f3.zag is honest about constancy
but does not make the mechanism native: the verdicts on the falsehood leg
came from string matching, not from reasoning.

## What this changes
- The volume-curve results for the FALSEHOOD concept stand only as
  learning-curve measurements conditional on the baked-in truth machinery;
  the "lie catcher" framing was overstated.
- Nothing else is retracted: the sarcasm/analogy/counterfactual/
  hypothetical learning curves used no such lists.

## What replaces it (this wave)
PREREG_LIECATCHER_REDESIGN.md freezes the redesign: delib_f4.zag removes
all three helpers and replaces them with an episodic fact ledger — claims
are contradiction-checked against world facts parsed from an independently
authored experience corpus. Same leg-b bars (12/12 withheld, 12/12 true
controls endorsed) must pass with zero baked-in world knowledge; any
test-derived string reintroduced anywhere is an automatic FAIL.

## Audit
- Grep for `is_known_false|is_known_true|is_absurd` across
  prose-learning/epistemic_wave/: delib_b2/b3/cnt/f2/f3/vol/sa/sarc.zag
  still contain the helpers (kept for the historical record; marked
  superseded). delib_f4.zag and delib_att.zag contain none.
- Removal from the historical binaries was deliberately NOT done: the
  evidence trail for the published volume curves must keep its exact
  inputs. New claims use the new binaries only.
