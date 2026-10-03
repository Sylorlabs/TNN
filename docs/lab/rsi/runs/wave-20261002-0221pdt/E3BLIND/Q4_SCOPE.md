# Q4_SCOPE.md -- E3BLIND mandate scope per debate Q4

Wave: wave-20261002-0221pdt, lane E3BLIND.
Ruling source: docs/lab/rsi/runs/wave-20261001-2321pdt/DEBATE.md
(Q4) and docs/lab/rsi/runs/wave-20261001-2321pdt/DEBATE/
JUDGE_RULING.md (Q4 full text, lines 151-195).

## The Q4 ruling, verbatim

From DEBATE.md:

"### Q4 BATTERY-E3: blind re-examination mandate scope"

"**Ruling: OVERTURN (narrow mandate).**"

"Blind re-test required for selection-step claims. Single-candidate
mechanisms cleared via the A1-A6 audit (performed, not assumed).
E1-W4 behavioral leg cannot be cited as construction evidence."

From JUDGE_RULING.md (the mandate definition):

"The E3 mechanism can only confound claims that have a structural
selection step among multiple candidates. Where no candidate set and
no selection step exist, there is no oracle pathway for a blind
re-test to remove; a masked re-test there discriminates nothing."

"So the mandate is: every construction claim whose evidence could
rest on an unmasked QUERY-carried expected value playing a selection
role must be answered, either by blind re-test (selection-step
claims) or by the A1-A6-style audit (single-candidate mechanisms,
audited per mechanism). No blanket masked re-examination of
everything is required."

"Named applications: (a) PF-A/PF-C battery results re-described per
CLUSTER-FINAL; (b) E1-W4's behavioral leg cannot be cited as
construction evidence (its confound is flagged in both E1 and E3
records: structure-driven answers vs oracle-verified BFS traversal
indistinguishable), while E1's structural leg (licensed derived
structures in persistent state) stands and kills H1c; (c) any
prior-wave construction observation on unmasked QUERY evidence
takes the same fork: blind re-test or A1-A6 audit before citation."

## IN SCOPE: selection-step claims (blind re-test required)

These claims have a structural selection step among multiple
candidates, where the evidence could rest on the unmasked
QUERY-carried expected value playing a selection role. All quotes
below are from the BATTERY-E3 records of
wave-20261001-2321pdt.

IN-S1. The selection-dependence claim (E3_RUN.md section 5):

"The refined H1d holds: every correct composition observation in
the PF battery depended on the trial's unmasked verifier
(t2_try_verify: accept iff executed output equals the
QUERY-carried expected value) to SELECT the right candidate among
multiple executable BFS chains."

IN-S2. The masked-mode selection claim (E3_RUN.md section 5):

"With the oracle withheld, the trial's masked policy (accept first
executable candidate) emits the first chain in deterministic BFS
order, right or wrong."

IN-S3. The PF-A2 re-description claim (E3_RUN.md section 5;
named application (a) of the ruling):

"PF-A2's 2/2 valid-composition result is re-described: BFS
enumeration plus oracle selection, not selective construction."

These three collapse into one mechanism (first-executable-wins
blind; oracle does the selecting when unmasked). The fresh blind
re-test on sealed worlds reports one verdict set per claim:
CONFIRMED-BLIND (selection-failure signature reproduced on fresh
sealed worlds) or OVERTURNED-BLIND (the blind trial selects the
sealed-valid composite, proving a selection mechanism beyond
oracle verification exists).

## OUT OF SCOPE: excluded from the blind re-test

OUT-1. ASSEMBLY WORKS BLIND. The E3 claim that "the blind trial
runtime-assembled GUARD/SETREG chain graphs with ET_DEP provenance,
promoted them as MAP nodes, and executed them" (JUDGE_RULING.md).
Justification: "The E3 mechanism can only confound claims that have
a structural selection step among multiple candidates. Where no
candidate set and no selection step exist, there is no oracle
pathway for a blind re-test to remove; a masked re-test there
discriminates nothing." Assembly is single-mechanism territory
(A1-A6 audit), not a selection-step claim.

OUT-2. E3A blind distractor observations (relation-agnostic
enumeration on the novel relation 80629). Observational evidence;
no candidate set and no selection step. Same justification as
OUT-1.

OUT-3. Oracle-present control results (E3A 2/2, E3B 2/2).
Validity/calibration gates, not construction claims. Same
justification as OUT-1.

OUT-4. E1-W4 behavioral leg. Justification: "E1-W4's behavioral
leg cannot be cited as construction evidence (its confound is
flagged in both E1 and E3 records: structure-driven answers vs
oracle-verified BFS traversal indistinguishable)". Excluded by the
ruling; a blind re-test cannot rescue it.

OUT-5. E1 structural leg. Justification: "E1's structural leg
(licensed derived structures in persistent state) stands and kills
H1c". It stands; it is a structural claim with no selection step.

OUT-6. ARENA-BLIND ROSTER. Justification: "Single-candidate
mechanisms cleared via the A1-A6 audit (performed, not assumed)"
and "This audit template is the correct instrument for
single-candidate mechanisms: categorical clearance via audit, audit
performed and committed, not assumed." The ORACLE-FREE branch of
the frozen decision rule was not triggered for ROSTER.

OUT-7. PF-A/PF-C battery results. Justification (named application
(a)): "PF-A/PF-C battery results re-described per CLUSTER-FINAL".
The ruling answers them by re-description, not by this lane's
blind re-test.

OUT-8. Any L3 or generality language. The E3 records state
"Criterion 0 not met; no L3 language anywhere" and "Does not
establish: broad generality, L3, or progress toward L3." Never
claimed; outside the mandate.

## What the re-test verdicts can and cannot do

The verdicts (CONFIRMED-BLIND / OVERTURNED-BLIND) apply only to
IN-S1 through IN-S3. They confirm or overturn the selection-step
claims; they do not promote, demote, repair, or re-frame any
claim, and they propose no repair (no-patch-treadmill rule).
Promotion or demotion of BATTERY-E3 claims beyond the mandate is
the coordinator's business.
