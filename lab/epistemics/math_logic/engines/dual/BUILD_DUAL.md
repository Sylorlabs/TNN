# DUAL ENGINE — Build Report

## Source files (committed)
- `engines/dual/dual.zag` — DUAL main (D + R, D↔R interface, 3x determinism).
- Uses `engines/common/*` (shared with ONE) + verbatim
  `deliberation_depth/harness/dlb_delib.zag` (real H5, not a stub).

## D (Deriver)
- Forward sweep: shared `one_mp/one_ui/one_pbc_direct`, BFS bound 3, no
  goal, no subproofs. (Same committed schemas, same match-and-bind.)
- Backward chaining on R directive (bound 8):
  - S_MP backward: consequent==goal → prove antecedent at depth-1.
  - S_UI backward: `cx_match_bvar` (binder as bindable variable).
  - S_PBC backward: subproof (assume not(goal), forward-BFS for false).
- D→R: claim indices + depths + complete audit chains.

## R (Referee) — real H5 via verbatim dlb_delib.zag
- Hypotheses: H0=WITHHELD (index 0, wins ties), H1=target, H2=not(target).
- R→D directives: `derive T to depth 8`, `derive not(T) to depth 8`, ordered
  lowest-preliminary-confidence-first (deterministic; tie → T first).
- **Frozen evidence rubric** (audited under KB4):
  - T derived at depth d → E_T supports H1 w=W(d), attacks H2 w=W(d).
  - not(T) derived at depth d → E_N supports H2 w=W(d), attacks H1 w=W(d).
  - false derived at depth d → E_F supports H0 w=1000, attacks H1/H2 w=1000.
  - W(d) = 1000/(1+d), min 1.
  - No evidence → H0 wins by lowest-index tie-break (R owns WITHHELD).
- **Frozen R config**: mode=1, shallow_rounds=1, deep_rounds=12, amin=1,
  amax=12, conf_thr=100, stab_win=2, eps=1, elim_margin=150, refute_thr=500,
  evcap=128.
- Verdict: leader==1 → DERIVED (conf=st.conf); leader==2 → REFUTED
  (conf=st.conf); leader==0 → WITHHELD (conf=0).
- Output labels D_STEPS and R_STEPS separately.

## Build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- CWD must be `engines/dual` (imports resolve relative to CWD).
- Command: `znc_linux_x86_64_abed8aa1 dual.zag --no-zagd --no-analyze --no-foreground-cache -o dual_bin`
- Pure Zag, zero RNG. 3x in-process reruns, byte-identical asserted.

## Smoke results (2026-09-25)
- P01-FORMAL: DERIVED, conf=1000 (R leader=H1).
- SMOKE01: DERIVED conf=1000. SMOKE02: WITHHELD conf=0 (H0 wins tie).
  SMOKE03: REFUTED conf=1000. SMOKE04: DERIVED conf=1000.
- Sealed guard: exit 3.
