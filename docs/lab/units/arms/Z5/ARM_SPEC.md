# Z5 — Recipe IDs: Arm Specification

**Arm:** Z5  
**Name:** Recipe IDs  
**Family:** IDENT  
**Status:** Implementation in progress; this spec written 2026-09-21 AFTER source work had begun (see §12).

## 1. Corrections (coordinator-issued, binding)

1. The original dispatch labeled Z5 **“Chunk diff sync.”** That label was wrong and is **void**. Z5 is **Recipe IDs**. All “chunk diff sync” material (including the first implementation drafted in `cl/arm.zag`) has been discarded.

2. An earlier purported frozen §3 quotation circulated from memory was a paraphrase and is **void**. The only authoritative sources are:
   1. `units/arms/briefs/Z5.json` (the brief file),
   2. the byte-verified verbatim §3 row (frozen at `PREREG_FREEZE.md:523`),
   3. nothing else.

   The brief and the verbatim row were byte-compared on 2026-09-21 and agree. Had they disagreed, the build would have blocked.

## 2. Mechanism (from the brief, verbatim)

> `Identity = deterministic cut-program; spans re-derived per recall (fixed op set, fuel limits).`

Concretely: a Z5 identity is a **recipe** — a deterministic, preregistered cut-program. On recall the arm **re-runs the recipe against the current stream** and re-derives the span. No span is stored as the recall path. A stored last-known span exists **only** for logging, for the cached-span cost baseline, and for the loud-failure log artifact — it is never consulted by `z5_recall`.

## 3. Binding kill criterion (from the brief, verbatim)

> `>15% of recalls on the edit curriculum hit ambiguity or failure (loud failures count — the claim is stability, not honesty); OR recipe re-run cost > 50× cached-span recall at 10× scale — unaffordable online (survives only as ID-stability layer over cached spans, conceding the mechanism).`

Two independent kill bars:

- **K1 (stability):** On the binding edit curriculum (M4), if more than 15% of recalls hit ambiguity or failure — **loud failures count** — the arm is KILLED. The claim under test is stability, not honesty.
- **K2 (cost):** If recipe re-run cost exceeds **50×** the cached-span recall cost at 10× scale, the arm is KILLED as unaffordable online. It may survive only as an ID-stability layer over cached spans, which concedes the mechanism.

## 4. Recipe: fixed opcode set (preregistered, frozen)

The opcode set is fixed at preregistration. Extending it is a prereg amendment, not an implementation decision.

| Op | Code | Semantics |
|----|------|-----------|
| `OP_LINE` | 1 | The k-th line in the 64 KiB window whose first-word anchor equals the recipe anchor. |
| `OP_BLANK` | 2 | The k-th blank line in the 64 KiB window. |

**Anchor derivation** (deterministic, byte-level):
1. Strip the trailing newline; let `e` be the end.
2. Skip leading spaces (`0x20`) and tabs (`0x09`); let `p` be the first non-indent byte.
3. If `p >= e`, the line is **blank** → `OP_BLANK`.
4. Otherwise scan forward over non-alphanumeric bytes to the first `[A-Za-z0-9]` byte `q`.
5. If found, the anchor is the maximal `[A-Za-z0-9]` run starting at `q`, truncated to **12 bytes** (zero-padded).
6. If no alphanumeric byte exists, the anchor is the first 12 raw bytes after indentation (zero-padded) and the op is `OP_LINE`.

**Window:** `window = byte_offset / 65536`. The recipe is evaluated within exactly one 64 KiB window.

**k:** the occurrence index (0-based) of the matching `(op, anchor)` pair among lines in that window, in stream order.

## 5. Fuel limits (preregistered, frozen)

- A recipe re-run scans **at most one 64 KiB window**.
- Hard overrun guard: the scan aborts after `65536 + 4096` bytes (the extra 4096 covers a line straddling the window edge).
- Exceeding fuel, or finding no k-th match, is a **loud failure** (return code `-1`), logged with the recipe and the last-known span.

## 6. Identity encoding

`ID = FNV-1a-64(op ‖ anchor[12] ‖ k ‖ window ‖ corpus)` — a 64-bit recipe hash concatenated with the 32-bit corpus tag (the corpus tag occupies the high bits in the implementation’s `u64` key as `((corpus as u64) << 32) | fnv`).

- The FNV-1a-64 is computed over: 4-byte op, 12-byte anchor, 4-byte k, 4-byte window (little-endian), then mixed with the corpus tag.
- **Collision policy:** 64-bit IDs may theoretically collide. On ingest, if a newly derived ID equals an existing slot’s ID, the existing slot is reused (the recipe is identical, so the identity is identical). Distinct recipes that hash to the same 64-bit value would alias — this is accepted as a measured risk; the M8 store-hash would catch any nondeterminism arising from it, and no collision was observed on the r1 corpora.
- ID `0` is reserved as the empty sentinel in the ID→slot map and is remapped if derived.

## 7. Corpus / stream rules

Three corpora, each with a fixed tag; the tag is part of the recipe parameters and the ID:

