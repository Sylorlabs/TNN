# JUDGE RULINGS, wave-20260924-2321pdt debate group

Role: independent judge. Method: both transcripts read in full
(ADVOCATE_BRIEF.md f449c2b1c, SKEPTIC_REPORT.md b3ddb79c4); every
material claim checked against the committed git record. Primary
evidence read: PREREG_DVID1_V3_2321.md (0ba679b11), BREACH_DISCLOSURE.md
(ca1d4a13a), REDTEAM_G1V3.md (5c886fb1f), FORK_RESULTS_2321.md
(b03063b37), TNCHAT_FIT_2321.md (c4f006ea7). No Python used in this
review (read and git only). Nothing pushed. No em-dashes appear in
this document.

Standing rules applied: pure Zag; never weaken a frozen kill bar;
a verdict is overturned only on cited evidence; the five governance
rulings awaiting Micah are his alone (this document recommends only,
and touches none of them); missing evidence means CANNOT-CONFIRM.

---

## M1. G1 v3 SUNSHAFTS: CONFIRM DISCARD [NEW], with two narrowings adopted

Ruling: CONFIRM. The DISCARD stands on evidence independent of the
disputed record-checks.

Decisive evidence: the red-team reviewer (5c886fb1f) independently
diffed committed base.bmp vs var_v3_1.bmp at byte level. Lifted-pixel
bbox: x 125..1023, y 308..458, zero lifted pixels with y < 300. The
committed verifier source (g1_verify_v3.zag, 39707e077) generates
wedge points as y = 300 - t*36 for t in 1..8, so every kept wedge
point has y <= 264. The lifted band is disjoint from the wedge set by
construction; 0 of 39 kept wedge points carry lift. This entails
KB2 = 1.0000 (< 1.12) and KB3 = 0.00 (< 60.0) under any correct
implementation of the frozen formulas. A verifier bug could only
misreport the margin, not rescue the candidate. Commit order PASS
(acf7cedce 00:57:43 UTC < 1da140387 01:17:00 UTC < 39707e077
01:24:34 UTC, ancestors verified). Purity PASS (no Python contact).
Baseline byte-identical to the S14 record (e4f65557...).

Narrowing (a) ADOPTED: the red-team report states "no pipeline was
re-run." Its KB2-KB8 figures are read from evidence_verify_v3.txt,
not recomputed by re-running the verifier. They are record-checks,
and the report's "recomputation" header overclaims for them. The
verdict does not depend on them (see the geometric proof above), but
the record is corrected: future red-teams re-run verifiers rather
than re-reading their outputs.

Narrowing (b) ADOPTED: the tripwire bar (50..150 per mille, measured
87.89) lives in run_g1v3.sh lines 118-130, not in the frozen prereg.
It is relabeled "runner sanity check (non-bar)" so no future wave
cites it as a passed kill bar. It carried no verdict weight; the
runner file is byte-stable within 39707e077, so no weakening occurred.

The "stand down until a genuinely new design idea" is a lane-scoped
verdict applying the 1421pdt ruling (mechanism redesign, not
re-freeze), not evasion of the hunt mandate.

No provenance header is owed: the frozen prereg requires it on
JUDGE_BRIEF.md only for READY-FOR-JUDGE; this verdict is DISCARD.

Verdict tag: G1 v3 SUNSHAFTS CONFIRM DISCARD [NEW].

---

## M2. Fork battery: CONFIRM 25/25 PASS [RE-CERT], with narrowings adopted

Ruling: CONFIRM on literal scope (toolchain identity and frozen
battery behavior at the tested commits).

Decisive evidence: FORK_RESULTS_2321.md (b03063b37) records 25/25
forks PASS with shell driver and pure-Zag harness in agreement;
pinned znc 498abcb5... byte-identical on all 25; probe 3b29aa06...
identical on all 25; negative controls NEG1/NEG2 discriminated on all
25 (the battery has teeth). Both origin/tnn-native-lab tips tested
read-only (14c8838558a superseded mid-wave, 7872124430 current).

