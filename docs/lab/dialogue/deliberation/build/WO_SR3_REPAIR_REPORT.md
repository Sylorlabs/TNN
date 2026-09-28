# WO-SR-3 Repair Report: Dialogue-Deliberation Scale Crash (100x)

**Date:** 2026-09-27
**Work order:** WO-SR-3 (P0)
**Scope:** `docs/lab/dialogue/deliberation/` — the Round-4 dialogue deliberation binary

## Plain-English summary

The dialogue system crashed partway through its 100x scale test (900 dialogues).
White-box diagnosis found **two** fixed-capacity cliffs stacked on each other:

1. A 64 KB scratch area for word keys was never cleared between questions.
   Every dialogue leaked about 896 bytes, so it filled up and crashed at
   dialogue 74 (65,536 / 896 = 73.1 — the math predicted the crash exactly).
2. After fixing #1, a second cliff appeared: a 128 KB text buffer that saved
   every answer so it could fingerprint the whole run at the end. It filled
   up at dialogue 515.

Both were fixed with broad native repairs (no bigger buffers, no special
cases). The 100x test now runs all 900 dialogues cleanly, twice, with
byte-identical output and zero changed verdicts across all 3,800 turn
judgments.

## Before / after measurements

| Measurement | Before fix | After fix |
|---|---|---|
| 100x dialogues completed | 73 (crash at 74) | 900 / 900 |
| 100x exit code | 1 (panic) | 0 |
| 100x turn verdicts | 1,299 before crash | 3,800, 0 flips vs 1x twins |
| 100x determinism (2 runs) | n/a (crashed) | byte-identical SHA `4dfa50b0…` |
| 1x output vs official | — | byte-identical SHA `c22c908e…` |
| Key arena used after 900 dialogues | would-be 806 KB (crash at 73) | 820 bytes of 65,536 |
| Response fingerprint memory | 128 KB fixed buffer | O(1): 652 bytes streaming state |
| Allocator perturbation (`MALLOC_PERTURB_=165`) | — | byte-identical output |

## Root cause 1: key arena never reset

`keya` is a 65,536-byte arena holding two lifetimes of data: permanent fact
keys installed at startup, and temporary per-question keys appended while
parsing each query. The arena's "used" pointer was initialized once and never
moved back, so every question leaked its temporary keys permanently.

- Measured leak: ~896 bytes (224 keys) per dialogue.
- Cliff: 65,536 / 896 = 73.1 → deterministic panic on dialogue 74.
- Trace: keya used 812 → 1,708 → 2,604 … → 65,324 then panic.

**Fix (broad, not a bigger buffer):** after installing fact keys, record the
persistent end-offset in the arena's reserved header word `[4..8)`. Before
each of the three runtime query-parsing paths, reset the used pointer to that
base. Fact keys are untouched (their offsets live in the fact table); only the
transient region is reclaimed. Four insertion points total, all commented
`WO-SR-3`.

## Root cause 2: response accumulator (found by the first fix)

With the key arena fixed, the run proceeded to dialogue 515 and panicked
again. Debug instrumentation showed the key arena flat at ~824 bytes, but a
separate 128 KB buffer (`dacc`) — which concatenated every answer plus
newline so the program could hash the whole transcript once at the end — had
grown to 131,034 / 131,072 bytes. The first crash had masked this second
cliff.

**Fix (broad, not a bigger buffer):** replaced the fixed transcript buffer
with an incremental SHA-256 running in pure Zag (`sh_init` / `sh_update` /
`sh_compress` / `sh_final`). The compression loop mirrors the vendored R33
one-shot implementation exactly; constant strings are copied verbatim. Memory
is O(1) — 652 bytes of hash state (sh_h 64 + sh_k 512 + sh_b 64 + sh_n 8 +
sh_c 4) regardless of run length, plus a separate one-byte newline slice. The final digest
is bit-for-bit the same SHA-256 of the same byte stream, so the `DIGEST` line
is unchanged.

