# JUDGE RULINGS: wave-20260927-2021pdt

Judge: independent debate judge (depth 2). Scope: the five motions of the
proposed verdict slate, ruled on cited evidence only. No em-dashes are
used in this document.

Binding prior terms honored. From the 1721pdt debate: C3 must be
genuine (behavioral distinctness, not median counts); K7 precedence
over K1/K6; M3 scoring verbatim from frozen text; M4's reflex list
exhaustive and exclusive; evidence notes Zag-generated from the same
Zag-computed values as the TSVs; the section 7 arithmetic is a frozen
defect to be fixed by redraft, never by post-freeze edit. From the
1421pdt debate: preservation of uncertified records with violations
labeled, not striking. From the frozen prereg itself: frozen section 6
("K3 or K7 failure means VOID"; "K7 is a validity gate, not a kill"),
M5's retune protocol, and item 7 (no Python anywhere).

Evidence read: the frozen prereg (freeze 8b456736b), the debate
transcript (1eb652a59), the independent red-team review (bb60f27f5),
the worker commits (d9e96ad91, 9625c211a, f26d510f3, 4750f1a19) and
their evidence files, the fork battery report (dbe397973), the FIT
report (evidence commit 78a8037fd, lane commit 927b3f3f7), the design
lane and survey reports (6062b4a94), and the LOOP_STATE.md tail.
The judge additionally ran independent checks: (1) f0/f2 calibration
identity across all 12 variants from iterations/iter1/calib1.txt;
(2) per-file blob-SHA comparison of src/tools/toolchain/ at 8929cdd93
vs the repaired pinned HEAD fc1a43b8c; (3) strict commit order by
merge-base across the EXP1c chain.

---

## M1. EXP1c wave 2: VOID (uncertified attempt), nothing adopted

Ruling: AMEND. The VOID verdict stands and is CONFIRMED. The proposed
treatment is amended on the C3 claim (struck, not footnoted), the znc
slice causal claim (downgraded to UNPROVEN), and the calibration vs
full-run agent bytes (explicitly labeled as different).

(a) VOID verdict: CONFIRMED. K7 is computed on the frozen quantity
with the instrumentation inversion fixed: among post-enumeration
selections only, counting 10*bonus < score. Data (red-team
hand-verified from run1.tsv): I-survive 0 post-enumeration selections
/ 0 learned; I-invent 89 post (11+18+22+10+16+12) / 0 learned.
Fraction 0 < 0.50, so K7 VOID is correct, including the addendum's
pre-implementation zero-denominator handling. The addendum's
"K7 takes precedence over any K1 firing" restates frozen section 6
("K3 or K7 failure means VOID"; "K7 is a validity gate, not a kill");
no DEAD label may attach to H1 on this evidence. The redrafted 1134
tick minimum (7x1 + 49x2 + 343x3) means the run was structurally
predestined to K7-VOID; that is exactly what K7 is for. Verdict: VOID
as a test of H1/H2, nothing adopted.

(b) C3 PASS claim: STRUCK. The frozen C3 requires ">= 3 qualitatively
distinct scripted strategies each reaching median >= 720/1200". The
judge's independent check of iterations/iter1/calib1.txt shows f0
(forage) and f2 (homebody) with IDENTICAL (ticks, e_end) in all 12
variants (e.g. variant 0: 1200/145 and 1200/145; identical across all
twelve). Only two behaviorally distinct surviving strategies are
demonstrated (the forage/homebody cluster and stormflee). The in-Zag
C3 gate (C3_DISTINCT=3) counts medians only and never tests
distinctness. This repeats 1721pdt finding F10, whose required
correction ("make C3 check behavioral distinctness, not just median
counts, or field a third genuinely distinct surviving strategy") was
not implemented this wave. The advocate's severability argument fails
at the stop decision: ITERATION1.md's decision section cites "C3 (3
distinct strategies >= 720): PASS (3/3, all 1200)" and stops the
retune on it, so the M5 stopping rule was not honestly satisfied as
claimed. The C3 claim is struck, not footnoted: a frozen gate may
not stand PASS on a false premise in a preserved historical record.
Recorded as C3 NOT-MET (false premise; repeat of 1721pdt F10, the
correction stays open). The M5 stop decision is labeled as taken on
that false premise. Materiality: nil for the kill bars, because the
K7-VOID is structural and independent; the advocate is right that the
P and R arms (both median 1200, behaviorally distinct) substantially
meet the sim-diversity concern C3 guards, but that does not repair
the worker's specific false claim about the three calibrators.

