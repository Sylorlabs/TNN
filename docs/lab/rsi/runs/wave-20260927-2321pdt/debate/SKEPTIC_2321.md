# Skeptic report: wave-20260927-2321pdt (five motions)

Role: skeptic AGAINST the proposed adoption slate.
Wave: 20260927-2321pdt. Branch: tnn-native-lab.
Working copy: ~/workspace/tnn-rsi.
Records judged: exp1c/REDTEAM_EXP1C_2321.md (3636d2fe4),
forks/FORK_RESULTS_2321.md (9926b0860),
design_lane/HUNT_2321.md (3dc45ca35),
INTERACTIVE_SURVEY_2321.md (9c6646c04),
debate/ADVOCATE_2321.md (the adoption slate under attack).
Binding precedent: the 2021pdt verdicts and judge rulings e97d1b9c0
("a void test cannot kill a hypothesis"; K6 operationalization R3
recorded as reasonable with future adoption requiring a frozen
operationalization first; addendum d9e96ad91 judge-legitimate; K4
CANNOT-CONFIRM and K5 INCOMPLETE per frozen text; the C3 F10
correction history).

Standing rules observed in this brief: pure Zag discipline (text
debate, no code, no Python), no em-dashes anywhere, nothing pushed,
the six governance rulings undecided and unrelitigated, all sealed
blind pairs untouched, Micah's frontier dirs untouched.

## The skeptic's verbatim provenance probe

"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

