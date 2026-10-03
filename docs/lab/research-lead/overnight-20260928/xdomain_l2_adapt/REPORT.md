# REPORT: XDOMAIN-L2-ADAPT (cross-domain arithmetic to planning, length mismatch)

Worker: XDomain L2 Adapt Worker. Branch: tnn-native-lab, local only,
nothing pushed. Frozen PREREG.md (commit f5a4db6ea) plus transparent
PREREG_AMENDMENT1.md (commit b7026931c, pre-implementation).

## Verdict: XDOMAIN-L2-ADAPT-PASS (K1-K11 all pass)

## What was tested

X = SUM over price facts (arithmetic domain), learned independently:
ev_teach (201,81,231),(231,81,261),(261,81,291); ev_query
(201,91,291) promotes MAP_X with relseq [81,81,81]. X outputs a scalar
total.

Y = ALLOC budget procedure (planning domain), learned independently:
ev_teach (301,82,311),(311,82,321),(321,82,331); ev_query
(301,92,331) promotes MAP_Y with relseq [82,82,82].

Z world: accumulate three prices, then allocate twice:
(101,81,102),(102,81,103),(103,81,104),(104,82,105),(105,82,106);
query (101,70,106). Y's trained 3-step interface does not fit the
2-step world: a genuine length (interface arity) mismatch.

The mismatch defeats the FULL unified pipeline, not a weakened one:
C (relseq [82,82,82] unsatisfiable from frontier 104), A (no plen-4
fact path from 104; MAP_Y contract is plen 4), B (ordering only),
trial (full path needs plen 6; chain pass caps at plen 5).

## Per-bar results (frozen bars K1-K11)

- K1 (A1 L2-TREAT): PASS. ans=106; adapted MAP 117 with type-16 edge
  117->MAP_Y (45) and relseq [82,82]; MAP_Z (139) LINK14 to 117 and
  to MAP_X (27); no LINK14 MAP_Z->MAP_Y; exactly one adapted MAP.
  All 7 assertions p1-p7 = 1.
- K2 (A2 L2-XDEPTH): PASS. Y trained with FOUR steps
  ([82,82,82,82]); truncation depth not hardcoded: longest-first
  tried Lp=3 (rejected: only two r82 facts at frontier), promoted
  Lp=2. ans=106; adapted MAP 161 src=MAP_Y (85), relseq [82,82];
  MAP_Z LINK14 to adapted and to MAP_X, none to native Y.
- K3 (A3 L2-IMPOSSIBLE): PASS. ans=-2; zero type-16 edges
  workspace-wide. The operator fired, found no licensable prefix
  (dead end at 104), created nothing: clean reject, no hallucinated
  truncation.
- K4 (A4 L1-REGRESSION): PASS. Full-length world, query
  (101,70,107): ans=107; zero type-16 edges (operator never fired;
  exact composition won with COMP-SEGS n=2 27 45); MAP_Z LINK14 to
  MAP_X and MAP_Y.
- K5 (A5 NO-ADAPT CONTROL): PASS. A1 setup verbatim under the
  one-line no-adapt build (adapt_on 1 -> 0): ans=-2, zero adapted
  MAPs. The exact pipeline (activate, rebind, compose, trial,
  bootstrap) provably cannot solve the mismatch task; the adaptation
  operator did the work.
- K6 (A6 ABL-X, A7 ABL-Y, A8 FRESH): PASS. All ans=-2. Z causally
  depends on X (no first segment without it) and on Y (nothing to
  truncate without it); the fresh learner fails outright.
- K7 (A9 REUSE): PASS. Both queries ans=106; adapted count 1 after
  the first query and still 1 after the second (Z persists via its
  taught fact; activate retrieves it; no spurious re-adaptation).
- K8 (determinism): PASS. 3/3 byte-identical runs for both binaries.
  sha256: xd_run1.txt
  595cb3d70cdfcf484ab73feeb95c37e7a59bc16c871d6e82630f04ea84658d64 ;
  xd_noadapt_run1.txt
  afe05166f464fcf6e6d93160634836ac379cf8f7cee6ca7d19bc99dc3818876f.