Narrowings ADOPTED: (1) 10 of the 25 entries are static fixtures that
cannot move and cannot fail on drift: seven forktest/* worktrees with
unchanged SHAs (293602fb1, a0e7f8ba2, 991432226, bd3097874,
cea8db22f, 3947dca1a, f875b3417) plus three wave3 worktrees on the
single SHA bd3097874 counted three times. Honest live count this
wave: 15. Future reports split live forks vs static fixtures.
(2) The driver gains a closing origin-tip re-check: both observed
tips were tested, but no documented re-observation after the last
fork test leaves a small untested window. (3) The pinned worktrees
are stale by design and disclosed; keep them only with a stated
purpose (worktree-corruption guard) or retire them.

Verdict tag: fork battery CONFIRM [RE-CERT] 25/25 PASS (15 live, 10
fixture).

---

## M3. tnn_chat FIT: CONFIRM FIT [RE-CERT], with narrowing adopted

Ruling: CONFIRM on literal scope.

Decisive evidence: TNCHAT_FIT_2321.md (c4f006ea7) records binary
reproducibility 2/2 (20273a99... and 1ada2fae... byte-identical to
frozen records), KB1 30/30 specific declines, KB2 17/17 answered,
KB5 10/10 answered, 9/9 run-pairs byte-identical, all 15 runs exit 0
with empty stderr, on merged HEAD ead33399e. No Python used.

Narrowing ADOPTED: the report's own scope sentences travel verbatim
with any future citation, so this FIT is never cited as merge review:

- "This re-certifies the frozen FIT instrument chain on the new merge commit only. It is not a candidate verdict and it is not merge review of the merged-in work."
- "This certifies the 38-fact closed-book probe chain only."

Verdict tag: tnn_chat CONFIRM FIT [RE-CERT] on ead33399e.

---

## M4. D-VID-1 V3: implementation VOID confirmed; prereg STANDS and is CERTIFIED prereg-only; lane reopens under 0ba679b11

Provenance header, quoted verbatim from the frozen prereg
(PREREG_DVID1_V3_2321.md, commit 0ba679b11):

- "RENDER_SHA: (to fill at implementation; sha256 of the frozen variant generator source ocean_dvid1_v3.zag, 64 hex chars)"
- "FIRST_RENDERED_WAVE: wave-20260924-2321pdt"
- "COMPONENT_LINEAGE:
    - D-VID-1 V1 (flow-advected foam breakup): DEAD [NEW], wave-20260923-2321pdt. Killed on frozen T1 bar: variant 606 vs baseline 580 per-mille foam flips, ratio 1.045 against bar <= 0.700.
    - D-VID-1 V2 (co-rotating foam breakup): DEAD [VOID], wave-20260924-0521pdt. Analytic no-op proof: bfade = o_clamp01k((200 - wz) * 1000 / 140) = 0 for wz >= 200; vortex disc wz 560..880, so every V2-retargeted term is gated dead (bupm = 1000, streak multiplier = 1, abupm dead code); ocean.zag diff exactly three hunks. Wave evidence VOID on a mid-wave python3 heredoc touching v2_verify.zag (frozen VKB5).
    - Whirlpool SCOOP: DISCARDED.
    - Whirlpool surface-planform: READY-FOR-JUDGE, QUEUED-UNJUDGED."
- "NEW_KNOWLEDGE_CLAIM: In-plane deterministic displacement of disc foam geometry (not breakup sampling) raises screen-space foam boil by at least 30 percent over the rigid-sweep baseline while holding the V-TEMP, V-SHARP, determinism, and cost bars, giving the loop a live non-rigid churn lever for whirlpool foam."
- "This prereg is the S8 return path for the 0521pdt debate M4 R3 closure: "DEAD is the coordinate-retargeting of breakup sampling for disc foam churn (bfade = 0 kills every retargeted term). OPEN under a fresh prereg only: (a) disc foam churn via a DIFFERENT mechanism (geometry churn), or (b) a redefined goal." This document takes path (a). It is a genuinely new mechanism, not a re-freeze of V1/V2."
- "No Python is authorized by this prereg. Not for the generator, not for the verifier, not for hashing, not for analysis, not for /tmp scratch. Any Python contact with a new wave artifact voids its wave evidence (M4 R1, prospective)."

### (i) Implementation/evidence VOID: CONFIRMED

The single python3 heredoc (exact command line in BREACH_DISCLOSURE.md,
ca1d4a13a) was Python contact in loop work. Under the 0521pdt M4 R1
prospective rule it voids the wave's D-VID-1 V3 implementation and
evidence. Under S3 no re-do cures it. The voided work products
(ocean_dvid1_v3.zag, substrate/, v3_bin) sit in dvid1_geomchurn/void/
for lineage disclosure only; they carry no evidentiary weight, support
no verdict, and must never be committed, reused, cited, or re-certified.
No verdict is rendered on V3. No sealed pair. No measurements cited.

### (ii) Prereg CERTIFIED for future-wave carryover (prereg-only)

The prereg 0ba679b11 STANDS and is CERTIFIED as the S8 return path.
Decisive evidence, all git-verifiable: committed ALONE at 2026-09-25
06:47:01 UTC (single-file commit, parent c4f006ea7); exactly one commit
in history touches the prereg path, so Python never read or wrote the
file after freezing; the breach came later (disclosure committed
06:55:45 UTC). Under the 1121pdt M5 precedent the voiding operation
must have an object (the evidence the contact touched or could have
contaminated); the prereg is outside that object set. The prereg
satisfies the 0521pdt M4 R3 reopen condition on path (a): geometry
churn is a genuinely different mechanism from V2's coordinate
retargeting (the skeptic concedes the mechanistic distinction holds on
paper), and it pre-authorizes no Python anywhere (VKB5).

On the worker's self-contradiction: the disclosure says both "the
prereg survives as a certified frozen prereg" and "the lane returns
only under a fresh prereg in a later wave per S8." The stricter
sentence is adopted, and it is satisfied: 0ba679b11 IS the fresh
prereg M4 R3 called for (genuinely new mechanism, never implemented
cleanly, never judged). The advocate's paraphrase ("under the frozen
prereg") is corrected to the disclosure's own words ("under a fresh
prereg"); that fresh prereg is 0ba679b11.

On the lineage objection: the heredoc processed a scratch byte-copy of
the implementation and its probes printed churn field internals (wx,
wz, vwx, vwz, gr, churn_gate). That was python-assisted debugging of
the implementation, and its products are void. It could not have
informed the prereg's frozen formulas, which predate the breach by
committed timestamp. Design confidence is not evidence; a future wave
implements the frozen formulas fresh and the kill bars judge the
result. The lineage is disclosed here so no future wave is ignorant
of it; disclosure plus voiding is the complete remedy the rules
provide. Declining carryover would either force a re-freeze of
identical formulas (barred by the 1421pdt anti-re-freeze reading) or
abandon a valid unjudged design, neither of which any rule requires.

### (iii) What reopens the lane

Implementation under the frozen prereg 0ba679b11 in a future wave, not
a re-authored prereg. Conditions, frozen here: the implementation is
authored fresh from the prereg document (never from the voided bytes);
every step is pure Zag with zero Python contact (VKB5 in full force);
all evidence is produced cleanly in that wave; the prereg's frozen
bars (VKB1-VKB7, G-LIVE) apply unchanged. The voided bytes remain in
void/ and are never a starting point.

The breach-timeline middle (breach at ~06:53 UTC, single invocation,
scratch-copy-only contact) rests on the worker's self-report plus
coordinator transcript review, not on the committed record; it is
accepted provisionally as credible (self-incriminating, exact command
line quoted, no cure attempted, S3 honored) and does not affect the
rulings above, which rest on git-verifiable ordering.

Verdict tags: D-VID-1 V3 implementation/evidence VOID; prereg
0ba679b11 CERTIFIED (prereg-only); no verdict on V3; no sealed pair.

---

## Precedents recorded (no new standing rules adopted)

P1. Pre-breach frozen preregs survive. A prereg committed alone before
any Python contact, never read or written by Python thereafter
(verified by single-commit history on its path), is outside the M4 R1
voiding operation's object set per the 1121pdt M5 precedent. It stands
as a frozen record and may be certified for carryover when it
satisfies the applicable reopen condition.

P2. Carryover certification carries lineage disclosure. When a
certified prereg's implementation lineage includes a voided Python
contact, the contact's exact scope is recorded in the debate record;
the future implementation is authored fresh from the prereg document,
never from voided bytes; voided bytes are never committed, reused,
cited, or re-certified.

P3. Red-team record-checks are labeled as such. A review that re-reads
verifier outputs without re-running the verifier reports those figures
as record-checks; future red-teams re-run verifiers.

P4. Runner bars are sanity checks. A bar defined only in a runner
script, not in the frozen prereg, is labeled "runner sanity check
(non-bar)" and never cited as a passed kill bar.

P5. Fork battery counts split live vs fixture. Static worktrees with
pinned SHAs are reported separately from live forks; the driver adds
a closing origin-tip re-check.

P6. FIT scope sentences travel. Any citation of a tnn_chat FIT
re-certification carries its literal-scope sentences verbatim; it is
never cited as merge review.

---

## Verdict slate

| # | Motion | Ruling | Deciding evidence |
|---|---|---|---|
| M1 | G1 v3 SUNSHAFTS | CONFIRM DISCARD [NEW], narrowings (a)(b) adopted | Lifted band y 308..458 disjoint from wedge set y <= 264 by construction; 0 of 39 kept wedge points carry lift; KB2 1.0000 < 1.12, KB3 0.00 < 60.0 |
| M2 | Fork battery | CONFIRM [RE-CERT] 25/25 PASS (15 live, 10 fixture), narrowings adopted | 25/25 PASS both harnesses; NEG1/NEG2 discriminate on all 25; 10 entries are static fixtures (7 forktest SHAs unchanged, 3 wave3 on bd3097874) |
| M3 | tnn_chat FIT | CONFIRM [RE-CERT] FIT on ead33399e, narrowing adopted | Binaries byte-identical (20273a99..., 1ada2fae...); KB1 30/30, KB2 17/17, KB5 10/10, 9/9 run-pairs identical; scope sentences travel verbatim |
| M4 | D-VID-1 V3 | VOID (implementation/evidence); prereg 0ba679b11 CERTIFIED prereg-only; lane reopens under 0ba679b11 | Python heredoc voided the phase (M4 R1, S3); prereg committed alone 06:47:01 UTC, never touched by Python, satisfies M4 R3(a); worker's stricter "fresh prereg" sentence is satisfied by 0ba679b11 itself |

Nothing in this document decides any of the five governance rulings
awaiting Micah. No candidate enters his judge queue: G1 v3 is
DISCARD, D-VID-1 V3 has no sealed pair and no verdict.
