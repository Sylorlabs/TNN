# TRANSFER_EVAL.md: C8/C12 Surface-Transfer Test

Wave: wave-20261002-0521pdt | Lane: ARENA | Date: 2026-10-02
Prereg: PREREG_TRANSFER_C8C12.md (committed alone as ca4ed3320)
Substrate: fixrun2/ (D5-fixed world, GEN-PASS this wave)
Scorer: arena_512 (cross-validated vs frozen scorer)

## Verdict: TRANSFER-PASS (T1 through T5 all PASS)

## Builds (T5 gate)

- INQ source via `git show` from commit 0ddb5e9ce; built with
  the pinned znc (pure Zag). Binary sha256
  09f59dcbee0fcd443a911f2bf24bff883960f457d0ce9acd59506d3c38339b1d:
  BYTE-IDENTICAL to the sealed INQ binary.
- REMAP source via `git show` from commit 18309290c; built with
  the pinned znc (pure Zag). Binary sha256
  4a80837a2ad90779c156584ec0be80aabc548ac6c29e5ec91d940ce010ec9a21:
  BYTE-IDENTICAL to the sealed REMAP binary.
- Zero contestant source changes. `which python3` returns
  nothing under the safebin PATH.

## Results

### INQ on fixrun2 (3 runs)
TOTAL 68, 0.852 (58/68) on all three runs. Per capability:
C1-C7 1.000, C8 4/4 = 1.000, C9 0.000, C10 1.000, C11 1.000,
C12 0.000, C13 1.000, C14 1.000, C15 0.000, C16 1.000.
tool_calls = 7 (4 C8 asks + 3 C7 asks), the honest inquiry count.

### REMAP on fixrun2 (3 runs)
TOTAL 68, 0.882 (60/68) on all three runs. C12 6/6 = 1.000.

### T1 (C8 transfer): PASS
INQ scores 4/4 on the C8 items in fixrun2 (new entity names and
attribute values; same double-test-turn plus observe_result
structure).

### T2 (C12 transfer): PASS
REMAP scores 6/6 on the C12 items in fixrun2 (new remap table and
segment values).

### T3 (no regression): PASS
INQ 58/68 >= 54/68 and REMAP 60/68 >= 54/68 (v6 baseline total on
fixrun2, from SEALED_EVAL_C9.md). Both contestants' per-capability
profiles on fixrun2 are identical to their frozen-world profiles.

### T4 (determinism): PASS
3/3 stripped reply streams byte-identical per contestant:
- INQ:
  ee4f10adf547c460d4a69c7e7f415076dae940f6918b99df7ba1d533efb85d7d
  (x3)
- REMAP:
  02d1b958c4fc1257f97a6db5d50bef3c718143d0881e177cb08eddf66b9c7024
  (x3)

### T5 (purity): PASS (see Builds)

## Interpretation

Both mechanisms survive a full surface change (new names, words,
values, remap table) with zero code changes and no score change
on any capability. This is evidence against surface coupling:
neither INQ's inquiry loop nor REMAP's remap application depends
on the frozen world's specific surface forms. Under the
ONE-SYSTEM rule, this is the right kind of evidence: the
mechanisms are generic over the world family, not handlers for
frozen-world strings.

## Scope honesty

fixrun2 comes from the same generator family as the frozen world
(same code, different RNG stream positions). This is surface
transfer, not broad generality: it does not establish survival
under new world families, new inquiry forms, adversarially
redesigned C8/C12 items, or interference between mechanisms.
The integrated continuing learner (one contestant carrying INQ +
REMAP + CAUSAL + DEFRECALL with no regressions) is still unbuilt;
that is the next one-system milestone, queued below.

## Queued next

- Integrated contestant experiment (prereg): v6 base + INQ +
  REMAP + CAUSAL sections in one binary on fixrun2; kill bars:
  per-capability scores >= the max of the individual candidates
  with zero regressions, 3/3 determinism, architecture
  accounting (no new modes/bridges/handlers).
- C15: DEFRECALL's scope is now bounded to roster-request bare
  prompts (ABSTENTION_TEST.md); a genuine prompt-intent
  discrimination mechanism would be a new 11-step frontier
  proposal, not a patch.
