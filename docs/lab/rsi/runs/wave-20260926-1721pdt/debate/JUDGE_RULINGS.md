# Judge rulings: wave-20260926-1721pdt

A debate can overturn a coordinator verdict only with cited evidence,
never rhetoric. The skeptic's provenance probe is present and answered
in substance: everything under judgment this wave is inherited and
re-certified ([RE-CERT]), nothing is [NEW], and the DP-1 sealed pair
remains queue-HELD [RE-CERT] after its 1421pdt repair, not re-judged
here. His six governance rulings remain open and untouched; this court
decides none of them and narrows none of them.

## M1: Fork battery: CONFIRM [RE-CERT]

The advocate's numbers are verified in the evidence file: 39 named
entries, 37 PASS with uniform byte-identical evidence (znc pin
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef on
37/37, probe pin 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
on 37/37, B2 bin pin 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
on 37/37), 2 extraction FAILs (rh-pull-1-head at 5802fec8, rh-pull-2-head
at 4b76bb59) with the identical cause recorded in each of the last five
waves (trees lack the pinned toolchain path; non-TNN research-doc
repos). The spot re-run of three 1421pdt entries was run before any
1421pdt verdict was cited and confirmed 3/3 on the fixed sed parser:
live tnn-native-lab at b6f96edaf PASS, fixture
wt-forktest-tnn-native-lab at bd3097874 PASS, pull/1 extraction FAIL on
identical cause. Harness provenance is clean (pure-Zag source sha
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738;
rebuilt binary sha
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
byte-identical to prior waves). Origin tip 39bf8d5d49 is identical at
run start and close; local HEAD unmoved at 45d449a56. Zero-Python
attestation holds.

On the skeptic's attacks:

1. Scope (toolchain only, not contents): LANDS as a written caveat. The
verdict line below reads "CONFIRM of toolchain and extraction
stability," which is exactly what the scope stamp certifies. It is not
a verdict on fork contents.
2. Coverage delta (39/4/3 versus 1421pdt's 40/6/5): the advocate gave a
named explanation and it checks out against the evidence. The
1421pdt queued pickups 006dfe027944f395a47ae8fe6e3329a9d7634e and
7c19065e7b1ce13f6479ba50b4f35e110156c734 are ancestors of the merged
run-start tip 45d449a56 and are tested through it, not as separate
entries. The newly enumerated entry is arch-wave-0926-1421 at
a222f8f178 (the pre-merge 1421pdt archive state). The 1421pdt run-start
entry is now a fixture ancestor. The skeptic's trend warning (live set
shrinking while merged content grows) is recorded and genuine; it does
not overturn this wave's accounting.
3. Five waves of the same two pull-head extraction FAILs: LANDS as a
standing caveat. It is an instrument limit, not a regression: the
cause is unchanged, both trees still lack the toolchain path. The
skeptic is right that pull heads are the most likely place for new
content to appear, which is exactly why the caveat travels with the
verdict every wave.
4. Duplicate inflation (39 named, 31 unique): LANDS as a caveat. All 8
duplicates are named per P8; the load-bearing count is 31 unique
commits, and the verdict line carries it.
5. 35 of 39 entries are fixtures: this is determinism by design (P12),
not gaming. The 4 live entries (3 unique live commits) are the ones
that could have changed.
6. 1421pdt's historical exposure to the mis-parsed extraction: noted.
The corrected verdicts match, so no 1421pdt verdict changes, but the
skeptic is right that 1421pdt's certifications rested on mis-parsed
output for their lifetime. The record now shows the corrected
confirmation.

Minting P19 (coverage delta accounting): when a wave's fork battery
reports fewer named entries, fewer live entries, or fewer unique live
commits than the prior wave, the wave report must name the cause of
the delta (merged pickups becoming ancestors, newly enumerated refs,
enumeration changes) before the motion can be CONFIRM'd. A bare count
drop is not certifiable. This wave satisfies P19: the delta is fully
accounted (merged pickups, one newly enumerated archive entry,
run-start entry becoming a fixture ancestor).

Ruling: CONFIRM [RE-CERT]. Certified: toolchain and extraction
stability on 31 unique commits (37/37 toolchain-bearing entries PASS,
byte-identical evidence; 2 extraction FAILs on standing identical
cause; P14 archive staging noted). Caveats carried: scope is toolchain
only; pull/1 and pull/2 remain uncovered (standing hole, fifth wave);
duplicate count inflation disclosed; live set shrank while merged
content grew (watch as a trend, not a verdict changer).

## M2: Interactive TNN: CONFIRM [RE-CERT]

The negative finding stands on four pillars, all cited. The 135-commit
merge range 28ec31ab0..45d449a56 yielded exactly one chat|repl|interactive
grep hit: the known false positive (substring "repl" inside "replay"
and "replication" in units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md).
Entry-point signature grep (fn main, stdin, readline, interactive_loop,
repl_loop) returned zero files. The wave delta added zero files under
src/ or units/ at all, which closes the skeptic's differently-named
entry-point hole for this wave specifically. Frozen pins re-verified by
sha256 and all match: baseline probe
1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
decline-gate probe
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7,
pinned znc 498abcb5... Git diff over docs/lab/rsi/fit_authority/ and
src/tools/toolchain/ across the delta is empty.

On the skeptic's attacks:

