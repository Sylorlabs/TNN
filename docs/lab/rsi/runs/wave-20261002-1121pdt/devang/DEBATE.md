# DEBATE.md - DEVANG6 Mandatory Debate Group Transcript

Wave: wave-20261002-1121pdt. Lane: DEVANG (queue item 4).
Rule: advocate / skeptic / judge with provenance probe.

## Provenance probe (skeptic opens)

SKEPTIC: What is new in DEVANG6 vs inherited? Specifically: is there ANY
mechanistic novelty, or is this DEVANG5 with a new bar and new test data?

ADVOCATE: Nothing mechanistic is new, and that is disclosed, not hidden.
devang6.zag differs from devang5.zag by exactly 2 comment lines (banner);
the compiled binary is byte-identical (sha256
a11bd3506987a83ee2f502a78e9af686e92b6cf53ff89d4b950e5dbb3d1e03df).
What is new: (1) the recalibrated K_ABL bar (gap >= 4, frozen in
RECALIBRATION_K_ABL.md + PREREG_DEVANG6.md before implementation);
(2) three fresh sealed families (B-tripleprime seed 888021, C-tripleprime
seed 888022, E-prime fresh tuples); (3) the sealed evaluation itself.

SKEPTIC: So DEVANG6 is a measurement wave, not a mechanism wave. Then the
verdict cannot credit any mechanism; it can only validate the bar and report
fresh measurements. Do you agree?

ADVOCATE: Agreed. DEVANG6 claims no mechanism. Its outputs are: (a) the
recalibrated K_ABL is validated as a working bar (gap 7 >= 4 on a fresh
draw, with the honesty arguments holding); (b) fresh measurements of the
unchanged mechanism (K_SEG 12/12, K_SEAL 9/20, K_DISC 6/6); (c) an honest
BUILD-FAIL on K_SEAL.

## The K_ABL recalibration

SKEPTIC: The recalibration was motivated by DEVANG5's leg-1 failure being
ruled bar-miscalibration. Isn't there a risk that the new bar was tuned,
consciously or not, to pass on the expected fresh data?

ADVOCATE: The four honesty arguments are frozen pre-implementation: (1) the
gap is the purpose-fit quantity; (2) the new bar is STRICTER against vacuous
front-ends (fails gap-1, old bar passed it); (3) threshold 4 is 2 below the
observed gap 6 (anti-fit margin); (4) decided on fresh data. On the fresh
B-tripleprime draw, gap = 7, passing with slack. Crucially, the OLD bar would
also have passed this draw (5/12 <= 5/12), so the recalibration did not
manufacture the pass.

SKEPTIC: But the old bar passing at exactly 5/12 shows this draw was kind.
Would the new bar have passed on DEVANG5's draw? Gap was 6 >= 4, yes. So both
bars pass both draws except DEVANG5 leg-1 where the old bar failed. The
recalibration's practical effect is to forgive DEVANG5's leg-1. Is that not
retroactive leniency?

ADVOCATE: It would be, if the old bar had been measuring the right thing.
But the old bar measured the null's absolute score, which is confounded by
word-length composition (B-doubleprime's 3-char-heavy words handed fixed-3
six free utterances). The gap measures what the ablation removes. Forgiving
a failure of a WRONG bar is not leniency; it is correction. And the new bar
is demonstrably stricter where it matters (gap-1 vacuous case).

JUDGE: The recalibration stands. It is validated, purpose-fit, and stricter
against the relevant failure mode. Attack C (red team) fails.

## The K_SEAL failure

SKEPTIC: 9/20 < 12/20. The mechanism is unchanged from DEVANG5 (14/20).
You classify this as a mechanism result, not miscalibration. But the test
was made harder (prefix ambiguity) than the calibration family. Isn't that
moving the goalposts within the wave?

ADVOCATE: The goalposts (12/20) did not move; they were frozen before the
test existed. The TEST was adversarial by design (K_SEAL's purpose). The
prefix ambiguity is disclosed. More importantly, the learner <= C2 pattern
holds across all three C-families (12v14, 14v14, 9v11), with and without the
ambiguity stress. The capability gap (no advantage on all-novel vocabulary)
is real and pre-existing; C-tripleprime just made it undeniable.

SKEPTIC: The draw variance (12, 14, 9) means a single draw can't reliably
place the learner relative to 12/20. Should the verdict not be
INCONCLUSIVE rather than BUILD-FAIL?

ADVOCATE: No. The bar is absolute (9 < 12), the run was valid, and the
pattern across draws supports a real gap. INCONCLUSIVE would be appropriate
if the measurement were invalid; it was valid but noisy. The honest verdict
is BUILD-FAIL with a noted variance caveat and a queued multi-draw
calibration for a future wave. Softening to INCONCLUSIVE would be
bar-weakening by another name.

JUDGE: BUILD-FAIL stands. The variance caveat is recorded; the kill is not
overturned. A future wave may recalibrate K_SEAL via a proper multi-draw
study, but this wave's bar is frozen and the failure counts.

## The floorcheck incident

SKEPTIC: A measurement tool was silently wrong (12/12 vs true 7/12) due to
a compiler miscompile. How do we know the OTHER tools (scoree, the sealed
binaries) are not similarly miscompiled?

ADVOCATE: Three lines of defense. (1) The miscompile pattern (`!(A && B)`
in while conditions) was grep-verified absent from devang6.zag,
genseal6.zag, and scoree.zag; it appeared only in floorcheck.zag (new code).
(2) The sealed binaries are byte-identical to DEVANG5's frozen binary,
whose outputs were extensively cross-checked in DEVANG5 (K_DISC predictions
confirmed, Family A dev reproduced). (3) The error was CAUGHT by an internal
consistency check (lemma vs measurement), which is evidence the verification
process works. Additionally, the corrected floor (7/12) is exactly consistent
with the ablation (5/12), closing the loop.

SKEPTIC: Acceptable. But this is the FOURTH pinned-znc miscompile. At what
point does the toolchain become unfit for sealed evaluation?

ADVOCATE: That is a governance question above this lane. Noted for the
coordinator: four independent miscompile patterns in the pinned znc now
documented in AGENTS.md. The mitigations (pattern greps, byte-verification,
consistency checks) held this wave, but the trend is concerning.

## Final judgment

JUDGE: DEVANG6 verdict: BUILD-FAIL on K_SEAL (9/20 < 12/20), classified as a
mechanism result. The recalibrated K_ABL PASSES (gap 7 >= 4) and is validated
as an honest bar. No mechanism is credited (none was proposed). The
floorcheck incident is resolved without affecting sealed results. The debate
upholds the red-team findings (all attacks fail) and the kill classification.
Queued next: multi-draw K_SEAL calibration; independent-adversary replication
of K_SEG/K_SEAL/K_ABL; investigation of the learner's C-family deficit
(never beats fixed-3 on novel vocabulary).
