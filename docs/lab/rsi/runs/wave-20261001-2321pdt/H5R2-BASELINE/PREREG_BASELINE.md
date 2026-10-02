# FROZEN PREREG: H5R2-BASELINE, simple-baseline comparison (pipeline step 5)

Lane: H5R2-BASELINE, wave-20261001-2321pdt. Status: FROZEN PREREG.

Lineage: TNN3H5R H5R2 (trial-loop t2_prov_ok provenance gate) reached
BUILD-PASS (SEALED_EVAL_H5R2.md) and REPRO-PASS (REPRO_H5R2.md) on the
four sealed worlds w_c1, w_c2, w_w3a, w_w3b. This lane is pipeline step
5: attack the simpler explanation. If a simpler mechanism explains the
sealed results as well as the provenance gate, the gate is not shown
necessary.

ORDERING RULE: this prereg is committed (with NAMECHECK.md) before any
baseline implementation file is written. Any baseline artifact whose
mtime predates the prereg freeze commit is UNVERIFIABLE ORDERING and
the comparison is VOID. Kill bars never move after freezing.

## 1. Question under test

Is there a SIMPLER explanation for the H5R2 sealed results than the
t2_prov_ok provenance gate (decline any trial candidate whose licensing
facts are not all live, tag-1, non-superseded)? Three skeptic
baselines, each a minimal modification of the committed H5R2 source
extracted via git show from commit
9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a.

### Baseline (b): NO-GATE (the "fix does not matter" control)

The exact H5R pre-fix trial loop: t2_trial accepts the first candidate
whose executed output matches the expected value, in BFS/node-id order,
with no provenance gating. This is the mechanism KILLED on KB-W2R 8/12.
Implementation: delete the t2_prov_ok helper (function plus its comment
block, lines 508-523 of the extracted source) and restore the four
t2_trial promote sites to the ungated form `if(v2!=-2){...}`. The
resulting file MUST be byte-identical to the verified H5R base blob at
commit 830f95ab7, SHA-256
d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384;
verified by hash before any world is assembled.

### Baseline (a): REVERT-TO-LATEST (recency heuristic, no gating)

A trial loop with NO provenance gating that simply anchors to the most
recently created facts. Rule, frozen: at each of the four t2_trial
promote sites, among the verifying candidates prefer the one licensed
by the most recently created facts; no liveness or supersession checks
anywhere; is_superseded unused. Composition preference is preserved
exactly: chain lengths still tried 2..4 before sums before counts
before single hops. Implementation: delete t2_prov_ok (helper, comment,
four call sites, ungated `if(v2!=-2)` as in (b)); reverse the inner
candidate enumeration on the three oldest-first paths so the last
verifying candidate in the original order is accepted first: chain
path inner p loop `let p:i32=0; while(p<np && ans==-2){` becomes
`let p:i32=np-1; while(p>=0 && ans==-2){` with `p=p+1;` becoming
`p=p-1;`; single-hop p loop likewise; count path relation loop
`let i:i32=0; while(i<nr && ans==-2){` becomes
`let i:i32=nr-1; while(i>=0 && ans==-2){` with `i=i+1;` becoming
`i=i-1;`. The sum path keeps its (subset-size descending, mask
descending) order unchanged: within a fixed subset size that order
already tries newer-fact subsets first, so first-match there is already
the recency choice. Net effect on the sealed worlds: on revert queries
with two verifying candidates (stale original fact vs live reverted
fact), the candidate via the most recently created fact is promoted.

### Baseline (c): RANDOM-ANCHOR (optional; "any anchoring suffices" test)

No provenance gating; at each promote site, promote one verifying
candidate chosen uniformly at random from the forward-enumeration
verifying set. Randomness is a fixed-seed deterministic LCG
(state = state * 1103515245 + 12345 mod 2^31), state kept in the unused
W header field 52, lazily seeded to 12345 on first use (field 52 is
zero after tnn2_init; zero is treated as uninitialized). Single-pass
reservoir sampling per path preserves the composition preference
(shorter chains first, then sums, counts, single hops). No clock or
time reads. Deterministic by construction, so the 3/3 byte-identical
protocol still applies.

What is explicitly NOT changed in any baseline: activate,
promote_graph, ev_teach_in, ev_teach, ev_observe, ev_query, ev_act,
miss_inquire, mp_run, t2_try_verify, t2_gather, t2_gather_sum, t2_chain,
bid, ref_prot, is_superseded (kept but unused by (a) and (c)),
supersede, resolve_uncertainty, revise_on_contradict, the 4-op ISA and
execute, the sealed driver template, and the world probe patterns. No
new modes, bridges, routers, or handlers. No core-ISA additions.

## 2. Reference scores (frozen, from SEALED_EVAL_H5R2.md + REPRO-PASS)

