# RESULT_F3A3.md

Wave: wave-20260930-1121pdt (worker F3A3). Prereg:
PREREG_PI_REV2_F3a3.md (freeze v3, FROZEN, committed alone at
53256838f, this wave's first act). Implementation: inherited
byte-identical from 847a8f10f (wave-20260929-2321pdt); NOT modified
this wave (git diff 847a8f10f -- <file> empty; working-tree sha256
dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12
matches the committed blob).

## What was run

The frozen binary was rebuilt from the unmodified source with the
pinned znc (sha256 498abcb5ab34...; build emitted the one benign
pre-existing analyzer lint A0102 on an ignored loadseq return,
reported at line 607 this build; source byte-identical to the
committed blob, so pre-existing by construction). Three executions
with argv[1]="v" (adversary byte per the F3a2 declared rule, last
letter of the corrected allowed set {k,m,r,v}), outputs in
EVIDENCE_F3A3_run{1,2,3}.txt. Binaries kept in /tmp (not committed).

## Evidence

3/3 byte-identical (sha256
b5389d713357d37bd5ca9c05b781e80d57a3a764f3cac60ebe1cd17de9527c8e),
exit 0, empty stderr, "=== RESULT fails=0 ===" and "BUILD-PASS"
on all three. cmp confirms each F3a3 run is byte-identical to the
inherited F3a2 evidence file (EVIDENCE_F3A2_run{1,2,3}.txt): the
re-run requirement is met, and determinism is re-demonstrated on
the same frozen binary.

## K-F3-1 scorecard (corrected text, first execution)

- COUNTEREXAMPLE_DETECTED(vab): present. PASS.
- DIAGNOSIS pos=0 byte=118 conflicts=0: present. PASS.
- PRIMITIVE-CONSTRUCTED pos=0 byte=118: present. PASS.
- CHECK P8-F2-alt-C0: PASS (certifies alt2==2, C0 broadcast-first):
  present. PASS.
- VERSION v3 ACTIVE (parent v2): present; no "VERSION v4" anywhere
  in the output. PASS.
- "vab"->"vvv" ("PREDICT vab -> vvv [ok]"): present. PASS.
- priors unchanged: "xab"->"xxx", "abc"->"ccc", "xy"->"xx",
  "defg"->"gggg" all present [ok]; no "wab" anywhere. PASS.
- reuse "vqw"->"vvv" with no new revision ("CHECK
  P8-F2-reuse-no-revision: PASS" then "PREDICT vqw -> vvv [ok]"):
  present. PASS.
- R-probe retention 8/8 named explicitly, all [ok]: "zag"->"ggg",
  "12"->"22", "q"->"q", "hello"->"ooooo", "ptc"->"ccc",
  "s"->"s", "eghjjupazbnf"->"ffffffffffff", "q"->"q". PASS.

K-F3-1: PASS under the corrected freeze-v3 text. Every corrected
line matches the frozen trace exactly.

## K-F3-2 / K-F3-3 / K-F3-4 (inherited)

- K-F3-2 (determinism): PASS. 3/3 byte-identical this wave
  (re-demonstrated); byte-identical to the inherited F3a2 evidence.
- K-F3-3 (anti-tuning): inherited verified PASS from F3a2 (zero
  char literal 'v'; zero "vab"/"vvv"/"vqv"; zero 118; argv data
  flow). Supplementary grep this wave on the committed blob:
  zero "vqw", zero 'v', zero 118; the reuse probe is assembled
  from "qw" literals plus the argv byte (source lines 807-808).
  No new finding; the inherited verdict is untouched.
- K-F3-4 (disjointness): inherited verified PASS from F3a2.

## Verdict

BUILD-PASS per the frozen verdict rule. The bounded revising
mechanism holds on the adversary-chosen byte under corrected
K-F3-1 text (v3 ACTIVE parent v2; vqw reuse probe; wab dropped;
8 R probes named explicitly). S1 narrowed further, not closed.
Labels per the reorientation: BUILD-PASS only, never SURVIVES.

## Step 4: independent reproduction from committed source

Source extracted with git cat-file from commit 847a8f10f
(sha256 dd3cb02d..., 840 lines, matches the working tree and the
committed blob), built with the pinned znc in /tmp, run three
times with argv[1]="v". All three repro runs: exit 0, empty
stderr, sha256 b5389d713357..., each cmp byte-identical to the
corresponding F3a3 evidence file. Reproduction: YES, byte-identical.

## Provenance header (machine-checkable, standing rule 2026-09-23)

- RENDER_SHA: N/A (no render; pure Zag experiment).
- FIRST_RENDERED_WAVE: N/A.
- COMPONENT_LINEAGE: prereg text new this wave (freeze v3,
  corrected K-F3-1; 53256838f); F3a3 evidence runs and this result
  doc new this wave; implementation inherited from 847a8f10f
  (unchanged); fixtures T/F1/R inherited from PREREG_PI_REV2.md;
  F2 evidence inherited from wave-20260929-2321pdt; F3a evidence
  and debate M5 inherited from wave-20260930-0221pdt; F3a2
  evidence, verification, and K-F3-2/3/4 verdicts inherited from
  waves 20260930-0521pdt and 20260930-0821pdt.
- NEW_KNOWLEDGE_CLAIM: K-F3-1 measured PASS against corrected text
  on the same frozen binary; step-4 independent reproduction
  confirmed byte-identical from committed source.

## Governance notes

STRICT-LETTER CAVEAT: the implementation commit predates the
re-freeze prereg; the re-freeze route was authorized by the
0221pdt debate motion M5. Commit order this wave: prereg
(53256838f) strictly precedes all evidence and result commits;
no implementation commit exists after the prereg (implementation
847a8f10f unmodified; diff empty). Pure Zag; pinned znc
498abcb5; zero Python; shell/git for orchestration only.

No em-dashes in this documentation.
