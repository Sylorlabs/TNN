# Hell-Hole Trial Phase-2 Contract

## Overview
Pure-Zag deterministic implementation of the TNN Internet Hell-Hole Trial Phase-2.
All epistemic decisions in Zag. No RNG. No timestamps in output.

## Components

### ht_read.zag — Stance Classifier
General deterministic English stance classifier.
- Input: claim text, result title, result snippet
- Output: 1=AFFIRM, 2=DENY, 0=IRRELEVANT
- Calibration: 34/40 = 85.0% on 2026-09-22 hand-labeled dev set
- See `calibration/report.tsv` for per-case predictions

### ht_sense2.zag — Sense-v2 Adapter
Adapter to real sense-v2 API (`ws2_sense.zag`).

**API:**
- `ht2_init(w, vp, lg, prev)` — Initialize session. Caller pre-allocates:
  - `w`: 1024 bytes as `*WsF`
  - `vp`: 256 bytes as `*WsV`
  - `lg`: 64 bytes as `*WsL`
  - `prev`: 32 bytes `[]u8` for ledger head
  - Wires mode 2 (READ-AND-EDITABLE), rule 1 (R-CORR)
- `ht2_begin(w, cand, searched)` — Begin fact cycle for candidate `cand` (0..18),
  with deterministic `searched` count from driver replay state.
- `ht2_add(w, cand, url, title, snippet, relevance, helper)` — Classify and ingest
  a result. Returns stance (1=AFFIRM, 2=DENY, 0=IRRELEVANT).
- `ht2_end(w, cand)` — Run sense decision, map to trial disposition.
  Returns: 2=INSTALL, 3=REJECT, 4=WITHHOLD, 5=REVISE. (6=CORRUPT reserved, never produced.)
- `ht2_deviation(w)` — Returns 1 if procedure deviation (sense 9 TAMPER or 10 WIRE_REFUSED).
- `ht2_head_hex(w)` — 64-char hex of ledger head.
- `ht2_ingest(w, cand, searched, url, title, snippet, relevance, helper)` — Convenience: begin+add+end.

**Candidate table (indices 0..18):**
- 0: C1 (known, trigger 3, prior P1)
- 1: C2 (unknown, trigger 1)
- 2: C3 (unknown, trigger 1)
- 3: C4 (unknown, trigger 1)
- 4: C14 (known, trigger 3, prior P2)
- 5: C5 (unknown, trigger 1)
- 6: C6 (unknown, trigger 1)
- 7: C7 (unknown, trigger 1)
- 8: C8 (unknown, trigger 1)
- 9: C9 (unknown, trigger 1)
- 10: C10 (unknown, trigger 1)
- 11: C11 (unknown, trigger 1)
- 12: C12 (unknown, trigger 1)
- 13: C13 (unknown, trigger 1)
- 14: C15 (unknown, trigger 1)
- 15: C16 (unknown, trigger 1)
- 16: A1 (known, trigger 3, prior P4, contra DENY)
- 17: A2 (known, trigger 3, prior P5, contra DENY)
- 18: A3 (known, trigger 3, prior P6, contra DENY)

**Disposition mapping (sense → trial):**
- Sense 1 (PROVISIONAL) or 6 (PROVISIONAL_MAJORITY):
  - chosen AFFIRM → INSTALL (2)
  - chosen DENY → REJECT (3)
  - else → WITHHOLD (4)
- Sense 0 (NO_SEARCH) or 2 (WITHHOLD) → WITHHOLD (4)
- Sense 5 (CONFIRM_INSTALLED) → INSTALL (2)
- Sense 4 (HOLD_INSTALLED):
  - REVISE (5) iff candidate contra-value has two distinct supporting domains
    (via `ws_domains2`)
  - else WITHHOLD (4)
- Sense 9 (TAMPER) or 10 (WIRE_REFUSED) → WITHHOLD (4) + procedure deviation flag
- Trial CORRUPT (6) reserved, never produced.