(c) K1/K6 numbers: SURVIVE AS MEASUREMENTS, never as kills. The
numbers are correct literal computations, hand-verified from the
independently reproduced TSVs (run1.tsv/run2.tsv byte-identical, SHA-256
0e82ba093953da59e0d4d1de25cf75501b5108992857ae281607c9519281c288;
84 RUN rows plus 48 IDIAG rows per TSV): K1 fires literally
(918 <= 1200); K6 fires literally on both arms (1082 >= 918;
1200 >= 920); K2 does not fire (918 > 24); K3 ok (P=1200).
The K6 ablation is a genuine intervention this wave (excludes
COMBINE-containing sketches from I-arm selection; medians move; M4
reflexes including H9 preserved, so no EXP1b-style void-reflex
dropout confound). The skeptic's "predestined, therefore
uninformative" point is noted and entered into the record: what these
numbers measure is the starvation dynamics of I arms that never
finish enumerating (I-invent's 89 post-enumeration selections against
399 sketches confirms the choice phase never materialized), not
invention or choice. But labeling preserves data where striking
destroys it (1421pdt precedent), and the "measurements from a voided
run" category with the explicit NOT-ADOPTED tag is exactly what
prevents the future mis-citation the skeptic fears. The judge
CONFIRMS the interpretive reading as binding precedent with cited
evidence: the frozen verdict mapping makes K7 a validity gate, a
void test cannot kill a hypothesis, so K1/K6 firings from a
K7-voided run are measurements only. Future waves citing this
category cite this ruling, not the debate transcript.

(d) znc slice claim: DOWNGRADED TO UNPROVEN; the workaround is KEPT
as effective and validated. The worker's specific causal claim in
ITERATION1.md (non-deterministic store smearing: a single pdat[0] =
16 corrupted indices 32, 35, 38, 41, 44) is UNPROVEN: the red team's
three purpose-built probes could not reproduce that pattern or any
non-determinism, and the original failing probe was never committed,
so no future worker can verify it. The loop's standard is that
claims rest on committed evidence. What the red team did confirm
independently is a different-signature allocator-overlap anomaly
(deterministic index-32 read-back of 64 after interleaved
_zag_malloc; same bug family, not the claimed one), which is
recorded as a separate observation, not as confirmation of the
worker's claim. The workaround (1024-element slices allocated up
front) is validated end to end by the red team's byte-identical
reproduction. In the preserved record the causal claim reads
UNPROVEN, not proven, and the workaround reads effective.

(e) Preservation: PRESERVED WITH LABELS, not struck. The iteration
stays as an uncertified historical record with violations labeled:
the struck C3 claim, the downgraded znc causal claim, the
calibration/full-run agent byte difference below, the NOT-MET
section 7, and the K4 CANNOT-CONFIRM / K5 INCOMPLETE honest
disclosures. The judge adds one required label the order check does
not cover: milestone 3 (f26d510f3) edits e1c_agents.zag by 23 lines
after milestone 2 (9625c211a) committed it, and e1c_run.zag first
appears at milestone 3, so "iteration 1" names two different agent
sources (the calibrated bytes and the full-run bytes). The red team
reviewed the final sources and verified M3/M4 on them, which
contains the damage for M3/M4 purposes, but the preserved record
must state explicitly that the calibration agents and the full-run
agents are not the same committed bytes.

Credited (uncontested): M3 implemented verbatim (frozen scoring,
deterministic argmax, B0 = 40/120 schedule, no bonus constants beyond
B0); M4 exactly the three frozen reflexes with verbatim conditions
(F2 mote-adjacent preemption gone, F3 H9 restored, F4 condition
drift corrected; the plank carve-out mirrors the frozen world's own
void-fall rule, fidelity not drift); the evidence note byte-identical
to fresh e1c_evidence.zag stdout with all seven medians matching
(P=1200, R=1200, Z=24, I-survive=918, I-invent=920,
I-survive-abl=1082, I-invent-abl=1200); determinism independently
reproduced end to end twice; pure Zag; commit order strict
(8b456736b < d9e96ad91 < 9625c211a < f26d510f3 < 4750f1a19, no
intervening commits, addendum committed alone before any
implementation file existed); K4 CANNOT-CONFIRM and K5 INCOMPLETE
honestly reported with no self-certification; no retune shopping
(the worker stopped at iteration 1 with per-iteration commits under
M5). The section-7 redraft addendum is confirmed judge-legitimate:
it was mandated by the 1721pdt binding forward requirement, is
pre-implementation, and changes no mechanism, bar, gate, horizon,
or bonus number.

