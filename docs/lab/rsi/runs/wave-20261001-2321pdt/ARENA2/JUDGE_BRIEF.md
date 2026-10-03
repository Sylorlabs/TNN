# JUDGE BRIEF: ARENA-REMAP (wave-20261001-2321pdt, ARENA2 lane)

## Provenance

- RENDER_SHA: 4a80837a2ad90779c156584ec0be80aabc548ac6c29e5ec91d940ce010ec9a21
  (sha256 of the sealed-run contestant binary bin/remap, built with the
  pinned znc from the committed implementation source
  remap_contestant.zag; zero source changes after the build)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: arena v6 refreeze 0.794 (54/68, wave-20261001-1721pdt
  REFREEZE_RECORD.md); sibling ARENA lane on inquiry (in progress, not
  duplicated here)
- NEW_KNOWLEDGE_CLAIM: Composing the learner's exposure-learned Zem
  templates with a runtime-parsed value permutation raises transfer
  (C12) from 0.000 to 1.000 with zero regressions on the other 15
  capabilities, showing transfer can be built as composition over
  existing learned state rather than as a new subsystem.

## Verdict: BUILD-PASS

All 8 frozen kill bars PASS on the sealed 68-item battery
(seed 71503461337030):

- K1 transfer: C12 = 6/6 = 1.000 (was 0.000)
- K2 no regression: all other 15 capabilities byte-identical to the
  v6 refreeze; total 60/68 = 0.882 (was 54/68 = 0.794)
- K3 determinism: 3/3 byte-identical stripped reply streams and
  byte-identical decision traces
- K4 pure Zag: zero non-safebin invocations; `which python3` empty
  at lane start and end
- K5 sealed validity: tool hashes match the refreeze record,
  regenerated world hash matches, pre-run key hash recorded,
  contestant never opens key/idmap/proofs, grep audit clean
- K6 negative controls: disabling either handler zeroes exactly its
  half (C12 = 3/6 each way); both halves causally necessary
- K7 architecture: 94 lines added, 0 changed; 0 new modes, bridges,
  routers, admission gates, or hardcoded semantic cases
- K8 no L3 claim: explicitly disclaimed against Criterion 0
  (researcher-authored recoding semantics; fixed form; no new
  representation invented). REMAP is L2 transfer infrastructure.

## What was built

Two question-type handlers in the existing test-turn dispatch
(established v6 pattern): remap_prod applies the question-given
permutation to the learned B-template output; remap_class checks a
candidate triple against the permuted learned A template. Both reuse
the learner's own exposure-learned Zem templates (the structures
behind v6's C10/C16 1.000); no sealed values are hardcoded; the
mechanism generalizes to any permutation and any learned template.

## Negative finding (not built, recorded)

C9 (causal) as implemented is unpassable by any genuine causal
mechanism: the 12 causal observations are perfectly symmetric
(x==y==z always, chain unidentifiable by design), there are zero
intervention turns, and the discrim items always list the true chain
first, so the only 3/3 mechanism is question-format parsing, rejected
as gaming. Recommendation: randomize candidate order and add real
intervention turns in the world generator before any future causal
lane. The C9 pick was rejected on this evidence; C12 was selected
instead.

## Scope

CANDIDATE mechanism only. No L3 claim, no TNN-2 substrate claim, no
TNN-beats-LLM claim. The canonical 0.573 is not moved by this result.
