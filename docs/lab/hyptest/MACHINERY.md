# hyptest Machinery (Crew M)

Native hypothesis-testing loop in pure Zag. The machinery proposes competing
hypotheses from taught covariation, derives discriminating predictions,
preregisters them in audited memory slots before seeing test data, ingests a
sealed test observation, and adjudicates by abandoning refuted hypotheses.

## Intake shape

All observations use one narrow sentence shape:

```text
<instance> is <category>.
<instance> are <category>.
```

The intake accepts `is` or `are` as the copula (plural agreement only; a
5-line fallback in `ht_parse_is`, added 2026-09-27 after the sealed interface
repair — possessives like "has"/"have" are still rejected as unparseable).
The Nth sentence about an instance fills attribute slot N (0-indexed).
Teach instances carry slots 0..K-1. The phenomenon instance carries slots
0..M-1 where M = K-1. The missing slot (K-1) is identified structurally as the
outcome — present in teach, absent in phenomenon. No semantic labels, entity
names, or category words are hardcoded; the machinery works from position
and taught text only.

## Phases

Each phase is a separate process invocation; state persists in a binary
state file. The audit ledger inside the state file records every memory op.

| Phase | Command | What happens |
|-------|---------|--------------|
| init | `hyptest init <state>` | Fresh state file |
| teach (A) | `hyptest teach <state> <file>` | Each non-empty line is one teaching episode; the Nth sentence about an instance fills slot N |
| hypothesize (B) | `hyptest hypothesize <state> <file>` | Phenomenon ingest (one episode) + covariation → hypothesis slots |
| observe (C) | `hyptest observe <state> <file>` | Test observation ingest (one episode); nothing else changes |
| adjudicate (D) | `hyptest adjudicate <state>` | Compare recorded predictions to observation; abandon refuted |
| dump | `hyptest dump <state>` | Inspect facts, hypotheses, episodes, audit ledger |

## Hypothesis formation (Phase B)

For each attribute slot s (0..M-1):
1. Read the phenomenon's value v for slot s.
2. Find teach instances (carriers) with slot-s == v.
3. If carriers are unanimous on their outcome-slot value o, form a hypothesis:
   "slot-s == v predicts outcome == o".
4. If no carriers or carriers disagree, emit a note; no hypothesis.

Each hypothesis is committed to the substrate BEFORE test intake:
- One `st_add` creates the hypothesis slot (strength 50, region USER).
- A second `st_add` creates a linked prediction slot.
- The hypothesis slot cites up to 4 support episodes via `st_evidence`.
- The prediction slot cites up to 4 (the last 4) support episodes.
- The union of linked slots covers all support episodes (6/6 on dev).

Support episodes are the teaching episodes for all slots of all carrier
instances. The phenomenon episode anchors the prediction temporally.

## Adjudication (Phase D)

For each hypothesis, the recorded conditional rule is instantiated against
the test instance:
- If the test carries the hypothesis's attribute value:
  - If the test outcome matches the prediction → SUPPORTED.
  - If the test outcome differs → REFUTED.
- If the test does not carry the attribute value → UNTESTED.

Decision:
- If any refuted: `st_abandon` each refuted slot (learner-reachable op only);
  keep the rest.
- If none refuted: WITHHOLD — explicitly abandon nothing. This covers:
  - All supported (observation confirms all predictions).
  - All untested (test doesn't bear on the hypotheses).
  - Mixed supported/untested (e.g. devB1: both rules predict the same
    outcome for the test combination, so neither is refuted).

## Deliberation flag

Build with `HT_DELIB=1` (default) for the full loop. Build with
`HT_DELIB=0` to disable deliberation: `hypothesize` forms zero hypotheses
and `adjudicate` always withholds. This is the K6a control — it proves the
predictions come from the native hypothesis machinery, not the narrator.

## Citations and K10

A single `st_evidence` slot cites at most 4 episodes (substrate limit).
Gold support sets contain 6 taught fact-episodes per hypothesis. The
machinery splits citations across the linked hypothesis+prediction slots:
- Hypothesis slot: first 4 support episodes.
- Prediction slot: last 4 support episodes.
- Union: 6/6 support recall; 6/7 precision including the phenomenon anchor.

The audit ledger records every `st_add`, `st_evidence`, and `st_abandon`
with op, slot, rc, stage, and citation episodes (d1=code, d2=cite_ep).
The dump phase renders the full ledger for verification.

## Files

- `build/hyptest.zag` — the machinery (pure Zag, no randomness).
- `build/build.sh` — assembles substrate + body, compiles with pinned znc.
- `battery/` — dev battery driver and scoring scripts.

## Determinism

No randomness anywhere. Byte-identical reruns verified under:
- 2× normal runs (same inputs).
- `env -i` (empty environment).
- `MALLOC_PERTURB_=165` (allocator perturbation).

All outputs and state-file SHAs match across conditions.
