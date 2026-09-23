# ARM X — Degenerate (whole stream / byte-level), family CTRL

## Mechanism (verbatim, frozen)

**"No chunking: whole stream as one unit (or byte-level addressing). The honest null arm."**

## Design

X ingests each corpus as a single monolithic unit. There is no chunking,
no ID→storage map, no index. The entire stream is one buffer; appends extend
it; recall slices by byte offset.

- **Unit ID:** pure arithmetic `(corpus << 24) | 0`. No persistent ID layer.
  M1 ID probe and M7 are N/A (with reread-byte footnotes).
- **Slots:** 2 monolithic slots (one per corpus in multi-corpus modes).
  Whole-stream units are never evicted; capacity does not bind.
- **Operations:**
  - `x_ingest`: store/replace the whole stream buffer.
  - `x_recall`: slice by offset (byte-level addressing).
  - `x_kill`: refused for sub-unit targets (reason 104); whole-unit kill
    would apply to the monolith.
  - `x_pin` / `x_weaken` / `x_revise`: act on the whole monolith.
  - `x_defect_content`: deterministic transforms (prose: every-7th-byte XOR;
    code: fixed same-length rename sequence).
- **BigBuf:** corpus storage striped across up to three ≤2^25-byte chunks,
  addressing the frozen toolchain's slice-indexing limit. Covers the ~95MB
  10x code stream.
- **Ledger:** 64-byte entries (16 words: op, slot, rc, b1..b5, a1..a5,
  stage@52, d1@56, d2@60). No pointers, no clocks.
- **M5:** retains actual corpus buffers in RAM so RSS reflects monolithic
  retention cost.
- **M8:** store image = concatenated slot arrays (1800 bytes); artifacts
  gate-compliant (store_hashes.txt, store_chain.txt, ledger.bin,
  ledger_chain.txt, alloc_trace.txt).

## Frozen literal readings (logged per the ambiguity rule)

- **M-3 (boundary fidelity):** whole-file blobs pass content but fail
  boundary by design. X reports M1/M2 boundary as `0.0`. This is not a bug;
  it is the frozen literal reading.
- **A18 (M3 valuable set):** the 1000-valuable schedule collapses to the
  2 whole-stream units that exist. `m3_valuable: 2` (actually marked).
- **M3 churn:** one growing whole-stream record receives 7,000 64-byte
  appends. All 3,000 sub-unit kill requests are refused (audited).
- **M4:** all 200 fixed-index defects target the same whole-stream ID.
  Boundary/content revisions preserve same-ID lineage. Kill rate 0.0
  (the monolith survives; kill-substitution false).
- **M7:** 500 lookups (not 5000; each X lookup scans the full 5.4MB stream
  with no index — 500 × 5.4MB = 2.7GB demonstrates the degenerate cost
  without a 45-minute run). M7 is N/A for X regardless; reread_bytes is
  informational.
- **M2:** episodes run for real (ingest + probe each episode). Criterion
  (recall ≥99.5% AND boundary ≥95% for 3 consecutive episodes) can never
  be met because boundary is 0.0 by design. ETC = 50+, censored. M9 shape
  "fast-then-flat" (takeoff 1, steepness 100.0, late gain 0.0) — instant
  memorization, no learning curve.

## Kill criterion A-44 (verbatim, frozen)

**"Floor bars (A-44): retired as candidate only if B2 ≥10× AND B5 ≥10×
(crew-4 battery). Universal floor rule text frozen at sign-off. If it
fires, the arm is KILLED — write the death certificate with evidence and
commit it. Dead arms die in public."**

Status: **DID NOT FIRE.** B2/B5 are Crew-4 battery metrics. X alone cannot
prove another arm is ≥10× better on both. No mapping from M1–M9 to B2/B5
was invented. The arm lives.

## Source layout

- `units/arms/X/cl/arm.zag` — one binary, `argv[1]` selects mode.
- `units/arms/X/substrate/` — R33_NATIVE_SHA256_V2, R33_NATIVE_IO_V1
  (byte-identical to B-64's copies).
- `units/arms/X/tools/scorecard_x.py` — assembler with arm label "x"
  (frozen `scorecard_assemble.py` hardcodes "b64"; not modified).

## Compiler

Frozen: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
