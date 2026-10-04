# RACE PREREGISTRATION: TNN vs LLM Lifetime-Learning Race (Program 1)

Status: FROZEN PREREG. Committed alone before any race implementation,
world generation, or contestant code. Any change to the design below
requires a dated amendment committed alone before the changed code runs.

Date: 2026-09-30 UTC
Worker: C1 (TNN vs LLM Lifetime-Learning Arena Worker)
Owned path: docs/lab/research-lead/overnight-20260928/lifetime_race/

## 1. Objective

Build the lifetime-learning race: a sealed, deterministic, multi-world
evaluation that measures which architecture turns new experience into
persistent usable knowledge more effectively. Stages A through L probe
one-shot learning, composition, correction, contradiction, novel
vocabulary, active inquiry, causal intervention, procedure acquisition,
transfer, interference, restart, and law change in one continuing
lifetime per contestant.

Primary question: which architecture turns new experience into persistent
usable knowledge more effectively?

## 2. Non-goals and claim discipline

- This race does NOT claim L3 for any mechanism. It measures behavioral
  lifetime-learning capability. L3 adjudication stays with the frontier
  workers under mandatory Criterion 0.
- Do NOT claim "TNN beats LLMs" unless a serious LLM baseline completes
  the same frozen benchmark with realistic memory/tools and equivalent
  information access. No LLM baseline is available in this environment
  (verified 2026-09-30: no ollama binary, no local inference server on
  11434, no LLM API keys in environment, and the Zag toolchain has no
  socket/TLS/HTTP so a pure-Zag runner cannot call an API). The LLM
  baseline is therefore marked PENDING. No LLM score will be fabricated,
  estimated, or implied.
- Do NOT claim "TNN beats humans": no human protocol is run here.
- The honest product of this wave: sealed race infrastructure, actual TNN
  contestant scores with cost curves, preserved sealed test, and a frozen
  LLM interface for a future external runner.

## 3. Fairness doctrine (for when the LLM baseline runs)

3.1 Identical observations. Both contestants receive byte-identical turn
    streams (briefing, observations, queries, tool results). Encoding may
    differ only as documented in the world generator output; factual
    content is identical.

3.2 The LLM baseline is NOT crippled. When available it receives: a
    frontier-class model, the full briefing, the same ASK/OBSERVE/
    INTERVENE tools with identical budgets, a persistent file-backed
    notebook that survives restart, and retrieval over its notes. It is
    told the world is synthetic and novel and that honesty (UNKNOWN /
    UNRESOLVED) is scored.

3.3 TNN receives its native mechanisms in a pure-Zag contestant: fact
    store with provenance, competing hypotheses, contradiction handling,
    correction propagation, merit-based memory, causal hypothesis set,
    and persistent native state across restarts.

3.4 Same tool budgets per stage. Single attempt per query for both.
    Parse failures count as wrong, not retries.

3.5 All costs charged to both: observations, teaching examples, tokens,
    tool calls, repeated context bytes, CPU time, peak RAM, persistent
    storage, latency, state growth, active hypotheses, learned structures.

## 4. Contestant freeze protocol

4.1 The TNN contestant (`race_tnn.zag`) is implemented, built, and its
    binary hash recorded BEFORE world generation begins.

4.2 Worlds are generated AFTER the contestant freeze. The generator seed
    is derived after the freeze commit. The contestant author (this
    worker) does not view the seed value during derivation or
    installation (mechanical /dev/urandom derivation, blind shell
    substitution; verified by pattern/count only).

4.3 The contestant is never modified after seeing any world content. Any
    bug fix after world generation requires a prereg amendment, a new
    seed, and regeneration.

## 5. Seed protocol

- New canonical race seed: 6 bytes from /dev/urandom as one unsigned
  integer, written directly to `lifetime_race/SEALED_SEED.txt` by shell
  redirection. Not viewed during derivation or installation.
- Installed blindly into `race_world_gen.zag` (the `sd` constant) via a
  shell variable; verified afterward by count/pattern only (old-seed
  count 0, exactly one numeric sd constant, baked value byte-matches the
  sealed file via grep -q through the variable, never displayed).
- Seed file sha256 recorded in the final report (not the seed value).

## 6. World specification (RACE-WORLD-1..3)

Three synthetic worlds W1, W2, W3, generated deterministically from the
sealed seed. No world exists before generation; no web source contains
its facts.

