# Debate transcript: wave-20260927-0821pdt (advocate / skeptic / judge)

Wave: wave-20260927-0821pdt. Branch: tnn-native-lab. Working HEAD at debate
time: 09bfaae63a6c3225729ca6c73f27c8da83efc5ee (lane commits landed after
the wave records this debate judges; the judged evidence is pinned by
commit in each record below).

Participants: ADVOCATE (argues for each proposed verdict), SKEPTIC (argues
against: gaming, confounds, weak bars, cost, citation-without-execution
risk, record-repair sufficiency, fork-battery relevance, prereg
sufficiency), JUDGE (renders a reasoned ruling with numbers cited per
verdict line).

Evidence before the debate: docs/lab/rsi/runs/wave-20260927-0821pdt/fit/
FIT_RESULTS_0821.md, docs/lab/rsi/runs/wave-20260927-0821pdt/fit/
SHA256SUMS_REPAIR.md, docs/lab/rsi/runs/wave-20260927-0821pdt/forks/
FORK_RESULTS_0821.md, docs/lab/rsi/runs/wave-20260927-0821pdt/forks/
ENUMERATION_MANIFEST.md, docs/lab/rsi/runs/wave-20260927-0821pdt/preregs/
(PREREG_B1_P9.md, PREREG_COMP2_P11.md, PREREG_EXP1c.md, PREREG_EXP2_K4.md),
and the tail of ~/workspace/tnn-rsi/LOOP_STATE.md (wave-20260927-0521pdt
verdicts).

Standing rule on tone (LOOP_STATE): debates relitigate nothing. They test
only what the judged wave added or changed.

## Skeptic's provenance probe (verbatim, required)

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

SKEPTIC's provenance accounting, which the advocate and judge accepted as
complete and correct:

- FIT behavioral battery (verdict 1): NEW EXECUTION this wave. The two
  probe instruments (baseline tnn_chat.zag, decline tnn_chat_decline.zag),
  the two R33 support sources, kb.txt, gaz.txt, the three probe fixtures,
  and the pinned znc are all INHERITED (frozen authority path, unchanged
  since the D1 freeze; merge-range diff on every FIT chain path verified
  empty). What is new: binaries rebuilt on HEAD 80c40a7af (2/2
  byte-identical to pins), 15 fresh probe runs (KB1/KB2/KB5, 3 runs each
  per instrument leg), 15/15 run-pair byte-identical comparisons, and the
  entry-point scan over merge range ecbe9b5b7..80c40a7af.
- SHA256SUMS record defect repair (verdict 2): NEW FILE this wave,
  docs/lab/rsi/fit_authority/SHA256SUMS. The nine checksummed files and
  their pins are INHERITED (frozen authority path); the sha256sum -c
  checkability is NEW.
- Fork battery (verdict 3): NEW EXECUTION this wave of an INHERITED
  battery. The harness (fork_battery.zag, frozen sha
  f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738 from
  the 2321pdt archive branch), the driver approach, the pinned znc, the
  expected output hashes are all INHERITED. What is new: fresh
  enumeration (50 named entries), fresh extraction and testing of 48
  toolchain-bearing entries, and this wave's manifest.
- The four prereg drafts (verdict 4): NEW DESIGN DOCUMENTS this wave
  (lane 3, prereg design commit 59b9df4b0b45ffef23704ad971ae9029e14d7126).
  The lineage each cites (EXP1/EXP1b DISCARD findings, P9 bar-set
  precedent, EXP2 judge ruling of 0221pdt, CV-P / COMP-2 PARTIAL
  [STACK], precedents P3, P10, P11) is INHERITED. The designs themselves
  are NEW but UNFROZEN and untested; they decide nothing.
- Prereg commit-order self-check (verdict 5): VACUOUS. The rule and the
  design commit are INHERITED; nothing new happened this wave.
- The six governance rulings, the sealed blind pairs, DP-1 (verdict 6):
  INHERITED and untouched; this wave adds zero evidence about any of them.
- Interactive TNN verdict (verdict 7): INHERITED instruments, NEW
  execution context (the FIT runs executed the instruments this wave, and
  the entry-point scan ran on the new merge range).

## Verdict 1: FIT behavioral battery

Proposed: CONFIRM FIT behavioral battery [RE-CERT]: KB1 30/30, KB2 17/17,
KB5 10/10, 15/15 byte-identical rerun pairs, binaries match frozen pins,
entry-point scan clean.

