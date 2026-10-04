# JUDGE RULINGS: wave-20260925-0821pdt verdict slate

Role: JUDGE. Standard of review: a coordinator verdict is overturned
only with cited evidence, never rhetoric. Frozen bars are never
weakened. Micah's six pending governance rulings (S7 strike, MD-SSD-1,
S11 pull, S11-AUD pull, C12 queue, Python-mirror logic) are his alone
and are not re-litigated here. The advocate argued for each verdict;
the skeptic argued against. Rulings follow, one per item, with numbers
cited.

## Item 1. Fork battery: CONFIRM

Ruling: CONFIRM the verdict as stated: CONFIRM [RE-CERT], 29/29 PASS,
with the new origin tip 40935c121b untested this wave.

The evidence shows the battery tested what it claims and claimed only
what it tested. All 29 forks recorded the identical pass vector
(grepped across all 29 full.logs, no exceptions); znc sha256 matched
the pinned sha 498abcb5... on every fork; the harness was rebuilt from
provenance-extracted source (sha f38d9154... as expected) and is
byte-identical to last wave's build; NEG1/NEG2 discriminated as
required everywhere; zero Python contact. Enumeration was fresh, and
the origin-tip move was disclosed with verbatim SHAs and filed as a
CANNOT-CONFIRM item with a next-wave pickup request. The skeptic's
points are noted and absorbed without overturning: the 29 entries
cover 25 unique commits (four explicit duplicates, all named in the
evidence), and the untested tip must be picked up next wave. The
verdict already carries the caveat, so no narrowing of the verdict
itself is needed. Directive for the record: the next wave's fork
battery must include 40935c121b as a live entry, and the coordinator
must acknowledge the pickup in the next wave's plan. If the origin tip
moves mid-wave again, the same disclosure-and-pickup discipline
applies.

## Item 2. ST-1 pristine re-verification: CONFIRM DEAD [NEW]

Ruling: CONFIRM DEAD [NEW].

The bars were frozen in PREREG_ST1_AUD.md (0521pdt) and re-frozen
unchanged in this wave's re-verification plan, committed alone at
a5513ba7c strictly before implementation. The frozen mapping says any
bar FAIL maps to DEAD with killing evidence. Two bars failed on
pristine evidence: KB2 measured +1.398 dB against the frozen <= 0.5 dB
bar (margin 0.898 dB, unambiguous), and KB7 measured 1.611 dB against
the frozen <= 1.5 dB bar (margin 0.111 dB). The pristine verifier was
authored fresh from the frozen spec, never copied the voided file,
and its key numbers were cross-checked with independent awk arithmetic
to the sample (E_st exact, Pearson 0.999605 vs 0.999606, RMS -1.761 vs
-1.76156 dB). Cross-time determinism is machine-checked: fresh
re-renders are byte-identical to the preserved WAVs
(4e9ea742...), the dry re-render reproduces the frozen gate
(7728fbee...), and the trace is byte-identical.

On the empty-python3 disclosure: no artifact contact, no void. The
worker disclosed a `python3` invocation with empty stdin that read no
files, wrote no files, and touched no wave artifact. Under the 0521pdt
judge precedent, no artifact contact means no taint, and the KB5
machine checks (pinned znc verified, token grep clean) do not depend
on the disclosure. The disclosure is credited; punishing it would teach
silence.

On the skeptic's re-framing argument: the evidence's root-cause note
is accepted as knowledge. In the Q24 stem domain the candidate
preserves energy at +0.013 dB and 42/42 pans are bit-exact; the KB2/KB7
failures are one algebraic mechanism (KB7 = 10*log10(2) - KB2 = 1.612
dB), produced by the frozen 0.89 peak normalization interacting with
constant-power panning. The DEAD verdict therefore attaches to this
wave's artifact under the frozen measurement contract, not to
world-derived stereo panning as an idea. That distinction is recorded
here as knowledge for a future re-prereg (stem-domain or
energy-renormalized bars, a new prereg, no weakening of these bars).
It does not overturn the verdict: the bars were frozen, the readings
are real, and the mapping is mandatory.

## Item 3. CV-P rotated-author re-test: CONFIRM PARTIAL (CONFIRMED on rotated fresh set) [NEW]

Ruling: CONFIRM PARTIAL (CONFIRMED on rotated fresh set) [NEW].

All nine frozen bars PASS on the fresh sealed 30, with cited numbers:
B1 30/30 honest resolutions (>= 24/30 required), 0 unflagged
confabulations; B2 10/10 inflection recall verbatim (>= 8/10); B3
10/10; B4 10/10 specific declines, 0 must-not-name violations; B5 0
coverage violations over 18 quoted decline words against all 38
stemmed KB sets (163 stemmed content words); B6 17/17 byte parity vs
the adopted cv1c rebuild; B7 1.0619x per-turn ops (<= 10x); B8 3/3 full
sealed runs byte-identical (transcript 30d0c3e7..., op-stream
6a6e86f3...), zero RNG; B9 seal integrity PASS with seal-commit pins
matching (8c515896..., 57002327...), zero probe bytes in candidate
sources, and the candidate binary never reading KEY.md. The candidate
is the 0521pdt implementation rebuilt byte-identical
(dcf98cdb...), not re-authored. Commit order verified: plan 382f70f95,
seal 35a54297c, then implementation.