6.1 Novelty. Entity names are random 2-syllable CV combos from a fixed
    consonant/vowel inventory, checked against a 10k common-English word
    list and against common English substrings longer than 3 chars. The
    generator aborts if any name fails the check. Attribute values,
    relation names, causal parameters, and novel vocabulary are drawn
    fresh per world per seed.

6.2 Per-world contents.
    - 12 entities, each with 3 attributes drawn from per-world value sets.
    - 8 directed relations from a per-world relation vocabulary.
    - Causal subsystem: 3 binary variables (P, Q, R); true graph drawn
      from {P->Q->R, P->R->Q, Q->P->R}; observational episodes consistent
      with all three chain hypotheses by design (observationally
      indistinguishable until intervention).
    - 2 procedures, each with 4 demonstrations.
    - 2 conflicting-claim pairs (stage D).
    - 4 correction episodes (stage C).
    - 6 novel words grounded mid-stream (stage E).
    - 1 law change (stage L).
    - Transfer pair (stage I): domain T1 sharing latent relation-graph
      shape with an earlier domain S under new labels; control domain T2
      with a different latent shape.

6.3 No recognizable benchmark templates. No ARC, no bAbI, no Winograd,
    no standard logic puzzles. Surface forms are generated, not copied.

## 7. Stages A through L (per world)

Turn kinds: brief, obs, query, act, toolresult, save, load, end.
Reply: exactly one JSON line per turn (ack / answer / tool call / done).

- A (one-shot facts): 10 fact observations, each shown ONCE. Then 10
  queries: 5 with literal wording, 5 paraphrased. Scoring separates
  literal recall (A1-A5) from semantic use (A6-A10).
- B (composition): 8 relation observations. Then 6 queries requiring
  2-4 hop chains never directly taught (B1-B6).
- C (corrections): 4 episodes. Each: teach fact F (obs), later present
  contradicting evidence from a higher-reliability source (obs), query
  (C1-C4; correct = corrected value). 2 collateral probes on unrelated
  facts (C5-C6; correct = unchanged). Later re-query 2 corrections
  (C7-C8; retention).
- D (unresolved contradiction): 2 setups. Each: evidence for H1 (obs),
  evidence for H2 (obs, balanced weight), query (D1-D2; correct answer
  is UNRESOLVED). Then discriminating evidence (obs), query again
  (D3-D4; correct = supported hypothesis).
- E (novel vocabulary): 6 word groundings (obs). Then 6 compositional
  queries using the novel words in unseen combinations (E1-E6).
- F (active inquiry): 3 items. Query posed with insufficient
  information; contestant receives an act turn (budget 3 tool calls);
  tool results delivered; then the query is re-posed and scored
  (F1-F3). Tool use itself is recorded.
- G (causal intervention): 2 puzzles. Observational episodes (obs)
  consistent with all three chain graphs. Act turn (budget 4;
  INTERVENE allowed). Tool results delivered. Query: predict an
  outcome under a stated intervention (G1-G2).
- H (procedure acquisition): 2 procedures x 4 demos (obs). Then 3 test
  queries per procedure with varied surface representation (H1-H6).
- I (transfer): domain T1 (shared latent shape, new labels) and control
  domain T2 (different latent shape) taught incrementally. Measure
  examples-to-criterion for each (criterion: 3 consecutive composition
  queries correct; cap 12 examples). Report T1 vs T2 counts. This stage
  yields measurements, not 0/1 scores.
- J (interference): 2000 unrelated noise observations. Then re-query:
  4 A-items, 3 B-items, 2 C-items (J1-J9).
- K (restart): save turn (runner records state checksum); runner
  archives the state dir, then resumes the contestant against the
  archived copy in a new path (true process boundary; no in-memory
  carryover). Re-query 4 items (K1-K4). Runner verifies post-load
  checksum matches the saved checksum.
- L (changed world): law-change notice (obs; a previously taught rule
  flips). 3 adaptation queries under the new law (L1-L3). 2 retention
  queries on unaffected context (L4-L5; correct = old values, no global
  forgetting).

Query counts per world: A10 + B6 + C8 + D4 + E6 + F3 + G2 + H6 + I(2
measurements) + J9 + K4 + L5 = 63 scored items + 2 transfer measurements.

## 8. Turn/reply protocol (frozen)

