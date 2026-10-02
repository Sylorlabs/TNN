# DEBATE TRANSCRIPT: wave-20260926-2321pdt

Wave: wave-20260926-2321pdt. Date of session: 2026-09-27.
Repo: ~/workspace/tnn-rsi, branch tnn-native-lab.
Implementation commit under judgment: 74565859f (all new files; no push).
Preregs: docs/lab/invention/survival/PREREG.md (frozen commit 3ac39fc14)
and docs/lab/onebrain/PREREG.md (frozen commit 1ab40adce), both authored
by Micah. Prereg commit-order self-check: PASS for both experiments (both
prereg commits are ancestors of 74565859f and strictly precede it, from
the commit record).
Roles: ADVOCATE (for adoption), SKEPTIC (against), JUDGE (reasoned
rulings with cited numbers). The transcript is the record; plain
language, no em dashes.

---

## 1. Opening slate

Items under judgment:

1. EXP1 invent-to-survive: coordinator verdict KILL H1 on K1. Numbers:
   medians over 12 variants, two byte-identical runs
   (sha256 ba4677cc8a786a0d52f0ec89a891c6d9b7e16436c484d61ff388d16a88521ebf):
   P=600, Z=89, R=600, I-survive=574, I-invent=574. K1 fires (574 <= 600).
   K2 PASS (574 > 89). K3 PASS (P=600 >= 480, run not void). K4 kills the
   invention claim on novelty independently (schemas plus authored scoring
   judged trivial recombination). K5 incomplete (no independent auditor).
   K6/A1/A2 not triggered. Verdict: NOTHING TO ADOPT.
2. EXP2 one-brain dispatch: coordinator verdict under review, leaning ADOPT
   machinery with caveats. Fresh 10-problem frozen holdout: one-brain 10/10
   vs single-deliberation baseline 0/10 vs shared-writes-off ablation 0/10.
   K1 through K6 all PASS, with a caveat on K4 (on 2/3 mechanism-test
   problems the attack-lens branch independently reached the shared
   verdict, so verdict-level evidence is partial).
3. Fork battery: 41 entries, 38 PASS, 2 extraction FAIL (pull/1, pull/2,
   trees lack the toolchain path, six waves running, expected), 1 CONFIRM
   under P20 scope stamp (rh-main at 27a4271f, commit absent locally after
   the pre-wave fetch). Queued item resolved: rh-tnn-native-lab-tip-start
   at d9ddc556 now testable and passes. Verdict line is a [RE-CERT] of
   toolchain stability.
4. Six owner governance rulings (S7 strike, MD-SSD-1, S11 image pull,
   S11-AUD pull, C12 queue, Python-mirror logic): STILL OPEN AND UNTOUCHED.
5. Prereg commit-order self-check: PASS for both experiments (substantive,
   from the commit record).

Contested questions are argued per item below.

---

## 2. Advocate brief

### Item 1 (EXP1)

The advocate defends the KILL H1 verdict as recorded. The numbers are
clean: two full 60-run executions byte-identical
(ba4677cc8a786a0d52f0ec89a891c6d9b7e16436c484d61ff388d16a88521ebf),
calibration gates C1 (P=600 >= 480), C2 (Z=89 < 150), C3 (three distinct
strategies at 600) all pass, and the frozen bar K1 fires on its face:
574 <= 600. K4 kills the invention claim a second, independent way: the
I arm's six schemas are the same primitives taught to P, the scoring
bonuses were authored to favor known-productive orderings, and the
resulting behavior is recombination of taught elements. NOTHING TO ADOPT
is the only verdict consistent with the evidence. The Python disclosures
are honest and the numbers stand on their own pins.

### Item 2 (EXP2)

The advocate defends leaning ADOPT, with caveats, for the machinery as
committed under docs/lab/onebrain/. The confirmatory holdout is fresh
and clean: frozen 2026-09-27T06:42:47Z with sha256 edab14df...
(holdout_freeze.txt), expected answers grounded in round-4 verified
behaviors and fixed before the machinery ever ran on the file, and the
developmental battery (which had been iterated with outcome knowledge)
was honestly discarded rather than quietly kept. All six kill bars pass
on the holdout: K1 10/10 vs 0/10 vs 0/10 (conjunctive requirement
satisfied); K2 poison test 6/6 causal with private-ledger control clean;
K3 scaffold removal 10/10 with zero fan_out calls in the driver; K4
delete/reorder changes traces 3/3 with the verdict distribution differing
from independent branches; K5 3x byte-identical; K6 no RNG by grep.
The machinery is pure Zag, deterministic, and the causal role of the
shared channel is proven by K2 and K4. Adoption as experimental record
is earned.