- K9 (no em/en dashes): PASS, byte-verified across all deliverables.
- K10 (frozen sources): PASS. un_patch.zag sha256-identical to
  composition_unified/un_patch.zag
  (3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2);
  cc_base.zag never modified (read-only, build concatenation only).
  The no-adapt build differs from the treatment build by exactly one
  line (diff verified: adapt_on 1 -> 0).
- K11 (architecture): PASS. 0 new edge types (uses 1,2,6,8,13,16;
  16 is the established adapted-from type), 0 new node types (tag 20
  only), 0 new opcodes, 0 modes, 0 bridges, 0 handlers, 0 semantic
  cases. All machinery pre-exists in base + unified patch.

## Adaptation white-box trace (A1, from xd_run1.txt)

The decision is traceable to learner state at every step:

```
ADAPT-TRY
TRUNC-FRONTIER m1=27 v1=104
TRUNC-TRY m2=45 Lp=2 v1=104
ADAPT-MK id=117 src=45 len=2
TRUNC-FRONTIER m1=45 v1=104
TRUNC-TRY m2=27 Lp=2 v1=104
TRUNC-TRY m2=27 Lp=1 v1=104
ADAPT-CREATED n=1
COMP-SEGS n=2 27 117
```

Reading: after rebind (tried=2 rejected=2) and compose (COMP-FAIL)
failed, the operator anchored at first-segment endpoint v1=104
(MAP_X=27 satisfied from s=101). It tried truncating MAP_Y=45 to
its longest proper prefix Lp=2, licensed it against the fact store
((104,82,105),(105,82,106)), execution-verified the assembled chain
to its own terminal, and promoted adapted MAP 117 with a type-16
edge to 45. The reverse attempts (truncating MAP_X at the same
frontier) were tried and cleanly rejected (no r81 facts from 104).
The unchanged compose_try then re-ran and solved with segments
[27, 117]. No relation, MAP, length, or query is named in the
operator; the truncation depth came from the fact store.

## Key numbers

- Tries to solution (A1 Z query): rebind tried=2 rejected=2;
  compose failed; adapt created 1 MAP; recompose tried=3 rejected=2,
  solved. No-adapt control: identical pipeline through compose, then
  trial and bootstrap, ans=-2.
- Ablations: ABL-X -2, ABL-Y -2, FRESH -2, IMPOSSIBLE -2 (zero
  adapted), REGRESSION 107 with zero adapted, REUSE 106/106 with
  adapted count stable at 1.
- Cognition lines added: 180 (trunc_patch.zag, non-blank
  non-comment). No base/patch modifications.

## Amendment note (transparency)

The originally frozen mismatch (rename 82 -> 83) was withdrawn by
PREREG_AMENDMENT1 before any implementation commit: a pilot build
showed the unified composition's contract fallback (mechanism A)
solves the rename directly (ans=106, COMP-SEGS n=2 27 40, zero
adaptation fired), so the rename does not require adaptation under
the current architecture. The amended length mismatch defeats
A+B+C+trial jointly, and the TRUNCATE-TAIL operator is something
none of the existing mechanisms can do. Testing the rename against
a C-only base was rejected as manufacturing the need by disabling
architecture.

## Files

All under docs/lab/research-lead/overnight-20260928/xdomain_l2_adapt/:
NAMECHECK.md, PREREG.md, PREREG_AMENDMENT1.md, trunc_patch.zag,
trunc_patch_noadapt.zag, xd_driver.zag, xd_driver_noadapt.zag,
un_patch.zag (verbatim copy), xd_full.zag, xd_full_noadapt.zag,
xd_bin, xd_bin_noadapt, xd_compile.txt, xd_compile_noadapt.txt,
xd_run1/2/3.txt, xd_noadapt_run1/2/3.txt, REPORT.md.

Commits stay local. Nothing pushed. Paper untouched.
