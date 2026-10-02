# RED-TEAM REVIEW: wave-20260927-1121pdt verdict slate

Reviewer: red-team lane. Working copy ~/workspace/tnn-rsi, branch
tnn-native-lab, reviewed at HEAD 97ab9ad18. Pure Zag only; no Python
invoked, written, or run anywhere in this review (file reads, grep, git,
shell builtins only). No em-dashes in this document. Nothing pushed.
docs/lab/continual_learning/ not modified (verified: git diff clean).

Method: independent re-verification of every coordinatable claim in the
coordinator's draft slate, by git-object evidence, not by re-reading the
lane's summary.

## Attack A: EXP1c gate evidence (six EXP1b corrections in 463b115b6)

VERDICT: GATE HOLDS. Spot-checked five of the six corrections by
independent git show of the commit's hunks, plus the deliverable:

1. A2_ABLATION.md rewrite: present with substance. Documents the two
   errors found by the independent reviewer (steps were replaced;
   counts 168, 97, 92, 45, 167 on v1/v2/v4/v5/v7) and the v5
   void-death confound, with the clean-ablation drop-0-in-all-12 result.
2. EVIDENCE_EXP1B.md "never builds" correction: present with substance.
   I builds a LAMP in 6/12 variants, places in 5/12 (v2, v5, v7, v8,
   v11), causally inert per the clean ablation.
3. NOVELTY_AUDIT.md heuristic relabeling: present with substance. Labels
   corrected to match kb.txt verbatim (H1/H2/H3/H4/H5/H6 real
   definitions), with the verdict-impact note intact.
4. EVIDENCE_EXP1B.md reflex-dependency record: present with substance.
   Counterfactual quoted: without the implementation-added void-safety
   reflex, I median drops to 102 with 9/12 void deaths.
5. EVIDENCE_EXP1B.md retune-2 verifiability note: present with
   substance. Retunes 1-2 left no artifacts; stopping rule
   unverifiable; K1-shopping cannot be ruled out.
6. BAR_RESULTS.md bounce-bug correction: present with substance. Bug
   pinned to the 2321pdt reimplementation 74565859f, original EXP1
   19f97c6cb credited with correct bounce, K1 KILL direction unchanged.

Deliverable docs/lab/invention/survival/WAVE_NOTES_EXP1B.md exists as
blob in 463b115b6 (git cat-file confirms) and opens with a full outcome
section (H1 KILLED by K4/K6, K1 passes on arithmetic, invention dead).

No hollow corrections found. Gate (a) satisfiable is independently
reproduced.

## Attack B: freeze ordering and the training-mass commit 5a043af3c

VERDICT: VALID FREEZE.

The mass commit adds exactly two new files
(kb_exp1c.txt, kb_p_exp1c.txt; 89 insertions, 0 deletions, 0
modifications to existing files). Read in full: both files are pure
knowledge text (world-physics statements, single-step heuristics
H1-H9, the P phased strategy). No runner code, no scoring, no logic,
no plan enumeration, no recipe table (the file itself states the
recipe table is not taught). It is input data, not implementation.

Ordering: 59b9df4b0 (0821pdt design drafts) strictly precedes
5a043af3c (mass), which strictly precedes 8b456736b (freeze), by
topology (--ancestry-path). No implementation commit exists anywhere
between freeze and HEAD 97ab9df4b0 (post-freeze commits are fork
results ab577d0e6 and candidate-lane docs 97ab9ad18 only). The frozen
prereg's section 11 records the freeze commit and bars any
implementation from preceding it. The prereg commit-order self-check
is valid, and the adoption check is correctly vacuous.