### Item 3 (fork battery)

The advocate defends the [RE-CERT] line: 38/38 tested entries pass with
uniform evidence (znc pin 498abcb5... on 38/38, probe sha
3b29aa0661... on 38/38, B1/B2/B3 and both negative controls identical
across all 38), the two FAILs are the expected extraction failures of
non-TNN doc trees (six waves running), the rh-main CONFIRM is a recorded
coverage gap under P20 (not a failure), and the queued d9ddc556 item is
resolved. The battery certifies toolchain and extraction stability, which
is exactly its scope.

### Item 4 (six governance rulings)

The advocate notes there is nothing to argue: these are Micah's rulings
to make, and the wave correctly left them untouched. Recorded as OPEN.

### Item 5 (prereg commit-order self-check)

The advocate records PASS as a substantive check from the commit record,
not a formality: both prereg commits are ancestors of 74565859f and
strictly precede the implementation. This is one of the few waves where
the self-check is verified against git rather than asserted.

---

## 3. Skeptic report

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

The skeptic answers its own probe, because everything below turns on it.

EXP1 artifacts: the world sources (src/*.zag), kb/, worlds/v00-v11, and
all result/audit docs are NEW this wave (committed in 74565859f; no
prior-wave lineage; the earlier Task 1 invention trial is cited in the
prereg for comparison but no code or render is reused). Inherited: the
pinned toolchain znc binary (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef),
the branch tnn-native-lab, and the prereg discipline itself.

EXP2 artifacts: onebrain.zag, ob_problem.zag, ob_encode.zag,
ob_baseline.zag, ob_run.zag, ob_ablate.zag, ob_score.zag, ob_poison.zag,
ob_delreord.zag, ob_scaffold.zag, problems_holdout.tsv (frozen), and all
result logs are NEW this wave. Inherited: the deliberation-v1 ledger
layout (reused, not forked) and the same pinned toolchain.

Fork battery artifacts: the 41 per-entry evidence dirs are NEW this wave;
the harness fork_battery.zag is inherited (extracted from the 20260923
archive branch, sha-verified) and the toolchain is the pinned binary.

### Item 1 skepticism

(a) The Python breach is a real red-line violation, honestly disclosed:
python3 used twice, once to count lines (output only) and once to rewrite
mote velocity lines in variants.zag (real edits to committed source).
The skeptic's charge: the velocity values written by Python are the ones
that produced the R=600 ceiling (five motes at plus/minus 1, one
stationary at P's home; R camps the stationary mote and hits 600). The
breach does not change the arithmetic of the runs, but it means the wave
cannot carry a pure-Zag attestation, and the velocity configuration that
decides the K1 outcome was authored through a prohibited tool. At
minimum the wave is compliance-tainted; the breach must be recorded and
it feeds the still-open governance question on Python use.

(b) The I arm likely violates the prereg's literal "six primitive
actions" requirement (it plans at schema level). The skeptic notes this
cuts AGAINST any attempt to rescue H1: I was given a higher-level,
arguably stronger representation than the prereg specified, and still
lost. The noncompliance cannot overturn the K1 kill; it only further
removes any claim that this wave tested the prereg-specified I machinery.

(c) The R=600 ceiling is the serious objection. R camps a stationary
mote at the per-world home cell and hits the 600 cap; the world leaves no
headroom for invention to demonstrate a gain. The prereg itself required
(C3) that the world not collapse to one dominant strategy, and the wave
notes concede R's camping is a ceiling effect. A K1 kill recorded in a
ceilinged world has the letter of the bar but weak epistemic content:
it shows this I did not beat this R here, not that invention machinery
cannot beat recall. The skeptic wants the record to say so plainly.

### Item 2 skepticism

The lean-to-ADOPT is premature in two directions. First, scope of
adoption: NO frozen subsystem regression battery was run on the new
onebrain module. Adopting toward standing deliberation machinery without
a regression sweep is exactly how a loop corrupts its own substrate.
Second, scope of claim: the holdout tests one ambiguity structure
(early-mislead/late-refutation) by construction, and in the ablation the
attack-lens branch (bv1) alone scores 10/10 on the holdout. So the
10/10 vs 0/10 headline does not establish that fan-out beats single
deliberation on hard problems generally; it establishes that within this
machinery, the shared channel is the causal carrier of the gain (K2/K4).
The coordinator's "lean to adopt" must be narrowed to experimental-record
adoption of the machinery, with wire-in explicitly deferred to a
regression-gated wave, and the H1-style claim narrowed to the tested
structure.

### Item 3 skepticism

The skeptic finds nothing to contest on the numbers but restates the
scope stamp: this battery certifies toolchain and extraction stability
only. The two pull-head FAILs and the rh-main CONFIRM are properties of
those forks' trees (no toolchain path) and local object-store coverage,
not toolchain regressions. The skeptic agrees with [RE-CERT] and notes
the P19 coverage-delta accounting checks out (40 to 41 entries, 4 to 2
extraction FAILs with d9ddc556 resolved, 33 to 34 unique commits).

### Item 4 skepticism

No skepticism beyond vigilance: these six are Micah's and the wave
touched none of them. Any debate content that narrows or decides them
would itself be a red-line breach. Recorded as OPEN, no relitigation.

### Item 5 skepticism

The skeptic accepts the PASS as substantive (verified from the commit
record: 3ac39fc14 and 1ab40adce both ancestors of 74565859f, strictly
earlier). No objection.

---

## 4. Judge rulings

### Item 1 (EXP1): coordinator verdict KILL H1 UPHELD; verdict record NARROWED with recorded caveats.

Ruling on (a), the Python breach: the breach TAINTS the wave's
compliance certification, not the arithmetic of the kill. The numbers
rest on verified pins (toolchain 498abcb5..., output sha256
ba4677cc... byte-identical x2), and Python did not compute any result;
but Python did write the mote velocity lines in the committed variants,
and those velocities are what produced the R=600 ceiling. The recorded
consequence: this wave cannot be certified pure-Zag compliant; the
breach is entered into the wave record (EVIDENCE.md already discloses
it); and it is flagged against the still-open owner governance question
on Python use. The K1 kill is not overturned by the breach, because the
bar fired on deterministic, pin-verified numbers.

Ruling on (b), the I-arm prereg-noncompliance: it does NOT undermine
the K1 kill. The I arm planned at schema level, a representation at
least as powerful as the prereg's six primitive actions; it still
failed 574 <= 600. Noncompliance cannot rescue H1. It does mean this
wave did not test the prereg-specified I machinery, which matters for
any future retune: the retune must implement the literal machinery.

Ruling on (c), the ceiling: the KILL H1 verdict stands as the frozen
bar demands (never weaken a frozen kill bar; 574 <= 600 fires on its
face). But the record is narrowed: this is a kill IN THIS WORLDS
CONFIGURATION, where R camps a stationary mote to 600 and no headroom
exists. The prereg's own C3 required no single dominant strategy; the
R=600 ceiling violates that spirit. The H1 question is therefore
recorded as killed-for-this-run but NOT settled: a retuned world that
removes the stationary-home-mote camping must re-test before the claim
is treated as dead. K4 (trivial recombination, schemas plus authored
scoring) and the incomplete K5 stand as recorded. NOTHING TO ADOPT:
upheld. Tag: [NEW] (new experiment, new numbers, new sources).

### Item 2 (EXP2): coordinator verdict NARROWED, not adopted as leaned.

The skeptic's two objections are sustained. The machinery is ADOPTED
only as EXPERIMENTAL RECORD under docs/lab/onebrain/ (the committed
sources, frozen holdout, and result logs), and explicitly NOT wired
toward standing deliberation machinery: no frozen subsystem regression
battery was run on the new module, and wire-in without one is
disallowed. A future wave may propose wire-in only after a regression
sweep.

The claim is narrowed to its tested scope: within this machinery and on
the early-mislead/late-refutation structure, the shared channel is the
causal carrier of the gain. The evidence for that narrower claim is
strong: K1 conjunctive 10/10 vs 0/10 vs 0/10 on the frozen holdout
(frozen 2026-09-27T06:42:47Z, sha256 edab14df...); K2 poison 6/6 with
clean private-ledger control (poisoned shared e6 flipped OB-01 R2 to R1
and changed every branch's consumption; poisoning one private ledger
left other branches byte-identical); K3 scaffold removal 10/10 with
zero fan_out calls in the driver; K4 trace changes 3/3 with the shared
verdict distribution differing from every independent branch run; K5 3x
byte-identical; K6 no RNG by grep. The noted caveats are entered into
the record verbatim: the attack-lens branch alone reaches 10/10 on the
holdout, so fan-out is not shown to be the only policy that solves
these problems; K4's verdict-level evidence is partial (2/3 problems
where a branch independently coincides). The developmental battery
numbers (13/15, 3/15, 3/15) remain developmental and are not cited as
evidence. The honest discard-and-refreeze repair is credited: it is
why the confirmatory numbers are trustworthy. Tag: [NEW] (new module,
new holdout, new causal evidence).

### Item 3 (fork battery): coordinator verdict UPHELD. Tag: [RE-CERT].

41 entries, 38 PASS, 2 extraction FAIL, 1 CONFIRM. Uniform evidence
verified by grep across all 38 PASS runs (znc pin 498abcb5... 38/38,
probe sha 3b29aa0661... 38/38, B1/B2/B3 and both negative controls
uniform). The FAILs are expected (pull/1 at 5802fec8 and pull/2 at
4b76bb59 lack the toolchain path, six waves running). The CONFIRM is a
P20 coverage gap for rh-main at 27a4271f (commit absent locally), not a
failure. The queued d9ddc556 item is resolved (now testable, passes).
The verdict line is a re-certification of toolchain and extraction
stability, nothing more. Tag: [RE-CERT].

### Item 4 (six governance rulings): RECORDED AS OPEN AND UNTOUCHED.

S7 strike, MD-SSD-1, S11 image pull, S11-AUD pull, C12 queue, and the
general Python-mirror-logic question: all six remain Micah's decisions.
This debate decides none of them and relitigates none of them. The
EXP1 Python breach (item 1a) is flagged as relevant context for the
open Python question, without deciding it.

### Item 5 (prereg commit-order self-check): PASS UPHELD.

Substantive from the commit record: 3ac39fc14 (EXP1 prereg) and
1ab40adce (EXP2 prereg) are both ancestors of 74565859f and strictly
precede it. Recorded as a real pass. Tag: [NEW] (this wave's check).

---

## 5. Final verdict table

| Slate item | Verdict | Judge action | Tag |
|---|---|---|---|
| 1. EXP1 invent-to-survive | KILL H1 on K1; NOTHING TO ADOPT | UPHELD, record narrowed (ceilinged world; claim not settled) | [NEW] |
| 1a. EXP1 Python breach | Breach recorded; wave not pure-Zag certifiable | Recorded consequence; kill arithmetic unaffected | (compliance note) |
| 1b. EXP1 I-arm noncompliance | Does not undermine K1 kill | Noted for future retune | (compliance note) |
| 2. EXP2 one-brain dispatch | Adopt as experimental record only; no wire-in; claim narrowed to tested structure | NARROWED from lean-to-adopt | [NEW] |
| 3. Fork battery | 38 PASS / 2 extraction FAIL / 1 CONFIRM | UPHELD | [RE-CERT] |
| 4. Six governance rulings | OPEN AND UNTOUCHED | Recorded; not decided | (owner) |
| 5. Prereg commit-order self-check | PASS, both experiments | UPHELD | [NEW] |

Tags per the provenance-honesty rule: [NEW] = artifact first appears in
this wave (EXP1 sources and numbers; EXP2 module, holdout, and causal
evidence; this wave's self-check). [RE-CERT] = re-certification of
inherited stability (fork battery toolchain/extraction). No [STACK] and
no [VOID] items this wave.

---

## 6. Queued-next list

1. EXP1 world retune: remove the stationary-home-mote camping that
   produces the R=600 ceiling (per the prereg's C3 no-dominant-strategy
   requirement), implement the literal six-primitive-action I machinery,
   run pure-Zag with zero tooling breaches, then re-test H1.
2. EXP2 holdout broadening: build additional frozen holdouts over
   ambiguity structures other than early-mislead/late-refutation before
   any claim beyond the tested structure.
3. EXP2 regression sweep: run the frozen subsystem regression battery
   against the onebrain module before any wire-in toward standing
   deliberation machinery is proposed.
4. EXP2 K4 hardening: if verdict-level evidence is wanted, design
   delete/reorder tests where no independent branch reaches the shared
   verdict.
5. Fork battery: rh-main at 27a4271f remains CONFIRM under P20 (coverage
   gap); pull/1 and pull/2 remain extraction FAILs until their trees
   gain the toolchain path.
6. The six owner governance rulings remain awaiting Micah; nothing in
   this wave decides or narrows them.

---

Session notes: no commit, no push, .wave_lock untouched. Transcript
written to docs/lab/rsi/runs/wave-20260926-2321pdt/debate/DEBATE_2321.md
per the debate-group task. No em dashes used in this file.
