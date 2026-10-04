# REPORT.md: CERT-V2 Base Certification Harness

## Verdict: CERT-V2-COMPLETE

certify_base v2 folds the CERT-SWEEP adaptations into the committed
harness. v2 classifies every candidate as BASE / ADAPTER /
MECHANISM-EXPERIMENT / UNKNOWN before running anything; non-bases get
CERT-VERDICT NOT APPLICABLE with the exact cause, never FAIL. For BASE
class it auto-detects whether the base defines its own ev_query (drops
the driver glue if so, uses the glue driver otherwise) and trims a base
`fn main` from the scratch copy only. Re-ran v2 against all 5 sweep
targets: the 3 trial bases reproduce the sweep verdicts byte for byte
(same check outcomes, same 3/3 run hashes, same leak numbers); the 2
non-bases reproduce NOT APPLICABLE. ma_base.zag run as a v1 parity
check reproduces the H-BASECERT-1 reference exactly. Separately, the
new host+adapter cert certifies xio_core2.zag against
composition_collapse/cl_full.zag: XIO-CERT-VERDICT PASS (AC2, AC3, AC4,
AC5, AC6 all PASS, 3/3 deterministic). No base file on disk was modified
at any point (sha256 of all six bases re-verified after all runs; all
match the pre-run values in base_sha256_before.txt).

## Scorecard: v2 vs sweep (identical verdicts required, identical obtained)

| candidate | v2 class | A LEAK | B ARENA | C DETERMINISM | D CORRECT | v2 verdict | sweep verdict | match |
|---|---|---|---|---|---|---|---|---|
| composition_collapse/cl_full.zag | BASE | FAIL (40n/24e) | PASS | PASS 3/3 | PASS 4/4 | FAIL (A) | FAIL (A) | yes |
| grammar_codec/c_base_nomain.zag | BASE | FAIL (40n/24e) | PASS | PASS 3/3 | PASS 4/4 | FAIL (A) | FAIL (A) | yes |
| goal_inference/gi_base.zag | BASE | FAIL (40n/24e) | PASS | PASS 3/3 | PASS 4/4 | FAIL (A) | FAIL (A) | yes |
| xio_general/xio_core2.zag | ADAPTER | N/A | N/A | N/A | N/A | NOT APPLICABLE | NOT APPLICABLE | yes |
| belief_antifarm/belief_antifarm.zag | MECHANISM-EXPERIMENT | N/A | N/A | N/A | N/A | NOT APPLICABLE | NOT APPLICABLE | yes |
| meta_applicability/ma_base.zag (v1 parity) | BASE | FAIL (40n/24e) | PASS | PASS 3/3 | PASS 4/4 | FAIL (A) | FAIL (A) ref | yes |

Run-hash identity (the strongest equivalence signal, binary stdout only):
- cl_full v2 run hash `f43743437e302a39a0b50ac91341c4a43d0db073c9e30398011776820a296790`
  equals the sweep's sweep_cl_full.txt hash.
- gi_base v2 run hash is the same `f43743...a296790`, equals the sweep's.
- c_base_nomain v2 run hash `76e62d6e77ae90296527eedfb389af94f70092f425d92752f379868eeaf88346`
  equals the sweep's and the H-BASECERT-1 ma_base reference hash.
- ma_base v2 run hash is the same `76e62d...88346`, equals the v1 reference.
- xio_core2 and belief_antifarm never reach the run stage (classified out).

Per-check numbers identity (spot-verified from run outputs):
- All three trial bases and ma_base: CERT-A `n0=0 n1=800 e0=0 e1=493
  perprob_n=40 perprob_e=24 wrong=0` FAIL; CERT-B
  `raw_filled=1022 post200_allneg=1 edges_filled=4096
  edgepost100_allneg=1 evict_alloc=2 live=1022` PASS; CERT-D 4/4 exact.
  The leak signature is byte-identical to the sweep and to the v1
  reference on ma_base.

## v2 vs v1 comparison

v1 (`base_cert/certify_base`) assumed exactly one base shape: the base
defines no ev_query and no main, so the driver always supplied the
glue and the base was concatenated verbatim. Run on anything else it
died at compile (duplicate ev_query, duplicate main), which the sweep
correctly read as a harness portability finding, not base defects.

v2 (`certify_base_v2`) keeps the four checks, the 300s run timeout, the
scoring greps, and the verdict semantics byte for byte, and adds:

