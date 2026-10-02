# F-INT4 Level 1 Strengthening Report

Date: 2026-09-30. Worker: F-INT4 Level 1 Strengthening.
Status: FINT4-L1-PASS.
Source: F-INT4 disposition `86518edc4` (Level 1 recommendation).

## What was done

Built a standalone Level 1 strengthened XCAP test from a copy of the
TNN-1 source (`tnn1_l1.zag` in this directory; the TNN-1 build itself
was not modified). The Level 1 test (`t_xcap_l1`) replaces the
synthetic guide node with the real MAP node created by `promote_map`
inside `mp_run` during `ev_query` on a query miss.

Key implementation points:

- `newest_map` scans the workspace for the most recently promoted
  T_MAP node (type 20, highest field-24 promotion clock).
- The test teaches the same chain as the original `t_xcap`, runs
  `ev_query(W,101,40,201,0)`, verifies the answer is 201, then locates
  the real MAP node.
- Sanity check: the genuine promoted MAP has positive bid (it carries
  type-2 and type-6 self-edges from `promote_map`).
- `contradict_map` is applied to the real node. Both `map_standing`
  and `bid` are read before and after.

## Bar design note (honest deviation from the literal disposition)

The disposition suggested verifying "both `map_standing` and `bid`
demote." On a real promoted MAP node, `map_standing` starts at +1 or
higher (the promotion's own type-2 self-edge counts), so the original
test's absolute `st<0` bar is not the right observable. The Level 1
test instead verifies strict demotion: `st1<st0` and `b1<b0`. This is
the honest measure of "contradiction demotes both metrics" on the real
artifact, and it is a stronger property than the synthetic test's
absolute threshold (which started from a manually zeroed standing).

## Results

- XCAP-orig (original synthetic test): PASS.
- XCAP-L1 (real MAP node, strict demotion): PASS.
- L1-TOTAL: 2/2.
- Determinism: 3/3 runs byte-identical
  (sha256 `8842de4bc4d40d3d68973947b97a79684907e9dca78149d201eea0e7b8d20235`).

## What this establishes

The narrowed claim from the disposition is now demonstrated on the
real artifact of the query-miss path, not a synthetic simulation: a
CONTRADICTS edge against a genuine query-built MAP node demotes both
its query-path standing (`map_standing`) and its action-path candidacy
(`bid`), confirming the CAM-1 and ACT subsystems read and write the
same edge state on the same node.

## What this does not establish

Plan-to-guide conversion (ACT selecting a query-built MAP as a guide)
remains not demonstrated. No MAP-to-guide registration mechanism
exists in TNN-1 (per the disposition). This Level 1 result supports
the narrowed claim only.

## Governance

- Zero Python invocations. Pure Zag via the pinned compiler
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`. Build warnings only
  (A0102, non-blocking; same class as the original build).
- TNN-1 source inspected read-only; the test was built from a copy in
  the owned directory. The TNN-1 build was not modified.
- No em dashes in wave files (byte-verified before commit).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff
  verified before and after commit.
- No sealed FW1-FW9 files accessed.
- Explicit pathspecs on commit.

## Files

- `tnn1_l1.zag`: TNN-1 source copy plus `newest_map`, `t_xcap_l1`,
  and `run_l1` entry point. Build artifact `tnn1_l1_bin` not committed.
- `NAMECHECK.md`: Step 0 guard record.
- `FINT4_L1_REPORT.md`: this file.