## M2. Fork battery

Ruling: CONFIRM [RE-CERT], 55 named entries, 53 PASS, 0 FAIL, 2
UNTESTABLE. The numbers are undisputed and independently recomputed
from this wave's own verdict table (44 unique commits; 4 live, 51
fixture).

The skeptic's sharpest point is resolved by the judge's own
evidence, not by qualification. The demand was a per-file
byte comparison of the 12 restored toolchain files against
8929cdd93. The judge ran it: git ls-tree blob SHAs for every file
under src/tools/toolchain/ are identical at 8929cdd93 and at the
repaired pinned HEAD fc1a43b8c, except two build-cache files
(.zag-cache/zagd/semantic.record, .zagd.semantic-ready) that exist
only at fc1a43b8c and are part of the repair commit 37d1d3cab's own
additions, not pre-loss content. Every pre-loss file is therefore
restored byte-identically, and the restoration commit mechanism
(git checkout 8929cdd93 -- the 12 paths, recorded in
forks/FORK_ADDENDUM_1721.md) is consistent with that. The 1721pdt
FAIL is closed by content restoration: the local-tnn-native-lab
entry PASSES at fc1a43b8c with the probe compiling under the fork's
own znc and emitting R32_ZNC_PROBE_OK. The "unverified-pending"
qualification the skeptic requested is no longer needed and is
replaced by this judge verification.

Uniform battery evidence holds across all 53 PASS runs: znc pin
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
on 53/53, probe source sha
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
on 53/53, B1/B2/B3 pass, and both negative controls discriminate
(NEG1 E0002 on all 53; NEG2 "WRONG OUTPUT" differing at char 1 on
all 53). Harness rebuilt byte-identical to 1721pdt
(a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66).
The two UNTESTABLEs are rh-pull-1-head and rh-pull-2-head with the
identical content-dependent cause thirteen waves running (pinned
toolchain path absent in non-TNN research-doc trees); the counts
are never headlined without that caveat. Two cautions are carried
with the verdict but do not block it: the mid-run local HEAD move
(fc1a43b8c to 927b3f3f7 by another lane) was inert by pinning and is
disclosed, but each wave's "inert by pinning" is a per-instance
claim, not a structural fix for lanes racing the battery; and the
two former origin UNTESTABLEs became testable only because the
bedf8b4a object sat in the local store, so live origin coverage each
wave depends on local-store freshness, which the battery does not
measure (no fetch authorized).

## M3. tnn_chat FIT

Ruling: CONFIRM [NEW, process confirmation]. The standing re-run rule
(minted 0521pdt) made a fresh re-run due this wave (last fresh
re-run at 1421pdt, stale count 4 of 8); it was done, not skipped.
Numbers undisputed: decline and baseline binaries rebuilt with the
pinned znc are byte-identical to the frozen records (decline
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7;
baseline
1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c),
2/2 PASS; KB1 30/30 specific declines with 0 blanket refusals across
3 runs; KB2 17/17 answered with 0 declines and byte-identical
baseline parity; KB5 10/10 answered with 0 declines and byte-identical
baseline parity; 9/9 required rerun pairs byte-identical (15/15
including baseline pairs); all three output hashes byte-identical to
the prior wave records; all 15 runs exit 0 with empty stderr; zero
Python anywhere. The merge-range chain-diff over 80c40a7af..fc1a43b8c
shows exactly one change on the FIT chain paths: the additive
record-only docs/lab/rsi/fit_authority/SHA256SUMS file, every pin in
it matching the frozen records. Zero changes to any instrument
source, fixture, kb.txt, gaz.txt, R33 support, or the znc binary.

The process-only scoping is adequate and is enforced as part of the
verdict: this certifies the frozen 38-fact closed-book probe chain
on HEAD fc1a43b8c only. It is not a candidate verdict and not merge
review of the merged-in work. The report's caveats are binding:
closed-book probe instrument, not an open-domain conversational
model; the decline binary is a supervised red-team probe instrument,
not a general interactive TNN; the traveling confabulation caveat
(tnn_chat emits unflagged confabulations on out-of-KB questions)
carries verbatim from the 0521pdt survey; no live learning.
Record-keeping: the FIT record spans two commits; future citations
use the evidence commit 78a8037fd (lane commit 927b3f3f7 carries the
handoff).

## M4. Design lane and interactive survey