Probe: does baked-in H9 weaken the frozen bars? No. H9 ("if the step
you are about to take would land on a void cell, refuse that step")
is a single-step taught reflex, given to all three arms equally
(R, I-survive, I-invent), and the file quotes it verbatim in M4(c).
Effects on the bars: K4's novelty audit searches the committed mass
for key strategy steps, so adding H9 to the taught set can only
enlarge the skeptical attribution set (bar strengthening, if anything).
K7 guards the choice question mechanically and is unaffected by a
taught reflex. And the deeper direction is the EXP1b lesson fixed,
not repeated: in EXP1b, K1's PASS depended on an
implementation-added void-safety reflex absent from the frozen M2
text. M4(c) makes it explicit, taught, and equal across arms before
the freeze. This closes that loophole rather than opening one.
H9 contains no recipe, no multi-step strategy, and no information
about which composition wins.

## Attack C: redraft fixes and bar identity

K1-K7 byte-diff between the 0821pdt draft (59b9df4b0, section 6) and
the frozen prereg (section 6): diff reports zero differences
(BARS BYTE-IDENTICAL; only line numbers shifted). The kill bars were
not moved.

The two redraft fixes are not bar moves and not mechanism changes:

- H5 to H9 renumber: the draft's M4(c) said "taught H5", but kb.txt
  already defines H5 as the EAT rule (H1-H8 all taken). A literal H5
  void-safety would have made the training mass self-contradictory
  and poisoned the K4 novelty audit (void-safety events attributed
  to the EAT heuristic). Renumbering to appended H9 preserves the
  audit's fidelity. The rule's content is unchanged.
- world.zag path fix: "src/world.zag" does not exist at that
  repo-relative path; the committed template is
  docs/lab/invention/survival/src/world.zag (verified present; bounce
  fix 938d188cb verified in history). A path correction, not a
  mechanism change.

Both fixes happened at redraft time, before the freeze, and are
documented in the frozen prereg's section 0. Legitimate.

## Attack D: provenance, new versus inherited this wave

NEW this wave (properly tagged in the lane doc):
- EXP1c freeze package: mass extension 5a043af3c, frozen prereg
  8b456736b (bar-identical to the draft, fixes documented).
- Fork battery fresh re-run: evidence files written 2026-09-27 18:25
  UTC under the 1121pdt evidence dir, fresh scratch, harness rebuilt
  and sha-verified against pins, 3 live entries re-tested, 48
  fixtures pinned.
- CANDIDATE_LANE_1121.md gate-check findings and the five
  continual_learning interaction rule proposals.

INHERITED (properly attributed, not recycled-as-new):
- The six EXP1b corrections plus WAVE_NOTES_EXP1B.md are cited as
  the 0221pdt coordinator commit 463b115b6, correctly labeled gate
  evidence, never presented as this wave's work.
- The four prereg drafts are cited as 59b9df4b0 from 0821pdt lane 3,
  correctly labeled draft-to-freeze upgrade.
- The EXP1b training mass is inherited verbatim with exactly three
  documented deltas; EXP1b's own mass files untouched.
- The fork battery's old-snapshot entries (arch-20260923 etc.) are
  explicitly fixture re-runs for toolchain stability, with the scope
  stamp limiting the certification to toolchain/extraction.

No recycling smell: everything inherited is tagged [RE-CERT] or
explicitly attributed to its originating wave. The null candidate
hunt is honest (gate froze one draft, so the lane reports no new
implementation rather than manufacturing one).

One provenance note for the record: origin/tnn-native-lab's remote
tip moved at run start from 7aad68fad to 899757bc2, and 899757bc2 is
Micah's own red-team report (author micahcooley, 2026-09-27 11:23
PDT). The merge survey claim about "his six new .zag files" is
consistent with this.

## Attack E: fork battery CONFIRM, 49/51 with 2 perpetual UNTESTABLEs

VERDICT: CONFIRM stands this wave, but the perpetual UNTESTABLEs
need a structural decision.

What was verified: 51 named entries enumerated fresh at run start;
evidence shows live re-execution this wave (timestamps, fresh
scratch /tmp/fb1121, harness sha-verified against frozen pins,
exit 0 with 49/49 VERDICT=PASS). The 2 UNTESTABLEs (rh-pull-1-head
at 5802fec84, rh-pull-2-head at 4b76bb59f) have identical cause
across ten waves: trees lack the pinned toolchain path; they are
non-TNN research-doc repos. Nothing was faked; the manifest records
the same extraction reason.

