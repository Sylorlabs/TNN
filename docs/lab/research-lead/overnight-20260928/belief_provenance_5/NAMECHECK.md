# NAMECHECK: BELIEF-PROVENANCE 5 (open dynamics)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_5/`
Worker: BELIEF-PROVENANCE-5 subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-5: the open dynamics
from the BP-4 suggested-next list. All 7 falsifiable
predictions (FP1-FP7) are sealed by BP-2/BP-3/BP-4; this
lane does not re-open them. Non-ledger task; nothing
minted.

## Step 0: toolchain guard (recorded before any implementation)

- Safebin: `~/safebin` provisioned with the 36 allowed
  tools. `export PATH="$HOME/safebin"` held for the whole
  session.
- `which python3` returns NOTHING under the safebin PATH.
- `which python` returns NOTHING under the safebin PATH.
- znc resolves via the safebin symlink to the pinned
  toolchain
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (builds invoked by absolute path; verified present
  2026-10-03).
- Shell used only for: znc invocation, binary execution,
  git ops, file movement, sha256 checks. All scientific
  computation in pure Zag.
- Pre-prereg exploratory probes ran in /tmp/bp5probe
  (ephemeral, never committed): ev_observe type-7/type-3
  evidence edges, t2_revise_graph success on the
  chain-graph shape and revert on count/rootless shapes,
  activate() max-bid determinism. Probes established
  what is testable; all predicted numbers in PREREG.md
  are hand-derived from the frozen R1-R7 forms.
- Git discipline: explicit pathspecs only; commits local,
  never push; never `git reset`; never amend shared
  history; never modify other lanes. This worker touches
  only
  `docs/lab/research-lead/overnight-20260928/belief_provenance_5/`.
  If git writes fail with EPERM through the safebin
  symlink, retry via `/usr/bin/git` directly (per
  AGENTS.md lesson 2026-10-03); on index.lock
  contention, retry with sleep backoff, never remove the
  lock.
- Zag pitfalls honored: u8-backed belief state with
  direct index access (no `as *i32` + slice construction
  in functions); output through the frozen block's
  existing emit/e64 helpers; no reliance on `.len` of
  casts; `if` nesting at most 3; no `!(A && B)` in while
  conditions (De Morgan form); `[]u8 as *u8` never used.
- No em/en dashes in any lane file (byte-verified with
  grep before each commit).
- Frozen block reuse: `xf_block.zag` (the patched
  XHIER-COUNTMAP-FIX block) is concatenated VERBATIM as
  the base of `bp5_full.zag`; its SHA-256 is recorded in
  the prereg and re-verified before and after the build:
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
- Belief layer reuse: BP-4's `bp4_learner.zag` is copied
  VERBATIM to `bp5_learner.zag` (hash re-verified):
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
- New learner machinery this lane (disclosed in PREREG
  Section 1): exactly three functions in bp5_rules.zag:
  `bp5_form_fact` (B-FACT R1), `bp5_form_meta` (B-META
  R1), `bp5_fact_tombstone` (I1 enforcement). Everything
  else new is test-harness code in bp5_driver.zag
  (emergent-evidence absorption, meta-update mapping,
  R5 field28-delta trigger, world builders, in-driver
  bars). Build on BP-4, no redesign of the belief layer.

## Step 1: prereg commit (this commit)

- PREREG.md written and frozen BEFORE any implementation
  file exists in this lane. This NAMECHECK.md Step 0/1
  recorded.
- Commit contains ONLY: PREREG.md, NAMECHECK.md (this
  file).
- Implementation (bp5_learner.zag, bp5_rules.zag,
  bp5_driver.zag, bp5_full.zag, runs, REPORT.md) comes in
  a LATER commit, strictly after this one.

## Step 2: implementation (done)

- Files: bp5_learner.zag (verbatim copy of BP-4's
  bp4_learner.zag, SHA-256
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
  on both, `cmp` clean), bp5_rules.zag (new: exactly
  three learner functions, bp5_form_fact / bp5_form_meta
  / bp5_fact_tombstone, disclosed in PREREG Section 1),
  bp5_driver.zag (new: six world arms E-R3/E-R5/B-FACT/
  B-META/MH/CY, emergent-evidence absorption, meta-update
  mapping, R5 field28-delta trigger, in-driver bars).
- Built: `cat ../xhier_countmap_fix/xf_block.zag
  bp5_learner.zag bp5_rules.zag bp5_driver.zag >
  bp5_full.zag`; pinned znc by absolute path, build exit
  0 -> bp5_bin (408778 bytes; log: bp5_compile.txt;
  A0102 warnings are the benign ignored-return-value
  pattern pervasive in the frozen block itself, same as
  BP-4).
- xf_block.zag SHA-256 re-verified before AND after the
  build: 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
  (unchanged; the patched XHIER-COUNTMAP-FIX block).
- No Python/C/JS/Rust invoked at any point. Safebin PATH
  held for the whole session. `which python3` /
  `which python` still empty at build and run.
- No em/en dashes in any authored lane file
  (byte-verified with grep); the only dash bytes in the
  lane are znc's own A0102 warning text inside the
  machine-generated bp5_compile.txt, disclosed in
  REPORT.md.
- 0 new edge types (1/3/14 frozen; 16 pre-exists in the
  block per DESIGN.md P5, used for meta-rows), 0 new
  node types (tags 1/3/20 pre-existing), 0 modes, 0
  bridges, 0 handlers (one-system accounting).

## Step 3: runs + REPORT.md (done)

- 3/3 runs byte-identical: sha256
  6793bd2bd5798c1546702bac42efd8d74a974dc00a65a88448e317a29b58af2f
  for bp5_run1/2/3.txt (K-DET PASS).
- In-driver bars: 31/31 PASS (4 PCs + 27 K bars).
  E-R3: block-written type-7/type-3 route to R2/R3
  (110/90), R5 correctly absent on reverted revise.
  E-R5: R5 iff block revised (field28 201->999, sup
  50); control shows no spurious revision. B-FACT:
  formation partition (1,0)/(0,1)/(0,0), emergent
  evidence (110/80), R7 selection, eff branches, I1
  (record death, fresh recycle). B-META: formation,
  one event moves rival meta-rows oppositely
  (110 vs 80), R7 follows the revised policy. MH:
  no cascade on single R6 (60/100/100), 3-hop via
  per-hop application (60/60/60), min combiner. CY:
  fixpoint (80,80), R6 snap-up (60->80),
  0-absorption with reason-2 retirement.
  BP5-SUMMARY 31/31; 33/33 with K-DET/K-HYG.
- REPORT.md written with verdict BP-5-PASS. The 7
  sealed predictions stay sealed; this lane adds
  open-dynamics evidence only.
- Committed with explicit pathspecs, local only, never
  pushed.
- Ledger: non-ledger task, nothing minted; ledger file
  untouched.