Ruling: CONFIRM [NEW] for the design-lane entries and the survey
verdict, with the skeptic's two structural flags entered as
judge flags. The 1721pdt forward bar (survey method with counts,
per-lane blocker evidence with commit ids, explicit
nothing-manufactured statement) is met in full: 30 origin commits
plus 10 local first-parent commits surveyed; 11,765 files added
(2,098 .zag); docs/lab/onebrain3/traces/ listed (27 files,
unchanged); case-insensitive name scans with adding commits traced;
image_upscale changes enumerated; the message-text search over all
30 origin commits for ruling/governance terms with the one hit
dispositioned; the nothing-manufactured statement present and
specific.

Entries confirmed:
- EXP2-K4 corpus: HELD [NEW]. Blockers 1 (no loop-owned failure
  traces with known-correct outcomes) and 2 (spec-blind curation is
  a human collection protocol) are technical; blocker 3 (the loop
  is barred from repurposing Micah's closed fixtures, including his
  TA-CORPUS v1 seal 879bbb4cf and the 27 f71ff91f6 trace files) is
  governance. Judge flag: with blocker 3 being governance, this
  lane risks becoming a permanent HELD rather than a queued task;
  the loop needs a different K4 design or a decision to retire the
  lane, and endless HELDs must not be mistaken for progress.
- B1 mechanism: NULL [NEW]. No new round subtree, arm, or mechanism
  text in loop scope since the 1121pdt DISCARD; PREREG_B1_P9.md
  stays a re-freeze template (last touched 09bfaae63).
- COMP2-P11: HELD [NEW]. Judge-confirmed: the HELD rests on the
  K-HA-3 vs ruling-6 distinction; RULING_KHA3_2026-09-27.md inside
  57d055bbb records a test-determined ruling on the K-HA-3 spec
  clause and is not ruling 6, which remains OPEN. A future text
  search returning a differently named ruling document must be
  re-checked against this distinction, not assumed.
- Intelligence trades: HELD [NEW]. Judge flag: the lane's stated
  testability depends on the EXP2-K4 corpus, which the lane above
  holds as blocked; the two HELDs lean on the same blocker, which
  is one HELD with extra steps. This is noted for future wave
  planning, not a strike on this wave's stand-down, which is the
  honest entry.
- Sensory: NULL [NEW]. Standing stand-downs in force (G1, D-VID-1,
  ST-1 dead; E3 rejected by Micah in blind A/B); no new big realism
  lever in loop-owned scope.

Interactive survey verdict: NONE loop-owned [NEW]. Three new
interactive entry points found, all Micah's closed D2 new-learner
frontier (h1.zag chat REPL at 9dbd01e26, h2.zag chat REPL plus fuzz
driver at 7979a55b1, h3.zag chat/chat-fixed/chattrace at 7f5a8ccdb):
surveyed read-only, never built, run, certified, or re-judged.
The 16 other fd-0 hits are pre-existing (frozen batch probe
instruments and old-wave batch instruments), the one tui hit is a
code comment, EXP1c iteration 1 sources are clean batch sims. The
judge watches but finds this wave on the right side of the
survey-vs-narrate line: Micah's frontier commits are attributed and
read-only survey citations only.

## M5. Commit-order self-check and untouched lines

Ruling: CONFIRM. Commit order is strict end to end: 8b456736b <
d9e96ad91 < 9625c211a < f26d510f3 < 4750f1a19, verified by
merge-base with no intervening commits; the addendum was committed
alone before any EXP1c implementation file existed (first
exp1c/src appearance at 9625c211a). Nothing is adopted this wave,
so the check is VACUOUS for adoption. VALID here means order-valid
only, per the carried standing caveat: commit order evidences
commit order, never run order, and never content identity (the
calibration vs full-run agent byte difference is labeled under
M1). The other lanes' commits are lane-local and carry no EXP1c
implementation content.

UNTOUCHED [VOID] confirmed on inspection: the six governance
rulings (S7 strike, MD-SSD-1, S11 pull, S11-AUD pull, C12 queue,
Python-mirror logic) appear only as OPEN; all nine sealed blind
pairs (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14,
whirlpool-planform) appear only in untouched lists; DP-1 appears
only as the parent agent's queue decision; Micah's frontier dirs
(continual_learning, workbuddy, hyptest, epistemic_native, and the
surveyed onebrain, Self-PAM, composition, exp2d, D2 new-learner,
combiner_arch, shared-brain, Grow-with-me, NW-1 lines) were touched
read-only via git log and listings. No wave commit decides,
relitigates, or re-presents any of them.

