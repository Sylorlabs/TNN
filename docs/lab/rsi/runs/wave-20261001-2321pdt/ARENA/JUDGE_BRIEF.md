# JUDGE BRIEF: Arena INQ (wave-20261001-2321pdt)

## Provenance

- RENDER_SHA: 0218296e0 (evaluation record commit; judged artifact source
  committed at 0ddb5e9ce, binary 09f59dcbee0fcd443a911f2bf24bff883960f457d0ce9acd59506d3c38339b1d)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: arena v6 refreeze 0.794 (54/68, CONFIRMED
  wave-20261001-1721pdt); TCNP BUILD-PASS bounded (wave-20261001-2021pdt,
  procedure candidate, separate binary, not integrated here); INQ built on
  the v6 base source (c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89)
- NEW_KNOWLEDGE_CLAIM: A generic ask-observe-answer loop that emits an
  explicit observe request naming the missing fact parsed from any unknown
  fact query and absorbs observation results into the general fact store
  raises sealed-arena active inquiry (C8) from 0.000 to 1.000 with zero
  regressions on the other 15 capabilities across 3/3 byte-identical runs.

## Verdict: BUILD-PASS

All nine frozen kill bars pass (PREREG_ARENA_INQUIRY.md, frozen alone at
1156add31 before implementation at 0ddb5e9ce; commit order verified).

Per-capability sealed scores, before (v6 refreeze) and after (INQ), all
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
| C8 active inquiry | 4 | 0.000 | 1.000 |
| C9 causal intervention | 3 | 0.000 | 0.000 |
| C10 procedure invention | 2 | 1.000 | 1.000 |
| C11 representation invention | 2 | 1.000 | 1.000 |
| C12 transfer | 6 | 0.000 | 0.000 |
| C13 long interference | 6 | 1.000 | 1.000 |
| C14 process restart | 6 | 1.000 | 1.000 |
| C15 autonomous goal completion | 1 | 0.000 | 0.000 |
| C16 synthetic language | 6 | 1.000 | 1.000 |
| TOTAL | 68 | 0.794 | 0.853 |

Kill bars: K1 C8 4/4 PASS; K2 zero regressions on the 15 non-target caps
PASS (per-cap scores byte-identical; reply diff touches only 3 C7 lines
with reply still UNKNOWN, the 12 C8-block lines, and the done tail);
K3 3/3 byte-identical reruns PASS (stripped replies
3b1911236a81c742204f0800da14933ac713ed1e23c9905cf05bc4693dcbb46d;
traces d664b9eb600250e5fb5a8f7a1ee98b9f2710cc416305bfd5e59d7e6d8be76488);
K4 pure Zag PASS (`which python3` empty at lane start and end, zero
interpreter invocations, no PROCESS-FAIL); K5 sealed validity PASS
(rebuilt world_gen/arena hashes match the refreeze record, turns.jsonl
matches the sealed world, pre-run key hash recorded and key never
opened, zero C8 oracle strings in mechanism source); K6 negative
controls PASS (ask-off ablation 0/4, absorb-off ablation 0/4, both
halves causal, both reproduce the 54/68 baseline); K7 honesty PASS (C7
replies exactly UNKNOWN in all runs); K8 architecture PASS (+69/-3
lines, 0 new modes/bridges/routers/handlers/semantic cases, capability
from learner state); K9 L3 explicitly disclaimed PASS (fails C0-A
through C0-D; L1/L2 fact-acquisition infrastructure, not representational
invention).

## What this does not claim

No L3 claim. No TNN-2 substrate claim. No TNN-beats-LLM claim. The
canonical 0.573 is not moved (only a clean refreeze reproducing
composition without contamination can move it). Remaining sealed zeros:
C9 causal, C12 transfer, C15 goal. The parent task's "15 capabilities /
other 14" counts do not reproduce from the sealed records (16
capabilities, 68 items); flagged in the prereg, not asserted; the frozen
no-regression bar covered all 15 non-target capabilities and passed.

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/PREREG_ARENA_INQUIRY.md
- Implementation: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/inq_contestant.zag
- Binary: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/bin/inq
- Full record: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/SEALED_EVAL.md
- Sealed runs: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/sealed/run1 (run2, run3, runabla, runablb)
- Lane log: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/NAMECHECK.md

Nothing was pushed (local commits only, branch tnn-native-lab).
