# R32 E51AH — Implementation Contract

**Parent preregistration:**
`Research/R32_E51AH_GROUNDED_PRESERVATION_REPLAY_PREREG.md`

## Source lineage

E51AH must reconstruct the frozen E51X/E51Y terminal learner and E51AB local-384
direct learner through the same E51X -> E51Y -> E51AD assembly lineage used by
E51AE/E51AG. Reused parent support fragments are pinned by Git blob identity.

E51AH may reuse transformed E51AE policy, residual-score, trajectory-objective,
and evaluation helpers. It replaces only the residual support-selection and fit
tail described in the preregistration.

## Scientific implementation

- stages are fixed at development 108, validation 109, confirmation 110;
- the 32 learner-visible record columns are unchanged;
- record columns 34-37 are zero in all residual-fit records;
- the mature terminal and direct learners are immutable causal controls;
- UNKNOWN remains exactly zero and has no learned parameters;
- the candidate action interface remains generic candidate 0/candidate 1;
- the local replay arm uses the existing frozen 32-cell routing substrate and a
  384-sweep conditional-weight residual fit;
- arm 2 repeats the parent critical set cyclically to exactly the replay count and
  changes no record content or target pairing;
- forward and reverse fits must be identical before validation can open.

## Fail-early rule

Stage 109 is not built or evaluated unless at least one replay arm passes exact
development preservation and nonzero rescue. Stage 110 is not built or evaluated
unless the lowest-numbered eligible replay arm is exact at stage 109.

The selected replay arm is fixed from development before building stage 109.
No later eligible arm may replace it based on validation performance. Tradeoff
requires opposite net changes in known/no-unique reachability. Any required
integrity failure overrides the scientific outcome. Oracle success is computed
from its selected action, never assigned unconditionally.

## Evidence package

The authoritative package must include the preregistration, implementation
contract, machine-readable hardcoding ledger, every native fragment, assembler,
workflow, assembled source, source manifest, compiler identity, two byte-identical
native builds, compile logs, raw ledger, summary ledger, exit code, runtime,
confirmation status, and frozen outcome.

## Immutability

After any stage-109 output is exposed, the treatment, support selection, arm
ordering, thresholds, and decision rules cannot change under the E51AH identifier.
Infrastructure repair before sealed exposure is permitted only when it leaves the
scientific treatment unchanged and is documented.
