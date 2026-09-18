# TNN frontier master handoff — R33/R34

This file consolidates the currently verified TNN frontier, historical blockers, exact hashes, and next work so later agents do not have to reconstruct the program from scattered logs.

## Operating constraints

Frontier implementation and qualification are pure Zag using the local compiler at `/Users/Shared/micah/Documents/zag/znc`. Do not execute Python, PyTorch, TensorFlow, JAX, NumPy, Hugging Face, pickle payloads, historical Python verifiers, or foreign ML runtimes. Historical Python source may be read as inert text to reconstruct semantics in Zag. Shell, `rg`, archive listing, hashing, and build/evidence orchestration are allowed.

Preserve unrelated dirty work. Do not reset, checkout, clean, commit, or push as part of frontier qualification.

## Canonical R27

Canonical R27 remains immutable.

- development step: 60,423
- newborn restarts: 0
- raw SHA-256: `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`
- policy SHA-256: `983db6a9c771f4952392d288459d65dfb04c33a7cbca37ac9f10a4365c7887a8`

No R34 lane is canonical. `learn` remains closed. Learner authority remains false. Scientific exposure remains zero. No successor is promoted.

## Stable compiler

Pinned compiler:

`/Users/Shared/micah/Documents/zag/znc`

SHA-256:

`3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`

R33 closeout retained the stable compiler rather than promoting the older local candidate because full native bootstrap/fixpoint and broad compiler provenance/regression qualification were not established.

### Zag imported-constant ABI/compiler finding

During R34 v2/v3 integration, functions receiving slices could observe corrupt/zero slice lengths when allocation sizes or wire checks used an imported constant such as `CW_BYTES`/`R34V3_STATE_BYTES` across the problematic call shape. Direct literal-size probes worked. The bounded workaround was to define a lane-local literal-equivalent wire-size constant in the caller/harness and keep semantic equality with the imported contract value. This must remain documented because an apparently harmless refactor back to imported size constants can reintroduce the failure.

## R33 current closeout

Authoritative closeout remains fail-closed overall: `R33_FINAL_CLOSEOUT.json` reports `r33_complete=false`.

Fresh native/engineering gates already closed include:

- V68: PASS, original intended outer learner-packet shape
- V73: PASS, original six-slice caller
- V71: PASS, native checkpoint-module reproduction
- V92: PASS, native campaign with 339 selftest checks and 12 packet modes
- continuing-life bounded transport/baseline: PASS
- N19 repaired bounded runtime: PASS within its stated process-containment scope

Continuing-life evidence includes whole-record atomicity/refusal, world plus ingress state, pending credit, delayed continuation, fresh-process continuation, torn/corrupt refusal, and fail-closed `learn` exit 65.

N19 does not claim descendant/process-group containment beyond its bounded scope.

## N17 / historical verifier equivalence

N17 remains fail-closed for full verifier equivalence. The latest matrix has 54 engineering rows passing and 26 source/history rows blocked.

Blocked R27 rows:

- `R27-06 r26_sha`
- `R27-08 abstraction_s2g`
- `R27-09 abstraction_g2s`
- `R27-32 manifest_integrity`
- `R27-33 r26_verifier`

Blocked R26 rows:

- `R26-06 r25_hash`
- `R26-07 r25_digest`
- `R26-08 video_artifact_exists`
- `R26-09 video_artifact_frames`
- `R26-16 visual_name_state`
- `R26-17` through `R26-22` forbidden-token/source checks
- `R26-38` through `R26-44` policy locks
- `R26-45 deterministic_smoke`
- `R26-46 r25_lineage_regression`
- `R26-47 manifest_integrity`

Exact missing historical identities currently tracked:

- `state/r26-accepted-state.pkl` SHA-256 `df3acde273aa682642d13763a24208ff1dbb42968313cbe2a4256f7ccbc1f839`
- `state/r25-accepted-state.pkl` SHA-256 `6d0b14d8ab4a081b57c3762800475f8ecb67d2d7e9134a82e6f7690efc4e2957`
- full `src/r26_experiments.py` SHA-256 `1e87721a93666155aabc67016ccd9416684c00f1e3c02da57f2c712083fc444d`
- `state/r26-accepted-policy.json` exact admitted identity/hash still unresolved
- exact original R26 video artifact/path/hash and decoder/frame semantics unresolved
- exact R26 deterministic-smoke source/import/input identities and semantics unresolved

The historical R25 68/68 receipt is a witness only. It is not fresh behavioral evidence.

## Local archive recovery status

A prior sweep identified roughly 35 tar/zip archives. High-value bundles include:

- `Research/tnn-r27-native-master-shadow.tar.gz` / `.zip`
- `Research/tnn-v1-current-execution.tar.gz` / `.zip`
- `Research/tnn-r30-big-boom-shadow.*`
- `Research/tnn-pre-v1-r28-aeif-no-graph-shadow.*`
- `Research/tnn-r31-endogenous-chunking-shadow.*`
- additional TNN archives under Research and `/Users/Shared/micah/Documents/Codex/...`

The R27 native-master shadow bundle contains a valid manifest, docs/results/source/state shadow materials, `state/shadow-policy.json`, and `state/state_bridge_manifest.json`, but its member list did not contain the exact missing R25/R26 accepted-state members. `tnn-v1-current-execution.tar.gz` likewise did not yield those exact names in the initial inspection.

The archive-wide member/hash sweep is still required. Exact-match admission only: never substitute a similarly named shadow artifact for a missing historical release artifact.

## V91 semantic generator recovery

V91 actual native generator parity remains fail-closed. Historical parity was previously 0/16 generated strings, but native recovery substantially narrowed the intended semantic structure.