1. Classification before execution. BASE iff the candidate defines
   `^fn tnn2_init(`. Otherwise a standalone probe compile (scratch
   copy; stub `fn main()void { return; }` appended only when the file
   has no main) decides: "call to unknown function" in the probe log
   means ADAPTER (host-dependent layer); clean probe compile means
   MECHANISM-EXPERIMENT (self-contained file, no trial substrate);
   anything else means UNKNOWN. Non-bases exit 3 with
   CERT-VERDICT NOT APPLICABLE and the exact cause. v1 had no
   classification; its compile failures on non-bases were scored FAIL,
   misattributing a harness-scope boundary as a base defect (sweep L4).

2. ev_query auto-detection. If the base defines `^fn ev_query(` with
   the exact cert D2 signature
   `(W:[]u8,s:i32,r:i32,expected:i32)i32`, v2 uses
   cert_driver_noevq.zag (the sweep's sed-derived driver, provenance
   re-verified byte-identical in this directory) and the base's own
   richer ev_query is the entry point under test. If the base defines
   no ev_query, v2 uses cert_driver.zag with the glue, which is
   byte-identical to the v1 driver, so the ma_base path is literally
   the v1 path. A base ev_query with any other signature is a clean
   FAIL with the signature mismatch spelled out (the D2 contract is
   fixed; silently running a different contract would be worse).

3. Scratch-only main trim. If the base defines `^fn main(`, the
   scratch copy is cut from that line to EOF (same head -n idiom as the
   sweep). The on-disk base is never touched; the wrapper prints the
   sha256 of the untrimmed original.

4. Distinct exit codes: 0 PASS, 1 FAIL, 3 NOT APPLICABLE, 2 usage
   error (v1 used 2 for usage, 1 for everything else).

What v2 deliberately does NOT change: check semantics, budgets (20
problems, 20/20 per-problem growth, 1022/4096 arena fills, one
at-capacity eviction), timeouts, or scoring patterns. The run-hash
identity above is the evidence that nothing else moved.

## Host+adapter cert (optional scope, completed)

`cert_hostadapter.sh <adapter.zag> <hostbase.zag>` plus the pure-Zag
`cert_adapter_driver.zag`. The adapter must classify ADAPTER and the
host BASE under the v2 rules; the host's main is trimmed from the
scratch copy only; host + adapter + driver are compiled as one unit,
so AC1 (implicit in every run) is that the adapter's host-function
surface is fully satisfied by the host. Then five checks plus
determinism:

- AC2 REGISTRY: empty registry reads (count 0, find -1); xio_build
  writes a tag-40 node with the documented layout (fields
  m1/m2/c1/c2/rel1/rel2/answer/query-relation); find and count observe
  it. PASS.
- AC3 FAILCLOSED: xio_exec on garbage MAP ids returns -999999;
  xio_adapt with no registered adapter returns -2; xio_try with
  expected -2 returns -2; xio_sclass on a graphless node returns -1;
  xio_oty on it returns 0; xio_dep_rel with no provenance returns -1;
  xio_stage_exec on class -1 returns -999999. PASS.
- AC4 CLASS2 ROUNDTRIP: two facts (501,7): 3,5 taught; graph built with
  the learner's own t2_asm_sum; MAP promoted by the driver with DEP
  provenance edges to the licensing facts. xio_oty==1, xio_sclass==2,
  xio_dep_rel recovers relation 7, xio_stage_exec re-derives total 8
  through the class-2 path. PASS.
- AC5 ADAPT ROUNDTRIP: second class-2 MAP (8,9): 2,4 -> 6; adapter
  chains mA(501)=8 into mB(8)=6. xio_build/xio_find/xio_exec/xio_adapt
  all return 6; mismatched expected and unknown query relation return
  -2. PASS (the XIO-REUSE line in the output is the adapter's own
  logging, not a cert failure; the AC5 verdict line is emitted after
  it so scoring sees one line).
- AC6 GATE: with two same-class MAPs and one guard-only (class-0) MAP
  present, xio_try attempts only cross-class pairs (the sclass
  mismatch gate) and every attempt fails closed, returning -2 with no
  spurious adapter built (count stays 1). PASS.
- Determinism: 3/3 byte-identical, sha256
  `14890ecd186baea43df1f35284da19b63ffa8996230d649c7f79d77aa11a3756`.

