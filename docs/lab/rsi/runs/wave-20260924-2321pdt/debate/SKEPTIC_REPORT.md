# SKEPTIC REPORT, wave-20260924-2321pdt debate group

Role: SKEPTIC (red-team). Wave: wave-20260924-2321pdt.
Repo: ~/workspace/tnn-rsi, branch tnn-native-lab.
Method: every claim below was checked against the committed git record.
Summaries in worker reports were not trusted; the commits were read.
No Python was used in this review (shell and git only). No em-dashes
appear in this document. Nothing was pushed.

Each motion below contains the skeptic's provenance probe verbatim, as
required. A motion lacking it would be incomplete.

---

## MOTION 1: G1 v3 SUNSHAFTS, coordinator verdict CONFIRM DISCARD [NEW]

Provenance probe, verbatim: "What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?"

Answer: the artifacts under judgment are the committed 1721pdt wave
records, not new renders. Prereg acf7cedce (2026-09-25 00:57:43 UTC,
329 insertions, prereg plus NOVELTY_ARGUMENT_1721.md). Sign addendum
1da140387 (2026-09-25 01:17:00 UTC, single file, 66 insertions,
committed alone). Implementation and evidence 39707e077 (2026-09-25
01:24:34 UTC: three variant BMPs, base BMP, verifier outputs, validator
outputs, walltime log). The red-team review under judgment is
5c886fb1f, which created no renders and re-ran nothing. What is new in
this review: an independent byte-level BMP diff and a geometric
disjointness argument. What is inherited: the verifier's recorded
KB2-KB8 numbers, read from evidence_verify_v3.txt, not recomputed by
re-running the verifier.

### Attacks

(a) Independence of the recomputation. PARTIALLY SUSTAINED, not
verdict-changing. The report is honest that "no pipeline was re-run,"
but its section header "Frozen-bar recomputation from committed BMPs
and logs" overclaims for KB2-KB8: those numbers (KB2 ratio 1.0000, KB3
var 0.00, KB4 0.00, KB5 0.00, KB6 1.0000, KB7 0, KB8 2.10x) are read
from the frozen verifier's own output file and checked against the
frozen bars. If the verifier miscomputed a metric, the error survives
both the original run and this review, because both read the same
evidence_verify_v3.txt. Conceded in the other direction: the killing
evidence does NOT rest on the verifier. The reviewer independently
diffed base.bmp vs var_v3_1.bmp at byte level (2622 pixels with changed
channel bytes; lifted bbox y 308..458) and I verified the wedge
generator in the committed source
(g1_verify_v3.zag, commit 39707e077): v_wedge_y(r,t) = 300 - t*36 for
t in 1..8, so every generated wedge point has y <= 264, and every kept
wedge point is a subset of the generated set. The lifted band
(y >= 308) is therefore disjoint from every kept wedge point by
construction, which entails dL = 0 at all 39 kept wedge points, which
entails KB2 = 1.0000 (< 1.12) and KB3 = 0.00 (< 60.0) under any correct
implementation of the frozen formulas. A verifier bug cannot rescue
the candidate; it could only misreport the margin. The DISCARD verdict
stands on geometry, not on the verifier's arithmetic.

(b) The tripwire bar (50..150 per mille) lived only in the runner,
not the frozen prereg. SUSTAINED AS A LABELING CORRECTION. A bar that
exists only in run_g1v3.sh lines 118-130 is not a frozen kill bar; it
is a runner sanity check, and the report concedes exactly that. It
carried no verdict weight, it measured 87.89 per mille (inside
[50,150]), and the runner file is byte-stable inside the implementation
commit, so no weakening occurred. This is not a procedural hole that
changes any verdict. Narrowing: the debate record should relabel it
"runner sanity check (non-bar)" so a future wave cannot cite it as a
passed kill bar.

(c) The sign addendum adopting prose over the frozen formula.
NOT SUSTAINED. The addendum is the real thing: committed alone at
01:17:00 UTC, strictly before the implementation at 01:24:34 UTC, dated
pre-implementation, quoting the coordinator decision verbatim. The
correction did not weaken a bar: SGATE moved from the formula's 1088 to
the prose reading's 1152, both frozen measured quantiles passing about
10 percent by construction, derived from the committed phase-1
T-distribution measurement with no renders involved. Most decisively,
the addendum bought nothing: the verdict it enabled was DISCARD. A
post-hoc rescue that rescues nothing is not a rescue. Commit-order
discipline under S10 is satisfied (prereg < addendum < implementation,
all ancestors verified).