ADVOCATE: This is the strongest FIT record in weeks. The standing rule
(0521pdt) mandated a fresh re-run at least every 8 waves; stale count hit
11, and lane 1 ran it. Numbers: KB1 30/30 specific declines, 0 blanket
refusals, 3 runs; KB2 17/17 answered, 0 declines, byte-identical baseline
parity, 3 runs; KB5 10/10 answered, 0 declines, byte-identical baseline
parity, 3 runs. All 15 runs exit 0, all stderr empty. Binary
reproducibility 2/2 PASS (rebuild shas
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7 and
1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
byte-identical to frozen pins). Rerun determinism 9/9 required pairs plus
6 baseline pairs, 15/15 byte-identical. All three output hashes
byte-identical to the 1421pdt prior records. The merge-range diff on every
FIT chain path is empty. Entry-point scan: Layer 1 one hit (prior wave's
own survey prose), Layer 2 all 32 hits inside prior-wave prose, Layer 3
zero src/ or units/ changes, Layer 4 zero stdin-read hits across the 188
new .zag sources. Zero Python anywhere in this work. The staleness the
skeptic has flagged for three weeks is now cleared by execution, not by
citation.

SKEPTIC: I grant the execution numbers; I dispute the tag and the scope
claim. The proposed verdict reads [RE-CERT]. Nothing about this battery
is a re-certification: 11 waves of citation carried the 1421pdt evidence,
and this wave replaced the citation with fresh execution. Calling fresh
execution [RE-CERT] undersells what was done and blurs the very
citation-vs-execution line the standing rule exists to police. Second, the
scope: the merge range scanned (ecbe9b5b7..80c40a7af) predates this wave's
own lane-1 commit be5bb24c8. The verdict's "entry-point scan clean" must
be read as scoped to the scanned range, not as a blanket tip claim; the
traveling caveat (unflagged confabulations on out-of-KB questions) and the
closed-book-only limitation stay. Third, cost: lane 1 spent real compute
on 15 runs of a battery whose instruments, fixtures, and pins are frozen;
if the standing rule fires every 8 waves regardless, fine, but do not let
the rule become ritual. Also note the KB1 output carries the
decline-binary's two phrasing families ("My knowledge base contains
nothing about ...", "No knowledge-base fact ..."): the battery certifies
they are declines, not that the phrasing is good. I do not claim gaming; I
claim the tag is wrong and the scope needs the merge-range boundary
written in.

JUDGE: The numbers are executed evidence and the skeptic does not contest
them; the advocate is right that staleness is cleared by execution, not
citation. The skeptic is right on the tag. This wave's FIT item is a
fresh-execution PASS whose evidence is NEW, and the verdict tag must say
so, because [RE-CERT] in loop usage has meant carried-by-citation
confirmation (see the 0521pdt FIT verdict: "CARRIED BY CITATION [RE-CERT
by citation]"). To reuse it here erodes the distinction. NARROWING:
verdict 1 is narrowed to CONFIRM FIT behavioral battery PASS [NEW]
(fresh re-run execution this wave, KB1 30/30, KB2 17/17, KB5 10/10,
15/15 byte-identical rerun pairs, 2/2 binary reproducibility, entry-point
scan clean over merge range ecbe9b5b7..80c40a7af). Scope stamps carried:
38-fact closed-book chain only; closed-book limitation and the
confabulation caveat travel. The stale count resets to 0 this wave.

## Verdict 2: SHA256SUMS record defect repair

Proposed: CONFIRM SHA256SUMS record defect repair [NEW]:
docs/lab/rsi/fit_authority/SHA256SUMS created, all nine shas byte-verified
against pins before writing, third-party checkable via sha256sum -c.

ADVOCATE: The 0521pdt judge assigned exactly this repair and lane 1
executed it cleanly. All nine authority-path files were verified
byte-exact against the README.md and AUTHORITY_MANIFEST.md pins before
writing; the fixture shas were cross-verified against the FIT_1421.md
evidence. The drafting caught and corrected invented placeholder shas for
README.md and AUTHORITY_MANIFEST.md before commit, which is the self-check
working as designed. Third party verification is one command from the
repo root: cd docs/lab/rsi/fit_authority && sha256sum -c SHA256SUMS, all
nine OK at commit time. Zero Python. This converts pins-as-prose into a
machine-checkable record: exactly what the defect demanded.