Two interpretive readings are confirmed as judge precedent with
cited evidence, since future waves will cite them: (1) "measurements
from a voided run" is a real record category under the frozen
section 6 validity-gate principle (K1 918<=1200 and K6 1082>=918 /
1200>=920 are true computations from a K7-voided run; no kill claim
may be adopted from them); (2) the K6 operationalization this wave
(excluding COMBINE-containing sketches; red-team R3) is a
reasonable operationalization of "removing novel-composition steps",
not a deviation, but any future adoption must freeze the
operationalization first. The section-7 redraft addendum is confirmed
judge-legitimate: authorized by the 1721pdt debate's binding forward
requirement, committed pre-implementation, changing no bar, gate,
mechanism, horizon, or bonus number. It stays on the right side of
the governance line, and this confirmation is the explicit record of
that.

---

## Verdict lines for LOOP_STATE.md

1. EXP1c wave 2: VOID (uncertified attempt) [VOID], nothing adopted.
K7-VOID verified on the frozen quantity (I-survive 0
post-enumeration selections; I-invent 89 post, 0 learned; fraction
0 < 0.50); K7 takes precedence over the literal K1 and K6 firings
per frozen section 6, so no DEAD label attaches to H1. K1
(918 <= 1200) and K6 (1082 >= 918; 1200 >= 920) are correct literal
computations from the byte-identical TSVs (SHA-256
0e82ba093953da59e0d4d1de25cf75501b5108992857ae281607c9519281c288;
84 RUN plus 48 IDIAG rows each), recorded as measurements from a
voided run and NOT adopted as kills; judge-confirmed precedent: a
void test cannot kill a hypothesis. C3 recorded NOT-MET: the
"qualitatively distinct" claim is struck (f0 and f2 identical
outcomes in all 12 variants; the in-Zag gate counts medians only;
repeat of 1721pdt F10, correction still open); the M5 stop decision
is labeled as taken on that false premise. The znc slice-smear
causal claim is DOWNGRADED to UNPROVEN (red-team probes could not
reproduce it; the original probe is uncommitted); the 1024-element
workaround is validated end to end by byte-identical reproduction.
Calibration and full-run agent sources are not byte-identical
(e1c_agents.zag edited 23 lines at milestone 3; e1c_run.zag added
there); labeled explicitly; red-team M3/M4 verification covers the
final sources. Iteration preserved as an uncertified historical
record with violations labeled (1421pdt precedent). Verified:
M3/M4 verbatim, determinism reproduced end to end twice, pure Zag,
commit order strict
(8b456736b < d9e96ad91 < 9625c211a < f26d510f3 < 4750f1a19),
K4 CANNOT-CONFIRM and K5 INCOMPLETE honestly reported, no retune
shopping. Evidence: exp1c/ (d9e96ad91, 9625c211a, f26d510f3,
4750f1a19), red team bb60f27f5, debate 1eb652a59.

2. Fork battery: CONFIRM [RE-CERT], 55 named entries, 53 PASS,
0 FAIL, 2 UNTESTABLE (rh-pull-1-head 5802fec8, rh-pull-2-head
4b76bb59f, thirteenth wave, pinned toolchain path absent in their
trees, content-dependent cause, never headlined without this
caveat). The 1721pdt FAIL is closed: judge independently verified
the 12 restored toolchain files byte-identical to 8929cdd93
(identical blob SHAs at 8929cdd93 and fc1a43b8c; the two
build-cache files at fc1a43b8c are repair-commit additions, not
pre-loss content); local-tnn-native-lab PASSES at fc1a43b8c with
the probe emitting R32_ZNC_PROBE_OK. Both origin entries newly
testable and PASS at bedf8b4a; one new archive entry (1721pdt
wave archive at 4042f15bf) enumerated and PASS. Harness rebuilt
pure-Zag byte-identical to 1721pdt
(a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66);
znc pin 498abcb5 uniform 53/53; probe sha 3b29aa06 uniform 53/53;
B1/B2/B3 pass and NEG1/NEG2 discriminate. Caution carried: the
mid-run local HEAD move was disclosed and inert by pinning, but
that is a per-instance claim, not a structural fix; live origin
coverage depends on local-store freshness (no fetch authorized).
Scope: toolchain and extraction stability only. Evidence:
forks/FORK_RESULTS_2021.md plus frozen ENUMERATION_MANIFEST.md.

