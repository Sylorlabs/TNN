# JUDGE RULINGS: wave-20260925-1121pdt verdict slate

Role: JUDGE. Standard of review: a coordinator verdict is overturned
only with cited evidence, never rhetoric. Frozen bars are never
weakened. Micah's six pending governance rulings (S7 strike, MD-SSD-1,
S11 pull, S11-AUD pull, C12 queue, Python-mirror logic) are his alone
and are not re-litigated here. The advocate argued for each draft
verdict; the skeptic argued against. I read both briefs and
spot-checked the contested numbers against the committed evidence:
forks/FORK_RESULTS_1121.md, sensory PREREG_B1_1121.md and
REDTEAM_B1_1121.md, intel_trade PREREG_COMP2_1121.md,
EVIDENCE_COMP2_1121.md and REDTEAM_COMP2_1121.md.

Skeptic transcript completeness: the verbatim provenance probe ("What
is the provenance of the artifacts under judgment, and what exactly
is new versus inherited?") is present for all three items in
SKEPTIC_REPORT.md. No incompleteness to note.

## Item 1. Fork battery

Ruling: MODIFY the draft verdict line; do not overturn it. Verdict:
CONFIRM [RE-CERT], 30/30 PASS on the tested set, 26 unique commits,
origin tips 695997f5 and 236e5a17815f untested.

The numbers the briefs contest are undisputed in the committed
record. All 30 enumerated forks ran the full shell battery and the
rebuilt pure-Zag harness, and every fork recorded the identical pass
vector (grepped across all 30 full.logs with no exceptions, per
FORK_RESULTS_1121.md). The pinned znc sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
matched on every fork. The harness binary sha256
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
is byte-identical to last wave's build. NEG1/NEG2 discriminated as
required on all 30. Local HEAD stayed at
0ca683756af8354d202828be8922ddb02e834108 during the run. Zero
Python contact.

The skeptic's two attacks are factually correct and both are absorbed
by the committed file itself: 4 of the 30 entries test commits
already tested by another entry (origin-tnn-native-lab-runstart-tip
duplicates origin-tnn-native-lab at
84ed45077a554f9897ec55c2ca1430273c79eb69; wave3-probe, wave3-senses
and wave3-trades each duplicate forktest-tnn-native-lab at
bd30978748fa83bbea6e423a7074cf32b7304291, all named explicitly), so
26 unique commits were tested; and the origin tip moved twice around
the run, so 695997f5 and 236e5a17815f are untested by this wave's
battery and the tested run-start tip 84ed45077 was already superseded
when testing began. The file marks both tips as CANNOT-CONFIRM with
the remedy stated (pick up the latest tip in the next wave's
run-start entry).

The downgrade to CONDITIONAL CONFIRM is rejected on standing
precedent. The 0821pdt judge faced the identical structure (29
entries, 25 unique commits, four named duplicates, an untested new
tip 40935c121b) and ruled CONFIRM [RE-CERT], 29/29 PASS with the
caveats carried in the verdict summary and a pickup directive for
the next wave. Reversing that now for an identical disclosure pattern
would punish honest reporting, not improve it. The draft's flaw is
only that the one-line verdict does not carry the caveats the 0821pdt
judge required in the line itself. The modification: the slate must
read "CONFIRM [RE-CERT], 30/30 PASS (26 unique commits; origin tips
695997f5 and 236e5a17815f untested)." The coordinator carries
236e5a17815f into the next wave's run-start entry, and the
disclosure-and-pickup discipline from 0821pdt applies to any future
mid-wave tip move.

## Item 2. B1 BOUNCE (sensory)

Ruling: CONFIRM DISCARD [NEW], with prospective bar reformulation
required before any re-freeze in this candidate class. The skeptic
concedes DISCARD and I agree with it; the ruling below fixes the
record on what is banked and what is required next.

