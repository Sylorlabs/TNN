# ADVOCATE BRIEF: wave-20260925-0821pdt verdict slate

Role: ADVOCATE. This brief argues FOR each coordinator verdict on the
evidence as written. Standard: a verdict stands unless cited evidence
overturns it; frozen bars are never weakened; Micah's six pending
governance rulings are not re-litigated here.

## Item 1. Fork battery: CONFIRM [RE-CERT], 29/29 PASS

The battery is sound and the verdict is accurate for what was tested.

29/29 forks report the identical pass vector, grepped across all 29
full.logs with no exceptions: B1 compile/run stdout byte-matches
"FORKBATTERY-OK 42"; B2 rerun and recompile-identical (cmp clean);
B3 `znc check --strict --no-zagd` exit 0; NEG1 fails compile and check
as required; NEG2 compiles and checks but stdout differs as required;
PROBE byte-matches "R32_ZNC_PROBE_OK"; harness VERDICT=PASS exit 0 on
all 29. znc sha256 matches the pinned sha
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
on every fork. The pure-Zag harness was rebuilt from source extracted
read-only from the 2321pdt archive (extracted sha f38d9154... matches
expectation) and the built binary is byte-identical to last wave's
harness: the build is deterministic and provenance is intact.

Enumeration was fresh (`git branch -a`, `git worktree list`), not
stale lists: 4 live forks (tips moved since last wave, including the
new 0521pdt archive branch at 0ee06268e9) plus 25 fixture forks for
coverage. Duplicates are explicitly named, not hidden.

The origin-tip anomaly is disclosed plainly with verbatim SHAs: the
tip moved mid-run from 4d613edb1 to 40935c121b; both entries for the
run-start tip PASS; the new tip is recorded as a CANNOT-CONFIRM item
with a next-wave pickup request; local HEAD was unchanged at
382f70f955 the whole run, so no re-run was needed. Zero Python contact
by the worker. The verdict claims exactly what the evidence supports:
the run-start tip passed; the new tip is untested this wave. That is
the honesty standard working, not a hole in the battery.

## Item 2. ST-1 pristine re-verification: DEAD [NEW]

The killing evidence is valid and the bars were properly frozen.

The bars come verbatim from PREREG_ST1_AUD.md, frozen wave-20260925-
0521pdt, and this wave's re-verification plan (REVERIFY_PLAN_ST1_0821.
md) was committed alone at a5513ba7c strictly before implementation:
commit-order self-check holds. The frozen verdict mapping says any bar
FAIL maps to DEAD with killing evidence, and two bars failed on
pristine evidence: KB2 measured +1.398 dB against the frozen <= 0.5 dB
bar; KB7 measured 1.611 dB against the frozen <= 1.5 dB bar. These are
not inherited from the voided 0521pdt verifier: the pristine verifier
(456 lines, pure Zag, shell heredoc, pinned znc) was authored fresh
from the frozen spec, never copied the tainted file, and its key
numbers were cross-checked with independent shell/awk arithmetic: E_st
matches awk to the sample, Pearson 0.999605 (awk 0.999606), RMS ratio
-1.761 dB (awk -1.76156 dB). Cross-time determinism is machine-checked:
fresh re-renders hash to 4e9ea742..., byte-identical to the preserved
WAVs; the dry re-render reproduces the frozen gate 7728fbee...; the
trace is byte-identical.

The empty-python3 disclosure is credited, not penalized. The worker
volunteered that during debugging it once invoked `python3` with an
empty stdin script: it read no files, wrote no files, and touched no
wave artifact in any way. The 0521pdt judge precedent is that no
artifact contact means no taint, and the precedent governs here: the
KB5 machine checks (pinned znc verified, token grep clean for
rand/srand/random/time/clock) stand on their own, and none of the
killing numbers pass through the disclosed invocation. Voluntary
disclosure of a nothing-event is the behavior the loop wants; treating
it as a void would punish honesty and teach future workers to stay
silent.

The DEAD verdict follows the frozen mapping with cited killing
evidence. Nothing is weakened or re-interpreted.

## Item 3. CV-P rotated-author re-test: PARTIAL (CONFIRMED on rotated fresh set) [NEW]

The rotated evidence sustains the verdict.

All nine frozen bars PASS on the fresh sealed 30 authored by worker C1
from F9-CVP: B1 30/30 honest resolutions (>= 24/30 required), 0
unflagged confabulations; B2 10/10 inflection recall verbatim (>= 8/10
required); B3 10/10 exact-form verbatim; B4 10/10 specific declines
naming every key-listed payload word, 0 must-not-name violations; B5 0
coverage violations over all 18 quoted decline words against all 38
stemmed KB content-word sets (163 stemmed content words); B6 17/17
byte parity vs the adopted cv1c rebuild on inkb17.txt; B7 1.0619x
per-turn ops (bar <= 10x); B8 3/3 full sealed runs byte-identical,
transcript sha 30d0c3e7..., op-stream sha 6a6e86f3..., zero RNG in any
decision path; B9 seal integrity PASS: PROBES.md and KEY.md hashes at
scoring time equal the seal-commit pins (8c515896... and 57002327...),
the seal-open log was filled at scoring time not retroactively, 74
6-word probe n-grams find zero sealed probe bytes in the candidate
source, KB, gazetteer, or scorer, and the candidate binary never reads
KEY.md (0 references in source, runs in a directory that never
contained it).