Turn JSON, one per line in `turns.jsonl`:
- {"turn":N,"kind":"brief","world":"W1","text":"..."}
- {"turn":N,"kind":"obs","ev":{...}} with ev.t in
  fact|rel|rule|demo|claim|vocab|law|noise (fields documented in the
  generator output; all values are plain strings/ints, parseable)
- {"turn":N,"kind":"query","qid":"A3","q":{"t":"attr","s":"...","a":"..."}}
  q.t in attr|relpath|yn|choice|causal|proc|compose (fields documented)
- {"turn":N,"kind":"act","qid":"F1","budget":3}
- {"turn":N,"kind":"toolresult","qid":"F1","result":{...}}
- {"turn":N,"kind":"save"} / {"turn":N,"kind":"load","from":"..."}
- {"turn":N,"kind":"end"}

Reply JSON, exactly one line per turn:
- obs/brief/toolresult/save/load: {"ack":true}
- query: {"qid":"A3","answer":"...","conf":0.0-1.0}; answer may be
  "UNKNOWN" or "UNRESOLVED"; conf is recorded, not scored
- act: {"tool":"ask","q":"...","qid":"F1"} |
  {"tool":"observe","target":"...","qid":"F1"} |
  {"tool":"intervene","var":"P","val":1,"qid":"F1"} | {"done":true}
- end: {"done":true}

Tool semantics and costs: ASK returns a world-model fact matching the
question if one exists (cost 1). OBSERVE returns a relevant withheld
observation (cost 1). INTERVENE applies do(var=val) to the causal
simulator and returns the outcome (cost 2). Exceeding budget rejects
the call. Tool calls and results are logged.

## 9. Cost ledger (per contestant, per world)

observations, queries, teaching_examples, tool_calls {ask, observe,
intervene}, wall_ms_total, wall_ms_per_stage, state_bytes (state dir),
peak_rss_kb (getrusage at end), tokens (N/A for Zag contestant;
recorded when the LLM baseline runs), learned_structures (contestant
self-report: facts, relations, hypotheses, procedures, vocab entries),
active_hypotheses (contestant self-report at end).

## 10. Learning curves

For each query the runner records (observations_so_far, correct).
Accuracy is aggregated in observation bins per stage and overall,
producing capability-vs-experience curves, not just final scores.

## 11. LLM interface (frozen for future use)

`world/llm_prompt_pack.txt` per world: the full briefing, the turn
protocol rendered for an external runner, tool schemas, and answer
schemas. A future external runner with TLS capability can replay the
byte-identical `turns.jsonl` against an LLM baseline and submit
`replies.jsonl` for scoring by the frozen scorer. Until then: PENDING.

## 12. Validity bars (this wave)

V1: this prereg committed alone before any race implementation.
V2: contestant binary hash recorded before world generation.
V3: seed mechanically derived, never viewed during derivation or
    installation.
V4: zero Python anywhere in the wave (no .py under lifetime_race/;
    verified by find).
V5: zero em-dash bytes in new docs (verified by grep).
V6: LLM baseline explicitly PENDING; no fabricated scores.
V7: cost ledger complete for the TNN contestant.
V8: world-gen determinism: 2 runs from sealed seed, all artifacts
    byte-identical.
V9: contestant determinism: 3 full runs, reply sequences byte-identical
    (replies contain no timestamps by protocol).
V10: identical-observations structural check: the turn stream is a
    fixed artifact; any future contestant replays the same bytes.

ARENA-READY requires V1-V10. Otherwise ARENA-BLOCKED with the specific
failing bar documented. Performance scores are reported as measured;
no performance bar gates ARENA-READY.

## 13. What the TNN contestant is

`race_tnn.zag`: a pure-Zag one-life learner using TNN-native ideas
(fact store with provenance, competing hypotheses with evidence
weights, contradiction-triggered UNRESOLVED, correction with
supersession and provenance, merit-based memory under a cap,
causal hypothesis set with intervention-driven elimination,
demonstration-based procedure generalization, persistent state files).
It is a measurement instrument, not an L3 claim. Honest weaknesses
are reported as measured.

## 14. Governance

- Pure Zag for all race logic. Bash sequences process invocations only.
- No Python anywhere in this wave, including scratch and analysis.
- No em dashes in loop documentation.
- Commits local only on tnn-native-lab. Owned path only.
- Nothing pushed without explicit approval.
