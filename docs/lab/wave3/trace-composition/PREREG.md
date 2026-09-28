# PREREG — trace-composition (Wave 3)

**Investigator:** Wave-3 subagent (trace-composition) · **Date:** 2026-09-19
**Status:** written BEFORE any implementation or run. This file is frozen;
any design change after this point is recorded as an amendment below, never
edited in place.

## Program-law amendments incorporated (Micah, 2026-09-19)

- **A1 — scaling allowed.** The ban was on scaling *toy mechanisms*. This
  design must carry an explicit scale dimension (§6) and a next-scale test.
- **A2 — no randomness in the AI.** The composition system contains **zero
  RNG**: no random exploration, no random tie-breaks, no stochastic
  policies, no seeded RNG inside the system. All operators are deterministic
  functions of explicit state. A static runner check greps the system source
  for rng/random/time/syscall references; any hit = design violation.
- **A3 — designed adversarial curricula.** Test adversity is expressed as
  explicitly-designed adversarial trace sets (ADV-1..ADV-7, §5), not random
  fuzzing. No seeded RNG in the harness either — every cue and trace is a
  hand-specified constant. The verdict distinguishes "system is
  deterministic" (evidence D1/D2) from "tests were adversarial" (ADV suite).

## 1. Question

How do small verified traces compose into larger verified capabilities?
Concretely: are there composition operators over the trace substrate
(verified symbolic op-sequences over cue vectors, cf.
`brain/STATE_SCHEMA.md` §5) such that (a) a composite's execution semantics
equal the semantics of its parts applied in order, (b) the composite
carries the provenance of its parts, and (c) any unverified link
structurally refuses composition (no silent absorption)?

## 2. Hypotheses

- **H1 (soundness).** SEQ/BRANCH/ABSTRACT preserve execution semantics:
  `apply(compose(parts), cue) == reference(parts, cue)` element-wise on all
  trial cues, including boundary values and u8 wraparound.
- **H2 (provenance closure).** Every composite produced with `verified=1`
  has `provenance=PROV_COMPOSED`, `sources == union(parts.sources)`, and
  there exists no execution path that yields a `verified=1` composite
  containing an unverified link.
- **H3 (structural refusal).** Unverified or provenance-tampered links,
  non-predicate branch guards, and name collisions refuse with distinct
  status codes and leave no usable composite behind (output record is
  invalidated atomically).
