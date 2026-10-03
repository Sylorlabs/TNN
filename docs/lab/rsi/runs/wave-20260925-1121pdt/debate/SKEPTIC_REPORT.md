# SKEPTIC REPORT: wave-20260925-1121pdt debate

Role: skeptic, arguing against the coordinator's draft verdict slate.
Method: read the committed evidence for each item; every number below is
cited from a committed file I read, with file paths. No Python was used
in this review (reading and writing only). Where an attack fails against
the evidence, I say so.

Date: 2026-09-25. Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.

## Item 1: Fork battery. Draft verdict: CONFIRM [RE-CERT], 30/30 PASS

Evidence read: docs/lab/rsi/runs/wave-20260925-1121pdt/forks/FORK_RESULTS_1121.md,
committed as 0e4207fdb.

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

The artifact under judgment is the fork battery run itself, not a new
candidate. Everything is inherited: the shell driver was adapted from the
frozen wave-20260925-0821pdt driver, the pure-Zag harness
fork_battery.zag was extracted read-only from branch
tnn-native-lab-wave-archive-20260923-2321pdt (sha256
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738),
rebuilt with the pinned znc to a binary byte-identical to last wave's
build (sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66),
and the 30 enumerated forks are pre-existing branches, remote heads, and
worktrees. What is new this wave is only the enumeration (fresh
`git branch -a` and `git worktree list`, no stale lists) and the test
execution against run-start HEAD 0ca683756af8354d202828be8922ddb02e834108.
The verdict tag [RE-CERT] is correct; nothing here is new.

### Attack 1: the denominator is padded with duplicates

The report counts 30 entries, but 4 of them test commits already tested
by another entry in the same table. origin-tnn-native-lab and
origin-tnn-native-lab-runstart-tip test the same commit
84ed45077a554f9897ec55c2ca1430273c79eb69. wave3-probe, wave3-senses, and
wave3-trades each test the same commit as forktest-tnn-native-lab
(bd30978748fa83bbea6e423a7074cf32b7304291). The report names these
duplicates explicitly, so this is not hidden, but the headline "30/30
PASS" still leans on them. Unique commits tested: 26. The honest
headline is 26/26 unique commits PASS, with 30/30 entry rows as a
bookkeeping detail. A verdict that needs duplicate rows to reach 30 is
advertising coverage it does not have.

### Attack 2: the live-origin coverage was stale before testing began

The report's own CANNOT-CONFIRM section states the origin tip moved twice
around the run: 84ed45077 to 695997f5 before the battery started (seen on
a read-only ls-remote before any test ran), then to
236e5a17815f925bc405e659246d19498e934cfc during the run. The battery
tested the run-start tip 84ed45077 only. That means the battery
knowingly tested a superseded tip: at no point during the testing was
84ed45077 the live upstream. The two actual live tips of the wave,
695997f5e3df5979a10a0aa8137a1428483828e8 and
236e5a17815f925bc405e659246d19498e934cfc, are untested. A CONFIRM verdict
on "the fork battery" therefore confirms toolchain determinism across
enumerated forks, not the health of the live upstream the loop will build
on next wave. The draft verdict's scope is wrong: CONFIRM of what, the
report answers honestly in its CANNOT-CONFIRM items, but the slate's
one-line CONFIRM does not carry that scope.

### Attack 3: 26 of 30 are fixtures

Per the report's own live-vs-fixture split: Live 4, Fixture 26. Of the 4
"live" entries, only 3 are unique commits (0ca683756af8 local HEAD,
84ed45077 run-start origin tip, 393007563d new archive branch). The 26
fixtures are unchanged SHAs re-tested for coverage. Re-testing them has
real but thin value: every fork's znc copy verified byte-identical to the
pinned sha 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
and NEG1/NEG2 discriminated as required on all 30, which is genuine
determinism coverage, not nothing. But the marginal information of
re-running 26 byte-identical forks is near zero, and the verdict headline
should not lean on it.

### Concession: the work is honest, and the wave's own substrate was covered live

