# L3-SUF-1 NAMECHECK_BUILDER.md

**Role:** L3-SUF-1-BUILDER (worker, depth 2/2)  
**Date:** 2026-10-03  
**Prereg:** FROZEN at `6c70c3198` (PREREG.md, NAMECHECK.md NOT modified)

## Step 0: Toolchain Guard (per NAMECHECK.md)

**Safebin activation:**
- `export PATH="$HOME/safebin"` at startup.
- `command -v python3 python` returns nothing (verified 2026-10-03).
- `znc` 2026.07.0-dev works.

**Deviation:** `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh` referenced in NAMECHECK.md Step 0 does NOT exist in the repo. Safebin pre-exists at `~/safebin` with 49 tools including pinned znc. Builder used the pre-existing safebin; no Python was invoked.

**Pinned-znc workarounds honored (from AGENTS.md):**
- `_zag_malloc as *u8` + `[0..n]` alloc pattern; single output buffer + `_zag_raw_syscall` (no `_zag_print`).
- Shallow if-nesting (≤3); no `!(A && B)` in while; no `[]u8 as *u8`.
- u8-backed cells with little-endian pack/unpack (`ig`/`is`).

## Implementation

**Files:** `src/` (lane `docs/lab/research-lead/overnight-20260928/l3_suf_intermediate/src/`)
- `prelude.zag`: alloc, cells, emit, PRNG.
- `world.zag`: world interface + 8 builder-DEV worlds (W0, F-A…F-G).
- `learner1.zag`: consequence log, `l_surviving()`, flat forms, trace/proto, kb.
- `learner2.zag`: build_direct, probe, escalation, simplify, commit/defer.
- `learner3.zag`: arm pipeline (setup/try_commit/revise).
- `controls.zag`: C0 (ungraded), C1 (memorization), C3 (always-commit).
- `driver.zag`, `main.zag`: harness-scored stakes, bar evaluation.
- `build.sh`: compiles via `$HOME/safebin/znc`.

**Build:** `src/build.sh` → `src/build/suf` (264KB, pure Zag). Rebuild is byte-identical.

## Verification

**DEV battery (2026-10-03, `runs/dev_run7.log`):**
- GATE: PASS (C0 confidently wrong on W0/F-A/F-B/F-C).
- T0 (invent): PASS.
- T1 (active probing, RK-A retest): PASS.
- T2 (graded abstention, RK-B retest): PASS.
- T3 (poisoned reuse, RK-C retest): PASS (defer DATA-UNTRUSTED).
- T4 (reuse): PASS (ratio ok: 104 ≤ 208/2).
- T5 (recode transfer): PASS (part=1, bars=1).
- T6 (revision): PASS.
- T7 (retirement): PASS.
- Controls: C0/C1/C3 behave as specified.
- SUF-K1..K12 + KC0A..D: K2,K3,K5,K6,K7,K8,K9,K11 PASS; K1,K4,K10,K12 PENDING (audit/adversary); KC0B,KC0D PASS; KC0A PENDING; KC0C PENDING (adversary).

**Determinism:** 3/3 byte-identical runs verified (`cmp`, sha256).

## Code freeze

**Commit:** (pending - builder to commit with explicit pathspecs, local only)  
**Files frozen:** `src/*.zag`, `src/build.sh`, `CODEFREEZE.md`, `NAMECHECK_BUILDER.md`, `REPORT.md`.

## Handoff

Builder complete. Handoff package for adversary (frozen world interface in CODEFREEZE.md) and red-team (A-LIT/A-TRACE/A-SEARCH/A-TRIGGER/A-INFO/A-ORDER). Builder does NOT design sealed worlds or red-team.
