# PREREG H-PI-REV2-F3a2: Independent-Adversary Re-freeze (FROZEN)

**Date:** 2026-09-30 (wave-20260930-0521pdt, first act)
**Parent prereg:** PREREG_PI_REV2_F3.md (frozen d80106155,
wave-20260930-0221pdt). That wave's F3a run used adversary byte 'w'
and recorded BUILD-FAIL on K-F3-4 (bar text): 'w' occurs in the
frozen F1-reuse fixture "xqw". The kill was bar-design, not
mechanism: the white-box trace was clean on K-F3-1/2/3.
**Authority:** debate wave-20260930-0221pdt, judge motion M5 (AMEND):
"Re-freeze F3a with corrected K-F3-4 text and a byte from {k,m,r,v},
then re-run; then step 4 (independent reproduction) follows."
**Frozen implementation:** pi_rev2/proc_revise2.zag (committed
847a8f10f, wave-20260929-2321pdt). NOT modified this wave. This
prereg is an evaluation freeze only.
**Status:** FROZEN. Committed alone, before any F3a2 run, build, or
audit. No amendments after the freeze commit.

## Provenance header (machine-checkable, standing rule 2026-09-23)

- RENDER_SHA: N/A (no render; pure Zag experiment).
- FIRST_RENDERED_WAVE: N/A.
- COMPONENT_LINEAGE: prereg text new this wave; implementation
  inherited from 847a8f10f (unchanged this wave); fixtures T/F1/R
  inherited from PREREG_PI_REV2.md; F2 evidence and F3a evidence
  inherited from waves 20260929-2321pdt and 20260930-0221pdt;
  debate M5 of 0221pdt inherited as authority.
- NEW_KNOWLEDGE_CLAIM: the corrected F3a re-freeze is a second
  post-freeze adversary-byte first-letter world for the frozen
  H-PI-REV2 binary, under the corrected disjointness bar.

## What this prereg is and is not

This prereg freezes the corrected re-run the judge ordered. It is NOT
a new implementation. It is NOT a promotion verdict: on all bars
passing the verdict is BUILD-PASS (bounded revising mechanism holds
on a second adversary-chosen byte), never SURVIVES. It does NOT claim
the adversary is a separate human: the wave runner acts as the
adversary under a declared zero-discretion selection rule (disclosed
residual; the standing S1 concern about researcher-shaped kits stays
live for the pipeline's independent red team at step 10).

## Corrected disjointness audit (the 0221pdt finding)

The parent prereg's allowed-set disjointness rationale was
inaccurate. The 0221pdt audit established: only {i,k,m,r,v} are
genuinely absent from all frozen fixture inputs. 'i' was spent on the
F2 run; 'w' was spent on the F3a run (and killed K-F3-4 by occurring
in the F1-reuse fixture "xqw"); j,l,n,o,t,u occur in R inputs.
This prereg corrects K-F3-4 text to name the true disjointness bar
and audits the adversary byte against all prior fixture inputs,
including the executed F2 and F3a adversary fixtures.

## Adversary byte selection rule (declared before any run)

The corrected allowed set is {k,m,r,v}. The F3a2 adversary byte is
the LAST letter of the set in sorted byte order: 'v' (byte 118).
The rule is deterministic and declared here; no discretion remains
at execution.

## F3a2: second adversary-byte first-letter world (executable this wave)

Interface: the frozen binary's committed P8 argv convention
(argv[1]="v", single byte from the corrected allowed set). Instance:
("vab" -> "vvv"); reuse probe ("vqv" -> "vvv"). The binary runs its
full frozen P0-P7 prefix, then the P8 phase with c='v', then P9.

Frozen kill bars:

- **K-F3-1 (first-execution correctness).** On the first F3a2
  execution (exit 0, fails=0): COUNTEREXAMPLE_DETECTED("vab");
  DIAGNOSIS pos=0 byte=118 conflicts=0; PRIMITIVE-CONSTRUCTED
  (0,118); alt = index 2 (C0 broadcast-first); v4 ACTIVE with parent
  v3; "vab"->"vvv"; priors unchanged ("wab"->"www", "xab"->"xxx",
  "abc"->"ccc", "xy"->"xx", "defg"->"gggg"); reuse "vqv"->"vvv"
  with no new revision; R cell 8/8 after F3a2.
- **K-F3-2 (determinism).** Three full executions with argv[1]="v"
  are byte-identical (P0-P7+P8(v)+P9 output).
- **K-F3-3 (anti-tuning).** Grep audit of the committed
  implementation (847a8f10f): zero char literal 'v'; zero string
  literals "vab", "vvv", "vqv"; zero numeric literal 118; the byte
  'v' reaches machinery only through the argv data flow
  (allowed-set membership check, f2in/f2out construction).
- **K-F3-4 (disjointness, corrected).** 'v' occurs in none of:
  (a) the frozen T, F1, or R fixture inputs of PREREG_PI_REV2.md;
  (b) the executed F2 adversary fixture inputs ('i' fixtures);
  (c) the executed F3a adversary fixture inputs ('w' fixtures:
  "wab", "wqw", "www"). Audit of the frozen fixture strings and
  the F2/F3a evidence files. Kill: any occurrence of the byte 0x76
  in any of those.

Verdict on all four passing: BUILD-PASS (bounded revising mechanism
holds on a second adversary-chosen byte; S1 narrowed further, not
closed). Any bar failing: BUILD-FAIL with the killing line cited.

## F3b (non-first-letter world ("abz"->"zzz"), S4 stress)

Design stays FROZEN-DESIGNED from PREREG_PI_REV2_F3.md (inherited,
not re-frozen here). Execution remains deferred: the frozen binary's
committed P8 interface cannot express it; the interface extension
needs its own prereg plus implementation wave.

## Scope and red lines

Pure Zag; pinned znc 498abcb5; zero Python in wave work; no em-dashes
in wave documentation. No frozen bar weakened. The implementation is
not touched. Verdict labels per the reorientation: BUILD-PASS or
BUILD-FAIL only. K-F3-1 is a characterization bar on the frozen
trace; it does not certify mechanism correctness beyond the bar text.
