# REPORT.md: H-BASECERT-SWEEP-1 Cert Harness Sweep

## Verdict: CERT-SWEEP-COMPLETE

The certify_base harness was swept across the five active mechanism
bases. Result: the harness as committed works on exactly one base
family shape (the original ma_base.zag). With a documented sweep
adaptation (drop the driver's ev_query glue where the base defines its
own; trim the base's own main from the scratch copy only), the three
TNN-2 trial-family bases score identically to the base-cert reference:
CERT-A LEAK FAIL (same 40 nodes / 24 edges per problem signature),
CERT-B ARENA PASS, CERT-C DETERMINISM PASS (3/3 byte-identical),
CERT-D CORRECT PASS (4/4). The XIO-general core and the belief
antifarm files are not bases at all, so the checks are NOT APPLICABLE
to them rather than FAIL. No base file on disk was modified at any
point (sha256 of every base re-verified after all runs; all match).

## Scorecard

| base | A LEAK | B ARENA | C DETERMINISM | D CORRECT | overall |
|---|---|---|---|---|---|
| composition_collapse/cl_full.zag (collapsed composition) | FAIL | PASS | PASS 3/3 | PASS 4/4 | FAIL (A) |
| grammar_codec/c_base_nomain.zag (grammar codec) | FAIL | PASS | PASS 3/3 | PASS 4/4 | FAIL (A) |
| goal_inference/gi_base.zag (goal inference) | FAIL | PASS | PASS 3/3 | PASS 4/4 | FAIL (A) |
| xio_general/xio_core2.zag (XIO-general core) | N/A | N/A | N/A | N/A | NOT APPLICABLE |
| belief_antifarm/belief_antifarm.zag (belief antifarm) | N/A | N/A | N/A | N/A | NOT APPLICABLE |

Base sha256:
- cl_full.zag `f66a69bf8e91cc383787cfe837d3f84ed983ec7270137bdd8862c2e840ccf633`
- c_base_nomain.zag `b63cce0403a4e3a321dfaf0bc366ded1bfe39b876f082affe5b4861b66f85210`
- gi_base.zag `f5ec4cafc94d6fbd4548e00c90b2781c31cc1f8922cf85d62192aa82ade07a65`
- xio_core2.zag `5c0413af9a67583a36e22b3f333a36b11e5938f5ad0db`
- belief_antifarm.zag `8d74875d45d3bef8cc4b7d51732fcdd38ff`

## Method

Phase 1: ran the unmodified `base_cert/certify_base` wrapper on all
five files. All five failed at compile, four with duplicate-definition
errors and one with unknown-function errors. This is a harness
portability finding, not five base defects; the harness was built for
the exact surface of ma_base.zag and had never been run on any other
file.

Phase 2: adapted sweep for the three trial-family bases via
`cert_sweep/certify_sweep.sh` (modeled on the committed wrapper, same
four checks, same 300s run timeout, same scoring greps) plus
`cert_sweep/cert_driver_noevq.zag` (the committed driver minus only
the 6-line ev_query glue block, produced by sed from the committed
driver). Two adaptations, both documented in the wrapper output:
1. The driver's minimal ev_query glue is dropped wherever the base
   defines its own richer ev_query (ctx/decay/push + rebind machinery).
   The base's own entry point is the correct object under test: it is
   what workers actually exercise on a miss. CERT-D D2 runs through it.
2. Where the base defines fn main, the SCRATCH COPY ONLY is trimmed
   from the `fn main(` line to EOF so the driver's main links. The
   on-disk base is never touched; the wrapper prints the sha256 of the
   untrimmed original.

## Per-base detail

### 1. Collapsed composition base (composition_collapse/cl_full.zag)

Adapted run: CERT-A LEAK `n0=0 n1=800 e0=0 e1=493 perprob_n=40
perprob_e=24 wrong=0` FAIL. CERT-B ARENA
`raw_filled=1022 post200_allneg=1 edges_filled=4096
edgepost100_allneg=1 evict_alloc=2 live=1022` PASS. CERT-C 3/3
byte-identical (sha256 `f43743437e302a39a0b50ac91341c4a43d0db073c9e30
398011776820a296790`) PASS. CERT-D: D1 chain3=1003, D2
reject-then-3hop=104 via the base's own ev_query (base logs RB-STAT
and COMP-STAT lines; the COMP-FAIL line is base logging, not a cert
failure), D3 true miss=-2, D4 chain4=2004, PASS 4/4.

Disposition: the composition collapse (H-COLLAPSE-1, fragment DFS) did
not change the trial-graph leak. The leak signature is byte-identical
to the base-cert reference on ma_base.zag. Known limitation L1 (see
below) applies unchanged: any worker plan exceeding ~25 trial problems
on this base is invalid by construction.

### 2. Grammar codec base (grammar_codec/c_base_nomain.zag)

Adapted run: CERT-A LEAK `n0=0 n1=800 e0=0 e1=493 perprob_n=40
perprob_e=24 wrong=0` FAIL. CERT-B ARENA identical to reference PASS.
CERT-C 3/3 byte-identical (sha256 `76e62d6e77ae90296527eedfb389af94
f70092f425d92752f379868eeaf88346`, the same hash as the base-cert
reference run) PASS. CERT-D 4/4 exact PASS.