1. Manifest gap (pins in README.md, not SHA256SUMS): the worker
disclosed the gap explicitly, which is the honest basis the court
requires. This is acceptable confirmation basis for a stand-down wave
because (a) the gap was disclosed rather than hidden, (b) the pins are
stable across waves, and (c) the shas were independently recomputed
this wave and match. This is a records defect, not an evidence defect,
and it travels as a caveat. No precedent is minted here; the court
treats this as an application of standing practice, not a new rule.
2. Name-dependent scan method: the skeptic is right that the method
would not survive a wave that adds files. For this wave it survives
because zero files were added under src/ or units/. The caveat travels.
3. No probe chat executed: the standing rule (supervised run only on
change) was followed, and no change was found. The finding is static
analysis only, and the verdict line says so.
4. His .zag probe sources under docs/lab/ (src/uprobe.zag,
src/azprobe.zag in the two upscale commits): CLOSED by his authority,
not re-litigated, not inspected as interactive candidates. The
finding's scope names this convention.

Ruling: CONFIRM [RE-CERT]. No source-level chat/REPL entry point
exists in src/zag/ or units/ on this tip; the wave merge added no
interactive surface; all frozen instruments byte-identical to recorded
pins. Caveats carried: manifest path absent (pins disclosed in
fit_authority/README.md; records defect only); scan method is
name-dependent (closed for this wave by zero added files under src/
or units/); finding rests on static analysis, no behavioral probe run;
his probe sources under docs/lab/ are CLOSED and not re-litigated.

## M3: No-new-candidates stand-down: CONFIRM [RE-CERT]

Five independent signals converge, each cited in LANE_SURVEY_1721.md:
exactly one docs/lab/rsi/ commit in the 14:21 to 17:21 PDT window
(e8b913584, the 1421pdt evidence batch); zero prereg|design hits in
window name-status grep; prereg inventory unchanged with newest
PREREG_DP1_1721 from 2026-09-25; no new on-disk material outside the
committed 1421pdt batch; 27 untracked entries, zero matching
prereg|design, all older-wave build and frame residue by path.
Per-lane standing unchanged: G1 STAND DOWN, D-VID-1 STAND DOWN, CV-P
barred pending his ruling 6, COMP-2 ruling 6 open with P11 unresolved,
B1-class P9 reformulation not found, ST-1 DEAD. Merge-range loop work
is only the known DP-1 pair (18ad30fe3/02d1dcb31 from 2026-09-25),
already queue-HELD and repaired under P18 in 1421pdt. DP-1 stays HELD
[RE-CERT]; presentation of the repaired sealed pair to his ears is a
future-wave queue decision and is not ruled here. His six governance
rulings are untouched and are not narrowed by this debate.

On the skeptic's attacks:

1. Absence of evidence: the 27 untracked entries were classified by
path, not content-inspected. The court accepts this for a stand-down
wave because the committed name-status grep, the prereg inventory, the
on-disk draft check, and the single committed batch in the window are
four independent channels that agree, and because the lane survey is
read-only by mandate. The limitation is written into the verdict line.
2. Precedent stacking (P17, P18, P11, P9): noted. This ruling rests on
this wave's five cited signals, not on precedent reflex; the precedents
do procedural work (labeling, protocol) but no lane was judged by
inheritance alone.
3. DP-1 in limbo: LANDS as a recorded concern. The queue decision for
presenting the repaired sealed pair to his ears is owed a named future
wave, not indefinite drift. The court rules nothing about it here; it
records the obligation.
4. Procedural versus scientific stand-down: LANDS and is written into
the verdict line. CV-P and COMP-2 are barred by his open rulings, not
by lane evidence; the stand-down is procedural, pending his authority.

Ruling: CONFIRM [RE-CERT]. Zero new prereg drafts, zero design ideas,
zero re-aimed preregs, zero new candidates in the window
2026-09-26 14:21 to 17:21 PDT. The stand-down is procedural (his
rulings gate two lanes; lane evidence holds the rest) and is recorded
as such. DP-1 stays queue-HELD [RE-CERT]; the queue decision for
presenting the repaired pair is owed a named future wave.

## M4: Prereg commit-order self-check: VACUOUS [VACUOUS]

No loop candidates were proposed this wave, so no prereg/impl commits
exist and there is no ordering to check. Per P17 this is labeled
vacuous, not a pass. The skeptic's standing question (does a
stand-down wave need a vacuous motion at all) is answered: the debate
is mandatory and the motion list is fixed, so the motion is recorded
and adds zero information. No gaming is alleged and none is found.

Ruling: VACUOUS [VACUOUS]. Recorded null, not a pass.

## Precedents

One new standing precedent minted this wave:

P19 (coverage delta accounting): when a wave's fork battery reports
fewer named entries, fewer live entries, or fewer unique live commits
than the prior wave, the wave report must name the cause of the delta
(merged pickups becoming ancestors, newly enumerated refs, enumeration
changes) before the motion can be CONFIRM'd. A bare count drop is not
certifiable. First application: wave-20260926-1721pdt (39/4/3 versus
1421pdt's 40/6/5, delta fully accounted).

No other precedent was minted. The manifest-gap acceptance in M2 was
handled as an application of standing practice, not a new rule.

## Summary of verdict lines

- M1: CONFIRM [RE-CERT] (toolchain and extraction stability on 31 unique commits; caveats carried: scope, pull-head hole, duplicate inflation, shrinking live set as a trend to watch).
- M2: CONFIRM [RE-CERT] (no new interactive surface; caveats carried: manifest gap, name-dependent method, static-analysis-only finding, his probe sources CLOSED).
- M3: CONFIRM [RE-CERT] (stand-down on zero new material; caveats carried: procedural basis, untracked-by-path classification, DP-1 queue decision owed a named future wave).
- M4: VACUOUS [VACUOUS] (recorded null, not a pass).
- P19 minted. His six governance rulings untouched.
