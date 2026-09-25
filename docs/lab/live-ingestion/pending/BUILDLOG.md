# BUILDLOG — Pending epistemic state implementation

**Date:** 2026-09-25 UTC  
**Task:** Build, test, document, and commit Micah's live-ingestion epistemic state:  
> Claims are **KEPT IN TNN as PENDING** until verified true, verified false, or directly tested.

## Artifacts

| File | Size | Purpose |
|------|------|---------|
| `impl/pending_track.zag` | 45,521 B | kpp_ pending-store library |
| `impl/pending_cmds.zag` | 35,516 B | kpc_/cmd_ command layer + hold intercept phase B |
| `impl/make_fork.py` | 8.5 KB | Fork generator (base + lib + cmds + surgical edits) |
| `impl/instrument_kbp.zag` | 168,900 B | Built fork (base + lib + cmds) |
| `impl/R33_NATIVE_IO_V1.zag` | 6,533 B | IO substrate (copied for @import resolution) |

**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`  
**Compiler SHA-256:** `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`  
**Fork base:** `~/workspace/tnn-lab/knowledge/web_guides/live_ingest/knowledge/sources/instrument_kb.zag`  
**Fork base SHA-256:** `d7ce44ffe8866f7fb5869250cfba40fcd8140e22eb79d4a23b773969dedede41`  
**Build:** EXIT 0, binary 530,572 B at `/tmp/kbp_test` (test only, not committed)

## Fork edits (via make_fork.py, all explicit string replaces)

1. **verdict_core signature:** Added trailing `hold_on:i32` parameter.
2. **Multihop UNKNOWN-path:** On success (`rc=1`), if `hold_on==1`, stages winning side's first page index in `o_widx`, sets `o_wn=1`, sets `rc=7` (instead of 1). Factual `ANSWER|` print suppressed via `hold_on==0` gate.
3. **Blind UNKNOWN-path:** If `hold_on==1`, returns 7 (instead of 1). `o_ans`/`o_widx` already staged. Factual print suppressed.
4. **G4 UNKNOWN-path:** If `hold_on==1`, sets `rc2=7` (instead of 1). Factual print suppressed.
5. **Calibration call sites (3):** Pass `hold_on=0` (frozen evidence byte-preserved).
6. **cmd_verdict:** Takes `hold_on:i32`, captures `vrc`, on `vrc==7` calls `kpp_hold_from_verdict` BEFORE freeing staged buffers, returns its result.
7. **main:** Reads `holdpolicy.txt` (default OFF) via `kpc_hold_on`, passes to `cmd_verdict`. Adds dispatch for `kbpend`, `kbhold`, `kbpendlist`, `kbcorroborate`, `kbtest`, `kbrefute`.

## IO corrections (from prior worker's findings)

1. **kpp_read_chunk:** Positional raw `read(2)` with EINTR retry. Replaces incorrect `nio_read_exact` usage in streaming loops (which seeks to start and reads entire file).
2. **kpp_write_chunked:** Splits output into ≤1 MiB `nio_write_all` calls (substrate limit).
3. **kpp_read_proc:** Sequential `read(2)` loop for `/proc/meminfo` (not a regular file; `nio_read_exact` refuses with -7401/-7403). Used by `kpp_budget` for the frozen MemAvailable measurement.

## Ambiguity resolutions (frozen prereg §4-§6)

- **kbpend arg order:** `kbpend <claims.txt> <state>` (frozen §4a).
- **kbtest arg order:** `kbtest <pending-seq> PASS|FAIL <proto-id> <state>` (frozen §5b).
- **Seq non-reuse:** New seqs use `max(pending_max, resolutions_max)+1` via `kpc_max_seq_ever` (frozen §6: "its seq is never reused").
- **Multihop host staging:** Winning side determined by `n2>n1` (win==e2 iff n2>n1); stages first page index of winning side's `widx` array.
- **HELD provenance host:** Lowercased when stored, for consistent comparison in guard 4.
- **Held claim validation:** Non-empty, ≤600 chars, no `|` (format integrity). Full PARSE gate not applied (claim is a frozen-pipeline best sentence).
- **kbhold syntax:** `kbhold <on|off> <state>` (state dir parallel to other commands).

## Structural guarantee: zero pending reads in verdict/recall

Grep for `pending.txt` in `instrument_kbp.zag` (16 matches):
- 6 in comments/header
- 10 in code, ALL inside `kpp_`/`kpc_`/`cmd_` pending-command functions:
  - `kpp_rewrite_pending`, `kpp_no_pending_launder`, `kpc_max_seq_ever`,
    `cmd_kbpend`, `cmd_kbpendlist`, `kpc_load_pending`, `kpp_hold_from_verdict`
- **ZERO** in `verdict_core`, `cmd_verdict` (verdict path), `cmd_query`, `cmd_select`, `kb_load`, `load_installed`

## Smoke test results (2026-09-25 UTC)

| Command | Result |
|---------|--------|
| `kbpend` | ✅ Accepts valid, rejects DUPLICATE-KNOWN, PARSE-gate all-or-nothing |
| `kbhold on/off` | ✅ Writes `HOLD\|ON`/`HOLD\|OFF`, prints `HOLD\|ON`/`HOLD\|OFF` |
| `kbpendlist` | ✅ Lists `PENDING\|<seq>\|<claim>\|<prov>` lines |
| `kbtest PASS` | ✅ Promotes: `PENDING\|PROMOTED\|1\|1`, `KB\|1\|<claim>`, `RESOLVE\|1\|KB\|TESTED\|<proto>` |
| `kbtest FAIL` | ✅ Demotes: `REJ\|1\|<claim>\|TEST-FAILED:<proto>`, `RESOLVE\|1\|REJ\|CONTRADICTED\|<proto>` |
| `kbrefute` | ✅ Demotes: `REJ\|1\|<claim>\|CONTRADICTED:<host>:<title>` |
| Seq non-reuse | ✅ After promote seq 1, new claim gets seq 2 |
| Budget init | ✅ `MEMAVAILABLE_KB\|666748`, `PENDING_BUDGET_BYTES\|10667968` |

## Battery defect found (HON cases)

**The battery's 8 HON cases do not satisfy the frozen AGREE-bind rule.**

The frozen KB §2 rule (prereg §5a): `AGREE = bind && fullcov && digits-equal`, where `fullcov` = every claim content token is prefix-matched by some sentence token.

Example hon-01:
- Claim: "The Golden Gate Bridge has a main span of 1280 meters."
- P2 sentence: "The main span of the Golden Gate Bridge measures 1280 meters."
- Claim token "has" is not prefix-matched by any sentence token ("measures" ≠ "has").
- Result: `bind=1, agree=0, contra=0` → `PENDING|ERROR|no-agree-bind` (correct per frozen rule).

The battery author (blind, per README) approximated AGREE as "token overlap >= 2/3, digits equal", omitting fullcov. The verifier (`verify_battery.py`) documents: "fullcov is not machine-checkable from the prereg text; paraphrases are authored tight."

**Impact:** P3 kill bar (8/8 HON promote) cannot pass with the frozen rule. Only hon-06 ("Pont du Gard") appears to satisfy fullcov. This is a battery authoring defect, not an implementation defect. The implementation follows the frozen prereg exactly.

**Recommendation:** Battery HON cases need re-authoring with tight paraphrases that preserve all content tokens (or the prereg needs amendment, which requires Micah's approval).

## Inherited state

- Prereg commit `22695f27b8132bab69ed3d753c4cee81b1b7a3d8` (frozen).
- Battery commit `0bd7985a49adb559cde5014737c23d6eb78668e4` (frozen, defective HON).
- Three prior implementation workers interrupted (daemon restarts); no prior implementation commit.
- Library `pending_track.zag` (1,109 lines) inherited from 22:20 UTC worker; IO defects patched locally.
- Command layer `pending_cmds.zag` written fresh 2026-09-25.

## Not yet done

- Full P1-P7 battery run (blocked by HON battery defect; other classes not yet run).
- Hold intercept end-to-end test (requires UNKNOWN-path verdict setup).
- CAP capacity test (requires 44MB budget fill).
- P6 determinism (two full passes).
- P7 KB1-KB5 regression.
- Repo commit (no local git repo; parent handles via API).
