# PREREG COMP2-P11: Rotated-Author Re-test on a Fresh Sealed Set with the Stemmer Contingency (DRAFT FOR FREEZE)

Wave: wave-20260927-0821pdt, lane 3 (prereg design).
Status: DRAFT. This document is not frozen. It becomes frozen only when a
future wave adopts it as its prereg freeze commit. Until then, numbers may
change by redraft only, never by post-freeze edit.
Freeze commit: PENDING (to be recorded at freeze time).
Prereg design commit (lane 3, this wave): 59b9df4b0b45ffef23704ad971ae9029e14d7126.

## 1. Provenance header (machine-checkable)

COMPONENT_LINEAGE:
- CLAIM-VERIFY-1: ADOPTED wave-20260924-1121pdt (24/30 sealed honest
  resolutions, 0 unflagged confabulations).
- CV-1 decline-citation fix: ADOPT [RE-CERT] wave-20260924-1721pdt.
- CV-P stemmed-coverage gate: PARTIAL wave-20260925-0521pdt, CONFIRMED on
  rotated fresh set wave-20260925-0821pdt (adoption barred pending Micah's
  ruling 6, untouched here and untouched by this prereg).
- COMP-2 entity-bridged 2-fact composition, wave-20260925-1121pdt: MODIFY
  to PARTIAL [STACK], prereg ADOPT mapping VOID per P10 (the mapping
  rested on the materially false premise "adopted CV-P" for a PARTIAL
  base). The red team recorded the evidence as stemmer-contingent three
  levels deep (trigger, coverage sets, key): the numbers are provisional
  until ruling 6. Residuals: M5 author/implementer separation not met
  (self-attested, one session); no committed B5 transcripts; narrow probe
  templates (generality unproven); AUTHORING.md accuracy outstanding.
- Precedent P3: missing structural author/implementer separation caps at
  PARTIAL; a rotated-author re-test on a fresh sealed set is required
  before any adoption consideration.
- Precedent P11: stemmer-contingency records as [STACK] with
  re-derivation, not re-vote. When measured numbers depend on a
  ruling-gated component's logic at load-bearing levels, an adverse
  ruling requires re-deriving the evidence (key included) with clean
  logic, not re-voting the committed numbers.

NEW_KNOWLEDGE_CLAIM: none. This prereg re-tests the 1121pdt composition
capability claim under independent-discovery conditions. It decides
nothing about ruling 6.

