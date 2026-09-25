# VERDICT_R4 — Mechanical Recovery for Poisoned Subjects (+ no-stupid-limits repair)

**Status: PASS — all 8 frozen kill bars met.** Residual #4 of the integrated
one-brain + self-PAM composition red-team (finding F4), finished by the fifth
R4 crew (fourth resume) on 2026-09-25.

**Frozen prereg:** `docs/lab/onebrain/pam_integration/repairs/R4/PREREG_R4.md`
(also `~/workspace/ob_pam_repairs/R4/PREREG_R4.md`). Kill bars below are
extracted from PREREG_R4.md §2 — the only source.

## What was built

`M_REVISE=113` (overseer-only, routed through the N-AUTH choke points in
`sp_gate_one`, append-only revision rows, effective store rewrites superseded
`|EXT` → inert `|SUP`) — implemented identically in `build/src`,
`longhorizon/src`, `redteam/src` (`sp_gate.zag` SHA-256
`0fa841f7b9ec4904b04ec424ff047ef188e69c3b797eaa4f9756ff5cd9d14a06` in all
three trees).

## Directed deviation from the frozen prereg text

The frozen prereg §1.2 specified the revision table as "64 rows × 16 bytes"
and §1.3.8 as "(cap 64 → SP_R_REV_CAP fail-closed)". The parent task for this
resume directed the **deletion of that arbitrary cap** as the remaining law
violation (Micah's standing no-stupid-limits law; cf. the committed R2
chunked-storage repair). The change is semantically exact:

- Revision rows now live in physically-chunked, logically-unbounded storage:
  65536 rows/chunk × 16 B/row → 1,048,584 B/chunk, strictly under znc's
  genuine 2^25-byte (33,554,432) slice ceiling (load-bearing limit).
  Chunks allocated on demand, chained via 8-byte headers; chunk pointers
  ride the flat gate arena as i64 words (same shape as the committed R2 repair).
- Append order = row index order → newest-row (latest-wins) semantics,
  `chain_prev` audit chains, and the effective-store `|SUP` rewrite are
  unchanged. All 7 warrant checks stay in prereg order; the cap check is gone.
- `sp_rev_cycle`'s walk bound changed from `hops<=SP_REV_CAP` to `hops<=n`
  (n = live row count): data-derived, not arbitrary — n+1 hops among n rows
  force a repeated row by pigeonhole, i.e. a periodic walk that can never
  reach the target, so over-long walks still fail closed (refuse).
- `SP_R_REV_CAP=15` is kept as a reserved ledger code (now unused; commented).
- `redteam/src/ob_test_redteam.zag`: two mechanical accessor updates in
  `rt_r4_revise` Gate B (flat-arena `ob_g32(g2,G_REV+1*16+4/12)` reads →
  `sp_rev_get(g2,1,1)` / `sp_rev_get(g2,1,3)` — identical row/field values),
  plus the new `rt_r4_uncapped` probe (100 revisions past the old cap).
  This bends the prereg test plan's "existing attack functions byte-untouched"
  for exactly these two lines; every check name, value, and expectation is
  unchanged.

No frozen kill bar references the 64-row cap; all 8 are satisfiable — and
satisfied — without it.

## Kill-bar accounting (from PREREG_R4.md §2)