SKEPTIC: Sufficiency is the question, and the repair document itself
confesses a hole. Quote: "the frozen built-binary pins (1ada2fae...
baseline, 20273a99... decline) and the pinned toolchain pin (498abcb5...)
remain in README.md prose because those files do not live under this
directory." So a third party still cannot verify the binary pins and the
toolchain pin with the standard command; they must rebuild or trust the
FIT re-run. The repair fixes the authority-path half of the defect and
leaves the binary-toolchain half exactly as it was. That is partial
sufficiency, and a CONFIRM without a scope stamp would overclaim. Second:
self-correction during drafting (the invented placeholder shas) was caught
by the worker, not by an independent checker; the record should say
plainly that the file's correctness at commit time rests on one person's
draft-time grep. Third, nothing in this file certifies the R33 sources or
any candidate work: fine, but it must be stamped so the next wave does not
cite SHA256SUMS as broader authority than it is.

JUDGE: The repair is sufficient for the defect as assigned, and the
assignment was the authority-path record. The 0521pdt verdict's defect
read: "docs/lab/rsi/fit_authority/SHA256SUMS does not exist; pins live in
fit_authority/README.md; repair is assigned." Lane 1 delivered exactly
that. The residual the skeptic names (binary pins and toolchain pin still
in prose) is real and pre-existing, and this wave's FIT re-run
independently re-verified all three values by rebuilding and re-hashing
on HEAD 80c40a7af, so the residual is mitigated this wave, not open
forever. RULING: CONFIRM the repair [NEW], with the scope stamp: covers
the nine authority-path files only (the 38-fact closed-book probe chain),
not the R33 sources, toolchain, or candidate work; the binary and
toolchain pins remain prose records, verified fresh this wave by the FIT
rebuild, and stay queued as a future record item. The placeholder-sha
self-correction is recorded as draft-time self-check, not independent
verification: the file's committed content is final evidence, checkable
now by anyone. No overclaim, no gap papered over.

## Verdict 3: fork battery

Proposed: CONFIRM fork battery [RE-CERT]: 50 named entries, 48 PASS, 2
UNTESTABLE (rh-pull-1/2, pinned toolchain path absent, unchanged cause
nine waves running), 0 FAIL, 0 CONFIRM. Manifest drift: only the new
0521pdt archive branch.

ADVOCATE: Fresh execution this wave on a fresh enumeration: 50 named
entries, 48 PASS, 2 UNTESTABLE, 0 FAIL, 0 CONFIRM. Uniform evidence
grepped across all 48 PASS runs: znc pin 498abcb5... on 48/48, probe
source sha 3b29aa06... on 48/48, B1 byte-identical
FORKBATTERY-OK 42 on 48/48 (run sha 5dfe3c16...), B2 bin sha
75b85d3c... on 48/48, B3 strict exit 0 on 48/48, NEG1 failing as required
on 48/48 (E0002), NEG2 differing at char 1 on 48/48, tree probe
R32_ZNC_PROBE_OK on 48/48, harness VERDICT=PASS exit 0 on 48/48. Live
entries: local-tnn-native-lab (moved ecbe9b5b7 to 80c40a7af) and the
newly enumerated arch-20260927-0521pdt branch, both PASS at the pinned
commit. The two UNTESTABLEs are the expected pull-heads: git show
redirects left 0-byte znc.bin files, both deleted before archiving; cause
identical nine waves running (non-TNN research-doc trees, no src/).
Manifest drift vs 0521pdt: one new archive branch, no missing refs, all
remote tips unchanged at start and close, all 14 worktrees SHAs
re-verified unchanged. Zero Python in the worker's work. Scope stamp is
carried: toolchain and extraction stability only.

SKEPTIC: Fresh execution, yes; but let me press relevance and the two
UNTESTABLEs. First, fixtures: 48 of 50 entries are fixtures; the two live
entries test the same commit 80c40a7af twice. The three experimental
branches (exp1, exp2, exp-sensory) are under concurrent implementation,
tested at pinned commits while workers write new tips: the results
certify toolchain stability at stale commits, not at the moving fronts.
Second, the pull-head UNTESTABLEs: nine waves running with the same two
entries untestable for the same reason. The label changed from extraction
FAIL to UNTESTABLE per lane instruction, but the battery's coverage of
those trees has not moved in nine waves. When does a standing UNTESTABLE
become a queued coverage item instead of a verdict line? Third, the
lane-1 HEAD-move incident (see below) means the tested local HEAD
(80c40a7af) was already superseded by be5bb24c8 before the worker
finished; the advocate says pinned commits make this inert, and I agree
for the tested entries, but the "live" local-tnn-native-lab entry now
describes a HEAD the branch has already left behind. The verdict should
name the pinned commit it actually tested, which it does; I want the
parent to notice the loop's own wave-HEAD cadence is racing the
three-hour wave cadence.

