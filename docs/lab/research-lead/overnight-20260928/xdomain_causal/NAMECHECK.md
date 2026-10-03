# NAMECHECK: xdomain_causal (Cross-Domain Causal to Intervention Worker, RETRY-2)

## Step 0: Toolchain Guard (mandatory, executed first)

Worker executed at startup, 2026-10-02, before any research
computation:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty output before
"guard-check-done"). Safebin PATH active for all subsequent commands.
No forbidden executable was invoked at any point in this task. All
computation is pure Zag via the pinned znc
(`znc 2026.07.0-dev (edition 2026)`); shell used only to invoke znc,
run binaries, and for git/file ops.

## Step 1: Task Identity
- Worker: Cross-Domain Causal to Intervention (parent queue #2,
  GENERAL CROSS-DOMAIN COMPOSITION priority). RETRY-2 after daemon
  restarts.
- Mission: design the causal to intervention pair with the
  do-operator semantic gap; port XIO-general core verbatim
  (sha256-verified); test all four composition mechanisms (A, B, C,
  XIO-general); diagnose exactly where each fails and what the gap
  requires. 3/3 deterministic. Preregister before implementation.
- Verdict target: XDOMAIN-CAUSAL-COMPLETE (with gap diagnosis).

## Step 2: Commit-Order Self-Check
- PREREG.md committed ALONE in commit 2dc11c883 (2026-10-02),
  before any driver source existed. No implementation file predates
  it: cd_driver_*.zag, cd_full_*.zag, cd_bin_*, cd_run_*.txt were
  all created after the prereg commit (file mtimes 16:03+ vs prereg
  commit; `git log` shows PREREG.md as the first xdomain_causal
  commit).
- This NAMECHECK.md and REPORT.md are written after the runs.

## Step 3: Constraints Acknowledged
- Unfrozen only: all new files live in
  docs/lab/research-lead/overnight-20260928/xdomain_causal/.
  Frozen sources (composition_A, composition_B, composition_C,
  knowledge_composition, xio_general) read-only; concatenated, never
  edited.
- Pure Zag. Zero em/en dashes in worker-authored content
  (byte-verified with grep -P; clean).
- Paper untouched. Nothing pushed (local commits only).
- 0 modes / bridges / handlers / new core semantic cases.
- Explicit pathspecs for all git operations.

## Step 4: Port Fidelity (sha256, verified before and after assembly)

| Input file | sha256 |
|---|---|
| ../composition_A/cx_core.zag | dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6 |
| ../composition_A/cx_patch.zag | c7074c5928040014900f0a2eea8595f19074cfaf420b0632b2b8fd45977bcf12 |
| ../composition_B/cb_patch.zag | 1ffb8673c0e2ab8227fd9a242d308bc93af421bbd661f071ed02331e97a94244 |
| ../composition_C/cc_base.zag | dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6 |
| ../composition_C/cc_patch.zag | f7680504f19323c6f439d89aebbbbc1d7af3fcdded49094ae8bb3cae20e49a08 |
| ../xio_general/xio_core2.zag | 5c0413af9a67583a36e22b3f333a36b11e5938f5ad0dbc8e9079e2da04e9ebe9 |
| head -1567 ../knowledge_composition/kc_core.zag | 0e2cafe2e61952f3a715732adb2a8bdfdf5c3a2a9f4d331d576df8a24acb0ccd |

Assemblies (concatenation only):
- cd_full_a.zag = cx_core.zag + cx_patch.zag + cd_driver_a.zag
- cd_full_b.zag = kc_head (head -1567) + cb_patch.zag + cd_driver_b.zag
- cd_full_c.zag = cc_base.zag + cc_patch.zag + cd_driver_c.zag
- cd_full_xio.zag = cx_core.zag + xio_core2.zag + cd_driver_xio.zag
All four compiled with the pinned znc, warnings only, exit 0.

## Step 5: Build and Run Log
- cd_bin_a/b/c/xio built 2026-10-02; cd_compile_*.txt hold warnings.
- 12 runs total (3 per mechanism), all exit 0, each under 5 minutes.
- Determinism (sha256 of full run outputs):
  - A:   acf56c38678bfaaefefbaf61d60aa0e5459e1dd80dcd6e785bdc6f0c72e7712d (x3)
  - B:   a30dfaf94552a376c1066c0e5c836cf7e424953b8064d3089e436c46d7739281 (x3)
  - C:   fdf4ff51c39179ae14e4b0244ba56a54342040fcb69980c8aef25cef55ff4bbb (x3)
  - XIO: ab690089c8f5bc5d516024775c32ba507e8b9b8748e59145a27f52af2bf2659c (x3)

## Step 6: Kill-Bar Scorecard (all from cd_run_*1.txt; runs 2/3 identical)

- K1 COMPETENCE: TREAT X1=3, X2=6, Y1=1, Y2=2 on all four
  mechanisms (X1/Y1 via trial, X2/Y2 via rebind). PASS.
- K2 SURGERY-CASES-FAIL: TREAT Z1=-2, Z4=-2 on all four
  mechanisms; Z2=3, Z3=6 via rebind (predicted observational
  coincidence). Zero XIO-BUILD / CX-STAT / COMP-SEGS emissions in
  all 12 runs (grep count 0). PASS.
- K3 ABLATION: ABL-X all -2; ABL-Y Z1=-2,Z2=3,Z3=6,Z4=-2; FRESH
  all -2; on all four mechanisms. PASS.
- K4 ORACLE: 5, 3, 6, 4 on Z1..Z4 in every ORACLE arm. PASS.
- K5 XIO-DIAGNOSIS: AUDIT has_typed=0; GATE tried=0
  gate_rejected=12 (all MAPs sclass 0); stage(X,501)=3
  (confounded observational value); stage(Y,501)=515
  (relation-blind re-derivation); stage(X,515)=stage(Y,3)=
  -999999. PASS.
- K6 A-DIAGNOSIS: census contracts 4,4,3,3 (admitted); Z1=-2 with
  no CX-STAT; AUDIT npaths(3)=1 npaths(1)=1 (second stage has no
  plen-matching fact path). PASS.
- K7 B-DIAGNOSIS: co-use episode EP1=3, EP2=1, couse15=1 (>= 1
  type-15 edge); Z1 emits COMPOSE pairs=1 but ans=-2; no composite
  MAP promoted. PASS.
- K8 C-DIAGNOSIS: relseq [81,81,81] (X) and [88,88] (Y), non-empty;
  Z1/Z4 emit COMP-FAIL; DFS-PROBE (501,5)->-1, (501,3)->1 seg0=35,
  (502,4)->-1, (502,6)->1. PASS.
- K9 DETERMINISM: 3/3 byte-identical per mechanism (hashes above).
  PASS.

9/9 PASS. Verdict: XDOMAIN-CAUSAL-COMPLETE.

## Step 7: Standing Metrics
- New code: 4 drivers (~330 lines total), all unfrozen driver-level;
  mechanism cores byte-untouched (assembly by cat/head).
- Modes / bridges / handlers / new core semantic cases: 0/0/0/0.
- Cognition lines added: 0 to mechanisms; ~330 driver lines.
- Researcher-owned: world design (structural equation E=A+2C,
  confounded units, do-relations 93/94), drivers, arm definitions,
  B episode queries, oracle (ground-truth check).
- Learner-owned: all X/Y MAP graphs, rebind decisions, type-15 edge
  endpoints, trial verifies, all stage values.
- Paper untouched. Committed locally with explicit pathspecs;
  nothing pushed.
