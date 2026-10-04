# JUDGE: wave-20260928-1721pdt debate

Reasoned rulings with numbers cited. Each motion answers the
skeptic's provenance probe verbatim: "What is the provenance of the
artifacts under judgment, and what exactly is new versus inherited?"

## M1: Fork battery CONFIRM [NEW] as process confirmation only

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

RULING: CONFIRM, with the carry-forward documented and scope stamped.

On the provenance question: the battery execution itself is inherited
from the dead 1421pdt worker (enumeration 14:24 PDT, batch 14:25 to
14:28 PDT, all at run-start pin 547b2132c). What is new this wave is
the coordinator's integrity review: 59 evidence dirs exist on disk, 59
verdict lines extracted, summing to 57 PASS and 2 UNTESTABLE with zero
FAIL; the two UNTESTABLEs carry the expected cause line (pinned
toolchain path absent, git show exit 128) for rh-pull-1-head
(5802fec8) and rh-pull-2-head (4b76bb59); and the pin equals the
current tip byte for byte (git rev-parse HEAD:
547b2132c0435b11e51099ae8a598e5547095f52; no tracked-file changes
since the battery ran). The skeptic's fabrication worry is real in
principle but bounded in practice: the verdict lines encode
per-entry detail (pinned SHAs, commit ids, cause strings) that matches
the manifest's pinned-commit discipline, and the counts reproduce the
summary's numbers exactly (57/59 PASS, 48 unique commits per the
summary's own recomputation rule). The empty batch.log is noted as an
evidence-quality gap: no driver execution trace survives. It does not
change any verdict, because no verdict is computed from batch.log
content; all per-entry verdicts live in evidence/RESULT.txt. On the
0829pdt re-run precedent: that precedent demands a fresh re-run when
the pin changes; here the pin did not change, so the carried evidence
certifies the current tip directly. The verdict becomes debated this
wave, which discharges the "never debated" objection. Scope stamp
stands: process confirmation only (toolchain and extraction stability),
never the contents of the tested commits. Numbers cited for the
record: 59 named entries, 57 PASS, 0 FAIL, 2 UNTESTABLE; znc pin
498abcb5 uniform; harness binary sha256 a2e6284c byte-identical to
the frozen instrument; B1/B2/B3 pass; neg1_ok 57/57, neg2_ok 57/57;
R32_ZNC_PROBE_OK on all 57 tested; the 1721pdt probe-loss FAIL stays
closed (repair 37d1d3cab is an ancestor of the pin). M1 CONFIRMED.

## M2: H-C kill governance audit CONFIRMED-ON-RECORD [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

RULING: CONFIRM. The finding is on the record; the recommendation is
banked to Micah; the loop decides nothing.