Answer, verified by this skeptic from the git record (not taken on
the red team's word):
- New this wave, first committed at 7fbd485b6 (verified by
  `git log --diff-filter=A` on the exp1c source tree): all nine
  x1c_*.zag sources, written from scratch.
- New at 7fbd485b6: iterations/iter3/calib1.txt and calib2.txt
  (SHA-256 f0b1d41b254dd441aa53ecd5d73f80b9c79c9f4aa13ea058239dc82ea9bccb57),
  iterations/iter3/variants3.txt.
- New at 26669a08d (`git diff 7fbd485b6..26669a08d --stat` shows
  only the two TSVs added, no source edits): evidence/run1.tsv and
  evidence/run2.tsv (SHA-256
  da034c524a9380625f95eef340aa0882a6e068e41a86645cebc748f8202510d2,
  differing from the 2021pdt run SHAs 0e82ba09...).
- New at 0563e0cce: evidence/EVIDENCE_EXP1C.md (SHA-256
  8dbaed7673a409a332fd5ad2fe4242e6b2a05c1e0d58789295aa478bd9afaf33).
- Inherited and unchanged: frozen prereg 8b456736b with the
  section-7 redraft d9e96ad91, the 24-cell world physics template
  (blob fff8af2493bc6dbe9de6fc76f9a6206d887d586a), the EXP1c
  training mass pair (kb_exp1c.txt, kb_p_exp1c.txt, verbatim since
  5a043af3c), the P/R/Z arm concepts, the pinned toolchain
  (SHA-256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
  The fork battery's harness is byte-identical to the 1721pdt
  instrument (inherited machinery, disclosed in FORK_RESULTS_2321.md).
- The 1721pdt and 2021pdt attempts are lineage, not content: they
  used different source files (e1c_*) and different variant families,
  and this wave's medians (266/269) differ from 2021pdt's (918/920).
  Nothing is a re-certified old render. The six governance rulings
  and all sealed blind pairs are inherited and untouched.

Provenance verdict: clean. No old content is presented as new.

## Attacks on M1 (enter EXP1c iteration 3 as VOID, K1/K6 as certified measurements, C3 certified PASS)

### A1. The "DEAD via K1+K6" temptation is real and still live in the archive (SUSTAINED, BLOCKING as a required verdict-line correction)

Precision first: the literal string "DEAD via K1+K6" does not appear
in the worker's committed records. What does appear, committed at
0563e0cce, is:
- evidence/EVIDENCE_EXP1C.md: "K1 (median I-survive <= median R
  kills H1): I-survive=266 R=1200 KILL" and "K6 (ablation):
  I-survive median=266 abl=1200 KILL (ablation does not reduce
  survival)", "I-invent median=269 abl=1200 KILL (ablation does not
  reduce survival)".
- The milestone-3 commit message: "Verdicts: C1 PASS, C2 PASS,
  C3 PASS; K1 KILL, K2 survive, K3 ok, K4 CANNOT-CONFIRM, K5
  INCOMPLETE, K6 KILL (both ablations), K7 VOID (0/13 and 0/94
  learned fractions)."

The same document prints KILL labels whose own definitions say
"kills H1" and, two sections later, "K7 verdict: VOID". That is the
temptation in the archive, verbatim: any future adoption read can
quote the note's KILL labels and the commit message's "K1 KILL ...
K6 KILL" as adopted kills, because the note never states that K7
voids them. The red team's F1 corrects the framing for this wave's
verdict, but F1 lives in the red-team report, not in the evidence
note, and the note is what gets cited.

The 2021pdt precedent already settled the identical situation:
K1/K6 firings recorded as measurements from a voided run, NOT
adopted as kills, because a void test cannot kill a hypothesis.
The skeptic sustains F1 as REQUIRED and blocking: the wave verdict
line must enter VOID as a test of H1/H2 (K7) and must quote the
precedent verbatim, explicitly neutralizing the note's KILL labels.
Without that sentence in the verdict line, the adoption slate
leaves a loaded gun in the archive. The K1/K6 numbers themselves
are correct literal computations (hand-verified: 266 <= 1200;
1200 >= 266; 1200 >= 269); the attack is on the framing, not the
arithmetic.

### A2. The C3 "genuinely different decision rule" gloss exceeds what the measurement supports (SUSTAINED, required record correction)

The red team certifies C3 PASS and adds that f2 is "genuinely a
different decision rule, not a parameter tweak". This skeptic
hand-verified the C3 numbers from the committed calib1.txt and
found the composition the red team does not state:

The print order in x1c_calib.zag is `CALIB <v> <s> <ticks>
<e_end>` (variant first, strategy second). Recomputing dXY from
the printed rows:
- d01 = 7, variants {0,1,3,4,6,7,10}: matches the program and the
  red team.
- d02 = 12, d12 = 12: match the program.

But every one of the 12 f2 differences (vs f0 and vs f1) is an
e_end-only difference. Ticks are identical at 1200 for all three
calibrators in all 12 variants. The "vector-distinctness" that
certifies f2 as qualitatively distinct is carried entirely by
end-of-run energy residuals (e.g., 145 vs 197, 181 vs 199,
160 vs 150), never by survival differences. All three calibrator
medians sit at the 1200 ceiling, so the calibration discriminates
nothing about survival; the distinctness claim does all the work,
and it is outcome-based.

Two consequences:
1. The gate's threshold (dXY >= 1, x1c_calib.zag: "Pairwise
   distinct requires dXY >= 1") is a hair trigger. Any two
   non-identical implementations differ in at least one variant's
   energy residual, so the gate certifies "qualitatively distinct"
   nearly automatically. The gate cannot distinguish a genuinely
   different decision rule from a near-identical strategy with
   slightly different energy accounting. The binding F10/R1 fix
   required the in-Zag check, which is implemented and passes as
   specified; the skeptic does not dispute that. But the
   substantive claim the fix was meant to secure, a qualitatively
   distinct third calibrator, is not what the gate measures.
2. The f2 outcome differences are confounded with the eating
   filter: f2 eats only ACTIVE motes on its cell while f0/f1 eat
   any mote on cell. The e_end gaps may be driven as much by that
   action-effect tweak as by the patrol decision rule. The red
   team's "genuinely a different decision rule" rests on code
   reading, not on the measured gate.

The 2021pdt verdict struck the "qualitatively distinct" claim from
the record. This wave's red team reintroduces equivalent language
("genuinely a different decision rule") on thinner measured
grounds (energy residuals, hair-trigger threshold). The skeptic
requires: the verdict record must state the e_end-only composition
of the f2 diffs, and the "genuinely different decision rule" gloss
must be qualified or struck. The C3 PASS per the specified gate
stands (the gate is what was binding, and it passes); the gloss is
what must be corrected. Blocking for the M1 certification language
as written; not blocking for the VOID verdict itself.

### A3. The x1c_evidence.zag post-data edits are a retune window the loop's rules do not bar (SUSTAINED as caveat, with a required forward rule)

Timeline, verified from the git record:
- 7fbd485b6 (milestone 1) first-commits x1c_evidence.zag (439
  lines, buggy version) plus all other x1c sources, variants, and
  calibration outputs.
- 26669a08d (milestone 2) adds only run1.tsv/run2.tsv; no source
  edits. The worker therefore saw the full run outputs before the
  next step.
- 0563e0cce (milestone 3) commits the evidence note AND a 30-line
  diff to x1c_evidence.zag (`git diff --name-only
  7fbd485b6..0563e0cce` confirms the only source touched is
  x1c_evidence.zag).

The two fixes (CALIB completeness check iterating 0..36 over an
s*36+v layout, missing s=1/s=2; median work areas using base
offset 100 in a 128-element slice, exceeding bounds) are in the
verdict-computing instrument, edited after data visibility. The
"committed before next milestone" discipline governs
prereg-to-implementation ordering (satisfied: d9e96ad91 <
7fbd485b6 strictly), but nothing in the loop's rules bars editing
the verdict emitter between milestones 1 and 3. That window is
exactly where verdict-shopping would occur.

Mitigations that genuinely hold: the fixes were disclosed in the
commit message; the diff is minimal (verified: exactly the two
fixes, nothing else); the note is byte-identical to the fixed
generator's stdout; the red team hand-recomputed every number from
the TSVs. The 2021pdt precedent tolerated milestone-3 source edits
with explicit labeling.

What does not hold, and the skeptic will not concede it:
- The record does not state what the buggy generator emitted
  before the fix (crash vs wrong note vs wrong verdicts). The
  out-of-bounds slice write (med[100..183] on a 128-element slice)
  means the unfixed generator's medians were corrupt or it
  trapped; either way the worker saw a malfunction after seeing
  data, then edited the verdict instrument. The CALIB-check fix
  touches the C3 recomputation path, the exact verdict under the
  binding F10/R1 correction.
- The 2021pdt tolerance covered agent/run sources, not the
  verdict-emitting evidence generator. The evidence generator
  deserves the stricter rule because it is the verdict instrument.

Classification: caveat, not blocking, because disclosure, minimal
diff, byte-identical reproduction, and independent hand
recomputation all hold under the loop's current (tolerant)
standard. Required forward rule: the evidence generator is frozen
at milestone 1; any post-data edit to it invalidates the milestone
chain and requires a re-freeze, and the record must state what the
pre-fix instrument emitted.

### A4. The K6 ablation is a confounded intervention saturating at the ceiling (SUSTAINED as caveat on interpretation)

The advocate calls the ablation "a genuine intervention". The
numbers are correct (medians move 266->1200 and 269->1200; M4
reflexes preserved; sketch-space maximum 258 consistent with
n_distinct=258). The skeptic attacks what the intervention
measures, not whether it intervened:

1. Removing COMBINE from the candidate pool changes two things at
   once: (a) the invention channel (no novel-composition steps),
   and (b) the exploration risk profile. The I arms die during
   enumeration of COMBINE-containing sketches (n_replans in the
   hundreds, deaths during exploration); the ablation arm explores
   a smaller, safer pool (258 sketches, no COMBINE) and never dies.
   The survival gain 266->1200 is fully explained by (b): the agent
   no longer dies exploring dangerous plans. Ticks-survived cannot
   separate "invention doesn't help" from "exploration is lethal".
   The K6 firing is therefore a confounded measurement of the
   invention claim.
2. The ablation median is 1200, the maximum possible value. A
   saturated instrument quantifies nothing; it reports "survived
   everything". The dramatic 266-vs-1200 comparison carries zero
   information about the magnitude of any invention effect.
3. The ablation arm is not the I arm minus invention; it is the I
   arm with a different candidate pool (258 vs 399 sketches),
   different enumeration length, and different B0/(1+n) scoring
   dynamics (n caps differ). The action space changed, not just the
   claimed mechanism.

None of this disputes the literal firings, and under the VOID
framing they enter as measurements, not kills. The skeptic's
demand: the record must carry that the K6 operationalization is
confounded as an invention-claim ablation, and the 2021pdt forward
rule must be re-entered explicitly: any future adoption must freeze
the operationalization first (it was recorded as "reasonable", never
frozen for adoption). Caveat.

### A5. K7's evidentiary base is thinner than the record's phrasing suggests (SUSTAINED as caveat; correct the count)

From the note's enumeration table (enum_tick != -1 means completed
enumeration): I-survive (arm 3) completed in variants 2 and 5 only:
2/12. I-invent (arm 4) completed in variants 2, 5, 6, 8, 11: 5/12.
The red team's "7 runs completed enumeration" is the sum across
both arms (2+5), which is consistent, but any phrasing like "5/12
in each I arm" is wrong and must be corrected to 2/12 and 5/12.