Gate (a) is satisfied on the letter: the 0521pdt judge required a
rotated-author re-test, and this re-test ran the frozen candidate
(byte-identical rebuild of the 0521pdt cvp.zag, sha dcf98cdb...)
against a fresh sealed 30 authored by a different worker than the
implementer, with commit order verified (plan 382f70f95, seal
35a54297c, then implementation). The scorer is pure Zag on the pinned
toolchain, reads KEY.md from disk at scoring time only, and its sums
were cross-checked with shell awk (identical numbers). The ten-point
self-review names every residual honestly: depth 2/2 non-independent
red-team, single-session self-attestation on separation, the tie-break
guard limited to the exact-form corridor, the new scorer as
trust-bearing code. Because the residuals are disclosed rather than
hidden, and because the verdict is capped at PARTIAL per the 0221pdt
judge ruling with adoption still barred pending Micah's ruling 6, the
verdict is exactly as strong as the evidence and no stronger. That is
the correct fence.

## Item 4. DF-1 foreground defocus: DEAD [NEW]

The killing evidence is valid, the bars were properly frozen, and the
verdict is the honest output of the frozen mapping.

The prereg (PREREG_D2_0821.md) was committed alone at 0d977b976 before
any DF-1 source, verifier, scratch, or render existed: commit order is
clean. The mechanism was implemented exactly as frozen: separable
integer box blur R=7 (15x15), 12 px feather mask from the verbatim
frozen substrate geometry, blend out = (sharp*(12-w12) + blurred*w12 +
6)/12, no RNG. The dry rebuild gate reproduced the frozen hash
e4f65557... before work proceeded.

KB4 (the frozen E3 grain guard) requires |variant - baseline| <= 24
luma levels for every pixel. The pure-Zag probe measured max luma diff
48 (per-channel max 55, also > 24) at pixel (258,806), localized to
the lit edge of the left arch pillar: 203 of 1048576 pixels (0.019%)
exceed 24, all in the stone band y 786 to 986, 166 of 203 inside the
arch body rects, nothing at 49 or above. The bar failed as frozen; the
frozen mapping says any bar failed maps to DEAD with killing evidence.

Everything else passed and is documented, not trimmed: KB1 3/3
byte-identical renders at 6155ae84...; KB2 zero writes outside the
mask over 790773 checked pixels; KB3 efficacy 6.594 mean luma diff
(>= 1.5 required) and HF power ratio 0.002 (<= 0.7 required); KB5
purity (pinned znc verified before every compile, zero Python contact,
token greps clean); KB6 worst render 1.856 s (<= 2.0 s); KB7 33792
feather checks, zero overshoot. No sealed pair was prepared, which is
correct per the frozen sealing plan (a pair is built only on a clean
pass of every bar). The [NEW] tag is earned: grep found zero prior art
for defocus/blur/bokeh anywhere in docs/lab or any run dir, and D19
was the opposite mechanism (sharp dabs, DISCARDED), explicitly not
stacked. The mechanism behaved as a real R=7 lens would on a ~100-level
hard edge; the frozen bound is incompatible with genuine radius-7
defocus on hard edges. The candidate dies on its own bar, honestly,
with the root cause written up before the verdict.

## Item 5. D1 intelligence lane: NO-CANDIDATE

Honesty over padding is the right call, and the survey earns it.

The survey ranks the five intelligence metrics on VERIFIED numbers and
names deliberation quality the weakest verified metric, then shows
every mechanism class with a foothold is closed: D-SEARCH (KB-T1 miss
32.3pp/43.7pp; KB-T3 recall collapse 43.95pp), Ensemble OVT5 (KB-T1
40.74%/54.13% vs 10% bar; withheld true installs 32.9% vs
adversarial-false 18.1%), Trades Candidate A (ENS5 FIR 34.78%/54.46%),
ITER-FP, SHAPED-MEMBERS (SM-T1 and SM-T4 fails; red-team R1 proves
monotone reshaping preserves the R0 blocker relation exactly), and the
KB4 substrate second path (SP-B1 1891 bp vs bar strictly below 1842 bp,
DISCARD [VOID]). Standing closures are cited by name: S4, S11
(hypothesis-class level), the D-SEARCH/ITER-FP family, M4 R2, and the
collision rule against Micah's closed FS-F2C front.

Eight candidate ideas were considered and rejected with reasons, not
waved away: non-monotone reshaping (closure-gaming), corroboration-gated
install (evidence-predicted failure), blocker-margin weakening (wrong
direction), contradiction-predicate change (no mechanistic theory),
contest second path (not framable with a frozen kill bar in Phase 1),
motiondir-7 tail (N=7, underpowered), T2-targeted veto (collision rule),
stacking adopted components (C12 confounded-stack precedent). No prereg
was written and nothing was implemented: the lane stood down instead of
manufacturing a candidate. Forcing a candidate without a framable kill
bar would be exactly the padding the loop exists to prevent.
NO-CANDIDATE is the verdict the evidence supports.