JUDGE: The battery's job is toolchain and extraction stability on
explicitly pinned commits, and on that job the numbers are complete:
48/48 uniform evidence grepped, not sampled; 39 unique commits; all tips
re-confirmed at close. The skeptic's fixture critique is answered by the
battery's own classification rule (fixture = unchanged-SHA coverage;
live = moved, newly enumerated, or newly testable), which the judge
accepted in prior waves and which this wave applies consistently: live
entries 9 to 2 this wave is honest drift, not coverage loss. The
exp-branch staleness is disclosed in the report itself (pinned-commit
caveats, RESULT.txt pins the tested commit), and "mid-run tip movement
cannot have affected the results" is a statement about result integrity,
not a claim that stale commits cover the moving fronts: the scope stamp
(tool chain stability only, not contents) carries that. On the
UNTESTABLEs: nine waves of the same cause is itself the evidence; the
trees lack the pinned toolchain path, a property of their contents, and
the battery cannot test what the battery tests without it. RULING:
CONFIRM fork battery [RE-CERT] stands as proposed, with the scope stamp
carried verbatim: 50 named entries, 48 PASS, 2 UNTESTABLE
(rh-pull-1/2, pinned toolchain path absent, unchanged cause nine waves
running), 0 FAIL, 0 CONFIRM; toolchain and extraction stability only on
the tested pinned commits, not the contents of the tested commits. The
standing coverage question the skeptic raises (when UNTESTABLE becomes a
queued coverage item) is noted for the parent's queue, not decided here.
Lane-1's commit be5bb24c8 moved the branch tip after the run-start pin;
the tested local entry is explicitly the task-pinned run-start HEAD
80c40a7af, so no result is invalidated (see incident (c) below).

## Verdict 4: prereg drafts queued as designed-not-adopted (no verdict)

Proposed: QUEUE prereg drafts as designed-not-adopted (no verdict): EXP1c
(K7 choice-reality bar), EXP2-K4 (spec-blind curator, KH1-KH4),
B1-P9 (KB4a'/KB4b'/KB6'/KB0' reformulation), COMP2-P11 (ruling-6 gate
frozen, two-leg stemmer plan).

ADVOCATE: Four lane-3 design documents, each DRAFT, each carrying a
provenance header that names its lineage, each explicitly
NEW_KNOWLEDGE_CLAIM: none (or none yet). They decide nothing this wave:
they are frozen-bar candidates for future waves. EXP1c answers the
decisive EXP1b finding (B0 novelty bonus exceeded experienced mean
delta-energy within 600 ticks; EXP1b measured enumeration, not choice)
with a shrunk plan space, longer horizon, and decaying novelty bonus, plus
a K7 choice-reality bar. EXP2-K4 answers the 0221pdt judge ruling (K4
hardening could not fail by construction; rescuer lens b2 reached the
shared verdict 10/10 uncontrolled) with real-failure-trace sourcing, a
spec-blind curator, and KH1-KH4. B1-P9 operationalizes precedent P9 (a
bar set a content-free control would pass is unfit; flat-tint
counterexample kills KB4a/KB4b/KB6 as written) with KB4a', KB4b', KB6',
KB0'. COMP2-P11 answers precedents P3 and P11 (P3: missing
author/implementer separation caps at PARTIAL, rotated-author re-test
required; P11: stemmer-contingency records as [STACK] with re-derivation,
not re-vote) and keeps the ruling-6 gate frozen. None are adopted, so the
commit-order rule has nothing to gate and the Python-void rule is not
triggered. Design commit 59b9df4b0b45ffef23704ad971ae9029e14d7126.