The frozen bars failed with wide margins, measured twice. KB4a:
measured mean per-channel |delta| 2.03 against the frozen floor 3.5
(58 percent of floor, n=141,684 shadowed land pixels,
kb4_mean_x100=203). KB4b: 17 percent of those pixels reach mean
|delta| >= 3.5 against the frozen 25 percent (kb4_hit_frac_x100=17).
KB6: max 4-neighbor delta-field gradient 14 against the frozen cap 8
(1.75x the cap, kb6_maxgrad=14). The red team re-ran the committed
verifier against the committed BMPs and reproduced every number,
including the k=192 data-amount trial (mean 0.86, hit 2 percent,
max 15, grad 7) and the rerun hashes (var_r1 == var_r2 ==
ef32cd97..., k192 == fbb69aa2...). The frozen verdict mapping makes
PARTIAL unavailable and no bar may be moved this wave. DISCARD is
the only mapped outcome.

The skeptic's conceded interpolation stands as the structural kill
reason. From the two measured points (k=192: mean 0.86, grad 7;
k=384: mean 2.03, grad 14), the mix formula m = k*sh/1024/1024 is
proportional to k by the mechanism's own frozen math. KB4a needs
mean >= 3.5, which requires k >= ~625, where grad is ~23 against the
cap of 8. KB6 needs grad <= 8, which requires k <= ~219, where mean
is ~1.0 against the floor of 3.5. The gap is roughly 3x on both
axes, so no setting of the frozen mechanism's single knob can
jointly satisfy KB4a and KB6. The mechanism's effect is too weak to
see (the red team's independent inspection of the committed crops
confirmed indistinguishability, consistent with ~2/255 mean move)
and its hard gate edges too sharp to legalize.

The skeptic's two bar attacks land and are banked as prospective
requirements, not as verdict changes. KB6 as frozen is
single-worst-pixel hypersensitive (a global max over ~1M pixels),
and the measured 14 comes from hard on/off switches with nothing
visible at the discontinuities. KB4 is direction-blind: the red
team demonstrated that a content-free flat +4 tint would pass every
frozen bar (KB4a mean 4.0 >= 3.5, KB4b 100%, KB4c 4 <= 80, KB6 edge
gradient 4 <= 8, the rest trivial), so the frozen KB4 bars do not
encode the candidate's actual goal of spatially varying color from
the scene's own albedo. Reformulating the bars after the failure to
rescue this candidate is forbidden (that is weakening a bar to force
a pass, a standing red line). But any future re-freeze in this
candidate class must repair the bar set first: a direction bar (for
example delta-field vs bounce-field correlation) so a
magnitude-only cheat cannot pass, and a percentile-based or
boundary-aware edge bar in place of the global max. This is the
precedent P9 recording below.

Banked knowledge from this DISCARD: (a) on the r8c substrate, pass
3's aerial wash (up to 210/1024 toward (198,168,148)) plus the flat
cool fill spend the shadow-color budget inside the light pass, so a
post-pass recolor gets ~2/255 mean effect at honest mixes; (b) the
prereg calibrated effect-size bars against dab constants instead of
base-render pixel statistics, so future effect bars must be
calibrated with a probe program against the actual base render;
(c) the k-family joint-unsatisfiability finding (KB4a and KB6 cannot
be jointly satisfied within this mechanism class). The [NEW] tag
stands: the red team confirmed zero prior art for this mechanism
class, the only code difference between variants is the k constant
(4 diff lines), and the sealed queue was untouched.

## Item 3. COMP-2 (intelligence trade)

Ruling: MODIFY the draft. Verdict: PARTIAL [STACK], adoption doubly
gated, prereg ADOPT mapping VOID. The mechanism is genuinely new;
the numbers stand as measured; the evidence is stemmer-contingent
three levels deep and provisional until ruling 6 lands.

