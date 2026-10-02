# PREREG H-PI-REV2-F3a3: Second Corrected Re-freeze (FROZEN, freeze v3)

**Date:** 2026-09-30 (wave-20260930-1121pdt, first act)
**Parent prereg:** PREREG_PI_REV2_F3a2.md (frozen 97d58e38e,
wave-20260930-0521pdt). Freeze lineage: v1 = F3 (d80106155,
wave-20260930-0221pdt), v2 = F3a2 (97d58e38e), v3 = this freeze.
**Why a third freeze:** the 0821pdt independent verification
(F3A2_VERIFICATION.md) killed F3a2 on K-F3-1 bar text while the
mechanism evidence was clean. Four bar-design errors in the v2
K-F3-1 text, each documented against the frozen trace: (1) text
demanded "v4 ACTIVE with parent v3", trace shows "VERSION v3 ACTIVE
(parent v2)"; (2) text demanded reuse "vqv"->"vvv", trace shows
"PREDICT vqw -> vvv [ok]"; (3) text listed prior "wab"->"www",
which belongs to the F3a ('w') run and is absent from a fresh F3a2
execution; (4) text said "R cell 8/8", which is substance-correct
but the literal label never prints. K-F3-2/3/4 were verified PASS
in the same verification and stand as inherited.
**Authority:** wave-20260930-1121pdt worker assignment F3A3. The
re-freeze route was authorized by the 0221pdt debate motion M5
(originally ordered for the F3a K-F3-4 correction; this freeze
applies the same authorized route to the K-F3-1 text correction).
STRICT-LETTER CAVEAT: the implementation commit predates the
re-freeze prereg; the re-freeze route was authorized by the
0221pdt debate motion M5.
**Frozen implementation:** pi_rev2/proc_revise2.zag (committed
847a8f10f, wave-20260929-2321pdt). NOT modified this wave. This
prereg is an evaluation freeze only.
**Status:** FROZEN. Committed alone, before any F3a3 run, build, or
audit. No amendments after the freeze commit.

## Provenance header (machine-checkable, standing rule 2026-09-23)

- RENDER_SHA: N/A (no render; pure Zag experiment).
- FIRST_RENDERED_WAVE: N/A.
- COMPONENT_LINEAGE: prereg text new this wave (K-F3-1 corrected;
  K-F3-2/3/4 text carried unchanged from F3a2); implementation
  inherited from 847a8f10f (unchanged this wave); fixtures T/F1/R
  inherited from PREREG_PI_REV2.md; F2 evidence inherited from
  wave-20260929-2321pdt; F3a evidence and debate M5 inherited from
  wave-20260930-0221pdt; F3a2 evidence and verification inherited
  from waves 20260930-0521pdt and 20260930-0821pdt.
- NEW_KNOWLEDGE_CLAIM: the F3a3 re-run measures K-F3-1 against
  corrected text on the same frozen binary and the same adversary
  world ('v'); K-F3-2/3/4 results are inherited as verified PASS
  from F3a2, not re-adjudicated.

## What this prereg is and is not

This prereg freezes the second corrected re-run. It is NOT a new
implementation. It is NOT a promotion verdict: on all bars passing
the verdict is BUILD-PASS (bounded revising mechanism holds on the
adversary-chosen byte under corrected text), never SURVIVES. It
does NOT claim the adversary is a separate human: the wave runner
acts as the adversary under a declared zero-discretion rule
(disclosed residual; the standing S1 concern about
researcher-shaped kits stays live for the pipeline's independent
red team at step 10).

## Adversary world (unchanged from F3a2)

The adversary byte is 'v' (byte 118), the last letter of the
corrected allowed set {k,m,r,v} in sorted byte order, per the
selection rule declared and executed in F3a2. This freeze does not
re-select a byte; it re-runs the same world under corrected text.
Interface: the frozen binary's committed P8 argv convention
(argv[1]="v"). Instance: ("vab" -> "vvv"); reuse probe
("vqw" -> "vvv"). The binary runs its full frozen P0-P7 prefix,
then the P8 phase with c='v', then P9.

Because the binary and the byte are unchanged, the F3a3 executions
must be byte-identical to the inherited F3a2 evidence (sha256
b5389d713357... per run); a non-identical re-run voids the run and
does not count.

## Frozen kill bars

- **K-F3-1 (first-execution correctness).** On the first F3a3
  execution (exit 0, fails=0): COUNTEREXAMPLE_DETECTED("vab");
  DIAGNOSIS pos=0 byte=118 conflicts=0; PRIMITIVE-CONSTRUCTED
  (0,118); CHECK P8-F2-alt-C0: PASS (certifies alt2==2, C0
  broadcast-first); VERSION v3 ACTIVE (parent v2); "vab"->"vvv";
  priors unchanged ("xab"->"xxx", "abc"->"ccc", "xy"->"xx",
  "defg"->"gggg"); reuse "vqw"->"vvv" with no new revision (CHECK
  P8-F2-reuse-no-revision: PASS); R-probe retention 8/8 after F3a3,
  the eight probes named explicitly with their predictions:
  "zag"->"ggg", "12"->"22", "q"->"q", "hello"->"ooooo",
  "ptc"->"ccc", "s"->"s", "eghjjupazbnf"->"ffffffffffff",
  "q"->"q" (all [ok]).
- **K-F3-2 (determinism).** Three full executions with argv[1]="v"
  are byte-identical (P0-P7+P8(v)+P9 output). Inherited verified
  PASS from F3a2; re-demonstrated by this wave's three runs.
- **K-F3-3 (anti-tuning).** Grep audit of the committed
  implementation (847a8f10f): zero char literal 'v'; zero string
  literals "vab", "vvv", "vqv"; zero numeric literal 118; the byte
  'v' reaches machinery only through the argv data flow
  (allowed-set membership check, f2in/f2out construction).
  Inherited verified PASS from F3a2; text carried unchanged.
- **K-F3-4 (disjointness).** 'v' occurs in none of: (a) the frozen
  T, F1, or R fixture inputs of PREREG_PI_REV2.md; (b) the executed
  F2 adversary fixture inputs ('i' fixtures); (c) the executed F3a
  adversary fixture inputs ('w' fixtures: "wab", "wqw", "www").
  Audit of the frozen fixture strings and the F2/F3a evidence
  files. Kill: any occurrence of the byte 0x76 in any of those.
  Inherited verified PASS from F3a2; text carried unchanged.

Verdict on all four passing: BUILD-PASS (bounded revising mechanism
holds on the adversary-chosen byte under corrected text; S1
narrowed further, not closed). Any bar failing: BUILD-FAIL with
the killing line cited. Verdict labels per the reorientation:
BUILD-PASS or BUILD-FAIL only, never SURVIVES.

## F3b (non-first-letter world ("abz"->"zzz"), S4 stress)

Design stays FROZEN-DESIGNED from PREREG_PI_REV2_F3.md (inherited,
not re-frozen here). Execution remains deferred: the frozen
binary's committed P8 interface cannot express it; the interface
extension needs its own prereg plus implementation wave.

## Scope and red lines

Pure Zag; pinned znc 498abcb5; zero Python in wave work; no
em-dashes in wave documentation. No frozen bar weakened. The
implementation is not touched. K-F3-1 is a characterization bar on
the frozen trace; it does not certify mechanism correctness beyond
the bar text.

No em-dashes in this documentation.