SKEPTIC: Prereg sufficiency is my remit, and drafting is the cheap part.
EXP1c's K7 is a bar name, not yet a measurement; EXP2-K4's spec-blind
curator must survive the same wire-in temptation the 0221pdt ruling took
off the table; B1-P9's percentile-based edge bars must be shown to kill
the flat-tint counterexample before any re-freeze leans on them;
COMP2-P11 is a plan to re-derive evidence that may yet be voided by
ruling 6. The governance tightening (commit-order self-check, no
pre-authorized Python, void-on-sight preregs) means these drafts will be
judged harshly at freeze time: "DRAFT FOR FREEZE" is not a verdict, and I
want it on record that queuing them confers zero evidentiary weight. I
accept the no-verdict line but register that the loop now holds four
unfrozen designs whose freeze-time scrutiny is the only thing that
matters.

JUDGE: Both sides agree this line carries no verdict. RULING: QUEUE as
proposed: four drafts queued as designed-not-adopted, zero evidentiary
weight conferred, adoption requires the standing freeze-time gates
(commit-order, ruling-6 where applicable, pure-Zag, frozen bars before
implementation). The skeptic's scrutiny preview is banked, not ruled on.

## Verdict 5: prereg commit-order self-check

Proposed: VACUOUS prereg commit-order self-check: no loop candidate
implementation commits this wave; prereg design commit 59b9df4b0 exists
and strictly precedes any future implementation commits.

ADVOCATE: The rule (minted 09-24 governance tightening): the prereg's
first commit must strictly precede the implementation's. This wave has no
loop candidate implementation commits, so the check is vacuous by
definition. The prereg design commit 59b9df4b0b45ffef23704ad971ae9029e14d7126
exists in the record, so any future implementation commit will be ordered
against it. Nothing to gate.

SKEPTIC: Vacuous is the right word but let me stress the standing caveat
from the 0521pdt judge, which I want re-entered verbatim in substance:
the check evidences commit order only, never run order; sub-minute
margins on this repo's clocks are weak evidence; "pre-run, no scores
seen" must be asserted, not reported as a finding. Moreover, this wave's
own lane-1 HEAD-move incident shows multiple lane workers committing to
the same branch during a wave: commit order across lanes is meaningful
only if the implementation lanes actually pin their prereg commit before
writing code, which is a future-wave question this wave cannot answer.
The check stays vacuous; the caveat travels with it.

JUDGE: VACUOUS as proposed, with the standing caveat carried: the check
evidences commit order only, never run order; "pre-run, no scores seen"
must be asserted by the implementing lane, not inferred from timestamps.
Design commit 59b9df4b0 recorded for the ordering chain.

## Verdict 6: governance rulings, sealed pairs, DP-1 untouched

Proposed: UNTOUCHED [VOID]: the six governance rulings, all sealed blind
pairs, DP-1 presentation; none relitigated, re-presented, or decided.

ADVOCATE: The debate's standing rule is that debates relitigate nothing.
This wave's records touch none of the six governance rulings (S7 strike,
MD-SSD-1, S11 pull, S11-AUD pull, C12 queue, Python-mirror logic), none
of the sealed blind pairs (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14,
whirlpool-planform), and the DP-1 repaired pair stays queue-HELD per the
0521pdt ruling, a parent-agent queue decision. No verdict line this wave
depends on any of them. UNTOUCHED [VOID] is the honest tag.

SKEPTIC: I asked for one thing and got it: the records do not mention,
re-present, or decide any of the tainted items. I verified the FIT,
SHA256SUMS, fork, and prereg documents contain no blind-pair
re-presentation and no ruling decision. One observation for the parent:
the COMP2-P11 prereg draft discusses ruling 6 as a gate without deciding
it, which is the correct posture and must be preserved at freeze time.
The [VOID] tag stays; nothing was narrowed by debate.

JUDGE: UNTOUCHED [VOID] stands. The COMP2-P11 draft's ruling-6-gate
posture (discusses as gate, decides nothing) is the correct posture and
is recorded here so the freeze-time review holds it.

## Verdict 7: interactive TNN

Proposed: Interactive TNN: tnn_chat is runnable (FIT battery executed
against it this wave); no fake; entry-point scan confirms no new
interactive entry points.