- **H4 (reuse leverage).** Abstraction gives measurable reuse: a composite
  built from named-op references stores fewer op slots than its flattened
  expansion while executing identically. (Tests whether "capability builds
  up" or just "capability concatenates".)

## 3. What is NOT claimed

- This is a **substrate analog**, not the 435 real R27 traces: no Zag-native
  pickle reader exists (STATE_SCHEMA.md §10.1, READER_BLOCKED). Opcodes are
  the lab-canonical v1 semantics (FILTER_GT, MAP_MUL) from
  `wave2/whitebox/WHITEBOX_TESTS.md` Group 1.
- Three opcodes do not prove "general capability". The claim under test is
  the **mechanism of composition**, not generality.
- No learning, no RL, no reward shaping, no score tables, no exploration
  anywhere in this design. Composition is a structural operation, verified
  by construction + adversarial testing.

## 4. Design (summary; full spec in COMPOSITION.md)

Native Zag, one file `comp.zag`, importing only `common.zag` (for
`cl_check`/`nio_*`/`cl_number`). No learner core, no world, no syscalls in
system code.

- **Trace record** (fixed 92-byte layout, explicit offsets): id, verified,
  provenance, nops, sources-bitmask, support, kind (0=flat, 1=branch), op
  area (8 × {opcode,param} or 3 child indices for branch).
- **Named-op registry** (fixed 76-byte records): name_id, nops, provenance,
  flattened op list.
- **Operators:** `comp_seq` (chaining), `comp_branch` (conditional on a
  verified predicate-class trace), `comp_abstract` (named-op registration
  with flattening), `comp_apply` (pure deterministic executor, expands
  OP_NAMED via registry). `comp_apply` checks nothing about verifiedness:
  refusal happens at composition time, by design (documented in
  COMPOSITION.md).
- **Refusal codes:** 2101 UNVERIFIED_LINK, 2102 NOT_PREDICATE,
  2103 NAME_COLLISION, 2104 NAME_UNKNOWN, 2105 CAPACITY, 2106 BAD_OP.
  On refusal the output record is atomically invalidated.

## 5. Trial plan (all constants hand-specified; zero RNG)

Cue length 128 (trial scale; R27 native cue dim is 512 — see §6). Trace
store 64 records; registry 32 names; max 8 ops per record.

Groups (each check = one `CL_CHECK` line, `actual==expected` required):

- **G1 sanity:** single-trace apply of FILTER_GT / MAP_MUL matches
  hand-computed values (canonical v1 semantics).
- **G2 seq:** T1=(FILTER_GT 3), T2=(MAP_MUL 2); C=seq(T1,T2). Checks:
  apply(C)==reference on adversarial boundary cues; C.verified=1;
  C.provenance=PROV_COMPOSED; C.sources = T1|T2.
- **G3 seq refusal (ADV-1, ADV-2):** 5-trace left-fold with trace #3
  unverified → 2101 at the exact link, output invalidated; verified=1 with
  provenance=PROV_TAMPERED → 2101; op-count overflow → 2105.
- **G4 branch:** pred=FILTER_GT(100) (predicate-class), then=MAP_MUL(2),
  else=MAP_MUL(3); B=branch(...). apply(B)==element-wise reference on
  boundary cues (mask boundary at 100/101). Negative: MAP_MUL-only guard →
  2102 NOT_PREDICATE; unverified then-arm → 2101.
- **G5 abstract:** A=abstract(seq(T1,T2), name 7); trace using OP_NAMED(7)
  applies identically to flattened reference; idempotent re-abstract of
  identical ops → OK, registry count unchanged; name squat (different ops,
  name 7) → 2103 and registry still holds original (apply(name 7)
  unchanged); abstract of unverified → 2101; apply of unknown name →
  2104.
- **G6 nesting:** B2=abstract(trace with OP_NAMED(7) + FILTER_GT(10),
  name 11); apply(B2)==flattened reference; seq over named-using traces;
  sources/provenance propagate through nesting (sources(B2) ⊇ T1|T2).
- **G7 determinism:** build the same composite twice → byte-identical
  records; apply twice → byte-identical output; runner static check: no
  rng/random/time/syscall tokens in comp.zag.
- **G8 deep chain:** 8 single-op traces folded into one 8-op composite;
  apply == reference fold (linear-depth composition works).
- **G9 reuse footprint:** C_flat = seq-fold of 4 copies of (F,M) → 8 op
  slots; C_named = seq of 4 × OP_NAMED refs → 4 op slots; both apply
  identically → reuse halves stored slots (H4 evidence).
- **ADV-5 boundary cues** (woven through G1/G2/G4/G8): cues contain
  0, param-1, param, param+1, 255; MAP_MUL wraparound (e.g. 200*2 → 144).

Reference oracle: an independent direct executor (`tc_ref_apply`) over
plain op arrays — a different code path from the record-dispatching
`comp_apply`. Documented assumption: both implement lab-canonical v1
semantics.

## 6. Scale dimension (A1)

Trial scale is deliberately small (128-d cues, 64 traces, 32 names, 8 ops).
**Scaling argument:** every operator is O(cue_len) element application +
O(nops) sequencing; registry lookup is a deterministic O(N_names) linear
scan; memory is linear (92 B/trace, 76 B/name). No per-element state, no
N×N tables, no randomness at any scale. 10× (640 traces, 320 names,
512-d cues) ≈ 100 KB; 100× ≈ 1 MB. Composition depth is bounded only by
the build-time capacity constant.
**Next scale test (explicit):** S2 — 512-d cues (R27's native cue
dimension), 256-trace store, 64 named ops, composite depth 64, ADV suite
replayed 1:1. S3 — 1000 traces, 128 names; assert linear time scaling of
seq/apply. S2/S3 are NOT run in this trial; they are the named next step.

## 7. Falsification criteria (frozen)

- **F1 (soundness).** Any composite whose `apply()` differs element-wise
  from the reference semantics on any trial cue → **NEGATIVE** (composition
  is unsound).
- **F2 (structural refusal).** Any should-refuse case that yields a
  `verified=1` composite; any composite with incomplete source union; any
  refused link that leaves a usable composite behind → **NEGATIVE** on the
  refusal claim.
- **F3 (determinism).** Any nondeterminism in repeated identical
  builds/applies, or any RNG/time/uninitialized-memory read in system code
  → design violation; verdict **BLOCKED**, fix before any verdict.
- **F4 (reuse leverage).** If named abstraction cannot reduce stored-op
  footprint for reused sequences (G9 fails) → **NEGATIVE** on the
  "capability builds up" dimension (composition would be mere
  concatenation).
- **POSITIVE requires:** F1 clean on all groups, F2 clean on all ADV
  cases, F3 clean (static + repeated-build checks), and H4 demonstrated
  (G9 footprint reduction with identical semantics).
- **Honest negatives are first-class:** a clean F1/F2/F3 with failed H4 is
  reported as MIXED (sound + refusal hold, buildup claim fails), not
  re-framed.

## 8. Amendments

- **2026-09-19, post-freeze (before final verdict).** First run
  (EVIDENCE_20260920T002045Z) failed 1/92 checks (`g6_nested_oracle`).
  Root cause: harness setup defect — the name-11 use-site trace (slot 36)
  was never defined in `tc_setup`; the empty record applied as identity and
  the oracle correctly flagged the mismatch. This was a test-harness bug,
  not a composition-mechanism bug. Fix: added the missing trace definition
  (one line). Same session: tightened the runner's static no-RNG check to
  strip `//` comments first (first version false-positived on the word
  "RNG" in code comments). Reran from scratch: 92/92 pass
  (EVIDENCE_20260920T002106Z). The failed bundle is retained. No design,
  operator, or falsification-criteria change — prereg text above untouched.