Inherited: the comp2 mechanism spec (PREREG_COMP2_1121.md sections 2 and
4, the S11 decision-invariance proof carried verbatim), the frozen KB
(SHA-256 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1),
the pinned gazetteer, the F9-COMP authoring spec (carried, with the
narrow-template widening option in section 8), and the pinned toolchain
src/tools/toolchain/znc_linux_x86_64_abed8aa1 (SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
New: the rotated-author structure, the fresh sealed set, the two-leg
stemmer plan, and COMP-B7/COMP-B8.

## 2. Question

Does entity-bridged 2-fact composition hold up as an independent
discovery (not rule-implementation fidelity) on a fresh sealed set, under
a stemmer lineage that survives either outcome of ruling 6?

## 3. Mechanism (carried, frozen scope)

The candidate is the 1121pdt comp2 mechanism, rebuilt from the frozen
spec: pair deliberation fires only on single-fact decline; candidate
pairs (F,G) with F<G share at least one gazetteer entity; the first
lowest-index covering pair wins; emission is both facts byte-verbatim
with one space between. The single-fact path is behavior-identical to
the frozen deliberate_cv1. The S11 decision-invariance proof from
PREREG_COMP2_1121.md section 4 is carried verbatim and is not re-argued
here.

## 4. The two-leg stemmer contingency (P11, frozen)

Gate zero (frozen): NO implementation commit until Micah renders ruling
6. The prereg freezes now; execution waits on him. This prereg does not
touch ruling 6's content, does not relitigate it, and does not narrow it.

Leg R (ruling 6 favorable to Python-mirror-developed logic): the re-test
proceeds with the existing stemmer lineage, honestly annotated as
Python-mirror-developed in the provenance header. The 1121pdt 20/20 stays
[STACK]-conditional and is superseded by the new numbers.

Leg A (ruling 6 adverse to Python-mirror-developed logic): full
re-derivation with an independently developed stemmer. The new stemmer
is written in pure Zag from a natural-language stemming specification,
without reference to the Python mirror or to the CV-P stemmer sources;
trigger sets, coverage sets, and the answer key are re-derived under the
new stemmer. The 1121pdt 20/20 is retired, not re-voted (P11). Under Leg
A, every number in the new evidence must be reproducible from the clean
stemmer alone; any byte shared with the retired lineage voids the run.

The Python-mirror gate is kept explicitly: under either leg, adoption of
any COMP-2 result remains gated on ruling 6 having been rendered and on
the leg matching its outcome. A PASS under the wrong leg is VOID.

## 5. Rotated author, fresh sealed set (P3, M5)

The probe author is a different worker than the implementer (rotated:
neither authored the 1121pdt set). The author has not read the comp2
implementation; the implementer has not seen probe bytes. Both attest in
the seal attestation (dual attestation, not single-session
self-attestation). The fresh sealed 30-probe set (20 COMP, 10 UNANS) is
authored post-freeze from F9-COMP and committed sealed before any
implementation commit; SHA-256 pinned in the seal commit. Commit order:
prereg freeze, then seal, then implementation, strictly.

## 6. Metric it moves

Capability breadth (metrics priority 5): compositional question answering
over the frozen KB, measured as independent discovery rather than
spec fidelity. Current verified number: the 1121pdt 20/20, recorded as
stemmer-contingent [STACK], provisional, and not cited as a baseline
because the bars are absolute.

## 7. Cost budget

10x per-turn mean op count versus the adopted cvp binary on the fresh
sealed 30 probes, under the identical counting discipline. Exceeding 10x
is DEAD. Cost is compute only.

## 8. Kill bars (frozen; never moved after the seal)

COMP-B1 (composition recall): at least 14/20 COMP probes answered with
the key's expected fact pair, both facts byte-verbatim in index order
with exactly one space between. Fewer than 14 means DEAD.
COMP-B2 (no spurious composition): 10/10 UNANS probes decline through
the frozen decline path (no pair emitted). Any emitted pair means DEAD.
COMP-B3 (single-fact no regression): 17/17 inkb17.txt turns byte-identical
between the cvp rebuild and the candidate on identical fresh-conversation
inputs. Any deviation means DEAD.
COMP-B4 (cost): candidate per-turn mean ops at most 10x the cvp per-turn
mean ops on the fresh sealed 30, identical counting discipline.
Exceeding the budget means DEAD.
COMP-B5 (determinism): 3/3 full sealed runs byte-identical (transcripts
plus op-count streams). Zero RNG in any decision path (static check).
Zero Python contact with any wave artifact. Any nondeterminism means the
run does not count; a second nondeterministic run means DEAD.
COMP-B6 (seal integrity): sha256 of the sealed PROBES.md and KEY.md at
scoring time equal the pinned values from the seal commit; the seal-open
log is filled at scoring time, not retroactively; static grep confirms
no sealed probe bytes in the candidate sources, KB, build scripts, or
scorer; the candidate binary never reads KEY.md. A seal breach or any
Python contact means VOID.
COMP-B7 (author/implementer separation, new): author and implementer are
different workers with dual attestation in the seal attestation; the
authoring-time enumerator shares no code with the candidate (verified by
diff of the tool sources). Single-session self-attestation means VOID.
COMP-B8 (transcripts, new): B5 transcripts and op logs for all 30 probes
committed with the evidence. Missing transcripts means CANNOT-CONFIRM.

Verdict mapping (frozen): all bars PASS means the COMP-2 evidence is
re-certified as PARTIAL with M5 closed and the 1121pdt residuals cleared.
It does NOT mean ADOPT: the prereg ADOPT mapping stays VOID per P10, and
any adoption consideration remains gated on ruling 6 plus Micah's
decision (the standing boundary). Any bar FAIL means DEAD with killing
evidence. UNVERIFIABLE only on a named, pre-specified condition: (a)
commit-order failure; (b) seal breach under COMP-B6; (c) any Python
contact with a wave artifact; (d) wrong-leg execution under section 4.

## 9. F9-COMP widening option (frozen choice, made before freezing)

The 1121pdt red team flagged narrow probe templates (generality
unproven). Before freezing, the freezing wave either carries F9-COMP
verbatim (documenting the generality limitation again) or adopts the
frozen widened variant: interrogative forms beyond the 1121pdt set are
admitted provided each probe still satisfies F9.1-F9.8 and the key's
expected pairs are still enumerator-confirmed lowest valid pairs. The
choice is recorded in the freeze commit; it cannot change after.

## 10. Red-team confound list (considered before this draft freezes)

1. Key/candidate circularity: the key's expected pairs come from the
frozen spec plus the independent authoring-time enumerator, fixed at seal
time; the candidate is implemented after the seal from the same frozen
spec. COMP-B6/B7 guard both halves mechanically.
2. Stemmer lineage at three levels (trigger, coverage, key): the two-leg
design in section 4 is the guard. Under Leg A the red team verifies the
new stemmer was developed without reference to the retired lineage
(commit history and source diff).
3. Template narrowness: section 9 freezes the widening choice.
4. Ruling-6 anticipation: section 4's gate zero forbids implementation
before the ruling; the prereg conditions on the ruling without deciding
it. The red team verifies no implementation commit predates the ruling
record.
5. Single-fact regression: pair deliberation fires only on decline;
COMP-B3 guards it mechanically.
6. S11 decision-invariance: carried from PREREG_COMP2_1121.md section 4;
the red team re-verifies the concrete input still flips decline to
answer under the rebuilt candidate.
7. Pure Zag: no Python anywhere (instruments, harnesses, scorers,
fixture provisioning, /tmp scratch). Any Python contact voids the
evidence. No analysis before the prereg freeze commit.

## 11. Standing rules applied

Pure Zag literally. Frozen kill bars are never moved after the freeze.
Missing evidence means CANNOT-CONFIRM. The prereg freeze commit strictly
precedes the seal commit, which strictly precedes any implementation
commit (commit-order self-check). No em-dashes in this document. The six
governance rulings are untouched (ruling 6 is gated on, never decided
here). The sealed blind judge queue is untouched. Micah's frontier files
are untouched. Nothing is pushed to GitHub; commits stay local on
tnn-native-lab.

## 12. Gate conditions (what this draft waits on)

Gate zero: Micah's ruling 6 must be rendered before any implementation
commit. Then: a rotated author and implementer must be staffed (two
different workers); the fresh sealed set is authored post-freeze. This
draft waits in the queue until then.