The measured results are not in dispute. On the fresh sealed
30-probe set (seal d1ad73cb1; PROBES.md
eb00a7c8b5be31ccd3ff0f021f4e0e5abce0437decb1f503a4be1b11ebf5537c,
KEY.md 35802003ee0140ae6163efbd85d2750d59030ae8f55deeee854bdd0242f25aed):
COMP-B1 20/20 against a 14/20 bar; COMP-B2 10/10 declines; COMP-B3
17/17 byte-identical against the adopted cvp rebuild (binary
dcf98cdbd0648efa274d925b38818d3edbe00cd7d12f562564c2b5c308b0b4eb);
COMP-B4 7.17x per-turn mean ops against the 10x budget (P6 at 10.1x
disclosed individually, the bar is on the mean); COMP-B5 3/3 full
sealed runs byte-identical (transcript
243a6a9f3c1a78ac4c9b156d21f096655e1c7efa68588fcb5b5216ed53f63bf),
zero RNG; COMP-B6 seal integrity PASS, zero sealed probe bytes in
sources, binary never reads KEY.md. Commit order is strict
(5bf152b35 at 19:07:20 < d1ad73cb1 at 19:33:23 < 621e10957 at
19:48:50). The red team's source audit (192 diff lines in exactly
two hunks against the 0521pdt cvp.zag base, no gaming, no hardcoded
indices, no probe bytes, no RNG, no clock) corroborates the numbers
independently, and the red team's smoke test reproduced the behavior
(P1 answered with facts 0 and 2 verbatim, UNANS declined with the
frozen message, 10647/10127 ops inside the reported range).

The tag is [STACK], not [NEW], for the lane. The mechanism is
genuinely new (the red team found no prior entity-bridged
pair-enumeration mechanism, and the only prior art is the two
hardcoded do_compose templates handling a disjoint probe class), and
that newness is recorded in the provenance line. But the lane's
evidence is downstream of CV-P's Python-mirror lineage at three
load-bearing levels, shown by the red team and confirmed against
the committed source: the trigger is deliberate_cv1's dec==2, which
is CV-P's stemmed-coverage gate output; the coverage test runs over
kbws, the stemmed content-word sets produced by CV-P's stemmer, so
a different stemmer changes coverage sets, winning pairs, and
answers; and the sealed key was computed by the authoring enumerator
with byte-copied stemmer logic (the stemmer lineage is visible in
the source: comp2.zag line 1396 carries "(proven: 1/12 < 2/12 in
the Python mirror)", inherited verbatim from the 0521pdt CV-P base,
not introduced this wave). CV-P is PARTIAL with adoption explicitly
barred pending Micah's ruling 6 (0821pdt judge ruling, item 3).
The spirit of the stack rule is exactly this: a candidate downstream
of an unadopted, ruling-gated component is a stack verdict, not a
capability verdict with gates. The coordinator's "doubly gated"
framing reads as if the numbers stand and only adoption waits; they
do not stand unconditionally. If ruling 6 goes against
Python-mirror-developed logic, this lane is re-derived with an
independently developed stemmer (key included), not re-voted. The
numbers are recorded as conditional, never banked.

The prereg's verdict mapping ("ADOPT iff COMP-B1 through COMP-B6
all PASS") is STRUCK as void for this lane. On the mislabel's
materiality I split the difference between the briefs: the mislabel
("adopted CV-P" for a PARTIAL base) was material to the verdict
mapping, which has no coherent target (adopt into a PARTIAL base
whose own adoption is barred), and the mapping conflicts with
higher standing authority (the 0821pdt judge's adoption bar and
ruling 6). Lower text cannot override higher standing rules, so the
clause is void. But the mapping is severable: the mechanism, the
bars, and the PASS-on-bars verdict never depended on CV-P being
adopted rather than frozen and byte-pinned, so the measured
evidence keeps its standing as stemmer-contingent numbers. The
worker self-flagged the anomaly, kept the CV-P originals
byte-identical, and integrated nothing; no behavioral taint.

Gate (a), rotated-author re-test: not met this wave. Author and
implementer are the same worker in one session (self-attested,
disclosed under COMP-B6); the "independent enumerator" shares
byte-copied stemmer logic with the same author, so 20/20 measures
rule-implementation fidelity, not independent discovery. Per
precedent P3, missing structural author/implementer separation caps
at PARTIAL, which is the verdict rendered. Any future adoption
consideration needs a rotated-author re-test on a fresh sealed set.

Gate (b), ruling 6: pending, his alone. If it goes against
Python-mirror logic, this lane's evidence (key included) is
re-derived with an independently developed stemmer; it does not
survive as a re-vote.

