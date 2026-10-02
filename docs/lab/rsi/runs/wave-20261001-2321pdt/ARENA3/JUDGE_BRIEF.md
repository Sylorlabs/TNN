# JUDGE BRIEF: Arena TRX (wave-20261001-2321pdt, ARENA3 lane)

## Provenance

- RENDER_SHA: 9191e71de (evaluation record commit; TRX implementation
  source sha256
  24b6609838c94951d46bc720e977d3c4da71d07981e1178d53144ca2b17af692,
  binary 46731d65c79d11ffcb41fee4c458e13b9e8f6cd403f6a10e02d5242aaae997ff)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: arena v6 refreeze 0.794 (54/68, CONFIRMED
  wave-20261001-1721pdt); ARENA inquiry BUILD-PASS 0.853 (58/68, this wave;
  TRX base source
  456589d6aa01247596fa69b84289b9e2c7739e1ec755cfb1946fbbab14cbecce);
  ARENA2 sibling lane in progress (directory empty at ARENA3 lane start,
  no capability collision); TRX is the C12 transfer candidate built on the
  INQ candidate, and this lane's sealed run is their integration test.
- NEW_KNOWLEDGE_CLAIM: A generic transfer-by-relabeling loop that parses a
  segment relabeling from any remap_prod/remap_class question, applies it
  to the exposure-learned class-A/class-B templates (reusing the same
  machinery that powers zemprod/zemclass), and answers in the new notation
  raises sealed-arena transfer (C12) from 0.000 to 1.000 with zero
  regressions on the other 15 capabilities across 3/3 byte-identical runs.

## Verdict: BUILD-PASS

All nine frozen kill bars pass (PREREG_ARENA_TRANSFER.md, frozen alone at
829208f99 before implementation at 9191e71de; commit order verified).

Per-capability sealed scores, before (INQ baseline) and after (TRX), all
three runs identical:

| Cap | n | before | after |
|-----|---|--------|-------|
| C1 one-shot facts | 6 | 1.000 | 1.000 |
| C2 delayed fact use | 4 | 1.000 | 1.000 |
| C3 paraphrase | 6 | 1.000 | 1.000 |
| C4 compositional inference | 4 | 1.000 | 1.000 |
| C5 correction | 6 | 1.000 | 1.000 |
| C6 conflicting evidence | 3 | 1.000 | 1.000 |
| C7 uncertainty | 3 | 1.000 | 1.000 |
| C8 active inquiry | 4 | 1.000 | 1.000 |
| C9 causal intervention | 3 | 0.000 | 0.000 |
| C10 procedure invention | 2 | 1.000 | 1.000 |
| C11 representation invention | 2 | 1.000 | 1.000 |
| C12 transfer | 6 | 0.000 | 1.000 |
| C13 long interference | 6 | 1.000 | 1.000 |
| C14 process restart | 6 | 1.000 | 1.000 |
| C15 autonomous goal completion | 1 | 0.000 | 0.000 |
| C16 synthetic language | 6 | 1.000 | 1.000 |
| TOTAL | 68 | 0.853 | 0.941 |

Kill bars: K1 C12 6/6 PASS; K2 zero regressions on the 15 non-target caps
PASS (per-cap scores byte-identical; stripped reply diff vs the INQ run
touches exactly the 6 C12 lines); K3 3/3 byte-identical reruns PASS
(stripped replies
e692b5a47ebb4a0f1405e6c486c087a2358f5181853ca06290cf708d77fc69a5;
traces d664b9eb600250e5fb5a8f7a1ee98b9f2710cc416305bfd5e59d7e6d8be76488);
K4 pure Zag PASS (`which python3` empty at lane start and end, zero
interpreter invocations, no PROCESS-FAIL); K5 sealed validity PASS
(rebuilt world_gen/arena hashes match the refreeze record, turns.jsonl
matches the sealed world, pre-run key hash recorded and key never opened,
zero C12 literal answer/remap strings in mechanism source); K6 negative
controls PASS (prod-off ablation 3/6, class-off ablation 3/6, both halves
causal, both reproduce the INQ baseline on every other capability);
K7 honesty PASS (C7 replies exactly UNKNOWN in all runs; invalid
remap/non-template/no-template all reply UNKNOWN in the /tmp dev smoke
test); K8 architecture PASS (+80/-0 lines, 0 new
modes/bridges/routers/handlers/semantic cases, capability from learner
state plus the question-parsed relabeling); K9 L3 explicitly disclaimed
PASS (fails C0-A through C0-D; L1/L2 template-relabeling transfer
infrastructure, not representational invention).

## What this does not claim

No L3 claim. No TNN-2 substrate claim. No TNN-beats-LLM claim. The
canonical 0.573 is not moved (only a clean refreeze reproducing
composition without contamination can move it). Remaining sealed zeros:
C9 causal, C15 goal. The parent task's "15 capabilities / other 14"
counts do not reproduce from the sealed records (16 capabilities, 68
items); flagged in the prereg, not asserted; the frozen no-regression bar
covered all 15 non-target capabilities and passed. ARENA2's directory
was empty when this lane started; if it later freezes a C12 prereg, the
two lanes are independent competing runs on the same capability.

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA3/PREREG_ARENA_TRANSFER.md
- Implementation: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA3/trx_contestant.zag
- Binary: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA3/bin/trx
- Full record: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA3/SEALED_EVAL.md
- Sealed runs: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA3/sealed/run1 (run2, run3, runabla, runablb)
- Lane log: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA3/NAMECHECK.md

Nothing was pushed (local commits only, branch tnn-native-lab).
