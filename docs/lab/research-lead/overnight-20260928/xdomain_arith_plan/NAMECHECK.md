# NAMECHECK: xdomain_arith_plan (Cross-Domain Arithmetic-Planning Worker)

## Step 0: Toolchain Guard (mandatory, executed first)

Respawn worker executed at startup, 2026-10-02, before any research
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

## Step 1: Task Identity
- Worker: Cross-Domain Arithmetic-Planning (Battery B).
- Mission: Test H1 (typed contracts) and H2 (value composition) generality on arithmetic→planning.
- Verdict target: XDOMAIN-ARITH-PLAN-COMPLETE.

## Step 2: Constraints Acknowledged
- Unfrozen only. Frozen source read-only.
- Pure Zag. Zero em/en dashes (byte-verified before commit).
- Paper untouched: docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md never modified.
- Nothing pushed (local commits only).
- 0 modes/bridges/handlers. No ARITH_TO_PLAN template.
- Explicit pathspecs for all git operations.
- Preregistration strictly precedes implementation.

---

## Step 0 (respawn, 2026-10-02 ~15:50 UTC): Toolchain Guard re-executed

Respawned worker re-ran the identical safebin setup before any new
computation. Result: `which python3 python` returned NOTHING. Safebin
PATH active for every compile and run below. No forbidden executable
was invoked at any point. All computation is Zag compiled with the
pinned znc; shell is used only to invoke znc, run binaries, git ops,
and move files.

Pinned compiler: `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Preregistration (supersession)

PREREG.md (aa708f552) registered a different experiment (novel
typed-contract/value-composition mechanisms expecting success) than
the assigned task (verbatim H1/H2/H3 ports + XIO control, expecting
the chain-bound negative). It was SUPERSEDED transparently by
PREREG2.md, committed ALONE in 91e84ee0d BEFORE any driver,
assembly, binary, or run output under PREREG2 existed. PREREG.md was
never edited. The prior worker's implementation artifacts were moved
to superseded_prereg1/ untouched; ap.zag was renamed to
superseded_prereg1/ap_superseded_draft.zag (staged rename).

## Experiment identity (PREREG2)

- Pair: sum-then-plan. X = SUM (arithmetic, node -> number), r=71
  facts, query r=91. Y = PLAN (action sequences, number -> node),
  r=82 facts, query r=92. Z = plan(sum(s)), query (103,93) -> 203.
- X1: (101,71,5),(101,71,3),(101,71,7); Q(101,91)->15.
- X2: (102,71,4),(102,71,6); Q(102,91)->10.
- Y1: (15,82,201),(201,82,202),(202,82,203); Q(15,92)->203.
- Y2: (10,82,211),(211,82,212),(212,82,213); Q(10,92)->213.
- Gap: 30 facts (5000+i, 60+(i%10), 6000+i).
- Z facts: (103,71,6),(103,71,9); sum(103)=15; plan from 15 taught in
  Y1. Q(103,93)->203.
- Arms per mechanism: TREAT, ABL-X (r=91 MAPs deleted), ABL-Y (r=92
  MAPs deleted), FRESH. XIO adds ABL-XIO (xio_on=0).
- Driver scaffold (disclosed in REPORT.md): ap_comb/apx_comb creates
  one tag-8 combination-context node per arm so the base's sum trial
  branch (gated on comb_present) is attemptable; precedent
  xio_general/xg_driver.zag xgC_comb. Teaches no facts/answers.

## Assemblies (mechanism sources verbatim, catted directly, no copies)

- `ap_full_h1.zag` = `../invention_mutation/mu_core.zag`
  + `../invention_mutation/mu_patch.zag` + `ap_driver.zag`
- `ap_full_h2.zag` = `../invention_recombine/ir_base.zag`
  + `../invention_recombine/ir_patch.zag` + `ap_driver.zag`
- `ap_full_h3.zag` = `../invention_constraint/invent_base.zag`
  + `../invention_constraint/invent_patch.zag` + `ap_driver_h3.zag`
- `ap_full_xio.zag` = `../composition_A/cx_core.zag`
  + `../xio_adapters/xio_core.zag` + `ap_driver_xio.zag`

mu_patch.zag: H1 mutation stage (MUT_ON=1), ev_query redefined.
ir_patch.zag: H2 fragment recombination (frag_on=1), ev_query
redefined. invent_patch.zag: H3 constraint invention (invent_on=1),
ev_query_c added. xio_core.zag: typed I/O adapters (sha256
4d4d2e0e932b6a472e3cd8456d7e1c633218e611ce5df51d03507218440a8a7f per
xio_harder NAMECHECK; referenced, not copied).

Drivers are new (this worker): `ap_driver.zag` (H1/H2, plain
ev_query), `ap_driver_h3.zag` (H3, ev_query_c plen sweep 1..4 on Z,
plain ev_query on X/Y training), `ap_driver_xio.zag` (XIO,
xio_query; defines ev_query shim for cx_core's internal battery).

## Build record

Pure Zag. Zero em/en dashes in sources and docs (byte-verified with
grep for U+2013/U+2014 before commit). Frozen source read-only. Paper
untouched. Committed locally, nothing pushed. 0 modes / bridges /
handlers / new semantic cases / domain templates.

Binaries: `ap_bin_h1`, `ap_bin_h2`, `ap_bin_h3`, `ap_bin_xio`
(pinned znc; warnings only, A0102 class like prior workers).
Runs: `ap_run_h1_1/2/3.txt`, `ap_run_h2_1/2/3.txt`,
`ap_run_h3_1/2/3.txt`, `ap_run_xio_1/2/3.txt` (3/3 byte-identical
per binary; SHA-256 in REPORT.md).
Compile logs: `ap_compile_h1/h2/h3/xio.txt`.

## Result summary

- AP-COMP HOLDS all four binaries (X1=15, X2=10, Y1=203, Y2=213).
- AP-DET HOLDS all four binaries.
- AP-H1 KILLED (MUT-STAT tried=0: no plen-4 path from 103 to stage).
- AP-H2 KILLED (RECOMB-FAIL: no 82-facts on 103).
- AP-H3 KILLED (all plens 1..4 fail; plen 2..4 INVENT-FAIL).
- AP-XIO FAIL/control (adapters=0 all arms; oty-1 stage re-derives
  count, not sum: count(103)=2 != 15). NEW boundary finding.
- Verdict: XDOMAIN-ARITH-PLAN-COMPLETE.