Consequences for the K7 reading:
- The entire I-survive K7 denominator (13 = 6+7 post-enumeration
  selections) comes from 2 of 12 runs. The gate fires correctly per
  the frozen rule (0/13 < 0.50), but the "validity" conclusion rests
  on a choice phase that barely existed.
- In 10/12 I-survive runs and 7/12 I-invent runs, enumeration never
  completed: the agents died exploring. The VOID is correct per the
  letter of K7, and the sparsity strengthens the VOID as a test of
  H1/H2 (there is almost no post-enumeration choice behavior to
  test), but it weakens any broader inference: the record must say
  "the design failed to reach its own choice phase", not anything
  about learned behavior. The frozen K7 cannot distinguish "the
  design failed" (its intended meaning) from "the environment was
  too lethal for the exploration budget".

Caveat. The VOID stands; the interpretation must stay narrow.

## Attacks on M2 (CONFIRM the fork battery [clean])

### B1. The battery certifies baf48e474, not the wave's HEAD; the race pattern repeats (SUSTAINED as caveat)

FORK_RESULTS_2321.md documents the incident plainly: local HEAD
moved mid-run from the task-pinned baf48e474 to 9c6646c04 (another
lane's interactive-survey commit). Pinning made the results inert
to the move, which is verified and to the worker's credit. But the
proposed verdict "CONFIRM fork battery [clean]" must be pinned in
the verdict line itself: CONFIRM at baf48e474; 9c6646c04 was not
tested by this battery and is left for the next wave's
enumeration. The 2021pdt wave banked the identical open question
("the loop's wave-HEAD cadence racing the wave cadence ... pattern
repeats"); it has now repeated. An unpinned CONFIRM will be read as
certifying the wave tip. Caveat, provided the pin is written into
the verdict.

### B2. Staleness and headline scope (noted as caveats)

- tnn_chat FIT staleness is now 5 of 8 (not re-run this wave,
  queued separately). The battery's scope stamp ("toolchain and
  extraction stability only") is honest, so the staleness does not
  invalidate M2; but the wave's overall health claim must carry the
  5-of-8 caveat, not bury it in the fork report's tail.
- The "56 named entries" headline counts duplicates (44 unique
  commits; the live set is 2 named entries on 1 unique commit).
  The report discloses this (P8 duplication table), so this is a
  presentation caveat only: never headline 56 without the
  unique-commit count beside it.

## Attacks on M3 (CONFIRM the design lane NULLs with the EXP2-K4 redesign recommendation)

### C1. The 3-wave auto-retire expiry is a governance pre-decision smuggled into a design recommendation (SUSTAINED, BLOCKING as written)

HUNT_2321.md recommends the EXP2-K4 redesign with "a 3-wave expiry
clause to kill the permanent-HELD risk: if no curator path (his
decision) exists within 3 waves of the redesigned prereg being
draftable, RETIRE the lane with a written verdict instead of
holding forever."

This contradicts the recommendation's own reservation that "the
final retire/keep call is his". Silence is not a decision; retiring
on his silence decides it for him. It is deadline pressure on a
pending decision of Micah's, pre-committed by the loop without his
approval. The advocate's claim that "nothing here decides or
pre-decides any of his six rulings" is false as written: the expiry
clause conditionally pre-decides the retire/keep call.

The skeptic requires: strip the auto-retire clause, or convert it
into a question put to Micah ("the lane proposes a 3-wave expiry;
retire only on his explicit approval"). The M3 motion may not pass
with the expiry clause in its current form. Blocking.

### C2. "Mechanical selection attestation" relocates the spec-blindness problem; it does not resolve it (SUSTAINED as substantive objection)

Blocker 2 (F2) requires a spec-blind curator. The redesign's answer
is "attestation of mechanical application" of F1 (first 12 by
commit order satisfying the qualifying rule). But the corpus's
problem set is authored by the loop itself, with full knowledge of
the spec the corpus must probe. Spec-knowledge enters at authoring,
not at selection; mechanical selection over a self-authored,
spec-informed problem set does not produce spec-blindness. The
recommendation concedes this by punting F2 to the governance track
("ask whether attestation of mechanical application suffices, or
whether he supplies a spec-blind curator"): the technical redesign
does not solve blocker 2, it asks Micah to waive or redefine it,
which is the status quo, not a redesign. "Mechanical selection
attestation" renames the concern rather than resolving it. The
record should say so plainly. This does not block the NULL/HELD
confirmations, but it blocks presenting the redesign as a technical
solution to blocker 2.

### C3. The redesign is not self-executing (noted as caveat)

The technical track's key premise, that loop-generated failures of
the frozen machinery count as "real deliberation failures" under
the 0221pdt forward requirement (a), "would need the judge's
acceptance" (the recommendation's own honest caveat). The corpus
generation is loop-executable in pure Zag; its validity as a K4
corpus is not the loop's to grant. The recommendation is therefore
a proposal contingent on external acceptance, not an executable
path. Caveat.

## Attacks on M4 (CONFIRM the interactive survey NONE)

No substantive attack sustained. The method is documented
(11 commits, 1,208 added files, 222 *.zag, 4,149-line added diff
scanned for the full keyword set plus fd-0 reads, non-.zag files
scanned separately), every keyword hit is enumerated as a false
positive, and the previously surveyed Micah REPLs are correctly
left as read-only closed frontier. The skeptic notes one
presentation point: the survey covers fc1a43b8c..baf48e474 and its
verdict NONE is pinned to that range; the mid-battery HEAD move to
9c6646c04 is the survey's own commit, so no gap. M4 may pass.

## Attacks on M5 (CONFIRM the commit-order self-check VALID)

The chain d9e96ad91 < 7fbd485b6 < 26669a08d < 0563e0cce is strict
and merge-base verified; the prereg 8b456736b strictly precedes the
addendum and all implementation; the addendum was committed alone
before any EXP1c implementation file existed. VALID on its own
terms. The skeptic re-enters the standing caveat the advocate
already carries: commit order evidences commit order only, never
run order and never content identity. In particular, commit order
does not show that x1c_evidence.zag was frozen before data
visibility (A3 shows it was edited after), and it does not show
that the calibration ran before the full runs. M5 may pass with the
caveat restated, not implied.

## Summary of sustained attacks

Blocking (must be resolved before the verdicts enter as written):
1. A1: the wave verdict line must enter VOID as a test of H1/H2
   (K7) and must quote the 2021pdt precedent verbatim ("a void test
   cannot kill a hypothesis"), explicitly neutralizing the evidence
   note's and the milestone-3 commit message's KILL labels. The
   K1/K6 firings enter as certified measurements from a voided run
   only.
2. A2 (language): the C3 certification must state that the f2
   vector differences are e_end-only (ticks identical at 1200 in
   all 12 variants) and must qualify or strike the "genuinely a
   different decision rule" gloss; the dXY >= 1 hair trigger and
   the ceiling-sitting calibrators must be on the record.
3. C1: the EXP2-K4 redesign's 3-wave auto-retire expiry clause must
   be stripped or converted into an explicit question to Micah; it
   may not stand as a loop pre-commitment to retire on his silence.

Caveats (verdicts may enter with these attached):
- A3: x1c_evidence.zag was edited after data visibility;
  disclosure, minimal diff, byte-identical reproduction, and
  independent hand recomputation hold, but the loop needs a forward
  rule freezing the verdict emitter at milestone 1, and the record
  should state what the pre-fix instrument emitted.
- A4: the K6 ablation is confounded (exploration-risk change, not
  just invention removal) and saturates at the 1200 ceiling; the
  firings are correct computations but must never be read as
  evidence about invention; re-enter the 2021pdt rule that any
  future adoption freezes the operationalization first.
- A5: K7's base is 2/12 (I-survive) and 5/12 (I-invent) completed
  enumerations, not "5/12 in each arm"; the VOID records "the
  design failed to reach its own choice phase", nothing about
  learned behavior.
- B1: fork-battery CONFIRM must be pinned to baf48e474;
  9c6646c04 untested this wave; the HEAD-race pattern repeats.
- B2: FIT staleness 5 of 8 rides with the wave's health claim; the
  56-named headline must travel with the 44-unique-commit count.
- C2: "mechanical selection attestation" does not resolve F2
  spec-blindness; the redesign asks Micah to waive it, which is the
  status quo.
- C3: the EXP2-K4 redesign's validity needs the judge's acceptance
  of self-generated failures as "real deliberation failures"; it
  is not self-executing.
- O1 (red-team observation, endorsed): the note omits the
  addendum's explicit max-enum_tick comparison line; documentation
  completeness for a future iteration.

M4 and M5 may pass (M5 with the order-evidences-order caveat
restated).
