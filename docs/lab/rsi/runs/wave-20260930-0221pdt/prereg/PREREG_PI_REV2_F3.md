# PREREG H-PI-REV2-F3: Independent-Adversary Family (FROZEN)

**Date:** 2026-09-30 (wave-20260930-0221pdt, first act)
**Parent prereg:** PREREG_PI_REV2.md (frozen 7c11ac5af, wave-20260929-1721pdt).
**Parent implementation:** pi_rev2/proc_revise2.zag (frozen, committed
847a8f10f, wave-20260929-2321pdt). BUILD-PASS as a bounded revising
mechanism; no promotion; L3 criterion 12 and Criterion 0 open.
**Authority:** debate wave-20260929-2321pdt, judge motion M5 (AMEND):
"Next wave: independent adversary designs a post-freeze family (byte of
their choosing, plus at least one non-first-letter diagnosis world),
then the frozen binary is re-run under it; step 4 (independent
reproduction) follows."
**Status:** FROZEN. Committed alone, before any F3 run, build, or audit.
No amendments after the freeze commit.

## Provenance header (machine-checkable, standing rule 2026-09-23)

- RENDER_SHA: N/A (no render; pure Zag experiment).
- FIRST_RENDERED_WAVE: N/A.
- COMPONENT_LINEAGE: prereg text new this wave; implementation inherited
  from 847a8f10f (unchanged this wave); fixtures T/F1/R inherited from
  PREREG_PI_REV2.md; F2 evidence inherited from wave-20260929-2321pdt;
  debate M5 inherited as authority.
- NEW_KNOWLEDGE_CLAIM: the F3 family is a post-freeze adversary family
  for the frozen H-PI-REV2 binary: one adversary-chosen-byte first-letter
  world (F3a, executable now) plus one frozen non-first-letter world
  design (F3b, execution deferred).

## What this prereg is and is not

This prereg freezes the independent-adversary family the judge ordered.
It is NOT a new implementation: proc_revise2.zag is not modified this
wave. It is NOT a promotion verdict: on all bars passing the verdict is
BUILD-PASS (bounded revising mechanism holds on an adversary-chosen
byte), never SURVIVES. It does NOT claim the adversary is a separate
human: the wave runner acts as the adversary under a declared
zero-discretion selection rule (disclosed residual; the standing S1
concern about researcher-shaped kits stays live for the pipeline's
independent red team at step 10).

## Adversary byte selection rule (declared before any run)

The frozen allowed set from PREREG_PI_REV2.md is
{i,j,k,l,m,n,o,r,t,u,v,w} (lowercase letters occurring nowhere in
T/F1/R inputs and not as a first byte of any R input). The F2 run used
'i' (first in sorted order). The F3 adversary byte is the LAST letter
of the set in sorted byte order: 'w' (byte 119). The rule is
deterministic and declared here; no discretion remains at execution.

## F3a: adversary-byte first-letter world (executable this wave)

Interface: the frozen binary's committed P8 argv convention
(argv[1]="w", single byte from the frozen allowed set). Instance:
("wab" -> "www"); reuse probe ("wqw" -> "www"). The binary runs its
full frozen P0-P7 prefix, then the P8 phase with c='w', then P9.

Frozen kill bars:

- **K-F3-1 (first-execution correctness).** On the first F3a execution
  (exit 0, fails=0): COUNTEREXAMPLE_DETECTED("wab"); DIAGNOSIS pos=0
  byte=119 conflicts=0; PRIMITIVE-CONSTRUCTED (0,119); alt = index 2
  (C0 broadcast-first); v3 ACTIVE with parent v2; "wab"->"www";
  "xab"->"xxx", "abc"->"ccc", "xy"->"xx", "defg"->"gggg" unchanged;
  reuse "wqw"->"www" with no new revision; R cell 8/8 after F3a.
- **K-F3-2 (determinism).** Three full executions with argv[1]="w" are
  byte-identical (P0-P7+P8(w)+P9 output).
- **K-F3-3 (anti-tuning).** Grep audit of the committed implementation
  (847a8f10f): zero char literal 'w'; zero string literals "wab",
  "www", "wqw"; zero numeric literal 119; the byte 'w' reaches
  machinery only through the argv data flow (allowed-set membership
  check, f2in/f2out construction).
- **K-F3-4 (disjointness).** 'w' occurs in none of the frozen T, F1, or
  R fixture inputs (audit of the frozen fixture strings).

Verdict on all four passing: BUILD-PASS (bounded revising mechanism
holds on an adversary-chosen byte; S1 narrowed, not closed). Any bar
failing: BUILD-FAIL with the killing line cited.

## F3b: non-first-letter diagnosis world (frozen design, execution deferred)

The frozen binary's committed P8 interface cannot express a
non-first-letter instance (it hardcodes f2in = c+"ab" and asserts
pos==0). Extending the interface requires an implementation edit, which
is out of scope for this wave (this wave re-runs the frozen binary;
it does not modify it). F3b is therefore frozen HERE as a family
design; its execution is queued for a future wave under its own prereg
for the interface extension. Freezing the design now (post-freeze,
per judge M5) prevents the future builder from fitting the family to
observed behavior.

- **F3b-1:** after the frozen P0-P7 prefix (v2 = IF(P_x, C0, v1)
  ACTIVE), the failing example is ("abz" -> "zzz"). Monitor: v2
  predicts "bbb" (P_x false at pos 0; v1 broadcast-last), actual
  "zzz", so COUNTEREXAMPLE_DETECTED("abz") is expected. Diagnosis
  candidates over F={"abz"}: (0,'a'), (1,'b'), (2,'z'). The frozen
  position-ascending rank predicts (0,'a') with conflicts recorded
  ("abc" has 'a' at 0). This world is the S4 stress: the rank is
  unprincipled outside first-letter worlds, and this is the world
  that exposes it.
- **Frozen F3b bars (measurement protocol, not prejudged outcome):**
  B-F3b-1 determinism (3/3 byte-identical); B-F3b-2 trace completeness
  (diagnosis emitted with the conflicts list; construction and
  revision lines present or CANNOT-DIAGNOSE emitted); B-F3b-3 the
  verdict debate records which (p,b) the frozen rank selected and
  whether the S4 bias is confirmed or surprised. No pass/fail on
  correctness: the family characterizes the bias, it does not certify
  the mechanism.

## Scope and red lines

Pure Zag; pinned znc 498abcb5; zero Python in wave work; no em-dashes
in wave documentation. No frozen bar weakened. The implementation is
not touched. Verdict labels per the reorientation: BUILD-PASS or
BUILD-FAIL only for F3a; F3b is recorded FROZEN-DESIGNED with execution
queued, not a verdict.
