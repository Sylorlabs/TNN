# SELF-TEST REPORT — Experiment 2 implementer (onebrain)

**Binary:** `~/workspace/onebrain/impl/onebrain` (built from `onebrain.zag` via `build.sh`)
**Source:** 1358 lines pure Zag, zero RNG, no threads, fixed round-robin interleaving.
**Spec:** frozen prereg `docs/lab/onebrain/PREREG.md` @ `1ab40adceff78d71460b992b078508acea7e8abc`
(read in full before implementation; kill bars K1–K6 binding).

## What was built

`onebrain <mode> <problems.tsv>` — a deliberation binary reusing the
deliberation-v1 ledger geometry (25 rows × 552B: readings hid 0–9, fact
candidates hid 10–12, action bids hid 13–24; turn fields 13804–13820) as a
**new module** (no fork of v1's file). V1's spare turn field @13816 is
designated the **FORK flag**.

Pipeline inside `ob_deliberate` (the machinery):
`GEN readings → GEN facts → GEN actions → ELIM → FORK_ASSESS → SUBPASSES → ARGMAX`.

- **Ledger-driven fork (anti-scaffolding):** `fork_assess` is a deliberation
  phase that reads ledger state (≥2 surviving readings with ev=1 AND top-two
  fired-bid margin ≤12) and sets the FORK flag @13816. `ob_subpasses` acts
  **only** on that ledger flag (`if(t_get(led,13816)==0) return;`). The driver
  (`main`/`run_full`/`run_minimal`/`solve_one`) contains no `fan_out`/fork/
  subpass logic — verified by grep (only hit: the `fork_en` mode-config
  parameter, i.e. experiment-arm selection, never a per-problem decision).
- **One shared ledger:** K=2 sub-deliberations own reading partitions
  {0–4}/{5–9}, execute in fixed round-robin order over 2 rounds, and read/
  write the same 13820-byte ledger. Exactly one ledger in the address space
  during fan-out (ablate mode excepted by design).
- **Causal channel (K5 lesson wired in):** audits post eliminations
  (status=1) and fact invalidations; later passes' bid-cleanup and
  re-scoring read those writes. Reading rows are branch-read by action GENs,
  never re-derived.
- **Single reintegrated verdict:** one ARGMAX over the shared ledger;
  no voting ensemble.
- **Modes:** `single` (GEN→ELIM→ARGMAX baseline, no fork), `onebrain`
  (full, shared writes on), `ablate` (shared writes off — each branch on a
  discarded scratch copy), `poison` (onebrain + hook flipping the leading
  bid's supporting fact to invalid between rounds), `min` (bare driver loop,
  full machinery — the K3 scaffold-removal test).

## Test results

Builds clean: **PASS** (one error on first attempt — `prlen` arity — fixed;
clean since).

3 smoke problems (invented blind, never seen the frozen set):
- smoke1 `what is the capital of france?` → 1 reading
- smoke2 `forget the joke and compare moby dick and pride and prejudice` → 4 readings
- smoke3 `tell me a joke and remember the louvre` → 3 readings

| Check | Result |
|---|---|
| 3× reruns byte-identical (SHA-256), all 5 modes | **PASS** — 15/15 match (SHAs in RUNLOG §6) |
| Fork fires on multi-reading case | **PASS** — smoke2 `fork=1` (nread=4, margin=7), smoke3 `fork=1` (nread=3, margin=3) |
| Fork does NOT fire on trivial single-reading case | **PASS** — smoke1 `fork=0` (nread=1, margin=999) |
| Neuter test (shared-writes-off changes outcomes) | **PASS** — smoke2: onebrain → compose/227, ablate → joke/242. The denial (`AUDIT_DENY fact=12 by=6`) and cleanup (`AUDIT_CLEAN bid=13/15/22 dep=12`) are visible in the trace and decisive |
| K2 poison: branches update mid-deliberation | **PASS** — smoke3: `POISON fact=11` → round-2 `AUDIT_CLEAN bid=13 dep=11`, `bid=22 dep=11` → winner flips joke→memory (14/238) |
| K3 scaffold-removal: min driver still fans out | **PASS** — `min` verdict lines byte-identical to `onebrain`; fork=1 on smoke2/smoke3; driver grep clean |
| K6: no RNG in decision paths | **PASS** — grep clean |
| Edge cases (empty query, `???`, lone `forget`, bad mode) | **PASS** — no crashes, sane verdicts |

One-brain vs single on smoke2 also differs (compose/227 vs joke/242):
the fork + cross-talk changed the outcome, which is the H1-relevant signal
on this probe (not a claim about the frozen set).

## Prereg deviations

**None.** Every hard requirement is met as written:
ledger-driven trigger, one shared ledger, causal channel with neuter test,
single ARGMAX verdict, pure Zag, zero RNG, deterministic interleaving,
`min` driver with no fan_out call, poison hook between sub-pass rounds,
`problems.tsv` (id/query/expected) read with expected ignored at runtime,
no tuning to problems (built blind; smoke problems are the implementer's own).
One documented design choice within the prereg's latitude: the poison target
is the supporting fact of the current leading bid (most adversarial
instantiation of "flip a shared fact candidate to invalid").

## Notes for the measuring crew

- `expected` column is parsed but never read into any decision.
- A header row starting with `id\t` is skipped.
- Trace lines are emitted for every mode except `min`; verdict lines are
  identical between `onebrain` and `min`.
- `close_call` follows v1's exact semantics (margin vs best *fired*
  runner-up, which may be an eliminated bid — e.g. smoke2 onebrain
  `close=1` with runner=13). Flagged, not changed, to stay faithful to the
  reference geometry.