3. tnn_chat FIT: FRESH FIT PASS [NEW, process confirmation].
Certifies the frozen 38-fact closed-book probe chain only, on HEAD
fc1a43b8c; not a candidate verdict and not merge review. KB1 30/30
specific declines with 0 blanket refusals (3 runs); KB2 17/17
answered, 0 declines, byte-identical baseline parity; KB5 10/10
answered, 0 declines, byte-identical baseline parity; binaries
byte-identical to the frozen records (decline 20273a99, baseline
1ada2fae), 2/2 PASS; 9/9 required rerun pairs byte-identical
(15/15 including baseline pairs); all 15 runs exit 0, all stderr
empty; zero Python. Merge-range chain-diff shows exactly one
additive record-only file (SHA256SUMS, pins matching); zero
changes to instruments, fixtures, kb.txt, gaz.txt, R33 support, or
the znc pin. Traveling confabulation caveat carries verbatim.
Evidence: evidence commit 78a8037fd (lane commit 927b3f3f7).

4. Design lane [NEW]: EXP2-K4 corpus HELD (judge-flagged: blocker
reason 3 is governance, not technical feasibility; the lane risks
permanent HELD without a redesign or a retirement decision);
B1 mechanism NULL (no new mechanism text since the 1121pdt
DISCARD; P9 stays a re-freeze template); COMP2-P11 HELD
(judge-confirmed: rests on the K-HA-3 vs ruling-6 distinction;
RULING_KHA3_2026-09-27.md in 57d055bbb is not ruling 6); trades
HELD (judge-flagged: chained to the EXP2-K4 corpus; two HELDs on
the same blocker are one HELD with extra steps); sensory NULL
under standing stand-downs (G1, D-VID-1, ST-1 dead; E3 rejected
by Micah in blind A/B). Survey method with counts, per-lane
blocker evidence with commit ids, and the explicit
nothing-manufactured statement all present per the 1721pdt forward
bar. Evidence: design_lane/HUNT_2021.md.

5. Interactive survey [NEW]: NONE loop-owned. Three new chat entry
points found in the merge range, all Micah's closed D2 new-learner
frontier (h1 at 9dbd01e26, h2 at 7979a55b1, h3 at 7f5a8ccdb):
surveyed read-only, never built, run, certified, or re-judged.
The 16 other fd-0 hits are pre-existing (frozen batch probe
instruments and old-wave batch instruments); the one tui hit is a
code comment; EXP1c iteration 1 sources are clean batch sims.
Evidence: INTERACTIVE_SURVEY_2021.md.

6. Commit-order self-check [NEW]: VALID, VACUOUS for adoption.
Freeze 8b456736b < addendum d9e96ad91 < 9625c211a < f26d510f3 <
4750f1a19, strict, no intervening commits; addendum committed alone
before any EXP1c implementation file existed. VALID means
order-valid only: commit order evidences commit order, never run
order and never content identity. The section-7 redraft addendum is
confirmed judge-legitimate (authorized by the 1721pdt binding
forward requirement, pre-implementation, changing no bar, gate,
mechanism, horizon, or bonus number). The "measurements from a
voided run" reading and the K6 operationalization (R3, recorded as
reasonable; any future adoption must freeze the operationalization
first) are confirmed as judge precedent. Evidence: merge-base
verification this wave.

7. UNTOUCHED [VOID]: the six governance rulings (S7 strike,
MD-SSD-1, S11 pull, S11-AUD pull, C12 queue, Python-mirror logic)
remain OPEN; all sealed blind pairs (R9, C1, C2v3, S11-IMG, C12,
S11-AUD, S13, S14, whirlpool-planform) untouched; DP-1 presentation
remains the parent agent's queue decision; Micah's frontier dirs
(continual_learning, workbuddy, hyptest, epistemic_native, and the
surveyed onebrain, Self-PAM, composition, exp2d, D2 new-learner,
combiner_arch, shared-brain, Grow-with-me, NW-1 lines) touched
read-only via git log and listings. This wave neither decided,
relitigated, nor re-presented any of them.

Provenance: EXP1c wave 2 new this wave (section-7 redraft addendum,
fresh implementation sources, fresh calibration and full-run
evidence, Zag-generated evidence note, independent red-team review,
this debate) on the inherited frozen design (M1-M5, K1-K7, C1-C3
verbatim at 8b456736b; training mass at 5a043af3c; world template
blob fff8af2493bc6dbe9de6fc76f9a6206d887d586a; pinned toolchain
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef);
fork battery new full execution of inherited machinery; FIT new
fresh re-run of the frozen chain; design-lane and survey reports
new; rulings and pairs inherited and untouched.