H5R2: KB-W0 36/36, KB-W2R 12/12, KB-B2R 24/24, KB-W3 8/8, KB-B3 24/24,
KB-D1 3/3 byte-identical on all four worlds.

## 3. Frozen comparative kill bars

CB-1 (provenance margin): for each baseline B, H5R2 must exceed B by at
least 2 probes on a provenance-sensitive bar: max(12 - W2R_B,
8 - W3_B) >= 2. Baselines (b) and (c) are expected to fail here; (a)
is the dangerous one.

CB-2 (no full match): no baseline may equal the H5R2 reference on all
five bars (W0 36/36, W2R 12/12, B2R 24/24, W3 8/8, B3 24/24). A full
match means the simpler mechanism explains the sealed results as well
as t2_prov_ok, and the gate is not shown necessary.

CB-3 (determinism): 3/3 byte-identical full-stdout runs per baseline
per world, SHA-256 compared (the KB-D1 protocol). Any byte difference
is reported; a nondeterministic baseline is scored from its runs and
flagged, but the comparison on CB-1/CB-2 uses its observed scores.

Verdict BASELINE-BEATEN iff CB-1 holds for every baseline AND CB-2
holds (no baseline matches the full vector).

Verdict BASELINE-MATCHES iff some baseline matches the full five-bar
reference vector (CB-2 violated). A MATCHES verdict is informative, not
a failure to hide: it says exactly which simpler mechanism the sealed
battery cannot discriminate from the provenance gate.

## 4. Pre-registered expectations (not kill bars; recorded for honesty)

- (b) NO-GATE: expected to reproduce the killed battery: KB-W2R about
  8/12 (stale DEP edges on the 4 revert probes), KB-W3 below 8/8,
  behavioral bars 24/24, KB-W0 36/36.
- (a) REVERT-TO-LATEST: expected to match H5R2 on all five bars on
  these worlds, because on every revert query the last verifying
  candidate is licensed by the live reverted fact. If so, the honest
  verdict is BASELINE-MATCHES via (a): recency explains the results.
- (c) RANDOM-ANCHOR: expected to fail provenance bars on roughly half
  the revert probes (chance anchoring), behavioral bars intact.

## 5. Worlds and evaluation protocol (frozen)

5.1. The same four sealed worlds as the H5R2 battery: w_c1, w_c2,
w_w3a, w_w3b, extracted via git show from commit
e20ba54020dde7e38050dda9e54727d826fc7b45 and hash-verified against
SEALED_H5R2.md before use:
w_c1.zag 3246e635488c0b7c46d4a0fe41ea267a6777827a9d64333ecf3a869b8defd0e7,
w_c2.zag 28831f3b49e6fcf436a4537b0e8d6ae8bfdec15c8703037fce619beb5d88f0b8,
w_w3a.zag 3ec3b1631127c4c7ac1758329c32f65661396a11847c2c6b14a59aea65289843,
w_w3b.zag 7e69965d4c6a7e86486a370f68bc0e827bd289c076c10a1e4d49e781d5159e41.

5.2. Per baseline, four world files are assembled by the frozen rule:
byte-copy of the baseline substrate with the single line
`fn main()i32 { return run_all(); }` changed to
`fn main()i32 { return sealed_main(); }` (verified by diff), plus the
frozen DRIVER_TMPL.zag appended (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
extracted from commit 9db334bd4), plus one alias line selecting the
world (`fn sealed_main()i32 { return sealed_main_c1(); }`, etc.).
Assembly happens only after the implementation commit; world file
SHA-256s are recorded before any run.

5.3. Each world file is compiled separately with the pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1); 3/3 runs; full-stdout
SHA-256 compared per world (CB-3).

5.4. Scoring uses the driver's own markers, identical across baselines:
counts of "W0 ok" (target 36: 18 per C world), "W2R ok" (target 12),
"B2R ok" plus "B3R ok" (target 16 + 8 = 24), "W3 ok" (target 8),
"B3 ok" (target 24: 12 per W3 world), and zero FAIL/FAILURE marker
lines. The reference vector is reproduced by re-running the H5R2
worlds only if needed; the frozen reference scores in section 2 stand.

5.5. Negative controls: NC-B0 (a baseline world file is not a valid
assembly per 5.2: that baseline is VOID, not scored); NC-B1 (any
forbidden-executable invocation: PROCESS-FAIL, terminal); NC-B2
(prereg freeze does not strictly precede implementation: UNVERIFIABLE
ORDERING, VOID).

## 6. Pure-Zag construction

Builder PATH is $HOME/safebin (36 tools, no python3, verified at lane
startup and recorded in NAMECHECK.md Step 0). All research logic is
Zag compiled/run with the pinned znc. Shell is used only to invoke
znc, run binaries, do git ops, and move/copy files.

## 7. Documentation

No em-dashes in any lane documentation. Every doc is checked with
sh docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
before commit.