On the provenance question: all three commits are inherited from
Micah's own 2026-09-27 work; the audit adds no new test. What is new
is the reading: the K-HC4 frozen at a95e0d50c (BUILD.md section 6:
"learn the D1 six", PASS with D1/D2 deviations) versus the K-HC4
applied at 57d055bbb (TESTING.md line 138 and the kill bars: "minimum
capability includes swap-first-last", FIRES, kills H-C). The pickaxe
evidence is specific: "minimum capability includes" first appears in
the tree at 57d055bbb (log -S returns only that commit); "K-HC5" first
appears at 57d055bbb with no prior freeze commit; "K-HC4" appears only
at a95e0d50c and 57d055bbb. The skeptic's absence-based critique is
answered by the audit's own caveat, which stays on the record: the
cited HYPOTHESIS.md is absent from the tree, so a never-committed
document cannot be excluded; the finding is therefore
CONFIRMED-ON-RECORD, not proven-absolute, and the label says exactly
that. On the half-measure critique: the loop records the finding and
banks the recommendation (strike the kill or re-run H-C under the
original frozen bar) without altering his verdict, because his
frontier is his to judge and the loop may not decide it. This is not
passive acceptance of a redefined bar: the loop's own records now
carry the finding that the 57d055bbb H-C kill is UNVERIFIABLE as a
frozen-bar kill, and no future wave may cite it as a clean frozen-bar
verdict. The audit documents a bar change; it weakens nothing and
alters nothing of his. M2 CONFIRMED.

## M3: Design lane NULLs and HELDs [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

RULING: CONFIRM. The NULLs are range-scoped and labeled as such; the
HELDs rest on unchanged blocker evidence.

On the provenance question: the lane report HUNT_1421.md is new this
wave (produced by the dead 1421pdt worker, integrity-checked by this
wave's coordinator); the blocker evidence it cites is inherited from
2321pdt, 0221pdt, and 0829pdt. The survey range 81f0cfe12..547b2132c
contains exactly 1 commit (loop-owned 547b2132c), 4 files, all loop
records, 0 origin commits, 0 new mechanism text, 0 added .zag files.
The skeptic is right that NULLs over an empty range are trivially
true; that is precisely why they are recorded as NULL (nothing
surfaced) rather than as findings. Per-lane: EXP2-K4 HELD (expiry
question banked to Micah at 2321pdt, confirmed on his queue at 0221pdt,
not re-asked; no new blocker evidence); B1 NULL (0 mechanism hits in
docs/lab/invention/; P9 stays a re-freeze template); COMP2-P11 HELD
(ruling 6 still OPEN; tree-wide grep at the pin finds no new ruling-6
text); intelligence trades HELD (no genuinely new expensive capability
with a real mechanism; no knob proposed, and an expensive knob without
a capability would be manufacturing); sensory NULL (standing
stand-downs hold: G1, D-VID-1, ST-1 dead; E3 rejected by Micah in
blind A/B). The nothing-manufactured statement is present. On the
parking-lot critique: the loop has no escalation path it may use
without his ruling; the standing record (0221pdt) binds the loop
against self-executing retirement on his silence. HELD is the honest
verdict. M3 CONFIRMED.

## M4: Interactive survey NONE [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

RULING: CONFIRM, range-scoped.

On the provenance question: the survey file INTERACTIVE_SURVEY_1421.md
is new this wave; the range it sweeps is inherited coverage
(9f3827356..81f0cfe12 at 1121pdt found NONE; this wave extends to
547b2132c, adding one loop-owned commit). The sweep found 4 added
files, all survey records, 0 added .zag files outside prior records,
and none containing interactive entry-point code. The verdict is
explicitly scoped: NONE loop-owned in the merge range. The frozen
batch probes (fit_authority/tnn_chat.zag, tnn_chat_decline.zag) remain
the only loop-owned chat instruments, batch-only. The skeptic's
over-claiming worry is handled by the scope stamp in the verdict
itself: the wave claims nothing about the tree at large beyond the
range, and Micah's closed-frontier REPLs were surveyed read-only and
left untouched. M4 CONFIRMED.

## M5: EXP1c attempt-5 stand-down honored [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

RULING: CONFIRM.

On the provenance question: the stand-down is fully inherited from
the 0221pdt judge ruling; what is new this wave is the re-verification
that the commit record honors it (zero EXP1c commits, zero experiment
dirs, zero retune or re-run in the survey range). The skeptic is right
that a [NEW] tag on a trivial observation is thin; the tag marks the
verdict line as re-rendered and re-debated this wave, not as new
discovery, and the LOOP_STATE section will say so plainly. The judge
banked Q1 (exploration/exploitation redesign as a new design
direction) and Q2 (K7-bar attainability or re-specification) to Micah;
they stay banked and are not re-asked. On the "stuck on its top
priority" critique: the loop's highest-priority research direction is
a single continuing-life integration experiment, and EXP1c's stand-down
is one component, not the whole direction; the design lane's NULLs
this wave mean no new component was proposed, but the stand-down does
not freeze the rest of the roadmap. M5 CONFIRMED.

## M6: Commit-order self-check VALID, VACUOUS for adoption [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

RULING: CONFIRM.

On the provenance question: there are no candidate commits this wave,
so the check's input set is empty and the check is vacuous. The
verdict is VALID (the rule fired correctly on an empty set) and it is
worth exactly what it says: nothing is adopted this wave, so there is
nothing to gate. The skeptic's cover-concern is noted for the parent:
when the parent commits the carried 1421pdt lane files plus these
debate transcripts, that commit must stay record-only; any
implementation content landing alongside the record would need its own
prereg check at that time. The standing caveat is restated: commit
order evidences commit order only, never run order and never content
identity. M6 CONFIRMED.

## M7: tnn_chat FIT staleness 3 of 8 [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

RULING: CONFIRM at 3 of 8, not re-run, not due.

On the provenance question: the count is carried arithmetic; what is
new is this wave's increment. The record stands as: last fresh re-run
at 2021pdt (0 of 8); 2321pdt 1 of 8; 0221pdt 2 of 8; 0829pdt 2 of 8
(confirmed by that wave's judge; it stands as recorded even if the
sequence suggests an undercount). This wave is the next
verdict-bearing wave, so staleness advances one step to 3 of 8. The
skeptic's 4-of-8 alternative would require reopening the 0829pdt
judge's confirmed ruling; this debate does not relitigate settled
waves. Due at 8 of 8; not re-run this wave. The intervening commits
are docs-only loop records (547b2132c touches only wave-20260928-1121pdt
lane files), so no regression path exists for the FIT to miss. The
8-wave cadence is a standing rule the loop may not unilaterally
change; the re-examination question is banked as an open note, not a
verdict. The FIT instrument tests the frozen batch probe only; the
verdict claims no broader coverage. M7 CONFIRMED.

## M8: UNTOUCHED [VOID]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

RULING: CONFIRM.

On the provenance question: the items are all inherited; this wave
adds no new evidence about them and none is claimed. The six
governance rulings (S7 strike, MD-SSD-1, S11 pull, S11-AUD pull, C12
queue, Python-mirror logic) remain OPEN; the sealed blind pairs (R9,
C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform) were
not re-listed or re-presented; DP-1 presentation remains the parent
agent's queue decision; Micah's frontier dirs were touched only by
read-only survey. The skeptic is right that VOID is a placeholder;
that is what it is: the loop neither decided, relitigated, nor
re-presented any of these items. The H-C audit (M2) documents but
does not alter his verdict, and the loop decides nothing there either.
VOID repeated is honest as long as the verdict line says what it is:
a standing placeholder until Micah rules. M8 CONFIRMED.
