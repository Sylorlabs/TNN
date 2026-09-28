# H5 Deliberation Harness — `delib_harness` (Crew 2, Phase 1)

Pure-Zag deliberative judge harness. Reads judgment items (JSONL) + a depth
config, runs a real deliberative judgment procedure per item at the configured
depth (fixed SHALLOW, fixed DEEP, or state-ADAPTIVE), and emits per-item
results plus a SHA256-chained audit ledger of every deliberation step.

Status: Phase 1 — build + determinism proven on the tiny smoke battery only.
The full measurement matrix runs only after the coordinator confirms the
prereg freeze. **Do not run the battery at scale from this directory.**

## Layout

| File | Role |
|---|---|
| `delib_harness.zag` | `main` + run driver: arg handling, file IO, per-line dispatch, results emission |
| `dlb_delib.zag` | the deliberation procedure (genuine mechanism, §2) |
| `dlb_json.zag` | minimal JSON parser for item lines → `Item` struct |
| `dlb_cfg.zag` | depth-config (`key=value`) parser → `DCfg` struct |
| `dlb_ledger.zag` | SHA256-chained audit ledger |
| `dlb_util.zag` | arenas, output buffers, file read/write, string helpers |
| `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` | lab substrate copies (SHA256, syscalls) |
| `build.sh` | builds `./delib_harness` with the pinned znc (binary is scratch-only, never committed) |
| `run_determinism.sh` | Phase-1 determinism proof; writes `DETERMINISM_LOG.txt` |
| `smoke_items.jsonl` | 6-item smoke battery (2 admit, 2 revoke, 2 logic) |
| `smoke_{shallow,deep,adaptive}.cfg` | smoke depth configs |
| `CONFIG_FORMAT.md` | depth-config format (the parametric interface) |
| `ITEM_FORMAT.md` | item JSONL schema, caps, honest-scope note |
| `DETERMINISM.md` + `DETERMINISM_LOG.txt` | determinism proof |

## 1. Usage

```
./build.sh
./delib_harness <items.jsonl> <depth.cfg> <results.jsonl> <ledger.jsonl>
```

`results.jsonl` — one JSON object per item:

```json
{"id":"S4","task_type":"revoke","verdict":"H-KEEP","confidence":1000,
 "rounds_used":4,"evidence_consumed":4,"ground_truth":"H-KEEP","correct":1,
 "ledger_first":36,"ledger_last":48,
 "ledger_head":"7af909de6ead..."}
```

Malformed lines produce `{"line":N,"error":"E_PARSE_<code>"}` and do not abort
the run. Exit code: 0 = all clean; N>0 = N item errors; 101 = config error;
102 = IO error; 103 = ledger/write error.

`ledger.jsonl` — one JSON object per deliberation step, hash-chained:

```json
{"seq":44,"item":"S4","round":3,"action":"TEST",
 "detail":"h=H-REVOKE refuted w=650",
 "prev":"0bda4c188cc0...","hash":"eefb867fbf6c..."}
```

`hash = SHA256(prev_raw_32B || "<seq>|<item>|<round>|<action>|<detail>")`,
genesis `prev` = 32 zero bytes. Step 0 is `GENESIS`, step 1 is `CONFIG`
(canonical config summary, so the chain commits to the config too), then per
item: `BEGIN`, then per round `EVIDENCE` / `ELIMINATE` / `TEST` / `ROUND`, then
`VERDICT`. A separate Python checker re-derived all 18 smoke verdicts and
reverified every ledger hash chain — 0 mismatches.

## 2. The deliberation procedure (the genuine mechanism)

State per item: fixed-point (thousandths, i64) scores per hypothesis, an
alive-set, consumed-evidence count, and per-round leader/margin history.
Nothing is a stub: every round really does the work below.

Each round, in order:

1. **Natural stop (pre-round):** if no evidence remains (or cap reached) and
   ≤1 hypothesis is alive, stop — there is nothing left to deliberate.