ADVOCATE: This wave executed 15 live probe runs against binaries rebuilt
from the frozen sources on this HEAD: the instrument is genuinely
runnable, and "no fake" is evidenced by the byte-identical rebuilds and
the executed outputs (KB1 30/30 declines, KB2/KB5 answered, all stderr
empty). The entry-point scan over merge range ecbe9b5b7..80c40a7af found
no new chat/REPL/interactive entry points: Layer 4's stdin-read backstop
(standing addition from the 0521pdt judge) scanned all 188 new .zag
sources with zero hits; all hits in Layers 1 and 2 were prior-wave prose;
Layer 3 shows zero src/ or units/ changes. The tip-state statement is
carried: no runnable interactive TNN exists on this branch beyond the
frozen probe instruments (archived tnn_chat.zag and tnn_chat_decline.zag,
a stdin line loop over the 38-fact KB, /new resets the conversation).
The traveling caveat (unflagged confabulations on out-of-KB questions)
and the closed-book-only limitation travel with it.

SKEPTIC: I accept runnable and no-fake on the evidence of the 15
executed runs. My pressure is on the second half of the claim. The
entry-point scan's merge range is ecbe9b5b7..80c40a7af; lane 1's own
commit be5bb24c8 landed after the run-start HEAD and is not in the
scanned range. The tip-state statement in FIT_RESULTS_0821.md was written
against the run-start HEAD's merge range. The verdict as phrased,
"entry-point scan confirms no new interactive entry points," should be
scoped to the scanned range, with the post-range lane-1 commit noted as
wave-record files only (FIT_RESULTS_0821.md, SHA256SUMS_REPAIR.md, per
the incidents section). I do not allege a new entry point; I allege the
claim needs its range boundary written in, or it will be cited next wave
as a blanket tip certification.

JUDGE: The skeptic's scoping point is correct and cheap to fix. RULING:
verdict 7 holds, narrowed to state its range explicitly: tnn_chat is
runnable (15 live runs this wave against binaries rebuilt on HEAD
80c40a7af, byte-identical to frozen pins); no fake; entry-point scan over
merge range ecbe9b5b7..80c40a7af confirms no new interactive entry
points; the post-range lane-1 commit be5bb24c8 contains only this wave's
record files (FIT_RESULTS_0821.md, SHA256SUMS_REPAIR.md). Tip-state
statement carried: no runnable interactive TNN on this branch beyond the
frozen probe instruments; closed-book-only limitation and the
confabulation caveat travel.

## Required cross-cutting questions

(a) Carry-over from citation to fresh execution for FIT (is the staleness
now cleared?): YES. The 0521pdt verdict carried FIT by citation, 11 waves
stale, with the standing rule mandating a fresh re-run at least every 8
waves. This wave executed the full battery fresh (15 runs, 15/15
byte-identical run-pairs, 2/2 binary reproducibility, entry-point scan on
the new merge range). Zero drops vs the 1421pdt baseline. The stale count
resets to 0. The tag change from [RE-CERT] to [NEW] on verdict 1 records
exactly this transition.

(b) Is the SHA256SUMS repair genuinely sufficient as a record
(third-party check?): Sufficient for the defect as assigned: any third
party can run sha256sum -c SHA256SUMS from docs/lab/rsi/fit_authority and
get all nine OK (nine files verified byte-exact against the README.md and
AUTHORITY_MANIFEST.md pins before writing). The repair is explicitly NOT
a broader certification: it covers the 38-fact closed-book probe chain's
authority path only; the binary and toolchain pins remain prose in
README.md (verified fresh this wave by the FIT rebuild) and the R33
sources and candidate work are outside its scope. The residual is queued
as a future record item, not papered over.