Outstanding before any adoption consideration, all recorded in the
committed record and carried as residuals: M5 structural separation;
committed B5 transcripts and op logs (the 3/3 claim cites a
transcript SHA with no committed transcript or op log; corroborated
by the red team's independent spot check, accepted with the gap
noted); prereg/implementation accounting agreement (prereg
specified install-time entity precompute with ops excluded, the
implementation builds the matrix per declined turn and counts the
ops, inflating 7.17x conservatively, the bar still passes under
the stricter accounting); AUTHORING.md A3 accuracy (its "all pass"
phrase-list claim is inaccurate on its face against the frozen
F9.2/F9.3 spec, which the probes do satisfy, so the defect is
non-binding but noted); and paraphrase robustness (the 20 COMP
probes fall into about four surface templates and F9.5 explicitly
uses KB surface forms to avoid stemmer-sensitive inflections, so
generality is unproven). None of these voids the bars; together
they forbid reading this PARTIAL as "nearly adopted."

## Precedents recorded

P8. Fork-battery CONFIRM survives named duplicates and a superseded
tip. Named duplicate-commit entries (explicit SHAs, explicitly
labeled) do not invalidate the verdict; a mid-wave origin-tip move
covered by CANNOT-CONFIRM disclosure and a next-wave pickup
directive does not invalidate it either. The verdict line carries
both counts: entries tested and unique commits, plus the untested
tips. (Continues the 0821pdt judge's disclosure-and-pickup
discipline.)

P9. A bar set that a content-free control would pass is unfit to
certify its candidate class. When a flat tint or other
magnitude-only cheat would pass the frozen bars of a candidate
whose goal is content or direction (B1's frozen KB4 here), the
bar set must be repaired before any re-freeze: a direction or
content bar for the candidate class (for example delta-field vs
bounce-field correlation) and percentile-based rather than
global-max edge bars. Bar weakness that did not cause the verdict
is banked prospectively; it is never applied retroactively to move
a bar this wave.

P10. A prereg verdict mapping resting on a materially false premise
is void but severable. When the mapping's target premise is false
("adopted CV-P" for a PARTIAL base) and conflicts with higher
standing authority, the mapping is struck; the mechanism, bars, and
measured verdict keep their standing if they did not depend on the
false premise.

P11. Stemmer-contingency records as [STACK] with re-derivation, not
re-vote. When measured numbers depend on a ruling-gated component's
logic at load-bearing levels (here trigger, coverage sets, and
key), the disposition is [STACK], the numbers are recorded as
conditional, and an adverse ruling requires re-deriving the
evidence (key included) with clean logic, not re-voting the
committed numbers.

## Final verdict slate, wave-20260925-1121pdt

1. Fork battery: CONFIRM [RE-CERT], 30/30 PASS (26 unique commits;
   origin tips 695997f5 and 236e5a17815f untested). Directive:
   coordinator carries 236e5a17815f into the next wave's run-start
   entry; disclosure-and-pickup discipline from 0821pdt applies.
2. B1 BOUNCE: CONFIRM DISCARD [NEW]. KB4a 2.03 vs 3.5, KB4b 17%
   vs 25%, KB6 14 vs 8; k-family jointly unsatisfiable (~3x gap
   on both axes); effect sub-visible and independently confirmed.
   Knowledge banked: pass 3's wash plus flat cool fill spend the
   shadow-color budget (~2/255 at honest mixes); calibrate effect
   bars against base-render pixel statistics with a probe program.
   Required before any re-freeze in this candidate class: a
   direction bar and a percentile-based edge bar (P9).
3. COMP-2: MODIFY to PARTIAL [STACK], adoption doubly gated,
   prereg ADOPT mapping VOID. Mechanism genuinely new, numbers
   stand as measured but are stemmer-contingent three levels deep
   (trigger, coverage, key) and provisional until ruling 6. Gate
   (a): rotated-author re-test on a fresh sealed set (P3; M5 not
   met this wave). Gate (b): Micah's ruling 6; if it goes against
   Python-mirror logic, the lane is re-derived with an
   independently developed stemmer, not re-voted. Outstanding
   before any adoption consideration: M5 separation, committed B5
   transcripts and op logs, prereg/implementation accounting
   agreement, AUTHORING.md accuracy, paraphrase-robustness probes.

Scope confirmations: Micah's frontier files untouched. None of the
six governance rulings decided or touched. Sealed judge queue
untouched; no pair prepared or modified. No push, reset, rebase, or
merge. New precedents established: P8, P9, P10, P11. No Python was
invoked in this judging work (reading and writing only).