## Quirk found during repair (documented, replicated)

The legacy digest hashed `dacc[4..4+used]`, which runs **4 bytes past** the
last written byte (an off-by-four in the original). Those 4 bytes are
deterministically zero — proven by reconstructing sha256(1615 meaningful
bytes + 4 zeros) = the official digest `8c72590d…` exactly, with Python's
hashlib as oracle. The streaming code feeds 4 trailing zeros to replicate the
quirk, so the `DIGEST` line stays byte-identical. The quirk is commented
`WO-SR-3b` in the source.

## Verification

1. **1x regression:** rebuilt binary's 1x output is byte-identical to the
   official pre-fix output (SHA `c22c908e94a4b81ac9c32fefde4cbe5bcbba5e51bae2aeff6fadb300f7191599`).
2. **100x twice:** both runs rc=0, 900/900 dialogues, byte-identical stdout
   (SHA `4dfa50b00b9ba8ef6c67ee8f2d4422c19fbc2a5f42bf35d7f5904bb304ddee79`)
   and empty stderr.
3. **Zero flips:** all 3,800 turn verdicts (38 unique dialogue/turn/novel
   keys × 100 shards, including 500 novel-turn instances) match their 1x
   twins exactly.
4. **Streaming hash correctness:** standalone test — streaming("abc") with
   the 4-zero header prefix equals Python hashlib's
   `0a834ab0…6206a` and equals the one-shot `ns_sha256` on the same bytes.
5. **Allocator perturbation:** `MALLOC_PERTURB_=165` → byte-identical 1x
   output. The digest does not depend on heap garbage.
6. **Key arena bounded:** 820 bytes used after 900 dialogues (1.25% of the
   64 KB arena), flat — the leak is gone, not moved.

## Red team

- **Fact-key survival:** the reset only reclaims the transient region above
  the recorded base; fact-key offsets in the fact table are untouched. Proven
  behaviorally by 0 flips across 3,800 verdicts (every verdict depends on
  fact retrieval) and by the flat 820-byte arena (fact keys still resident).
- **No content-keyed cache / hardcode:** the diff is mechanical — 4 reset
  insertions + the streaming-hash functions. No lookup tables, no
  per-dialogue branches, no result memoization. The two 100x runs used the
  same binary on the same battery and agreed byte-for-byte; the 1x output
  matches the pre-fix binary built from different sources.
- **Digest vs external oracle:** the streaming implementation was verified
  against Python's hashlib on a known vector and against the one-shot
  `ns_sha256` on identical input before the 1x byte-identity check.
- **Long-query pressure (pre-existing limit, not a regression):** a single
  20 KB query panics with slice-index-out-of-bounds in the **original
  frozen binary**, the keya-only build, and the new build identically.
  Threshold is between 4 KB and 8 KB per query — a fixed query-parse buffer,
  unrelated to this scale fix (the scale battery's queries are all short
  dialogue turns). Documented here; not changed.
- **Digest quirk:** the off-by-four is replicated deliberately and
  documented, not silently "fixed," so the historical `DIGEST` values remain
  comparable.

## Honest scope

- The fix removes both capacity cliffs on the *dialogue-count* axis. A
  separate pre-existing per-*query* size limit (4–8 KB) remains; it is out of
  scope for WO-SR-3 and behaves identically before and after.
- The 128 KB transcript buffer is gone; the only O(n) memory left is the
  program's normal per-dialogue working state, which the 900-dialogue run
  proves bounded in practice.
- Verdict semantics are untouched: the 1x output is byte-identical, so every
  deliberation decision is exactly what the pre-fix binary produced.

## Files

- `deliberate.zag` — live source with both fixes (WO-SR-3, WO-SR-3b).
- `build/deliberate_r4_sr3fix.zag` — repaired frozen test copy used for the
  100x proof runs.
- `build/WO_SR3_REPAIR_REPORT.md` — this file.