| Corpus | Tag | File |
|--------|-----|------|
| prose | 1 | `prose.bin` |
| code | 2 | `code.bin` |
| fresh (churn) | 3 | `churn_fresh.bin` |
| t1_prose | 11 | `t1_prose.bin` |
| t1_code | 12 | `t1_code.bin` |
| t2_prose | 13 | `t2_prose.bin` |
| t2_code | 14 | `t2_code.bin` |
| t3 | 15 | `t3.bin` |

Recipes are always re-run against the **current stream of their own corpus**. There is no cross-corpus recall. Units are lines including the trailing newline (a final unterminated tail counts as a unit).

## 8. Ambiguity and failure (loud)

- **Ambiguity:** cannot occur by construction — `k` disambiguates identical `(op, anchor)` pairs, so the recipe always names exactly one line or fails.
- **Failure (loud):** the k-th match does not exist in the window (edits removed it, the anchor changed, or the window shifted). The recall returns `-1`, and the caller logs the recipe (op, anchor, k, window, corpus) plus the last-known span (offset/length). Killed IDs return `-2`; unknown IDs return `-3`.
- There is no silent fallback to the stored span. Ever.

## 9. Management operations (deliberate memory ops)

| Op | Effect |
|----|--------|
| `kill` | Sets `KILLED`, clears `LIVE`. All recalls fail loudly (`-2`). |
| `weaken` | Sets `WEAK`. Advisory only; recall unaffected. |
| `pin` | Sets `PIN`. Advisory only; recall unaffected. |
| `promote` / `valuable` | Sets `VALUABLE`. Advisory only; recall unaffected. |

Flags are stored per slot. Kill is the only op that changes recall behavior.

## 10. Edit curriculum (M4, binding)

- 100 boundary edits + 100 content edits, applied in one episode, positions derived deterministically from the corpus (every `n/100`-th line).
- **Boundary edits:** insert a 64-byte deterministic line before the target line (no RNG; bytes from a counter). Expected offsets after the edit shift by +64 for all later lines.
- **Content edits:** replace the first byte of the target line with `X`. This intentionally destroys the anchor for lines whose anchor starts at byte 0, exercising the loud-failure path.
- **Accounting:** after the edit, every ID is recalled against the edited stream. A recall counts as **failure** if the return code is negative OR the recalled bytes differ from the expected post-edit bytes at the expected post-edit offset. `fail_rate = failures / 200`. **Kill bar K1: fail_rate > 15% → KILLED.**
- Every loud failure appends `recipe=<op,anchor,k,win> last=<off,len>` to the M4 failure log artifact.

## 11. Cached-span baseline and cost ratio (K2)

- `z5_cached_recall` copies the stored last-known span: cost = span length in bytes. It is **never** used for battery metrics; it exists only for the K2 cost comparison.
- Cost accounting: `cost_recipe` = total bytes scanned by recipe re-runs (the `scanned` out-parameter); `cost_cached` = total span bytes. Ratio = `cost_recipe / cost_cached`.
- **Kill bar K2:** measured at 10× scale; ratio > 50 → KILLED (unaffordable online).

## 12. Build-process note (honesty)

The required pre-implementation `ARM_SPEC.md` was **not** written before coding began. The mechanism was preregistered in source comments, but the standalone spec document is being written after the implementation exists. This section records that fact so no reader infers the document predates the code.

## 13. Provisional items (PROVISIONAL-PENDING-FREEZE)

- **A15 M1 ID-swap probe:** 64 deterministic ID→slot remaps mid-trial (every `n/64`-th unit remaps its ID to the next slot). A remap counts as **pass** if the recall fails loudly (the recipe no longer resolves to the remapped slot) or returns exactly the other slot’s true bytes at its true offset. Any silent wrong-span return is a **fail**. Verdict `PASS` requires 64/64 passes with zero fails; otherwise `FAIL (side channel)`. The probe schedule (N=64) is provisional pending freeze.
- **M7:** C′ = every-100th unit of the surviving corpus with its first byte XORed `0xFF`; lookup schedule `(l*37) % nunits`; split 1666/1667/1667 across the three rounds. Bars: hit ≥ 90%, reuse ≥ 1.5, dedup ≥ 0.4. All provisional pending freeze.

## 14. Classification

Z5 is an **IDENT** (identity) arm: it answers “which unit is this” with a stable recipe-derived ID, not “what does it contain.” It is TNN’s candidate for the tokenization alternative’s identity layer: stability through positional insertions and content changes while the semantic locator (the anchor) survives.

## 15. Harness interface

One native binary, `argv[1]` selects the mode:

`m1-1x-prose | m1-1x-code | m2-t1-prose | m2-t1-code | m2-t2-prose | m2-t2-code | m2-t3-1x | m3-1x | m4-1x-prose | m4-1x-code | m5-1x | m5-baseline | m6-p2c-1x | m6-c2p-1x | m7-1x | m8-1x <outdir> <perturbation>`

`argv[2]` is the corpus root. M8 perturbations: `clean | frag | aslr | starve | freelist`.
