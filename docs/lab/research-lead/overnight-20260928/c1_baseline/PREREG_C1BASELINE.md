# PREREG: C1 Simple Baseline Comparison (pipeline step 5)

Date: 2026-09-30 UTC
Status: FROZEN (committed alone before any implementation).

## Question

Does the C1-CLEAN 63/63 canonical score require the contestant's
learner-owned inference machinery, or can a trivial control with no
inference match it? If a trivial baseline reaches 63/63, the score is
a world property, not a learning property.

## Frozen worlds

Reuse byte-identical worlds from commit e0a30377f
(docs/lab/research-lead/overnight-20260928/c1_clean/worlds/):
w0, w1, w2 (canonical), h0, h1 (exploratory consistency only).
World files are verified by sha256 against the e0a30377f blobs before
any run; worlds are never regenerated or modified.

## Frozen driver

Reuse run_race.sh extracted from the freeze commit b8d38d9c8
(sha256 4cd7bec75915fb93dc8e874d25f9ec6428ee604beadff79b9357ea1c092850a9).
Interface: baseline binary takes <turn.json> <statedir>, prints one
JSON reply line. Query replies carry "answer". No tool use by any
baseline (act turns answered with {"done":true}).

## Baselines (all pure Zag, compiled with the pinned znc)

### B1 MEM: persistent associative store, last-write-wins, zero inference

- State: append-only log of taught facts, one line per obs fact:
  "s|a|v" (byte 124 separators; values are lowercase alpha).
- obs with ev.t == "fact": append s|a|v.
- query with q.t == "attr": scan the log from the end; answer the v
  of the last line whose s and a match. If none, answer "".
- query with any other q.t: answer "".
- act: {"done":true} (never uses ask/intervene tools).
- brief/save/load/end/toolresult: {"ack":true}.
- No generalization, no hypothesis evaluation, no causal simulation,
  no procedure application, no chaining, no meaning composition.

### B2 FREQ: global most-frequent taught value

- State: list of taught values v (one per line), in teach order.
- obs fact: append v.
- query attr: answer the most frequent v in the list; ties broken by
  earliest first-seen. If list empty, answer "".
- all other queries: answer "".
- act: {"done":true}. All other kinds: {"ack":true}.

### B3 RAND: deterministic pseudo-random pick from observed values

- State: list of taught values v in teach order, plus a counter n
  (number of attr queries answered so far).
- obs fact: append v.
- query attr: if list empty answer ""; else answer
  list[(n*7919+13) % len], then n = n+1. Fully deterministic given
  the turn sequence; no wall-clock or address randomness.
- all other queries: answer "".
- act: {"done":true}. All other kinds: {"ack":true}.

## Runs

3 baselines x 5 worlds x 3 reps = 45 runs. Each run starts with a
fresh state dir (driver rm -f). Determinism: 3/3 reps per world must
be byte-identical on replies.jsonl and scores.jsonl (costs.txt may
differ on the wall_ms line only).

## Frozen predictions

- P-MEM1: MEM scores below 35/63 on every canonical world
  (w0, w1, w2). Rationale: MEM answers only attr queries from
  storage. Stage A (20, immediate recall) should be 20/20. Stages
  B (chain), D (yn), E (meaning), G (causal), H (proc), T (chain),
  L (proc) get 0 by construction. F (withheld) gets 0 (no tool
  use). C (delayed attr) and K (retention attr) score only where
  the exact (s,a) was taught before the query.
- P-MEM2: MEM gets 20/20 on stage A in every canonical rep.
- P-FREQ1: FREQ scores below 12/63 on every canonical world.
- P-RAND1: RAND scores below 8/63 on every canonical world.
- P-DET1: all 3/3 reps byte-identical per (baseline, world).

## Verdict rule (frozen)

- If any baseline scores >= 60/63 on any canonical world:
  C1-BASELINE-WORLD-PROPERTY. The 63/63 score is achievable without
  inference; the learning interpretation of C1-CLEAN is killed.
- Else: C1-BASELINE-LEARNING-PROPERTY. Pure storage and trivial
  statistics do not explain 63/63; the score requires the
  contestant's inference machinery (causal, procedural, chain,
  meaning, hypothesis). This strengthens the claim toward pipeline
  step 6 (alternative-explanation attack).

The 60/63 bar is set below 63/63 to allow for a few lucky attr hits
by FREQ/RAND while still killing the learning interpretation only
on a genuine match.

## Kill bars

- K1 ORDERING: this prereg commit strictly precedes the freeze
  commit strictly precedes the results commit (git merge-base).
- K2 WORLDS: the 10 world files verified byte-identical to the
  e0a30377f blobs before any run; all 45 runs executed; every
  result recorded honestly against the frozen predictions.
- K3 PURITY: pure Zag plus shell only; zero Python anywhere;
  no em dashes (shell-only check_no_dash.sh); contaminated paper
  untouched.

## Out of scope

No new capability claim. No L3 claim. LLM baseline remains PENDING.
Step 6 (alternative-explanation attack) follows regardless of
outcome, using the H0 law-revert miss as anchor.
