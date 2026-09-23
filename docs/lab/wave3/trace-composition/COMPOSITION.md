# COMPOSITION.md — composition operators over the trace substrate

**Wave 3 · slug: trace-composition · 2026-09-19**

## 1. The substrate (what is being composed)

From `brain/STATE_SCHEMA.md` §5: a Trace is a verified symbolic
operation-sequence over a cue vector, with `ops` (symbolic opcodes),
`verified`, `support`, `sources`, `provenance` (`SELF_VERIFIED`), `anchors`.
The wave-2 white-box suite (`wave2/whitebox/WHITEBOX_TESTS.md`, Group 1)
proved natively that the two lab-canonical opcodes are pure symbolic
functions of (cue, opcode, param): **FILTER_GT** (keep `v` iff `v > param`
else 0) and **MAP_MUL** (multiply, u8 wraparound). That is the substrate
this investigation composes.

This trial works on a **substrate analog**, not the 435 real R27 traces:
no Zag-native pickle reader exists yet (STATE_SCHEMA.md §10.1). The
mechanism under test is *composition of verified op-sequences*, not the
content of any particular trace.

## 2. The three operators

### 2.1 SEQ — sequential chaining

`comp_seq(store, a, b, out)`: the composite's op-sequence is the
concatenation of `a.ops` and `b.ops`. Preconditions (all structural):

- `a.verified == 1 && b.verified == 1`
- `a.provenance ∈ {SELF_VERIFIED, PROV_COMPOSED}` and same for `b`
  (a composite of composites stays composable; anything else is a foreign
  object and refuses)
- `a.nops + b.nops ≤ TC_MAX_OPS` (capacity is a build parameter, §5)

Postconditions on success: `out.verified=1`,
`out.provenance=PROV_COMPOSED`, `out.sources = a.sources | b.sources`,
`out.support = min(a.support, b.support)` (weakest-link — a documented
design choice, not a discovery), `out.ops = a.ops ++ b.ops`.

### 2.2 BRANCH — conditional on a verified predicate

`comp_branch(store, pred, t_then, t_else, out)`: a composite of **kind=1**.
Execution semantics (element-wise, deterministic):

```
mask[i]  = apply(pred.ops, cue)[i]      # nonzero = true
then[i]  = apply(t_then.ops, cue)[i]
els[i]   = apply(t_else.ops, cue)[i]
out[i]   = mask[i] != 0 ? then[i] : els[i]
```

Predicate-class test (structural, inspectable): a trace is predicate-class
iff `nops ≥ 1` and **every** op is in the FILTER family (in the lab-canonical
v1 vocabulary: `OP_FILTER_GT`). A MAP_MUL-only trace is not a predicate —
no mask semantics can be read off it — and refuses with NOT_PREDICATE.
All three parts must satisfy the SEQ-style verifiedness/provenance
preconditions; sources union over all three.

### 2.3 ABSTRACT — naming a verified sequence

`comp_abstract(store, reg, t, name_id)`: registers a **flattened**
definition of `t.ops` under `name_id`. Flattening expands any OP_NAMED
references at abstract time (bounded recursion), so every registry entry is
a flat, inspectable op list — no hidden indirection chains. Rules:

- `t` must satisfy the verifiedness/provenance preconditions (abstracting
  an unverified trace refuses: UNVERIFIED_LINK).
- Re-abstracting the **identical** op list under an existing name is
  idempotent success (deterministic; registry unchanged).
- Registering a **different** op list under an existing name refuses with
  NAME_COLLISION and leaves the registry untouched (no silent overwrite —
  name squatting is structurally impossible).
- Definitions may then be *used* via the `OP_NAMED` opcode inside traces;
  `comp_apply` expands them through the registry. Applying an unknown name
  refuses with NAME_UNKNOWN.

### 2.4 The executor

`comp_apply(store, reg, t, cue, out)` is a **pure deterministic executor**.
It dispatches on `kind`: flat → sequential op application with OP_NAMED
expansion; branch → the mask semantics of §2.2. **It checks nothing about
verifiedness.** This is deliberate: verification is enforced at
*composition time* (the only place new verified objects come into being),
exactly like a type system that checks at construction, not at every use.
The verified flag travels with the record; execution is orthogonal.

## 3. The structural guarantee (what "refuses" means)

Refusal is **structural, not advisory**: the operator returns a status code
(2101–2106) and the output record is atomically invalidated
(`verified=0, provenance=PROV_NONE, nops=0, kind=0`). There is no code path
that yields a `verified=1` composite containing an unverified link —
proven by the adversarial suite (ADV-1..ADV-4) in the trial, each paired
with its tampered input per the playbook's negative-case rule.

## 4. Determinism (program law A2)

The system contains **no RNG, no time reads, no uninitialized memory**:
- Every record header is explicitly initialized (the playbook's
  `nio_alloc`-is-not-zeroed rule is honored everywhere).
- Registry lookup is a linear scan in registration order (no hash
  nondeterminism); idempotent re-abstraction is order-independent.
- The runner statically greps `comp.zag` for
  `rng|random|_zag_raw_syscall|_zag_print` — wait, `_zag_print` is used for
  the CL_CHECK output contract, which is fine and deterministic. The grep
  covers `rng|random|_zag_raw_syscall` plus `_zag_i64_to_str`? No —
  `_zag_i64_to_str` is deterministic (used by cl_number). The forbidden
  set is: RNG, randomness, raw syscalls, time. Output printing is the
  deterministic test contract, not system behavior.

## 5. Scale dimension (program law A1)

| Dimension | Trial | S2 (next) | S3 |
|---|---|---|---|
| cue length | 128 | 512 (R27 native dim) | 512 |
| trace store | 64 | 256 | 1000 |
| named registry | 32 | 64 | 128 |
| max ops/record | 8 | 64 | 64 |

Complexity: operators are O(cue_len) element application + O(nops)
sequencing; registry lookup O(N_names) linear scan; memory linear
(92 B/trace, 76 B/name). No per-element state, no N×N tables, no
randomness at any scale. Trial ≈ 12 KB of records; 100× ≈ 1 MB.
S2/S3 are named next steps, not run here.

## 6. Relation to banned / prior art

- No score tables, no N×N scale-ups, no RL/reward shaping, no random
  exploration: composition is structural and deterministic.
- DO_NOT_REPEAT §8.7 (aggregate-only reporting): every group reports
  per-case CL_CHECK lines; refusals are per-link, never aggregated.
- DO_NOT_REPEAT §5 (B000 trace-helper defect): this trial does not use the
  prototype trace helper; records are explicit byte layouts with documented
  offsets, initialized by hand.
- The "capability builds up" claim is tested, not assumed: H4/G9 measure
  whether abstraction yields real reuse (footprint reduction) or is merely
  concatenation with extra steps.
