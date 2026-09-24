# Crew C — Frozen Prereg: Training TNN on KB Management as a Deliberate Skill

**Date frozen:** 2026-09-23. **Crew:** C (learning side of KB-CONTROL).
**Status:** FROZEN — no changes to curriculum, rubric, or kill bars without a
signed amendment. (Sibling crews: A root-cause, B conscious fork, D red-team.)

## 1. Background and objective

Micah's law: *"TNN must CONSCIOUSLY control its knowledge base — expensive but
thorough, never subconscious... it needs to be trained on how to do that."*

The 1GB audit (`docs/lab/knowledge/ingest_1gb/FINDINGS.md`, RT-G3) showed the
current machinery revises facts **subconsciously**: a revise that "succeeded"
silently destroyed an unrelated fact's last 126 bytes (padding-blind `bb.used`
overwrote the final blob chunk's data tail; `rtg:0259999` → NOTFOUND).

Crew C owns the **learning** side: can TNN itself practice KB operations as a
**deliberate, audited skill** — state the target, predict the bytes it will
touch, verify bounds, write, read back, confirm neighbors intact — and can
deliberate practice drive collateral damage to zero and keep it there?

## 2. Claims under test

- **C1 (learnability):** A native deliberative operator that starts with a weak
  prior (fast "subconscious" habit: trust cached hints, skip verification)
  reduces collateral damage to zero through deliberate practice + deliberate
  post-mortem lesson installation, with a visible learning curve.
- **C2 (retention):** The installed skill persists — no regression 1,000
  episodes after training ends.
- **C3 (generalization):** After training, the operator scores zero collateral
  on a held-out adversarial battery whose trap geometries never appeared in
  training.
- **C4 (own-operation):** The deliberate protocol's verification steps
  (bounds checks, neighbor digests, read-back compare) live in TNN's own
  decision path (pure Zag), not in a Python wrapper. Causal proof: stubbing
  those steps out of the Zag binary reintroduces collateral on the same
  battery the full binary passes clean.

## 3. The deliberate operator (pure Zag: `kbc.zag`)

A native, deterministic, deliberative KB operator. Per commanded operation it
chooses actions one at a time from an explicit action set; every choice is
emitted to an audit trace. Action set:

`STATE → PREDICT → VERIFY → (WRITE | REFUSE) → READBACK → NCONFIRM → DONE`