2. **EVIDENCE** (if any remains): consume the next evidence item in payload
   order; add its `supports` weights and subtract its `attacks` weights for
   all *alive* hypotheses (dead hypotheses' scores are frozen).
3. **ELIMINATE:** drop every alive hypothesis trailing the leader by
   ≥ `elim_margin` (leader immune; ties → lowest hypothesis index).
4. **TEST:** take the runner-up (highest-scoring alive non-leader) and attempt
   refutation — scan consumed evidence for an attack on it with weight
   ≥ `refute_threshold`. A hit eliminates it (`refuted w=<n>`); a miss is
   recorded (`holds`). This is a deliberate hypothesis-testing action, not
   just re-scoring.
5. **ROUND:** recompute leader/margin; confidence = 1000 if a single hypothesis
   remains, else `clamp(margin, 0, 1000)`.
6. **STOP** if any fires:
   - fixed modes: `rounds >= shallow_rounds` / `deep_rounds`;
   - adaptive (DEPTH_DEF §6 verbatim, §12 amendment): `rounds >=
     adaptive_max_rounds` (recorded as `cap=1` in the VERDICT detail), or
     (`rounds >= k` where `k = adaptive_min_rounds`, and every one of the
     last `k` per-round absolute confidence gains
     `g_i = |c_i - c_{i-1}|` (with `c_0 := c_1`) is `< epsilon`).
     Confidence drops never count as settled. `conf_threshold` and
     `stability_window` are still required config keys but are ignored
     by the §6 rule.
   - the round changed nothing (no evidence consumed, no elimination).

Verdict = surviving leader's hypothesis id; confidence as above. Zero RNG, no
timestamps, no PIDs; evidence order is payload order; every tie breaks to the
lowest index. The same item + config always yields the same verdict,
confidence, rounds, evidence count, and ledger bytes.

**Honest scope:** the harness does not parse natural language. The battery
crew pre-encodes premises/observations as weighted evidence links
(`supports`/`attacks` over named hypotheses). The genuine, tested machinery is
the eliminative deliberation loop — evidence gathering, hypothesis
consideration/elimination, refutation testing, confidence, and the stopping
rule — not NLP.

## 3. Determinism

`run_determinism.sh`: rebuilds from source, runs the 6-item smoke battery
twice under each of the three configs, `cmp`s results and ledgers, checks the
error path (malformed line) twice, and records SHA256s. Result 2026-09-23:
**PASS — all cmp clean**, including byte-identical binary rebuilds.
Smoke accuracy (sanity only, not gated): shallow 5/6, deep 6/6, adaptive 6/6 —
the shallow miss (S4) is by design: two rounds cannot reach the decisive
refutation evidence, which is exactly the depth effect H5 will measure.

## 4. Parametric interface (Crew 1 coordination)

Crew 1's frozen spec (`docs/lab/deliberation_depth/DEPTH_DEF.md`) had not
landed when this harness was built. The harness is parametric: **every**
numeric knob of the deliberation procedure comes from the depth-config file
(see `CONFIG_FORMAT.md`); no depth numbers are hardcoded. Mode names are
`shallow` / `deep` / `adaptive`, matching the brief. If the frozen spec renames
keys, a thin rename shim will be added — the procedure itself needs no change.

## 5. znc notes (applied from AGENTS.md)

- Struct literals use `.field=` syntax (bare `field=` fails to parse).
- No `[]u8` slice `==`; all string compares via `nio_equal`.
- All indexed numeric tables live in `[]u8` arenas with explicit
  little-endian accessors (ZNC-2026-09-21-007 `as []i32` aliasing bug).
- Struct fields touched only through `*T` function parameters (ZNC-004/010).
- `nio_alloc` zeroes; arenas explicitly re-zeroed per item.
- No single allocation near the 2^25-byte slice-index limit (largest: 8MB ledger buffer).
- `_zag_arg` slices never freed; no `try` identifier; no `};`; nesting ≤4.
- Build with `--no-zagd --no-analyze --no-foreground-cache`; no `.zagd`,
  no binaries committed. `/tmp` is a full 512MB tmpfs — battery workdirs stay
  out of it.
