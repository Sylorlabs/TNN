# Mandatory debate: wave-20261001-0221pdt verdict slate
Coordinator-inline (no descendants; twelfth consecutive wave run
inline-only after eleven descendant-subagent runtime defect kills).
Date: 2026-10-01, ~03:00 PDT.

## Verdicts under debate

V1. H-EXP2 v2: BUILD-PASS (K-X1..K-X6 all pass, sealed).
V2. ddes_followup: BUILD-FAIL (committed implementation does not
    compile) + UNVERIFIABLE ORDERING (prereg and implementation in one
    commit 904e9b6f6).
V3. H-PI-REV2 step 5: DEFERRED (no frozen baseline bar text exists).
V4. Fresh disjoint adversary byte set {k,m,r}: FROZEN declaration.
V5. Fork battery: 85 PASS / 1 FAIL / 2 UNTESTABLE (88 entries).
V6. DEVANG2 retry: QUEUED (no frozen prereg).

---

## ADVOCATE (for the slate)

V1: The numbers are clean. W-A identified (2,3) at round 4 with 3
probes against a budget of 6 (K-X1); W-B identified (2,1) at round 5
with 4 probes against a budget of 10 (K-X2). Survivor counts
16->10->8->2->1 decrease strictly in three consecutive rounds
(K-X3). Both worlds' round logs are byte-identical across two runs,
zero stderr (K-X4). The grep audit shows expseq.zag never mentions
any law file name or path and opens only history and state files
(K-X5). Every executed probe scored >= 2 (4,2,2 and 4,2,2,2) (K-X6).
The commit-order self-check holds: the prereg was frozen in 1121pdt,
the implementation came this wave. The prereg itself frames the
claim as bounded L2, so there is no overclaim to police. BUILD-PASS
is the only honest verdict.

V2: The implementation does not compile under the pinned znc (arity
check FAILED: ddes_world takes 15 params, 6 call sites pass 14; main
never wires Phase B). A non-compiling implementation cannot execute
its prereg; BUILD-FAIL is mechanical. The same-commit ordering is a
fact of the git history (904e9b6f6 contains both files). UNVERIFIABLE
ORDERING follows from the loop governance rule, not from anyone's
judgment. The diagnostic build in /tmp shows the design's bars would
hold if completed (3/3 byte-identical, K-F1..K-F6 all pass), which is
exactly the information the next wave needs. Nothing is lost; the
lane is re-freezable.

V3: Inventing baseline bars post-hoc would be the bar-moving the
owner forbids. Deferral is the governance-correct move, and the queue
item (write and freeze a baseline-comparison prereg) is concrete.

V4: The set {k,m,r} is derived mechanically from the frozen fixture
strings, verified by byte audit. The selection rule continues the
F3a2/F3a3 convention. Zero discretion was exercised.

V5: 85/88 PASS with the two UNTESTABLEs explained (PR-head trees lack
the pinned toolchain path, same as prior waves) and the one FAIL
explained (the rotated old-LIVE pin diverges from the frozen
instrument, which is precisely why it was rotated to a fixture).
Current LIVE at eb47b8def is PASS. The battery did its job.

V6: No frozen prereg exists; advancing would violate the
advance-only-on-frozen-prereg instruction. Queued is correct.

## SKEPTIC (against the slate)

V1: Three challenges. First, the toolchain repair: the `[]i32`
miscompile was found by trial and error, and the rewrite changed both
programs substantially. How do we know the rewrite didn't change the
prereg's specified algorithm? Second, W-A and W-B were both solved in
3-4 probes with first-round probes identical ([2,0,3,2]); is the
enumeration actually doing multi-round discrimination, or is the
first probe doing all the work and the rest is pruning theater?
Third, the probe enumeration is 1554 candidates per round and the
prereg said 1654: the audit calls it an erratum, but could a
1554-vs-1654 discrepancy hide a missing length class?