Result: XIO-CERT-VERDICT PASS against host
composition_collapse/cl_full.zag. Note on the "certified base"
wording: no trial base passes all four base checks (CERT-A FAIL is the
frozen, documented trial-graph leak, inherited by every trial-family
base). The host used here is the trial-family base whose v2 base-cert
signature is the reference one (A FAIL leak 40/24, B/C/D PASS); the
adapter cert does not re-litigate the leak, it certifies the adapter
layer against that host. xio_query end-to-end (the unified query with
rebind/miss/inquiry coupling) is intentionally out of scope; it is
covered by the XIO lane's own experiments.

Feasibility note: the full host surface xio_core2 needs (34 functions
including rebind_try and rb_chain_plen) is defined by cl_full.zag and
gi_base.zag. ma_base.zag and c_base_nomain.zag lack rebind_try and
rb_chain_plen, so they cannot host this adapter version; the wrapper
would report that as a compile FAIL with the log, which is the honest
signal.

## Known limitations (carried forward, plus v2-specific)

L1. Trial-graph leak (CERT-A FAIL on all four trial bases, 40 nodes +
   ~24 edges per problem, zero reclamation). Unchanged from the sweep;
   capacity rule unchanged (problems x 40 + teaching residue under
   1024). Not repaired here; reclamation is a separate frontier and
   the bases are frozen lineages.

L2. Eviction latency cliff (inherited from H-BASECERT-1). CERT-B does
   exactly one at-capacity alloc_node; fine on all four bases.

L3. v2's main trim keys on `^fn main(`. A base spelling main
   differently would fail at compile with duplicate main and be scored
   FAIL with the log; no such base is known.

L4. v2's ev_query contract is fixed at the 5-argument D2 signature. A
   base defining ev_query with a different signature gets a clean FAIL
   naming the mismatch, not a silent skip of D2.

L5. The classifier's ADAPTER probe depends on znc's "call to unknown
   function" diagnostic text. If a future znc rewords it, ADAPTER
   candidates would fall to UNKNOWN (still NOT APPLICABLE, still not
   FAIL). The probe appends a stub main only when the file lacks one,
   so a main-bearing library with undefined calls is still caught.

L6. The host+adapter cert covers xio_core2's registry, fail-closed
   behavior, class-2 re-derivation, value-level adaptation, and the
   mismatch gate. It does not cover xio_query end-to-end or the
   class-0/class-1 stage executors on production-built MAPs; those
   belong to the XIO lane's experiments.

## Files in this directory

- NAMECHECK.md: worker identity + Step 0 toolchain guard record.
- REPORT.md: this file.
- certify_base_v2: the v2 harness (sh wrapper, safebin tools only;
  executable bit set). Exit 0 PASS, 1 FAIL, 3 NOT APPLICABLE, 2 usage.
- cert_driver.zag: v1 driver, byte-identical copy (sha256
  82d201a93ec98f9796f5b66ac8df81c4bd226c738337003524b73e70175accd2).
- cert_driver_noevq.zag: v1 driver minus the ev_query glue block,
  derived by sed from cert_driver.zag and diff-verified byte-identical
  to the sweep's cert_driver_noevq.zag (sha256
  7950bce53efb1a65e2d6b1fc9fbd2caeeee78328dcd506e533a1dcc38abac96e).
- cert_hostadapter.sh: host+adapter cert wrapper (sh, executable bit
  set). Exit 0 PASS, 1 FAIL, 3 NOT APPLICABLE, 2 usage.
- cert_adapter_driver.zag: pure-Zag adapter checks AC2 through AC6.
- v2_cl_full.txt, v2_c_base_nomain.txt, v2_gi_base.txt: full v2 wrapper
  outputs for the three trial bases (3 run hashes each, per-check
  lines, verdicts).
- v2_xio_core2.txt, v2_belief_antifarm.txt: v2 classification outputs
  (NOT APPLICABLE, exit 3).
- v2_ma_base.txt: v1 parity run output.
- hostadapter_xio_core2.txt: full host+adapter wrapper output
  (XIO-CERT-VERDICT PASS, 3/3 deterministic).
- base_sha256_before.txt, base_sha256_after.txt: base integrity
  evidence (all six bases byte-identical before and after).

## New code purity

All new wrapper code is shell (safebin tools only). The compiled
payloads were base + pure-Zag driver, and host + adapter + pure-Zag
driver, in every run. No Python or other interpreter was invoked at
any point. One real bug was found and fixed during construction: a
greedy sed in the classifier's unknown-function extraction ate the
whole match (fell through to UNKNOWN); fixed to a negated-class
pattern and re-verified (xio_core2 now classifies ADAPTER).