**Source-verified corrections:**
- `ws_result_hash` returns 64-byte lowercase hex. Pass directly to `ws_add_result`.
  Do NOT hex-encode a second time.
- Ledger head: read raw `w.*.lg.*.prev` (32 bytes), apply `ws_hex` once,
  return 64 lowercase hex chars.

**Known limitations:**
- The installed table (`w.*.inst`, WsT) is NOT initialized. A znc compiler bug
  miscompiles the `inst` field of the 19-field WsF struct; storing/reading
  `w.*.inst` corrupts the heap (variant of ZNC-2026-09-21-012). The trial's
  fact lifecycle (`ws_fact_begin`/`ws_add_result`/`ws_decide`) never reads
  `w.*.inst` — it uses `w.*.installed` ([]u8) for known facts. The P1-P6 prior
  table is therefore skipped; per-candidate installed values are set via
  `w.*.installed` in `ht2_begin`.
- Candidate claim/query strings are best-effort reconstructions, not the frozen
  originals. The exact 19 strings must be obtained from the task source and
  substituted before delivery.
- `ht2_init` takes pre-allocated substructs (znc bug: `nio_alloc` inside a
  function taking `*WsF` corrupts the session). Caller allocates in `main`.
- Returning `*WsF` from a function is broken in this znc build; use out-param
  initialization.

### ht_p2.zag — Session Driver
Entry points (via `argv[1]`):
- `init <session_dir> <arm>` — Emit SESSION_INIT event TSV.
- `next <session_dir>` — Emit single JSON line with next candidate.
- `observe <session_dir> <envelope-path>` — Ingest envelope, emit events + summary JSON.
- `consult <session_dir> <helper-path>` — Ingest helper response, emit events + summary.
- `replay <session_dir>` — Rebuild from envelopes, emit deterministic HTSV.
- `end <session_dir> <reason>` — Emit SESSION_END event. No sense operation.

**I/O:**
- Each field read capped at 16 KiB. Documented.
- Uses `nio_open_root`, `nio_open_child`, `nio_read_exact`.

**Event format (TSV):**
```
seq \t hash \t type \t k=v \t k=v ...
```
- `seq`: integer sequence number
- `hash`: 64-char hex SHA-256 of canonical form
- `type`: SESSION_INIT, QUERY_ISSUED, STANCE_RECORDED, TRIAL_DISPOSITION, SESSION_END, etc.
- `k=v`: lexicographically sorted by k, values HTSV-escaped

**Hash canonicalization:**
```
prior_hash + "\n" + type + "\n" + "k1=v1\n" + "k2=v2\n" + ...
```
- `prior_hash`: previous event's hash, or "GENESIS" for seq 0
- `type`: event type string
- `k=v` pairs: sorted lexicographically by k, values escaped, each followed by "\n"
- SHA-256 of the canonical bytes, hex-encoded lowercase

**HTSV escaping:**
- `\` → `\\`
- tab (0x09) → `\t`
- newline (0x0A) → `\n`
- CR (0x0D) → `\r`

**Summary JSON:**
- `observe`/`consult` output a final line starting with `{"disposition"`
- Example: `{"disposition":"WITHHOLD","consult":false}`
- Non-summary lines are treated as events by the supervisor.

## Determinism
- No RNG anywhere in AI decision paths.
- No timestamps in Zag output.
- No nondeterministic map iteration.
- `replay` must produce byte-identical output across runs.

## Calibration
- `calibration/report.tsv`: 40 cases, 34 correct (85.0%)
- 6 misses documented (see report)
- Classification performed in Zag via `ht_read.zag`

## Build
```bash
cd ~/workspace/ht_p2_work/build
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 ht_p2.zag -o ht_p2_bin
cp ht_p2_bin ~/workspace/ht_p2_work/ht_p2_bin
```