V2: The diagnostic /tmp build is doing real scientific work (3/3
byte-identical, K-F1..K-F6 pass) that will never be adopted because of
a process technicality. Is UNVERIFIABLE ORDERING throwing away a
working result? And who verified the arity claim: did anyone
actually run znc on the committed ddesp.zag, or is this a
reading-of-source claim?

V5: The duplicate label means the driver had a real flaw (two entries,
one result dir). The line-19 result was clobbered and had to be
re-run. How do we know no other entry suffered a clobber or a silent
skip? The tally says 88 entries and 88 RESULT.txt files now, but the
re-run happened after the fact: what proves the other 86 are from
this wave's instrument?

## JUDGE (with cited numbers)

V1: The skeptic's first challenge is answered by the sealed runs
themselves. The prereg specifies the algorithm at the level of
hypothesis pruning, probe enumeration (all sequences length 1..4),
and distinct-trajectory scoring with a fixed tie-break; the rewrite
changed only the integer-array representation (u8-backed get32/set32
instead of []i32), which is semantics-preserving by construction and
was validated by the sealed outcomes: W-A IDENTIFIED 2 3 and W-B
IDENTIFIED 2 1, both equal to the sealed laws fixed in 1121pdt, which
the learner never saw (K-X5). A representation change that leaked or
altered the algorithm could not systematically recover both sealed
pairs. On the second challenge: the first-round probes are identical
because round 1 starts from the same INIT state (0,0,0) with 16
survivors in both worlds; the enumeration is deterministic, so the
top probe is the same. Discrimination across rounds is real: W-B
needs round 3's [3,4,2] (lamp_on then pressurize, SCORE 2) to split
(2,1) from (2,2), and round 4's [1,2] to finish; survivor counts fall
16->10->8->2->1. That is multi-round discrimination, not theater.
On the third: 6+36+216+1296 = 1554, and the binary prints
"CANDIDATES 1554" every enumeration round in both sealed logs. A
missing length class would change the printed count; the erratum is
arithmetic in prose, not in code. V1 BUILD-PASS STANDS.

V2: The arity claim was verified by compiling the committed
ddesp.zag with the pinned znc: arity check FAILED, 15-param
definition vs 14-arg call sites, 6 sites. That is a compiler verdict,
not a reading. On the process point: the governance rule exists
precisely because a working result with unverifiable ordering cannot
distinguish "prereg guided implementation" from "implementation
guided prereg". The diagnostic's value is preserved as information
(the design's bars hold under mechanical completion), and the lane is
re-freezable next wave at low cost. Discarding adoptability while
keeping the information is the rule working as intended. V2
BUILD-FAIL + UNVERIFIABLE ORDERING STANDS.

V3: No frozen bar text exists in any of the searched preregs or the
M5 debate record; inventing it now would be the forbidden move.
DEFERRED STANDS, with the queued prereg item.

V4: The byte audit is mechanical and reproducible (fixture strings ->
union abcdefghijlnopqstuvwxyz -> free kmr). FROZEN STANDS.

V5: The duplicate label is a real driver flaw, owned: two entries
shared one result dir, and the earlier result was clobbered. The
remedy (re-run under a distinct label) is complete and documented.
On silent skips: every driver entry's RESULT.txt contains its ref sha
and entry label; the manifest's 88 rows each carry a distinct
(entry, ref) pair, and the two same-label rows now have distinct
labels (local-20260930-2321pdt-tip vs rotated-old-live-23c2c02).
The instrument question: the harness records znc_sha256 per entry,
and the FAIL entry's cause line proves the pin check actually fired
this wave (it caught the divergence rather than passing blindly).
85 PASS / 1 FAIL (explained) / 2 UNTESTABLE (explained) STANDS.

V6: QUEUED STANDS.

## Outcome

No coordinator verdict overturned. The skeptic's challenges are
answered with cited evidence above; none met the bar of cited
evidence against a verdict. The driver duplicate-label flaw is
recorded as a process lesson: future drivers must assert unique
entry labels before running (pre-run gate addition).
