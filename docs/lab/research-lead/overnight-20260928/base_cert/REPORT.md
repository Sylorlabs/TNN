# REPORT.md: H-BASECERT-1 Base-Trial Certification

## Verdict: BASE-CERT-COMPLETE

The certification battery is built, runs, and scores the current base:
CERT-A LEAK **FAIL**, CERT-B ARENA **PASS**, CERT-C DETERMINISM **PASS** (3/3
byte-identical), CERT-D CORRECT **PASS** (4/4). Overall `CERT-VERDICT FAIL`
because the leak check fails, which is the correct outcome: the harness
catches the exact defect that sank the meta-applicability v1 wave.

## Base under test

`docs/lab/research-lead/overnight-20260928/meta_applicability/ma_base.zag`
(identical copy in `meta_applicability_v2/`), the TNN-2 trial base used by
recent workers. sha256
`0e2cafe2e61952f3a715732adb2a8bdfdf5c3a2a9f4d331d576df8a24acb0ccd`.
The base file on disk was never modified; the cert concatenates a scratch
copy with the driver at compile time.

## How to use

```
docs/lab/research-lead/overnight-20260928/base_cert/certify_base <base.zag>
```

Exit 0 iff all four checks PASS. Prints per-check lines and
`CERT-VERDICT PASS|FAIL`. Files: `certify_base` (sh wrapper, safebin
tools only), `cert_driver.zag` (pure-Zag cert binary source, appended to
the base), `cert_bin` (reference binary compiled against the base above;
the wrapper recompiles per invocation, so this binary is evidence, not
the mechanism).

## Check results on the current base

- CERT-A LEAK: `n0=0 n1=800 e0=0 e1=493 perprob_n=40 perprob_e=24
  wrong=0` FAIL. 20 fixed trial problems leak exactly 40 nodes and ~24
  edges per problem, linear, with zero reclamation. Trial candidate graphs
  accumulate; nothing is ever freed.
- CERT-B ARENA: `raw_filled=1022 post200_allneg=1 edges_filled=4096
  edgepost100_allneg=1 evict_alloc=2 live=1022` PASS. Past-capacity
  `alloc_raw`/`link_edge` return -1 cleanly, no stall; one at-capacity
  `alloc_node` evicts and returns a live node.
- CERT-C DETERMINISM: 3 runs, sha256
  `76e62d6e77ae90296527eedfb389af94f70092f425d92752f379868eeaf88346`
  all three, PASS.
- CERT-D CORRECT: D1 chain3=1003, D2 reject-then-3hop=104, D3 true
  miss=-2, D4 chain4=2004, all exact, PASS.

## Failure disposition (repair vs document)

The CERT-A failure was NOT repaired in the base. Rationale, recorded for
governance:

1. The TNN-2 base is frozen. Patching the leak inside `ma_base.zag`
   would change the substrate that existing worker results were measured
   against, breaking frozen-bar discipline.
2. The meta-applicability v2 prereg already designates trial node
   reclamation as a separate research frontier, not a hotfix.
3. A leak fix changes capacity planning for every experiment, so it
   needs its own prereg, kill bars, and freeze, not a cert-worker edit.

The leak is therefore documented below as a known base limitation with
exact triggers. Any experiment whose design exceeds the capacity implied
by the leak rate must either stay under it or preregister a reclamation
frontier first. This is precisely the K7-style misattribution guard the
battery was built for.

## Known base limitations (exact triggers)

L1. Trial-graph leak (CERT-A FAIL). Trigger: any sequence of trial
problems via `t2_trial`/`mp_run`. Rate: 40 live nodes + ~24 live edges
per problem, linear, unbounded, zero reclamation (rejected candidate
graphs are never freed). Consequence: the 1024-node arena exhausts at
~25 problems; the v1 meta-applicability wave died at problem 21
(C-P5: 1022/1024, mid-trial eviction, wrong answer). Capacity rule for
workers: problems x 40 + teaching residue must stay under 1024, or the
experiment is invalid by construction.

L2. Eviction latency cliff. Trigger: any `alloc_node` when live nodes are
at 1024. Each such alloc runs `evict_node`: a full 1024-node scan where
every node pays `is_prot` (4096-edge scan) plus `bid` (roughly six more
4096-edge scans), about 30M primitive ops, measured ~0.8s CPU per
eviction. Every further alloc re-triggers it. Measured: a single trial
doing ~40 post-capacity allocs burned 34s CPU (answer still correct).
Near-capacity trials are therefore not just wrong-risk (L1), they are
unrunnable within normal time budgets. CERT-A deliberately stays at 20
problems (800 nodes) to measure the leak without tripping this cliff;
CERT-B does exactly one at-capacity alloc.

L3. Base file is not self-contained. Trigger: compiling `ma_base.zag`
alone. `ev_query` is referenced by the base's own self-tests but defined
only in each experiment's patch, so the base fails to compile standalone
(`native: call to unknown function ev_query`). The cert driver supplies
a minimal trial-path `ev_query` (activate, else mp_run). Any future base
refactor should either define the trial entry point in the base or
document the required patch surface.

L4. Eviction can corrupt live trial state (inherited from the v1 saga,
not re-triggered here). Trigger: mid-trial eviction when the lowest-bid
victim is part of the in-progress trial. Observed in v1 as trial=11
tries, ans=-2 WRONG at C-P5. In this wave's probes the answer stayed
correct under eviction pressure, but correctness under eviction is not
guaranteed by the mechanism; it held by luck of victim selection.

## Design notes

- The leak check uses per-problem growth budgets (20 nodes, 20 edges)
  rather than literal "return to baseline", because teaching legitimately
  persists facts; the budget is the operational form of the check.
- The 300s per-run timeout in the wrapper converts any future stall into
  a CERT-C FAIL rather than a hung cert.
- Pure Zag: the cert binary is compiled from base + `cert_driver.zag`
  only. Shell is used solely to invoke znc, run the binary, and compare
  hashes, matching the established build.sh precedent.

## Run outputs

- `cert_run1.txt`: full wrapper output for the scored run (compile,
  3 run hashes, per-check verdicts).
- `cert_compile.log`: znc output for the reference binary build.
- `cert_bin`: reference binary, sha256
  `db01f2eb191ada61b4795db6d3f7aed1567c08187374b37008c7acc831b9d825`.