(d) "Stand down until a genuinely new design idea": verdict or evasion
of the hunt mandate? VERDICT, NOT EVASION. The mandate is to hunt free
lunches, not to keep a dead lane on life support. G1 v3 is the second
consecutive mechanism miss on sunshafts (v2 DISCARD confirmed at the
1421pdt debate; v3 killed on KB2/KB3 with zero overlap between lift and
wedge set). The 1421pdt judge already ruled that any future shaft wave
must be "a mechanism redesign, not a re-freeze." Standing the lane down
until a genuinely new design idea exists is that ruling applied. It
would be evasion only if extended to the whole hunt; the verdict is
lane-scoped.

### Recommended ruling: CONFIRM

CONFIRM DISCARD [NEW] for G1 v3, with the (b) relabeling noted. Every
killing number is grounded in the committed record; the mechanism-miss
reading (sector-agnostic angular-minimum predicate lifts pixels that
never intersect the frozen upward wedge fan) is consistent with the
recomputed evidence. No CANNOT-CONFIRM item survives: the records are
present.

---

## MOTION 2: Fork battery [RE-CERT], 25/25 PASS (commit b03063b37)

Provenance probe, verbatim: "What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?"

Answer: the artifact under judgment is FORK_RESULTS_2321.md plus the
scratch at ~/workspace/tnn-forkbattery-2321pdt (outside the repo). What
is inherited: the harness source (extracted read-only from archive
branch tnn-native-lab-wave-archive-20260923-2321pdt, sha f38d9154...,
rebuilt byte-identical to last wave's a2e6284c... binary), the pinned
znc (498abcb5...), the probe (3b29aa06...), the frozen battery
procedure. What is new this wave: the observation itself, 25/25 forks
tested at their current commits, including the moved origin/tnn-native-lab
tip 7872124430 and the moved origin/main tip 6e621178, both tested
read-only, plus the new archive branch
tnn-native-lab-wave-archive-wave-20260924-1721pdt. Nothing was checked
out, merged, reset, or pushed.

### Attacks

(a) Third straight wave of 100% PASS: divergence detector or ritual?
PARTIALLY SUSTAINED, narrowed. The battery has teeth, and the negative
controls prove it: NEG1 (unterminated string) exits 1 on compile and
check, NEG2 (wrong-output program) fails the byte-compare, on all 25
forks, zero CANNOT-CONFIRM. A silently broken toolchain would be
caught. But the headline count is inflated by static fixtures: 7
forktest/* detached worktrees carry unchanged SHAs across waves
(293602fb1, a0e7f8ba2, 991432226, bd3097874, cea8db22f, 3947dca1a,
f875b3417), and the three ~/workspace/tnn-rsi-wave3/ worktrees are
literally the same commit bd3097874 counted three times. That is 10 of
25 entries that cannot move and therefore cannot fail on drift. The
battery did track real movement this wave (origin/main moved since last
wave, origin/tnn-native-lab moved mid-wave), so it is not pure ritual,
but the honest live count is 15, not 25. Narrowing: report live vs
fixture entries separately, or refresh/retire the static worktrees.

(b) Origin moved mid-wave; any untested window? NARROWED TO A SMALL
PROCEDURAL GAP. The report states the move was observed before the
battery ran (run-start tip 14c8838558a superseded by 7872124430) and
both tips were tested read-only, never checked out or merged. That
covers the observed move. What is missing: no documented closing
re-observation of the origin tip after the last fork test. A move
between the final test and the report commit would leave an untested
tip. The window is small and nothing in the record suggests a second
move, but the driver should add a closing tip check and record it.

(c) Six forktest worktrees share old SHAs: stale fixtures? SUSTAINED
AS DISCLOSED. They are stale by design (pinned old commits), and the
report discloses the SHAs rather than hiding them. Stale is not the
same as dishonest, but a fixture that can never change contributes no
detection power; it only guards against worktree corruption. Keep them
only if that is the stated purpose.

Python contact: none claimed, shell/git/sha256sum only; no .py
involvement in the battery path. No evidence to contradict.

### Recommended ruling: CONFIRM, NARROWED

CONFIRM the 25/25 PASS re-certification on its literal scope (toolchain
identity and frozen battery behavior at the tested commits). Narrowings
for the record: (1) split future counts into live forks vs static
fixtures; (2) add a closing origin-tip re-check to the driver;
(3) state the purpose of the pinned worktrees or retire them.

---

## MOTION 3: tnn_chat FIT [RE-CERT], FIT on ead33399e (commit c4f006ea7)

Provenance probe, verbatim: "What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?"

Answer: the artifact under judgment is TNCHAT_FIT_2321.md. What is
inherited: the frozen FIT instrument sources (tnn_chat.zag c0776ad6...,
tnn_chat_decline.zag a87011fe..., R33_NATIVE_IO_V1.zag e6379ddb...,
R33_NATIVE_SHA256_V2.zag 9824f6db..., all extracted read-only from the
2321pdt archive branch and hash-matched), the frozen fixtures from the
1121pdt wave, the 38-fact KB (HEAD's canonical kb.txt 3ef27296... and
gaz.txt b75fd113..., hash-matched). What is new: the rebuild and probe
runs on merged HEAD ead33399e (merge of origin/tnn-native-lab into
tnn-native-lab), with both binaries reproducing the frozen shas
(20273a99..., 1ada2fae...) and all three probe outputs byte-identical
to the prior wave's records across 9/9 run-pairs.

### Attacks

(a) Literal scope vs the merge: does FIT say anything about the merge?
THE REPORT CONCEDES THE POINT ITSELF, so there is nothing to overturn.
It states: "This re-certifies the frozen FIT instrument chain on the
new merge commit only. It is not a candidate verdict and it is not
merge review of the merged-in work." And: "This certifies the 38-fact
closed-book probe chain only." The FIT verdict therefore carries zero
weight about the contents of the merged-in commits. I verified the
merge commit exists as described (ead33399e, parents 63156682c1 and
14c8838558a, "Merge remote-tracking branch 'origin/tnn-native-lab'
into tnn-native-lab"). The one verification I could not reproduce from
this clone is the "193 origin commits" figure (this clone's history
shows 1 commit of difference on that leg); the figure is immaterial to
the verdict either way. Narrowing: the [RE-CERT] label must never be
cited as evidence about the merge; it is evidence about the instrument
chain only. The report already says this; the debate should keep it
quoted.

(b) Same binary hashes re-certified for many waves: what would make
this check FAIL? IT HAS DISCRIMINATING POWER IN ITS NARROW SCOPE, and
the failure modes are explicit. FAIL triggers: either rebuilt binary
sha differs from the frozen record (STOP condition, probes do not run),
KB1 not 30/30 specific declines or any blanket refusal, KB2/KB5
answers wrong or not byte-identical to the baseline binary, or any of
the 9 run-pairs not byte-identical. That is a toolchain-and-KB drift
canary by design: it fails if the pinned znc, the KB sources, or the
build environment drift. It will never fail on the merge's semantic
content, because that is outside its literal scope (see (a)). Calling
that a weakness misunderstands the instrument. The byte-identical
outputs across waves are the point, not a ritual.

Python contact: none claimed; extraction, build, run, and greps via
shell only. No evidence to contradict.

### Recommended ruling: CONFIRM, NARROWED

CONFIRM the FIT re-certification on its literal scope: the 38-fact
closed-book probe chain on HEAD ead33399e, binary reproducibility 2/2,
KB1 30/30, KB2 17/17, KB5 10/10, determinism 9/9. Narrowing: the debate
record must carry the report's own scope sentence verbatim so no future
wave cites this FIT as merge review.

---

## MOTION 4: D-VID-1 V3, prereg CERTIFIED prereg-only (0ba679b11), implementation evidence VOID after python3 breach (ca1d4a13a)

Provenance probe, verbatim: "What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?"

Answer: the artifacts under judgment are (1) the frozen prereg
PREREG_DVID1_V3_2321.md, committed alone as 0ba679b11 (2026-09-25
06:47:01 UTC, 328 insertions, single file, parent c4f006ea7); and
(2) the breach disclosure BREACH_DISCLOSURE.md, committed alone as
ca1d4a13a (2026-09-25 06:55:45 UTC, 109 insertions, single file).
What is inherited: the V1/V2 lineage and the M4 R3 reopen condition
from the 0521pdt debate, the D-VID-1 baseline (ocean.zag) and its
frozen bars. What is new: the V3 geometry-churn design (frozen
formulas), and the self-disclosed python3 heredoc that patched a
scratch byte-copy of the implementation. The implementation itself
(ocean_dvid1_v3.zag, substrate/, v3_bin) exists UNCOMMITTED in the
working tree; no implementation or evidence commit exists, which is
correct for voided evidence.

The prereg's provenance header, quoted verbatim:

"## Provenance header (frozen)

- RENDER_SHA: (to fill at implementation; sha256 of the frozen variant
  generator source ocean_dvid1_v3.zag, 64 hex chars)
- FIRST_RENDERED_WAVE: wave-20260924-2321pdt
- COMPONENT_LINEAGE:
  - D-VID-1 V1 (flow-advected foam breakup): DEAD [NEW],
    wave-20260923-2321pdt. Killed on frozen T1 bar: variant 606 vs
    baseline 580 per-mille foam flips, ratio 1.045 against bar <= 0.700.
  - D-VID-1 V2 (co-rotating foam breakup): DEAD [VOID],
    wave-20260924-0521pdt. Analytic no-op proof: bfade =
    o_clamp01k((200 - wz) * 1000 / 140) = 0 for wz >= 200; vortex disc
    wz 560..880, so every V2-retargeted term is gated dead (bupm = 1000,
    streak multiplier = 1, abupm dead code); ocean.zag diff exactly
    three hunks. Wave evidence VOID on a mid-wave python3 heredoc
    touching v2_verify.zag (frozen VKB5).
  - Whirlpool SCOOP: DISCARDED.
  - Whirlpool surface-planform: READY-FOR-JUDGE, QUEUED-UNJUDGED.
- NEW_KNOWLEDGE_CLAIM: In-plane deterministic displacement of disc foam
  geometry (not breakup sampling) raises screen-space foam boil by at
  least 30 percent over the rigid-sweep baseline while holding the
  V-TEMP, V-SHARP, determinism, and cost bars, giving the loop a live
  non-rigid churn lever for whirlpool foam.
- This prereg is the S8 return path for the 0521pdt debate M4 R3
  closure: "DEAD is the coordinate-retargeting of breakup sampling for
  disc foam churn (bfade = 0 kills every retargeted term). OPEN under a
  fresh prereg only: (a) disc foam churn via a DIFFERENT mechanism
  (geometry churn), or (b) a redefined goal." This document takes path
  (a). It is a genuinely new mechanism, not a re-freeze of V1/V2.
- No Python is authorized by this prereg. Not for the generator, not
  for the verifier, not for hashing, not for analysis, not for /tmp
  scratch. Any Python contact with a new wave artifact voids its wave
  evidence (M4 R1, prospective)."

### Attacks

(a) Under the STRICT lineage reading, is the prereg really untainted,
or does the breach poison the whole V3 line? SPLIT FINDING. The prereg
document is untainted as a document, and this is git-verifiable: it was
committed alone at 06:47:01 UTC, the python contact came later
(self-reported ~06:53, disclosure committed 06:55:45), and python never
read or wrote the prereg file. Time-ordering protects the document's
content. But the worker's "void assessment" is self-serving where it
matters: it claims "The prereg survives as a certified frozen prereg"
while in the same breath conceding "the lane returns only under a
fresh prereg in a later wave per S8." Those two sentences contradict
each other, and the debate should adopt the stricter one. The poison
runs prereg-formulas -> implementation bytes -> python-processed
byte-copy: the heredoc did not just touch random bytes, it inserted
probes that printed the churn field's internals (wx, wz, vwx, vwz, gr,
churn_gate) at a probe pixel. That is python-assisted inspection of the
mechanism's behavior. Under the strict lineage reading (a redo must be
genuinely re-authored; the 1421pdt judge barred re-freezes in favor of
fresh preregs), certifying 0ba679b11 as reusable would let the loop
launder python-inspected design confidence through a nominally clean
document. The document stands as a frozen historical record; it must
not be certified for carryover.

(b) The timeline is only half verifiable, and the worker's assessment
leans on the unverifiable half. VERIFIED FROM GIT: prereg committed
alone at 2026-09-25 06:47:01 UTC (single-file commit, parent
c4f006ea7); breach disclosure committed alone at 06:55:45 UTC. NOT
verifiable from the committed record: the breach time (~06:53), the
claim that python touched only the disposable scratch copy
(/home/hatch/workspace/tnn-frames/dvid1_geomchurn/probe.zag, deleted
via rm outside the repo), and the claim of a single invocation. Those
rest on the worker's self-report plus coordinator transcript review.
I accept them provisionally: the disclosure is detailed (exact command
line quoted), self-incriminating, attempts no cure (S3 stands), and
correctly voids the wave's own evidence. But the debate record should
note the ordering rests on testimony, not on the committed record, and
treat the worker's void assessment as advocacy, not fact.

(c) Is "in-plane geometry churn" genuinely different from V2's
coordinate-retargeting, or the same idea displaced to a different
stage? THE MECHANISTIC DISTINCTION HOLDS, in one sentence: V2 retargeted
the breakup sampling coordinates (bup/sbup/abup) whose every retargeted
term the bfade = 0 fade law gates to dead code in the disc, while V3
leaves breakup sampling untouched and instead re-evaluates the
geometric foam masks (crest, steepness, arm, streak) at churn-displaced
disc-plane positions (mwx, mwz), where the fade law is provably identity
on those terms, so the displacement survives the law that killed V2.
The test of the distinction: the V2 analytic no-op proof cannot be
re-run against V3, because G1 shows the displaced terms reach foam_d
through max() with bupm = 1000 and the streak breakup factor = 1 in the
disc (the prereg's honest limitation even concedes ringf2 is dead there
via sprox2 = 0). That is analytic, not empirical: the distinction is
established on paper, but nothing about V3's actual behavior is known,
because the wave's evidence (smoke renders 06:49-06:52, all
measurements) is void under M4 R1. The M4 R3 reopen condition (a) is met
on the mechanism description, so this prereg is not a re-freeze of V2.
What it is not is a tested mechanism.

(d) Certify the prereg for a future wave, or strike the whole V3 line?
NEITHER BLANKET OPTION; the honest split is: VOID the wave's
implementation and evidence (concur with the worker), keep the prereg
as a committed frozen document, and DECLINE to certify 0ba679b11 for
carryover. The lane reopens only under a genuinely re-authored fresh
prereg in a later wave, per S8 and the 1421pdt precedent against
re-freezes. Striking the entire V3 line including the document would
punish the self-disclosure and destroy a procedurally valid frozen
record; certifying it for reuse would create the laundering path
described in (a). The middle path costs one fresh prereg write and
removes the taint question entirely. The uncommitted implementation
bytes (ocean_dvid1_v3.zag, substrate/, v3_bin) must never be committed
or reused as a starting point; a future implementation must be authored
from the fresh prereg, not from these bytes.

### Recommended ruling: VOID, NARROWED

VOID: the wave's D-VID-1 V3 implementation and evidence are void (M4 R1
prospective; S3, no cure). No verdict on V3 is rendered, no sealed pair,
no measurements cited. NARROWED: the prereg document 0ba679b11 stands
as a committed frozen record with commit-order PASS, but the debate
declines to certify it for carryover; the lane returns only under a
genuinely re-authored fresh prereg. This rejects the self-serving half
of the worker's void assessment while keeping its honest half.

---

## Cross-motion notes for the judge

1. The G1 v3 red-team review (5c886fb1f) is the strongest artifact in
this debate: its killing evidence is geometrically certain and
independent of the verifier it otherwise leans on. The (a) caveat
should be recorded so future red-teams re-run verifiers rather than
re-reading their outputs.

2. The fork battery and the chat FIT are both honest instruments with
explicitly narrow scopes. Their risk is not dishonesty but scope creep
in later citation. Both reports already contain their own scope
sentences; the debate should keep those sentences attached to any
future citation.

3. The D-VID-1 V3 breach was handled the way the rules intend:
self-disclosed with the exact command line, no cure attempted, wave
evidence voided, implementation left uncommitted. The remaining
question is only whether the prereg is reusable, and the strict reading
says no. This is a recommendation; the five governance rulings awaiting
Micah are his alone, and nothing here decides them.

4. No Python contact was found in the G1 v3, fork battery, or chat FIT
evidence paths beyond what those reports disclose (none). The single
python3 contact this wave is the disclosed D-VID-1 V3 heredoc.