Shortcuts available to the weak prior: `TRUST_HINT` (use the spec's cached
hint as the target offset instead of reading the authoritative slot table),
`WRITE_DIRECT` (skip PREDICT/VERIFY), complacency skips of READBACK/NCONFIRM
after consecutive clean episodes, and `REUSE_TABLE` (on multi-op sequences,
reuse the previous op's slot table instead of re-reading the image).

**Decision rule (the learned skill lives here).** At each phase the operator
consults its lesson memory (a file it reads/writes deliberately across
episodes): the highest-strength applicable lesson wins; with no applicable
lesson it falls back to the weak-prior habit. Lessons are keyed
`situation × phase → action`, plus general lessons (`GEN:always_protocol`)
that apply to every situation. Lesson installation/strengthening happens in a
**deliberate post-mortem step, also pure Zag** (`kbc learn`), which reads the
teacher's verdict (COLLATERAL byte list or CLEAN) and the episode's own trace,
attributes the failure to the first missing/faked/wrong step, and installs or
strengthens the corresponding lesson. After ≥3 collateral episodes with
*different* situation keys, the post-mortem installs
`GEN:always_protocol` ("run all six steps from authoritative geometry on
every op, no exceptions") — the deliberate insight that specific patches keep
failing on new traps.

**Weak prior (the untrained habit being unlearned):** prefer TRUST_HINT at
PREDICT, skip VERIFY, skip READBACK/NCONFIRM once `clean_streak ≥ 2`,
REUSE_TABLE on sequence ops after the first. This models "subconscious"
operation. The NEG control (below) freezes this prior forever.

**Verification genuinely gates the write:** VERIFY recomputes the write range
from the authoritative slot table read out of the image, checks it against
every live neighbor's extent, and only then permits WRITE; a failed VERIFY
forces REFUSE (fail-closed, mirroring `sc_recall`). NCONFIRM takes FNV-1a/64
digests of every neighbor's full record extent before and after the write and
compares them inside the binary. READBACK compares the written payload bytes
against intent inside the binary. Python never computes bounds, digests, or
write parameters — it only builds fixtures, runs the binary, byte-diffs
images, and parses the trace.

## 4. Episode and store model

Each episode: a fixed-size store image plus a text spec.

**Image layout (little-endian):**
`[u32 magic 0x4B424331][u32 nslots][u32 blob_end][slot table: nslots ×
16 B = u32 id, u32 off, u32 len, u32 live][blob region: records
[u32 id][u32 len][len payload bytes], zero-padded to 8-byte alignment]`

**Ops:** `revise(slot, new_payload)` with `newlen ≤ oldlen` (in-place rewrite
of the payload extent `[off+8, off+8+oldlen)`, tail zeroed; `newlen > oldlen`
must be REFUSED, fail-closed), and `delete(slot)` (clear live bit, compact by
memmoving `[gap_end, blob_end)` down to `gap_start`, update moved slots'
offsets and `blob_end`). The slot table in the image is **authoritative**; the
spec additionally carries possibly-lying cached hints (`hint_used`,
`hint_off[]`) — the RT-G3 analog (padding-blind `used`).

**Legitimately-touched sets** (scorer-computed from the authoritative table;
any changed byte outside = collateral):
- revise: `[off+8, off+8+oldlen)` of the target record only.
- delete: the target's live-bit bytes + `[gap_start, blob_end_old)` blob
  region + updated slot-table entries of moved slots.
- REFUSE: empty set — any changed byte = fail.

**Trap taxonomy** (each a deliberate analog of a real failure mode):
- **T1 stale-hint:** hint disagrees with the authoritative table; TRUST_HINT
  writes to the wrong offset → collateral. (RT-G3 shape.)
- **T2 boundary:** record ends exactly at blob/chunk end; hint is
  padding-blind; sloppy end computation overruns the last fact's tail —
  the literal 126-byte-clobber geometry.
- **T3 seq-stale:** 2–4 op sequences; hints reflect the pre-sequence table and
  offsets shift after delete+compact; REUSE_TABLE on op ≥2 → collateral.
- **T4 compact-clobber:** delete+compact with a stale/short `blob_end` hint;
  wrong memmove length clobbers the last fact's tail.
- **T5 refuse-cases:** `newlen > oldlen`, dead slot, hint pointing outside the
  image — must REFUSE; attempting = fail.
- Clean episodes (no trap) are interleaved throughout: the shortcut habit is
  harmless on them, which is exactly why the weak prior survives without
  deliberate practice.

## 5. Curriculum (basics → advanced; deterministic, zero RNG)

Episode parameters are derived from the episode index by fixed formulas — no
random number generator anywhere (fixture builder, operator, scorer).

| Phase | Episodes | Content |
|---|---|---|
| P0 basics | 60 | single revise/delete; T1 40%, T5 10%, clean 50% |
| P1 boundaries | 60 | T2 boundary-size facts at exact pad/chunk edges; T1 30% |
| P2 multi-chunk | 60 | chunked stores; T4 compact traps; T2 carryover |
| P3 adversarial sequences | 80 | T3 sequences (2–4 ops), mixed traps, clean controls |
| **Held-out battery** | 60 | **novel** geometries never trained on: new chunk sizes, new pad alignments, new hint-lie patterns (offset shifts, inflated `used`), novel 3-op interleavings, clean controls |
| **Retention** | 1000 | mixed clean/trap episodes, lesson memory **frozen** (no post-mortem installs) |

Total training: 260 episodes. Held-out and retention fixtures are generated
from disjoint index ranges with disjoint geometry parameters from training —
verified by a script that asserts zero overlap of (chunk, pad, lie-pattern)
tuples between train and held-out sets.

## 6. Grading rubric (per episode)

- **FAIL:** any collateral byte (changed byte outside the legit set), with
  attribution to the first missing, faked, or wrong deliberate step, derived
  from the trace + verdict byte list. Faked-step detection: the scorer
  independently recomputes the legit range and neighbor digests from the
  authoritative table and final image; a trace whose claimed range ⊉ actual
  changed bytes, or whose claimed post-op digests mismatch recomputation, is
  marked faked.
- **PROCESS-VIOLATION:** no collateral, but a protocol step skipped or faked.
- **PASS:** no collateral + full six-step (or justified REFUSE) trace.
- **FALSE-REFUSE** (secondary): refusing a legal op — tracked separately; a
  degenerate always-refuse policy would pass collateral bars, so kill bar (a)
  also caps false-refuse rate.

Episode→binary invocations: `kbc operate` (deliberate op; emits trace +
final image), Python scores → verdict file, `kbc learn` (deliberate
post-mortem; updates lesson memory). Retention skips `learn` (memory frozen).

## 7. Controls

- **NEG (frozen weak prior):** the same binary with post-mortem disabled runs
  the full 260-episode curriculum + held-out battery. Expectation: persistent
  collateral on trap episodes — proves the curriculum is hard and the
  learning (not the harness) did the work in V1.
- **POS (full protocol as upfront instruction):** binary starts with
  `GEN:always_protocol` pre-installed at max strength, no practice needed.
  Expectation: flat zero-collateral from episode 1 — proves the protocol
  itself is sufficient; V1's claim is the *learning curve converging to POS*.
- **Ablation for C4:** a `KBC_SKIP_VERIFY` build (VERIFY/NCONFIRM decision
  logic stubbed to no-ops, trace honestly shows skipped steps) runs the
  held-out battery. Expectation: collateral reappears — causal proof the
  verification steps in the Zag decision path do the work.

## 8. Kill bars

- **(a) Held-out generalization:** **zero FAIL** (zero collateral episodes) on
  the 60-episode held-out adversarial battery after training, with
  false-refuse rate ≤ 5% and protocol compliance = 100%.
- **(b) Retention:** **zero FAIL** across the 1,000 post-training episodes
  with frozen lesson memory, protocol compliance ≥ 99%.
- **(c) Own-operation:** (i) all bounds/digest/readback/write-parameter logic
  resides in `kbc.zag` (Python computes none of it — attested by code
  inspection + a grep-able `FORBIDDEN` list in the scorer: it may not import
  or reimplement FNV, bounds, or legit-set logic beyond the independent
  recheck used for faked-step detection); (ii) the `KBC_SKIP_VERIFY` ablation
  shows **>0 FAIL** on the same held-out battery where the full binary shows
  zero. If the ablation shows zero FAIL, C4 is falsified (the harness, not
  TNN, would be doing the verification).

**Verdict rule:** all three bars must PASS for the crew's headline claim
("deliberate practice installs a reliable KB-management skill") to be
declared. Any bar FAILED → headline claim rejected; report what the curve
actually showed.

## 9. Determinism and measurement integrity

- Zero RNG in all decision paths (operator, post-mortem, fixture builder,
  scorer). Byte-identical reruns: 50 sampled episodes run twice; SHA-256 of
  (trace + final image + lesson-memory delta) must match exactly.
- Learning-curve plot: collateral-episode rate and protocol-compliance rate
  per 10-episode window across the 260 training episodes, V1 vs NEG vs POS.
- Lesson-memory snapshots hashed every 20 episodes (shows *what* was
  learned and when the general lesson installed).
- No training on held-out geometries: overlap assertion script must pass
  before the battery runs.

## 10. Commit plan

1. This prereg **alone** → `docs/lab/knowledge/kb_control/crewC/PREREG_CREWC.md`.
2. After verdict: `kbc.zag` + glue + fixtures + `VERDICT_CREWC.md` (curve
   data, kill-bar results, lesson-memory history) → same directory.
   No binaries, no `.zagd` files, no `.zag-cache`.

## 11. Limits (not claimed)

- The store is a minimal model of the 1GB blob geometry (records, padding,
  chunking, slot table), not the production store; transfer to the real
  `s5_store`/`igb` machinery is crew B's lane.
- "Learning" here = deliberate memory agency (lesson install/strengthen via
  post-mortem), the program's established learning mechanism — not gradient
  or evolutionary methods.
- Micah's standing "test both" rule is honored via the NEG/POS/ablation
  controls rather than a second learner architecture; a competing
  architecture fork is out of scope for this crew.