| Bar | Result |
|---|---|
| **K1** — Poisoned subject → legitimate overseer `M_REVISE(S=NEG,E=POS)` → warranted POS INSTALLS (`disp=SP_INSTALL`, `reason=SP_R_OK`, `fwd=1`), exactly one `SP_L_REVISE{ep,S,E}` row | **PASS** — `r4v_k1_applied,1,1`, `r4v_k1_pos_install,1,1`, `r4v_k1_pos_fwd,1,1`, `r4v_k1_pos_reason,0,0`, `r4v_k1_ledgered` +1 |
| **K2** — non-overseer `M_REVISE` (valid N-AUTH) → REFUSED (`SP_WITHHOLD`, `SP_R_UNAUTH`; no row; poison still withholds) | **PASS** — `r4v_k2_refused`, `r4v_k2_reason,9,9`, `r4v_k2_no_row`, `r4v_k2_still_poisoned` |
| **K3** — `M_REVISE` without cited superseding evidence → REFUSED, all four sub-cases | **PASS** — (a) `r4v_k3a_reason,12,12` (b) `r4v_k3b_reason,12,12` (c) `r4v_k3c_reason,13,13` (d) `r4v_k3d_reason,11,11` + out-of-range `k3e1/k3e2` |
| **K4** — revised-away falsehood re-emitted → WITHHOLD; `M_REVISE` citing the dead line → REFUSED `SP_R_REV_BAD_EVIDENCE` | **PASS** — `r4v_k4_neg_withhold`, `r4v_k4_neg_reason,2,2` (CONTRADICTED), `r4v_k4_dead_evidence,12,12`, `r4v_k4_self_cycle,14,14` |
| **K5** — machine-checked ledger audit: `SP_L_REVISE` count == applied; one row per applied revision; `SP_L_REV_REFUSED` count == refused with reason in `a2`; store text still carries original `\|EXT` lines (raw suffix check) | **PASS** — `r4v_k5_revise_n,1,1`, `r4v_k5_refused_n,9,9`, `r4v_k5_store_unmutated,1,1` (×2 lines) |
| **K6** — no revision → poisoned-subject sequence withholds as frozen refs; pre-revision section byte-identical (`rf_f4_*` + `RT_FINDING F4-POISON-FREEZE`) | **PASS** — new output's pre-revision section (218 lines) byte-identical to the pre-change binary's section (captured 2026-09-25 pre-edit; itself byte-identical to the Sep-24 `run2.out` section) |
| **K7** — long-horizon T1–T5 unchanged vs frozen refs | **PASS** — `ob_lh_bal` 3/3 `cc7e86ed4a00be36bb4f5a2aacc6456197281270b4eb40717ebb1ca017ea93e9`, `ob_lh_int` 3/3 `356b7873bf07942c6b2283ed087911d3bfa724cea1ab707fb1ccaf14821cec3b`; the only battery delta vs the frozen tree is the R4 recovery probes in the redteam battery |
| **K8** — zero RNG in decision paths; all batteries 3x byte-identical | **PASS** — grep `rand\|srand\|random\|lcg\|entropy\|_zag_random` over all three `src/` trees: 0 hits; smoke 3/3, redteam 3/3, LH 3/3+3/3 byte-identical |

## Beyond-64 demonstration (the cap-removal proof)

New `rt_r4_uncapped` probe (battery tail, after `rt_r4_revise` — K6 section untouched):

- 100 overseer `M_REVISE` rows applied on one gate (pairs `u0..u99`,
  S=NEG-line, E=POS-line): all 100 `disp=SP_INSTALL`, `reason=SP_R_REVISE_OK`.
- `G_REV_N=100`, `SP_L_REVISE` ledger count = 100, `SP_L_REV_REFUSED` = 0 —
  no silent drops, no refusals.
- Read-back past the old cap: row 64 = {S:141, E:140}, row 99 = {S:211, E:210},
  row 0 `chain_prev` = -1 — rows are really stored, not dropped.
- Supersession holds for beyond-cap targets (`sp_superseded(141)=1`);
  effective store renders line 211 `|SUP` (inert) and line 210 `|EXT` (live).
- End-to-end: warranted `u99|POS` claim INSTALLS through the normal
  draft→verdict path (`disp=SP_INSTALL`, `fwd=1`, `reason=SP_R_OK`); the
  revised-away `u99|NEG` falsehood re-emitted WITHHOLDS `CONTRADICTED`.
- `RT_FINDING,R4-UNCAPPED,100-revisions-past-old-cap-readback-clean`.

## Evidence

- `evidence/smoke/run{1,2,3}.out` — 3/3 SHA
  `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`
  (reproduces the inherited pre-change SHA exactly), `OB_FAILURES,0`, zero stderr.
- `evidence/redteam/run{1,2,3}.out` — 3/3 byte-identical, `RT_FAILURES,0`,
  `RT_K3_HITS,0`, zero stderr. (SHA recorded in `*.sha256`.)
- `evidence/longhorizon/ob_lh_bal_run{1,2,3}.out` + `ob_lh_int_run{1,2,3}.out`
  — 3/3 byte-identical each, frozen-ref SHAs above, `OB_FAILURES,0`.
- `RUNLOG.md` (workdir) records inherited state, the change, and every battery result.

## Residuals

None open on R4. The repair is complete and committed on `tnn-native-lab`.
Ready for the merged R1–R4 tree.
