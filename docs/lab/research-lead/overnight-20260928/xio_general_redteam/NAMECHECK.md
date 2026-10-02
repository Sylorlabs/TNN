# NAMECHECK.md -- XIO-General Red-Team Worker

## Step 0: Worker Toolchain Guard (mandatory)

Setup executed 2026-10-02 (session start):
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `guard-check-done` with NO python3/python lines printed. The
forbidden executables do not resolve in the safebin PATH. Guard: PASS.

Toolchain verification: all computation in this wave is pure Zag
(compiled and run with the pinned znc) plus POSIX shell utilities
(cat, sha256sum, cmp, git) for assembly, hashing, comparison, and
commits. No Python, no C, no other interpreters invoked at any point.

## Scope

Adversarial battery against the FROZEN generalized XIO core
(xio_core2.zag, XIO-GENERAL-COMPLETE, commit a36206064). The core is
attacked, never modified. Five attacks:

- B1 sclass defeat via output-dead INC cells (new machinery: xio_sclass)
- B2 class -1 over-conservatism (new machinery: unknown fail-closed path)
- B3 sclass-difference gate admits a same-type pair (new machinery: gate)
- B4 class-2 stage dispatch on a non-sum INC-only graph (new machinery)
- B5 exact A1 rerun (old red-team kill vs the new core)

Frozen inputs verified before assembly:
- ../composition_A/cx_core.zag sha256 must equal
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  (value recorded in the XIO-general REPORT.md).
- ../xio_general/xio_core2.zag is referenced read-only in assembly.

## Build log

Assembly (frozen base + frozen generalized core + new driver):
```
cat ../composition_A/cx_core.zag ../xio_general/xio_core2.zag xrt_driver.zag > xrt_full.zag
znc xrt_full.zag -o xrt_bin 2> xrt_compile.txt
```
Runs (3x, byte-identity check):
```
./xrt_bin > xrt_run1.txt
./xrt_bin > xrt_run2.txt
./xrt_bin > xrt_run3.txt
sha256sum xrt_run1.txt xrt_run2.txt xrt_run3.txt
cmp xrt_run1.txt xrt_run2.txt && cmp xrt_run2.txt xrt_run3.txt
```

## Zag notes

- Driver uses only the frozen base's own constructors
  (t2_lit/t2_guard/t2_set/t2_inc/t2_mov, seq_link, link_edge,
  promote_graph, ev_teach, xio_query) plus one local promote
  variant (xrt_promote) that mirrors promote_graph exactly minus
  the ev_teach_in answer-fact teach, so hand-built MAPs cannot
  poison the query relation via activate().
- No `as *i32` slice construction anywhere in driver code.
- Output uses the base's emit/e64 idiom (builtin _zag_i64_to_str);
  stdout bytes verified by inspection of all three run files.

## Scorecard (from xrt_run1/2/3.txt, 3/3 byte-identical, sha256
5fb0645b5337fa94d1005aef3706da70e1ad68ca578adc6537c9da007ceb102b)

- B1 sclass defeat: KILL. S=131: sclass=1, oty=1, exec=24 (NODE),
  plen=-1, but xio_stage_exec(S,21)=3 (NUMBER). The new core
  mis-stages a behaviorally-chain MAP through the count branch;
  the old core merely excluded it. Composition still ans=-2.
- B2 class -1: BOUND. M=13: sclass=-1, behaviorally correct sum
  (exec0=8, deprel=84), stage fails closed (-999999). Meaningful
  chain->sum composition impossible (ans=-2, adapters=0). The gate
  admits both -1/0 directions (tried=2); staging fails them closed.
  Fail-closed as documented, but the "total over graph structure"
  claim is overstated: a MOVE-epilogue sum variant is unclassifiable.
- B3 gate nonsense: KILL. XIO-BUILD id=72 m1=14(S,class1) m2=27(C,class0)
  mid=2 ans=71. S is behaviorally a chain (execS=33) staged as a
  counter (stageS=2); the gate admitted the same-type pair; the
  number-as-node handoff verified via id collision. Reuse on fresh
  subject 41 returns 71, determined by node 2, not subject 41.
- B4 class-2 garbage: KILL. XIO-BUILD id=83 m1=21(C,class0) m2=11(T,class2)
  mid=33 ans=10. T is the constant-5 function (execT 5/5); the class-2
  stage never runs T's graph, re-deriving a sum from T's DEP edges
  (stageT(33)=10). Reuse on subject 51 confidently answers 3.
- B5 A1 rerun: KILL (not fixed). Exact old-A1 world: all 3 MAPs class 1,
  gated=6 tried=0, ans=-2 adapters=0. Control (trial chain) ans=2.
  sclass does not fix the structural-INC exclusion.