The attacks above land on the verdict label and the denominator, not on
the work. The worker did fresh enumeration, found and tested the new
archive branch tnn-native-lab-wave-archive-wave-20260925-0821pdt at
393007563d, tested the moved local HEAD 0ca683756af8 (382f70f95 to
0ca683756af8), confirmed local HEAD did not move during the run, rebuilt
the harness deterministically, and disclosed the tip moves under
CANNOT-CONFIRM instead of burying them. The wave's own build substrate
(the local working copy) was tested live, so this wave's evidence rests
on tested ground. This is not theater; it is honest coverage work with
an over-broad verdict label.

### Skeptic position on item 1

Reject the unqualified "CONFIRM [RE-CERT], 30/30 PASS." The defensible
verdict is CONDITIONAL CONFIRM: 26/26 unique commits PASS (byte-identical
pinned znc, identical pass vectors, deterministic harness rebuild), with
CANNOT-CONFIRM on the live origin tip (695997f5 and 236e5a17815f
untested; the tested 84ed45077 was already superseded when testing
began). The coordinator should carry the latest tip into next wave's
run-start entry, as the report itself recommends, and the slate should
report the unique-commit denominator.

## Item 2: B1 BOUNCE (sensory). Draft verdict: DISCARD [NEW]

Evidence read: docs/lab/rsi/runs/wave-20260925-1121pdt/sensory/PREREG_B1_1121.md
(committed alone as b2b2a3349),
docs/lab/rsi/runs/wave-20260925-1121pdt/sensory/b1/EVIDENCE_B1_1121.md,
docs/lab/rsi/runs/wave-20260925-1121pdt/sensory/REDTEAM_B1_1121.md
(commit 7b453bb0b, AGREE with DISCARD), implementation commit c91c88ff4.

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

