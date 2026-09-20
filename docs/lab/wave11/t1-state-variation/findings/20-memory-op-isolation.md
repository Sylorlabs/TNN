# Slice 20 — implementation-level isolation of memory ops (Track 1)

## 1. Slice
Slice 20: implement Slice 13's logical firewall as concrete module boundaries, an allowed call graph, and static enforcement in the Zag codebase.

## 2. Falsifiable claim
A static import-allowlist + call-site argument checker can guarantee that no memory-op, verdict, integrity-refusal, or ledger-write code path can call the variation function or feed judgment values into it — with 20/20 detection of planted violations, 0 false positives on the reference build, and byte-identical replay preserved with variation enabled.

## 3. Design
Module partition (five-organ layout, `docs/lab/wave9/integration/impl/`):
- `vary.zag` (NEW): pure deterministic variation fns, `vary_*` prefix only. Sole export: `vary_pick(digest:i32, tag:i32, n:i32) i32` — maps (state digest, expression tag, candidate count) to a candidate index. No mutation; imports only `substrate/cl/common.zag`.
- Memory-op implementers: `substrate/st_memory_core.zag` — the 30-op deliberate surface (`st_add/kill/pin/unpin/promote/demote/strengthen/weaken/overwrite/force_pin/...`, cf. `docs/lab/wave5/strength-trial-run/trial/st_memory_core.zag`). Sole legal home of `st_*`/`mem_*`.
- Judgment modules: `o1_memory.zag`, `o2_eliminate.zag`, `o3_consolidate.zag`, `o5_govern.zag` — verdicts, promotion decisions, structural revision, refusals. Never call vary.
- Constitution: `ledger.zag`, `substrate/o_audit.zag` — append-only; vary never writes.
- Expression surface (the ONLY vary callers): `o4_recall.zag` (phrasing/order/elaboration of composed traces) and the render tail of `loop.zag`.
- Digest source: new read-only accessor `st_state_digest(s:*StStore) i32` in `st_memory_core.zag`, hashing the FULL internal state (via the existing `R33_NATIVE_SHA256_V2.zag` the substrate already imports). This is the only value vary may consume — verdicts are ints, digests are ints, so the boundary is enforced by convention + checker (see below), implementing output = f(input, full state).

Allowed call graph (everything else forbidden):

```
main.zag -> loop.zag                       (phase sequencer)
loop.zag -> o1_memory, o2_eliminate,
            o3_consolidate, o5_govern      [judgment phase]
o1 / o3  -> substrate/st_memory_core.zag   [deliberate ops]
st_memory_core -> substrate/o_audit.zag,
                  ledger.zag               [append-only ledger]
---- PHASE SEAM: judgment+ledger freeze; digest taken ----
o1_memory -(read-only)-> st_state_digest() [full-state digest]
loop.zag [render tail] -> o4_recall.zag -> vary.zag   [variation phase]
vary.zag -> substrate/cl/common.zag ONLY
```

Enforcement (three layers):
1. **Compile-time import allowlist:** a static checker extending the no-RNG auditor parses bare `@import("...")` directives (bare-directive rule per AGENTS.md) and fails the build on any edge outside the graph — in BOTH directions: `vary.zag` may not import judgment/memory/ledger modules, and no judgment/memory/ledger module may import `vary.zag`.
2. **Call-site argument rule:** `vary_pick(`'s first argument must be `st_state_digest(` (or a variable assigned from it). A grep-checker verifies every call site; a verdict int passed as a digest fails the check and the review.
3. **Audit-time:** every vary call logs `(digest, tag, pick)` in the render log; replay-from-logged-state verification (law 2) turns any wiring leak into a byte-mismatch failure.

Where the firewall sits: at the **phase seam inside `loop_episode`** (runtime: all judgment and ledger appends complete before any vary call; vary reads only the frozen post-judgment digest) **plus** the **import-graph boundary** (compile-time). Either alone is defeasible — a runtime seam without import checks can be re-wired by a future builder; import checks without a runtime seam leak via shared mutable state. Both must hold.

Code-review checklist (any change touching either side):
1. New `vary_*` call site? Must live in `o4_recall.zag` or loop's render tail — else reject.
2. New import in/into `vary.zag`? Must be `common.zag` only — else reject.
3. Any `vary_` output reaching a `st_*` op, o2 verdict, o5 revision, or ledger append? Reject.
4. `vary_pick` first arg not `st_state_digest(`? Reject.
5. `loop_episode` reordered so a vary call precedes a judgment/ledger append? Reject.
6. Variation `(digest, tag, pick)` logged for replay? Required.
7. New memory op? Must live in `st_memory_core.zag`, follow the deliberate-op audit pattern, never call `vary_*`.

## 4. Kill bar
Prereg, evaluated on the reference build plus an adversarial wiring-probe trial:
- K1: checker catches <20/20 planted forbidden-edge/argument violations — dead.
- K2: checker false-positives on the clean reference build — dead (unusable).
- K3: 100-episode wiring-probe trial (10 probes routing vary outputs into memory ops / judgment values into vary): ≥1 probe alters a verdict, memory decision, refusal, or ledger entry vs the no-vary control — dead.
- K4: replay from logged full state with vary enabled is not byte-identical — dead (law 2).
- K5: any MUST-NOT field (verdict, memory decision, refusal, ledger bytes) differs between two runs at identical full state — dead.

## 5. Honesty notes
- This is a wiring guarantee, not a semantics guarantee: it stops accidental leakage, not a builder who deliberately renames modules to evade the checker. Enforcement is social + static, not cryptographic.
- Zag has no newtype to distinguish digest-vs-verdict ints (both i32); the digest-argument rule is convention + grep, not type-checked. A dedicated Digest struct alias would harden it (not yet verified against znc).
- Slice 13's logical design was not present in this workspace's findings dir at write time; this implements the brief's MAY/MUST-NOT split directly — reconcile with Slice 13 before building if it published a different logical split.
- Felt-intensity retirement (K4/K3', wave10) is respected: vary consumes only the state digest (store contents, strengths, stages), never a "feeling" value; no feeling machinery is reintroduced.
- Residual leak vector: shared mutable `StStore`. A judgment module could mutate state mid-render. Mitigated by the phase seam (judgment frozen before render) but rests on `loop.zag` discipline; a snapshot-freeze (`st_snap` before render, writes refused after) would harden it.
- Track 2's fenced RNG arm (AMENDMENT_2026-09-20_RNG_ARM_B.md) must live behind this firewall or stricter; this slice blesses no RNG in the canonical path.

## 6. Next build step
Build the import-allowlist checker as an extension of the no-RNG auditor, run it against the five-organ reference build (`docs/lab/wave9/integration/impl/`), then plant 20 forbidden-edge and 20 forbidden-argument violations and confirm 20/20 detection with 0 false positives — the cheapest test that can fire K1/K2 before any trial code is written.