(c) Does the lane-1 HEAD-move incident during lane 2's run invalidate
anything?: NO. Lane 1 committed be5bb24c8 ("wave-20260927-0821pdt lane 1:
FIT fresh re-run PASS ...") while lane 2 was still running at its
task-pinned run-start HEAD 80c40a7af. The fork battery extracts every
entry at pinned commits via read-only git show; per-entry RESULT.txt
pins the tested commit; the live entries (local-tnn-native-lab,
arch-20260927-0521pdt) are explicitly the run-start HEAD 80c40a7af, which
the new archive branch tips. Mid-run branch-tip movement cannot have
affected any result. Lesson carried for the parent's queue: lane commits
landing mid-battery are inert under pinned-commit extraction, but the
loop's own wave-HEAD cadence now visibly races the three-hour wave
cadence; the battery should keep pinning and stating the tested commit
(which it did).

(d) Tag audit ([NEW]/[RE-CERT]/[STACK]/[VOID]):

- Verdict 1: narrowed [RE-CERT] to [NEW] (fresh re-run execution this
  wave; see judge ruling above). The prior wave's FIT line was
  carried-by-citation [RE-CERT by citation]; this wave replaces citation
  with execution, and the tag must not recycle.
- Verdict 2: [NEW] kept (new file, new checkability).
- Verdict 3: [RE-CERT] kept (fresh execution of the inherited battery;
  confirms stability, certifies no new knowledge).
- Verdict 4: no verdict, QUEUE. Correct; zero evidentiary weight.
- Verdict 5: VACUOUS. Correct; nothing to gate this wave.
- Verdict 6: [VOID] kept (untouched).
- Verdict 7: narrowed wording to carry the scanned merge range; tag is
  descriptive, not a certification tag, and the tip-state stamp stands.
- No verdict line warrants [STACK] this wave: no stacked component claims
  were tested.

## Final rulings (judge)

1. CONFIRM FIT behavioral battery PASS [NEW]: KB1 30/30 specific
   declines, 0 blanket refusals (3 runs); KB2 17/17 answered, 0 declines,
   byte-identical baseline parity (3 runs each); KB5 10/10 answered, 0
   declines, byte-identical baseline parity (3 runs each); binary
   reproducibility 2/2 PASS; rerun determinism 9/9 required run-pairs
   byte-identical (15/15 including baseline pairs); all three output
   hashes byte-identical to the prior wave records; entry-point scan
   clean over merge range ecbe9b5b7..80c40a7af; 38-fact closed-book
   chain only; zero Python in this work; stale count resets to 0.
   (Tag narrowed: proposed [RE-CERT] overturned to [NEW].)

2. CONFIRM SHA256SUMS record defect repair [NEW]:
   docs/lab/rsi/fit_authority/SHA256SUMS created; all nine shas
   byte-verified against the README.md and AUTHORITY_MANIFEST.md pins
   before writing; third-party checkable via sha256sum -c (all nine OK
   at commit time). Scope stamp: authority-path files only (the 38-fact
   closed-book probe chain); binary and toolchain pins remain prose in
   README.md, verified fresh this wave by the FIT rebuild; R33 sources
   and candidate work outside scope.

3. CONFIRM fork battery [RE-CERT]: 50 named entries, 48 PASS, 2
   UNTESTABLE (rh-pull-1/2, pinned toolchain path absent, unchanged cause
   nine waves running), 0 FAIL, 0 CONFIRM. Toolchain and extraction
   stability only, on the tested pinned commits (local entry explicitly
   the run-start HEAD 80c40a7af), not the contents of the tested
   commits. Manifest drift: one new archive branch
   (tnn-native-lab-wave-archive-20260927-0521pdt at 80c40a7af); no
   missing refs; all remote tips unchanged at start and close; all 14
   worktrees SHAs re-verified unchanged.

4. QUEUE prereg drafts as designed-not-adopted (no verdict): EXP1c,
   EXP2-K4, B1-P9, COMP2-P11. Zero evidentiary weight conferred;
   adoption requires the standing freeze-time gates.

5. VACUOUS prereg commit-order self-check: no loop candidate
   implementation commits this wave; design commit 59b9df4b0 recorded.
   Standing caveat carried: commit order only, never run order.

6. UNTOUCHED [VOID]: the six governance rulings, all sealed blind pairs,
   and DP-1 presentation; none relitigated, re-presented, or decided.

7. Interactive TNN (scoped): tnn_chat runnable (15 live runs this wave,
   binaries rebuilt on HEAD 80c40a7af byte-identical to frozen pins); no
   fake; entry-point scan over merge range ecbe9b5b7..80c40a7af confirms
   no new interactive entry points (post-range lane-1 commit be5bb24c8
   is wave-record files only). Tip state: no runnable interactive TNN
   beyond the frozen probe instruments; closed-book-only limitation and
   the confabulation caveat travel.

## Debate integrity attestations

- The skeptic's provenance probe above appears verbatim: "What is the
  provenance of the artifacts under judgment, and what exactly is new
  versus inherited?"
- Provenance of every artifact on the slate is addressed in the probe
  section (new vs inherited enumerated per verdict).
- This debate relitigated nothing: the six governance rulings, the
  sealed blind pairs, and DP-1 were not touched, re-presented, or
  decided.
- Zero Python touched by this debate group (read-only reads of the wave
  records via file tools; this transcript authored with the file tool).
- Zero em-dashes in this transcript (rule verified by grep before
  commit).