Recommendation to the parent and the debate group: a tenth wave of
UNTESTABLE with unchanged cause is a coverage-status smell, not a
TNN-coverage failure (no TNN code is uncovered). Two options: (1)
formally reclassify rh-pull-1/2 as permanently OUT OF SCOPE with
the recorded reason, reporting the battery as 49/49 on the scoped
population, rather than perpetuating wave-by-wave UNTESTABLE counts
that inflate the named-entry denominator; or (2) actually cover
them (vendor the pinned toolchain into the pull-head extraction).
The current CONFIRM-with-UNTESTABLEs is defensible only because the
results doc scopes the certification to toolchain and extraction
stability and documents the identical cause. Do not let the 51-entry
headline stand without the scope caveat.

## Attack F: continual_learning interaction rules, overreach check

VERDICT: no overreach found. All five proposed rules constrain the
loop, never his work:

(a) Standing his-frontier entry in LOOP_STATE.md: descriptive
    citation only (paths, prereg 8c22ffb9b, build+run 36342eb51
    with his GO, in-repo red-team 899757bc2 with NO-GO marked
    not-relitigated). Marked CLOSED to the loop. Recording his own
    stated verdicts is citation, not certification.
(b) No loop code imports his directory: a loop-internal import ban.
    Verified true today (grep outside his dir finds only this wave's
    two lane docs; git diff on his dir is clean).
(c) Citation rule for future probes: requires the loop to cite his
    MANIFEST SHAs as canonical for continual-learning claims, not
    present loop copies as canonical, and not copy his D1 psm.zag
    deviation into loop PSM copies. Governs the loop's own
    documentation of its own probes. Not a constraint on him.
(d) Fixtures as closed teaching corpus: a loop-internal ingestion
    ban plus a cite-as-prior-work rule for the loop's own probes.
(e) His Python build tools under his own authority: states the
    loop's pure-Zag rule does not reach into his directory and
    forbids the loop from running his tooling. A boundary on the
    loop, not on him.

Material fact for the debate group (not overreach, but load-bearing
for slate item 5): the in-repo red-team report 899757bc2 recording
NO-GO is authored by micahcooley himself (commit message "Red team
report: continual-learning flagship benchmark -> NO-GO",
2026-09-27 11:23 PDT), written after his GO at 36342eb51. The slate
frames the GO/NO-GO discrepancy as something the parent may decide
to surface to Micah. The red team notes: Micah already wrote the
NO-GO himself, so the discrepancy is his own later judgment on his
own work, not a loop finding awaiting his attention. Any surfacing
must carry that authorship fact; the loop must not present it as
new information. The loop's CLOSED stance is correct.

## Zero-Python attestation

This review used zero Python. Evidence gathered by git show,
git log, git diff, grep, sed, and file reads only. No Python
interpreter was invoked, no Python tooling written or run.

## Commit record (local only, nothing pushed)

This file: to be committed by the red-team lane with message
"wave-20260927-1121pdt: red-team review of EXP1c freeze plus verdict
slate".

## Items the debate group must confront

1. Perpetual UNTESTABLEs: ten waves of identical rh-pull-1/2
   UNTESTABLEs. Recommend either formal permanent OUT OF SCOPE
   classification with reason, or actual coverage of the pull-heads.
   CONFIRM is defensible this wave only with the scope caveat intact.
2. The 899757bc2 NO-GO red-team report is Micah's own authorship,
   postdating his GO. Slate item 5's "parent decides whether to
   surface" framing must be updated: there is nothing to surface
   that he did not write himself. Carry the authorship fact.
3. Everything else in the slate reproduces under independent
   re-verification: gate evidence substantive, freeze ordering valid,
   bars byte-identical, provenance clean, no implementation exists
   yet, adoption check correctly vacuous, governance rulings and
   sealed pairs untouched (not reviewed here per task scope).