Gate (a) is satisfied on its letter: the 0521pdt judge required a
rotated-author re-test, and one was run against a fresh sealed 30
authored post-freeze by a different worker than the implementer, with
seal discipline machine-checked. The skeptic is right that separation
within one session is self-attested, not structural, and the verdict
must not be read as an independence claim: "(CONFIRMED on rotated
fresh set)" means the bars survived a fresh author, nothing more. The
residuals (non-independent red-team, self-attested separation,
tie-break guard limited to the exact-form corridor, the new scorer as
trust-bearing code) are disclosed in the evidence, and the verdict is
capped at PARTIAL per the 0221pdt judge ruling. That cap is the fence
that keeps the verdict honest. Adoption remains barred pending Micah's
ruling 6, which is his alone and untouched here. Nothing is integrated;
CV-1 baseline integration stays HELD.

## Item 4. DF-1 foreground defocus: CONFIRM DEAD [NEW]

Ruling: CONFIRM DEAD [NEW].

The prereg was committed alone at 0d977b976 before any DF-1 source,
verifier, scratch, or render existed; commit order is clean. The
mechanism was implemented exactly as frozen (R=7 separable integer box
blur, 12 px feather from the verbatim frozen geometry, integer blend,
no RNG; passes 1-5 byte-identical; mask counts recomputed exactly at
257803/5229). The dry rebuild gate reproduced the frozen hash
e4f65557... before work proceeded.

KB4, the frozen E3 grain guard, requires |variant - baseline| <= 24
luma levels for every pixel. The pure-Zag probe measured max luma diff
48 at pixel (258,806) (per-channel max 55, also above 24), with 203 of
1048576 pixels (0.019%) above 24, all in the stone band y 786 to 986
and 166 of 203 inside the arch body rects, nothing at 49 or above. The
bar failed as frozen; the frozen mapping says any bar failed maps to
DEAD with killing evidence. KB1, KB2, KB3 (6.594 mean diff >= 1.5; HF
ratio 0.002 <= 0.7), KB5, KB6 (worst 1.856 s <= 2.0 s), and KB7 (33792
feather checks, zero overshoot) all passed and are documented. No
sealed pair was prepared, which is correct per the frozen sealing plan
(a pair is built only on a clean pass of every bar).

The [NEW] tag stands: the grep survey found zero prior art for
defocus/blur/bokeh, and D19 (sharp dabs, DISCARDED) was the opposite
mechanism, explicitly not stacked. The candidate dies in its first
wave on its own bar, honestly measured, with the root cause written up
before the verdict.

The skeptic's governance point is accepted as knowledge, not as a
verdict change: the frozen R=7 mechanism and the frozen <= 24
everywhere bound were jointly unsatisfiable on this substrate's
~100-level hard edges (a genuine R=7 defocus must move edge pixels by
up to roughly half the step; 48 observed). The probe tail is the
signature of genuine defocus, not amplification. This DEAD verdict is
therefore the verdict on the frozen pair, not on defocus as an idea.
The next defocus prereg must resolve the bar-vs-mechanism tension
before freezing (a smaller radius with an edge-aware bar, or a bar
that distinguishes edge shift from amplification); that is a new
prereg with new bars, never a weakening of KB4.

## Item 5. D1 intelligence lane: CONFIRM NO-CANDIDATE

Ruling: CONFIRM NO-CANDIDATE.

The survey ranks the metrics on verified numbers, names deliberation
quality the weakest verified metric, and shows every mechanism class
with a foothold closed by standing rule or voided verdict: D-SEARCH
(KB-T1 miss 32.3pp/43.7pp; KB-T3 recall collapse 43.95pp), Ensemble
OVT5 (KB-T1 40.74%/54.13% vs 10% bar; withheld true installs 32.9% vs
adversarial-false 18.1%), Trades Candidate A (ENS5 FIR 34.78%/54.46%),
ITER-FP, SHAPED-MEMBERS (SM-T1/SM-T4 fails; red-team R1 proves monotone
reshaping preserves the R0 blocker relation), and the KB4 second path
(SP-B1 1891 bp vs bar strictly below 1842 bp, DISCARD [VOID]).
Standing closures cited: S4, S11 (hypothesis-class level), the
D-SEARCH/ITER-FP family, M4 R2, the collision rule. Eight ideas were
considered and rejected with reasons; no prereg was written; nothing
was implemented.

Forcing a candidate without a framable frozen kill bar would be
padding, which the loop exists to prevent. The skeptic's caution is
noted for the record: the eight rejections were self-reviewed, and the
non-monotone reshaping rejection in particular leaned on a taste
judgment ("unprincipled") plus an extension of S11 beyond its letter.
Those rejections should face adversarial review before they harden
into pseudo-closures. That caution does not overturn this wave's
verdict: on the evidence as it stands, NO-CANDIDATE is the honest
output, and the lane stands down rather than manufacturing work.

## Summary of rulings

1. Fork battery: CONFIRM [RE-CERT], 29/29 PASS (25 unique commits;
   new origin tip 40935c121b to be picked up next wave).
2. ST-1 pristine re-verification: CONFIRM DEAD [NEW] (KB2 +1.398 dB
   vs <= 0.5; KB7 1.611 dB vs <= 1.5; empty-python3 disclosure: no
   contact, no void; DEAD attaches to the artifact and the frozen
   bar-domain choice).
3. CV-P rotated-author re-test: CONFIRM PARTIAL (CONFIRMED on rotated
   fresh set) [NEW] (all nine bars PASS; gate (a) satisfied on its
   letter; residuals disclosed; adoption barred pending Micah's
   ruling 6).
4. DF-1 foreground defocus: CONFIRM DEAD [NEW] (KB4 max luma shift 48
   > 24; no sealed pair prepared, correctly; R=7 plus the frozen bound
   were jointly unsatisfiable, recorded as knowledge).
5. D1 intelligence lane: CONFIRM NO-CANDIDATE (honest survey; verified
   numbers; closures binding; no padding).