Notes: `c_base.zag` and `c_base_nomain.zag` differ only by the main
function and a comment (7 diff lines); the nomain variant was used so
the sweep needed no main trim. The base's ev_query behaved identically
to the driver's minimal glue on the fixed problem set, hence the
matching run hash.

### 3. Goal-inference base (goal_inference/gi_base.zag)

Adapted run: CERT-A LEAK `n0=0 n1=800 e0=0 e1=493 perprob_n=40
perprob_e=24 wrong=0` FAIL. CERT-B ARENA identical to reference PASS.
CERT-C 3/3 byte-identical (sha256 `f43743...a296790`, same as the
cl_full run) PASS. CERT-D 4/4 exact PASS.

### 4. XIO-general core (xio_general/xio_core2.zag): NOT APPLICABLE

This file is an adapter layer, not a base. It defines only
`xio_oty`, `xio_sclass`, `xio_dep_rel`, `xio_gather_direct`,
`xio_has_typed`, `xio_stage_c2`, `xio_stage_exec`, `xio_build`,
`xio_exec`, `xio_find`, `xio_count`, `xio_adapt`, `xio_try`,
`xio_query`, and calls host-base functions (`ng`, `seq_nx`,
`t2_gather`, `t2_asm_chain`, ...) that it does not define. It has no
main, no `tnn2_init`, no `mp_run`, no arena surface. The raw wrapper
run fails compile with `native: call to unknown function ng` (and
`seq_nx`), which is the expected shape of an adapter file compiled
without its host, not a defect. Certifying it would mean certifying a
host base plus this adapter, which is a different harness. Marked
NOT APPLICABLE with exact cause, not FAIL.

### 5. Belief antifarm (belief_antifarm/belief_antifarm.zag): NOT APPLICABLE

This file is a self-contained mechanism experiment (H-DECEPT-4
betrayal-history-aware reliability update), not a TNN-2 trial base.
It has its own `main` running hardcoded world phases (D4 betrayal
phases with preregistered expected reliabilities 869/769/681/620/571
and penalties 2/8/15/20/25) and defines no trial substrate
(`tnn2_init`, `mp_run`, `activate`, arena allocators are all absent).
The raw wrapper run fails compile with duplicate `fn main`. The
cert checks (trial problems through mp_run, 1024-node arena, trial
correctness) have no substrate to run against here. Marked NOT
APPLICABLE with exact cause, not FAIL. Its own preregistered
self-tests are the applicable evidence for this file, out of scope
for this sweep.

## Known limitations (exact triggers)

L1. Trial-graph leak (inherited by all three trial-family bases,
CERT-A FAIL on each). Trigger: any sequence of trial problems via
`t2_trial`/`mp_run`. Rate: 40 live nodes + ~24 live edges per problem,
linear, unbounded, zero reclamation. Capacity rule unchanged: problems
x 40 + teaching residue must stay under 1024 nodes or the experiment
is invalid by construction. NOT repaired here: the bases are frozen
lineages; reclamation is a separate preregistered frontier.

L2. Eviction latency cliff (inherited; see base-cert REPORT.md L2).
CERT-B does exactly one at-capacity alloc_node per base; all three
returned a live node via eviction with no stall.

L3. Bases under test define their own ev_query and (two of them) their
own main, unlike ma_base.zag. The committed `certify_base` wrapper
fails these at compile. This sweep's `certify_sweep.sh` handles both
cases; see Method. Recommendation: fold these two adaptations into the
committed harness (guardian or research lead decision; not done here,
out of scope).

L4. xio_core2.zag and belief_antifarm.zag are not certifiable by this
harness at all: one is a host-dependent adapter, the other a
self-testing mechanism file. Scoring them FAIL would misattribute a
harness-scope boundary as a base defect. Future sweeps should classify
candidate files as base/adapter/mechanism-experiment BEFORE running
the wrapper.

## Files in this directory

- NAMECHECK.md: worker identity + Step 0 toolchain guard record.
- REPORT.md: this file.
- cert_driver_noevq.zag: committed driver minus the 6-line ev_query
  glue (produced by sed from the committed driver; diff-verified).
- certify_sweep.sh: sweep wrapper (same checks/scoring as the
  committed wrapper; executable bit set).
- raw_cl_full.txt, raw_c_base_nomain.txt, raw_gi_base.txt,
  raw_xio_core2.txt, raw_belief_antifarm.txt: Phase 1 unmodified
  harness outputs (compile failures as described).
- sweep_cl_full.txt, sweep_c_base_nomain.txt, sweep_gi_base.txt:
  Phase 2 adapted sweep outputs (full wrapper output incl. 3 run
  hashes and per-check lines).

## New code purity

All new code in this sweep is shell (wrappers) plus the
sed-derived driver variant. The compiled payloads were base + pure-Zag
driver only. No Python, no other interpreter, was invoked at any
point; safebin PATH was active for every command (Step 0 guard).