The mechanism is genuinely new. The prereg's prior-art grep over
docs/lab/rsi/runs for bounce, ambient light, color bleed, indirect
illumination, global illumination, and albedo returned zero hits outside
this wave's b1 directory, and the red team re-ran the grep and confirmed
it. What is inherited: the r8c substrate (b1_baseline.zag reproduces the
committed r8c baseline hash
e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d), the
vendored substrate R33_NATIVE_IO_V1.zag (sha256 e6379ddb..., pinned
equal to the G1 wave's copy), and the pinned toolchain. What is new: the
b1_pass (pass 3b) two-bounce mechanism with frozen k=384, the k=192
data-amount variant (exactly 4 diff lines from the k=384 source: the k
constant and its trace string), the pure-Zag verifier b1_verify.zag, and
the renders (k384 var_r1/var_r2 sha256 ef32cd97..., k192 fbb69aa2...,
first rendered this wave). The sealed judge queue was untouched. The
[NEW] tag is correct.

### Attack 1: KB6 is a hypersensitive bar, and the DISCARD leans on it

KB6 as frozen is the max 4-neighbor gradient of the |delta| field over
roughly 1M pixels (the BMPs are 3145782 bytes, i.e. 1024x1024 pixels).
Measured 14 vs the frozen cap 8. The red team confirms the 14 comes from
hard on/off switches (the luma gate at 24 and the sky/land mask) and that
the worker's crops plus independent inspection show nothing visible at
those discontinuities. A single mask pixel anywhere in a megapixel field
can kill a candidate under this definition. That is a foreseeable
miscalibration for any mechanism with hard gates, and the prereg authored
it anyway. The DISCARD therefore rests in part on a bar that measures an
invisible artifact. Had the prereg frozen a percentile-based or
boundary-aware edge bar, as the red team now recommends for future waves,
KB6 would not have fired.

### Attack 2: KB4 is direction-blind, and that is the deeper bar failure

The red team demonstrates that a flat +4 tint over the KB4 population
would pass all seven bars: KB4a mean 4.0 >= 3.5, KB4b 100%, KB4c 4 <= 80,
KB6 edge gradient 4 <= 8 with zero interior gradient, KB3/KB5 unchanged,
KB1/KB2/KB7 trivial. A flat tint carries zero indirect-illumination
content, so the frozen KB4 bars do not encode the candidate's actual goal
(spatially varying color from the scene's own albedo). This is the
strongest attack on the verdict's meaning: had the mechanism been a
content-free flat tint instead of an honest bounce, the loop would have
banked it as [NEW] indirect illumination. The DISCARD is therefore luck
as much as judgment: the mechanism failed bars that a cheat would pass.
The bars are unfit to certify this candidate class, and any future PASS
on these bars should be treated as suspect until a direction bar (e.g.
delta-field vs bounce-field correlation) is frozen.

### Attack 3 (conceded): two measured points are enough to kill the k-family

The task asks whether interpolating from only k=192 (mean 0.86, grad 7)
and k=384 (mean 2.03, grad 14) is enough to declare the whole family
dead. I concede it is. The mix m = k*sh/1024/1024 is proportional to k by
the mechanism's own frozen math, so mean|delta| and the boundary gradient
scale near-linearly with k (grad exactly 2x across the doubling; mean
2.36x). KB4a needs mean >= 3.5, which requires k >= ~625, at which grad
is ~23, nearly 3x the KB6 cap. KB6 needs grad <= 8, which requires
k <= ~219, at which mean is ~1.0, a factor 3.5 below the KB4a floor. Even
under generous interpolation error the gap is roughly 3x on both axes,
and at the KB6 boundary the effect is sub-visible by the red team's own
crop inspection. The red team's structural kill reason (the k-knob couples
effect size to edge gradient, so no setting of the frozen mechanism can
jointly satisfy KB4a and KB6) stands. This attack fails against the
evidence.

### Attack 4 (conceded): the verdict cannot be downgraded to UNVERIFIABLE/PARTIAL

The task asks whether bar weakness should downgrade DISCARD to
UNVERIFIABLE/PARTIAL with a re-freeze. No. The frozen verdict mapping
says "DISCARD on any bar failure" and "PARTIAL is not available: the bars
are conjunctive." Reformulating the bars after the failure to rescue the
candidate is the same sin as weakening a bar to force a pass, which is a
standing red line. Frozen is frozen. The red team's AGREE with DISCARD is
correct, and the repair is prospective only: re-freeze next wave with a
direction bar and a percentile-based KB6. I do not overturn DISCARD.

### Credibility ding (does not change the verdict)

The worker's EVIDENCE states "Anomalies: None in the harness," but the
red team found three: evidence/diffmap_k384.png and
evidence/diffmap_k384_x20.png are byte-identical (the 20x amplification
never happened); the PNG crops were produced outside run_b1.sh with no
ffmpeg command recorded anywhere in the lane dir; and .zag-cache plus
.zagd.semantic-ready were committed as build byproducts. The worker's
self-certification needed the sibling red team as a backstop. Relatedly,
the worker's post-mortem framing ("architecture, not a data gap") needed
the red team's correction: the calibration error WAS a data gap, just not
a missing-data one (dab constants were used instead of base-render pixel
statistics). None of this changes DISCARD, but it shows the evidence
cannot be taken on the worker's word alone.

### Skeptic position on item 2

DISCARD stands and I do not overturn it: KB4a/KB4b fail with margin
(2.03 vs 3.5; 17% vs 25%) on a sub-visible effect confirmed by
independent rerun (kb4_mean_x100=203, kb4_hit_frac_x100=17), the k-family
is structurally dead per the conceded interpolation, and the frozen
mapping mandates DISCARD. The attacks that land are about the bars, not
the verdict: KB6 as frozen is hypersensitive single-worst-pixel
machinery unfit for gated mechanisms, and KB4 is direction-blind and
would have passed a content-free flat tint, so the bar set cannot be
trusted to certify this candidate class. Accept DISCARD, bank the two
knowledge items (pass 3's aerial wash plus flat cool fill spend the
shadow-color budget; calibrate effect bars against base-render pixel
statistics with a probe program), and require bar reformulation before
any re-freeze.

## Item 3: COMP-2 (intelligence trade). Draft verdict: PARTIAL [NEW], adoption doubly gated

Evidence read: docs/lab/rsi/runs/wave-20260925-1121pdt/intel_trade/PREREG_COMP2_1121.md
(committed alone as 5bf152b35),
docs/lab/rsi/runs/wave-20260925-1121pdt/intel_trade/EVIDENCE_COMP2_1121.md
(committed as 621e10957),
docs/lab/rsi/runs/wave-20260925-1121pdt/intel_trade/REDTEAM_COMP2_1121.md
(committed as 36eb88f8f, MODIFY), seal commit d1ad73cb1 (alone).

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

What is new: the comp2_try pair-enumeration mechanism (192 diff lines in
exactly two hunks against the 0521pdt cvp.zag base), the fresh sealed
30-probe set (20 COMP, 10 UNANS, authored post-freeze from F9-COMP), the
sealed key, and the verdict question itself. The [NEW] tag on the
mechanism is correct: the red team's grep found no prior entity-bridged
pair-enumeration mechanism, and the only prior art is the two hardcoded
do_compose templates handling a disjoint probe class. What is inherited,
three levels deep: (1) the trigger, deliberate_cv1's dec==2, which is
CV-P's stemmed-coverage gate output; (2) the coverage test, which runs
over kbws, the stemmed content-word sets produced by CV-P's stemmer; (3)
the key, computed by the authoring enumerator pair_enum.zag with
byte-copied stemmer and stopword logic from the adopted source. The
stemmer carries the ruling-6 Python-mirror lineage: comp2.zag line 1396
contains "(proven: 1/12 < 2/12 in the Python mirror)", identical line and
content in the 0521pdt CV-P base, inherited verbatim, not introduced this
wave. So the mechanism is new, but the evidence stack it stands on is
inherited from a PARTIAL, adoption-barred component at all three load
bearing levels.

### Attack 1: the mislabel was material, not merely documentary

The prereg's provenance header and section 2 call the base "adopted CV-P,"
and the verdict mapping says "ADOPT iff COMP-B1 through COMP-B6 all PASS."
CV-P is PARTIAL, confirmed on a rotated fresh set wave-20260925-0821pdt,
with adoption explicitly barred pending Micah's ruling 6. The red team
calls the taint documentation-level and severs the ADOPT mapping as a
policy clause conflicting with higher authority. I push further: the
mislabel is the premise of the verdict mapping, not a typo in it. An
ADOPT mapping written against a false premise has no coherent target.
Adopt into what, a PARTIAL base whose own adoption is barred? With the
mapping void, which the red team and I both require, the verdict is bare
numbers with no decision attached. "PARTIAL [NEW], adoption doubly
gated" is then the coordinator doing interpretive work the evidence does
not support. The honest label names the structure: this is a stack
verdict on a candidate downstream of an unadopted, ruling-gated
component, not a capability verdict with gates.

### Attack 2: one mind, two implementations, engineered probes

The sealed set was authored and implemented by the same worker in one
session (self-attested, disclosed under COMP-B6). The "independent
enumerator" is an independent implementation but shares byte-copied
stemmer logic and the same author. The key and the candidate are two
implementations of one frozen rule by one mind, so 20/20 measures
rule-implementation fidelity, not independent discovery. The red team
concedes this ("honest as a capability-existence proof; weak as a
generality claim"); I add that this paper review cannot break the
circularity either, because it re-verifies the same worker's artifacts
rather than independently re-deriving the key. M5 structural
author/implementer separation is not met, and per precedent P3 that caps
below full adoption regardless. On generality: the 20 COMP probes fall
into about four surface templates (author/publication-year,
birth-year/authorship, landmark/city/date, tower/height), and F9.5
explicitly uses "KB surface forms to avoid stemmer-sensitive
inflections," so paraphrase robustness is untested by design. 20/20 on
engineered probes is the floor of a generality claim, not the ceiling.

### Attack 3: the evidence is stemmer-contingent, so "doubly gated" understates the dependency

This is the strongest attack and the red team already makes it; I press
it to its conclusion. COMP-2 is downstream of CV-P's Python-mirror
lineage at three levels: the trigger (dec==2 from the stemmed-coverage
gate), the coverage sets (kbws from CV-P's stemmer), and the key (byte
copied stemmer in the enumerator). If ruling 6 goes against
Python-mirror-developed logic, the 20/20 does not survive as a number to
be re-voted; the key, the coverage decisions, and the winning pairs must
be re-derived with an independently developed stemmer. The coordinator's
slate ("PARTIAL [NEW], adoption doubly gated") reads as if the numbers
stand and only adoption waits. They do not stand unconditionally. The
disposition should be recorded as [STACK]: evidence contingent three
levels deep on a ruling-gated component, provisional until ruling 6
lands. The red team's MODIFY reaches "stemmer-contingent, not merely
adoption-barred"; the slate has not absorbed that modification.

### Attack 4: the lane's paperwork is the thing being gated, and it is loose

The same lane that mislabeled its base has three more paperwork defects,
all found by the red team: AUTHORING.md A3 claims all probes avoid a
phrase list including " in 18" and " in paris," but P1 "published in
1851" contains " in 18" and P6-P8 and P16 contain " in paris"
case-insensitively; COMP-B5 cites a transcript SHA
(243a6a9f3c1a78ac4c9b156d21f096655e1c7efa68588fc2b5b5216ed53f63bf) with no
committed transcript or op log; and the prereg specifies install-time
entity precompute with ops excluded from per-turn costs while the
implementation builds the fact-entity matrix per declined turn and counts
the ops, inflating the measured 7.17x relative to the prereg's
accounting. Each is minor and conservative in direction (the bar still
passes under the stricter accounting). Together they show the lane's
paperwork reliability is what the gates are actually testing, and gates
should be strict on paperwork this loose. None of this voids the bars;
all of it argues against any reading of PARTIAL as "nearly adopted."

### Concessions: the numbers were honestly obtained

I do not dispute the measured results. The red team's source audit found
no gaming in comp2.zag: no hardcoded pair indices, no probe bytes, no
KEY.md token, no RNG, no clock; seal hashes match the d1ad73cb1 blobs
(PROBES.md eb00a7c8..., KEY.md 35802003...); commit order is strict
(5bf152b35 at 19:07:20, d1ad73cb1 at 19:33:23, 621e10957 at 19:48:50);
zero Python in wave sources. The 7.17x per-turn mean ops sits inside the
frozen 10x budget against the standing priority that 10x cost for a
genuine new capability is good, and the capability is real as an
existence proof: a documented decline class converted into verbatim
2-fact answers, 10/10 UNANS declines holding, confabulation impossible
by construction. The worker self-flagged the governance anomaly and kept
the original CV-P files byte-identical with nothing integrated. The
attack is on what the verdict label claims the numbers mean, not on the
numbers.

### Skeptic position on item 3

Reject the slate's "PARTIAL [NEW], adoption doubly gated" as
underspecified. My disposition: PARTIAL [STACK], mechanism genuinely new,
numbers stand as measured, evidence stemmer-contingent three levels deep
(trigger, coverage, key). Consequences: the prereg's ADOPT mapping is
void; if ruling 6 bars Python-mirror logic, this lane is re-derived with
an independently developed stemmer, not re-voted; M5 structural
separation, committed B5 transcripts and op logs, prereg/implementation
accounting agreement, AUTHORING.md accuracy, and paraphrase-robustness
probes are all outstanding before any adoption consideration. The
mislabel was material to the verdict mapping, not merely documentary,
and the slate should not present contingent numbers as banked results.

## Summary of skeptic positions

1. Fork battery: reject unqualified CONFIRM and the 30/30 headline.
   Verdict should be CONDITIONAL CONFIRM on 26/26 unique commits with
   CANNOT-CONFIRM on the live origin tip (695997f5 and 236e5a17815f
   untested; the tested 84ed45077 was already superseded when testing
   began). The work is honest; the label is over-broad.
2. B1 BOUNCE: DISCARD stands (conceded: the k-family interpolation is
   sufficient, and the frozen mapping forbids downgrading). The bars,
   however, are unfit for this candidate class: KB6 is hypersensitive
   single-worst-pixel machinery, and KB4 is direction-blind and would
   have passed a content-free flat tint. Require bar reformulation
   before any re-freeze.
3. COMP-2: reject "PARTIAL [NEW], adoption doubly gated." The honest
   disposition is PARTIAL [STACK]: genuinely new mechanism, honestly
   measured numbers, evidence contingent three levels deep on
   ruling-gated Python-mirror lineage, with the prereg's ADOPT mapping
   void and re-derivation (not re-vote) required if ruling 6 goes
   against that lineage.

Scope confirmations: Micah's frontier files untouched. None of the six
governance rulings touched or decided. Sealed judge queue untouched (no
pair prepared or modified). No push, reset, rebase, or merge performed;
this report is the skeptic's only local commit.