Recovered high-level dataset constraints:

- train_n = 1800
- test_n = 72
- total = 1872
- condition dimension = 42
- groups: name 8, object 8, location 8, motive 6, action 8, kind 4
- exactly four known active groups and two unknown active groups per retained example
- motive examples hide location + action
- other kinds hide motive + action

Recovered 16 intended semantic rows:

1. lena / folder / motive / bad=getting wet
2. ana / glass / motive / bad=making noise
3. omar / folder / belief / l=desk
4. lena / book / location / l=cabinet
5. ravi / cup / promise / l=shelf
6. ana / cup / motive / bad=falling
7. mira / notebook / belief / l=desk
8. ravi / notebook / motive / bad=falling
9. ana / report / belief / l=table
10. mira / notebook / location / l=cabinet
11. omar / phone / promise / l=drawer
12. lena / cup / belief / l=room
13. nora / glass / belief / l=desk
14. sam / book / belief / l=room
15. jon / folder / belief / l=bag
16. nora / glass / belief / l=desk

`V91_INTENDED_FAILURES,0` means those intended rows/constraints were recovered. It does not mean generator parity.

Still unknown for true V91 parity:

- the two missing one-hot groups for each example
- exact original generator method
- RNG algorithm/state/seed progression
- multinomial/sampling rules
- exact model/forward math and precision behavior
- tokenizer/BPE state and merge path
- any additional hidden preprocessing required by the historical generator

Do not hardcode oracle output strings. Historical Python can be read as text only.

## R34 v1

`Research/R34_NATIVE_CONTINUAL_LEARNER_V1`

R34 v1 established an actual pure-Zag integer online learner rather than a hardcoded response fixture. It used a small tabular Q-style state with deterministic native RNG, evaluator-owned delayed reward delivery interface, full learner-state serialization, SHA-256 integrity, and fresh-process reload.

Fresh bounded results included:

- A baseline 64/64 due to the neutral initial tie policy
- B baseline 0/64
- A after training 64/64
- B after training 64/64
- A retained after B 64/64
- 192/192 enabled online updates
- update-disabled control: 0 updates and B remains 0/64
- deterministic identical seed/experience state
- corrupt and torn checkpoint refusal
- fresh-process reload preserving A/B, updates=192, fingerprint 512355

V1 is engineering evidence only.

## R34 v2

`Research/R34_NATIVE_CONTINUAL_LEARNER_V2`

V2 moved the learner into the persistent R33 world with observations, movement, inspect/touch actions, hidden regime changes, three-tick delayed consequences, causal action-ID matching, latent context allocation/reuse, full checkpointing, controls, and resource accounting.

Qualified evidence:

`Research/R34_NATIVE_CONTINUAL_LEARNER_V2/EVIDENCE_20260916T011333Z`

Receipt:

- failures=0
- scientific_exposure=0
- canonical_r27_mutated=false
- learner_authority_granted=false
- learn_opened=false
- foreign_ml_runtime_used=false

Behavioral witness:

- untrained A baseline 8/16
- trained A 16/16
- trained B 16/16
- two latent contexts allocated
- return A 15/16 with zero score/count updates during return evaluation
- total A+B updates 48
- update-disabled B control 0 updates, 12/24 positive
- reward-scrambled A control 0/16 after training
- deterministic learner/world/ingress replay
- exact pending-credit fresh-process continuation
- inner corruption refusal 2005
- torn checkpoint refusal

Qualified v2 source SHA-256:

`39ace96fc275aa0c8894217a393600ac806fe4a10011e82585b4703c7cb8dec0`

Qualified binary SHA-256:

`1e76ee36e147c47615a18d580e5346ced888d6837aad78e2b318ac83f08cee19`

## R34 v3

`Research/R34_NATIVE_CONTINUAL_LEARNER_V3`

V3 separates learner source from world/evaluator source. The learner core imports only observation contracts. The harness owns world/regime/reward/checkpoint operations.

The latest pre-freeze native behavioral run reached `R34V3_FAILURES,0` with the same bounded behavioral gates as v2. That run is not the final frozen qualification until `run_native.zsh` closes structural isolation, persistence, fresh-process continuation, corrupt/torn refusal, hashes, and receipt in one evidence directory.

## Existing native learning precedent

`Research/tnn_r32_e46_terminal_order_discriminator.zag` contains earlier pure-Zag integer learning primitives including `e45_rng_next`, `e45_rng_range`, `e45_linear_predict`, `e45_linear_update`, `e45_shadow_predict`, and `e45_shadow_update`.

## Claim boundary

Current evidence supports bounded claims about native online adaptation, delayed causal credit, persistence, deterministic replay, controls, and latent context reuse in the specified test worlds.

Current evidence does not support a claim that TNN beats LLMs, beats transformers generally, reaches AGI, or wins 90% of capability categories. No equal-comparison benchmark suite establishing those conclusions exists yet.

## Frontier order

1. Freeze R34 v3 with structural isolation plus the full v2 persistence/control battery.
2. Continue V91 reconstruction from historical source text/logs/archives until actual generator semantics are recovered or the blocker is irreducible with local evidence.
3. Complete archive-wide R25/R26 exact-member and hash recovery; admit exact matches only.
4. Implement additional pure-Zag verifier equivalents only when source semantics are fully reconstructed.
5. Re-run independent adversarial review over R34 v3 and the repaired R33 historical-equivalence lanes.
6. Only after continuity and authority gates close should any integration with `learn` or canonical state be reconsidered.
7. Build equal-comparison benchmark infrastructure before making architecture-versus-LLM claims.
