# REDTEAM_SELF: CONTLEARN-LH (adversarial self-review)

Wave: wave-20261002-0221pdt. Lane: CONTLEARN-LH. The red team attacks the
lane's own design, oracles, and verdict. Only hyphens are used here.

## Attack 1: is the longer horizon a real test or just more of the same events?

PARTLY UPHELD as a real test, with a precise scope. The three
unrelated-fact episodes (48/96/120) are, by themselves, "more of the same
events": they caused zero measurable change (REUSE_A 12/12; chains 4,5
and the sanity family intact through V=276; census shows no eviction
pressure, N1=317 of 1024). If the battery had contained only those, the
horizon would have been vacuous.

What makes it a real test is the subset-conflict design: conflicting
evidence was injected on the ORIGINAL chains' own licensing facts, which
genuinely threatened the composed structures. The learner responded with
live downstream revision (the MAP's executable composition was
restructured and re-executed at contradiction time). The horizon is real
exactly where it touches the chains' own evidence, not where it adds
unrelated volume. The curve discriminates these two interference kinds;
the single-point CONTLEARN3 design could not.

## Attack 2: does interference actually threaten the DEP citations?

NO, and the diagnostic proves it. Every MAP's DEP citations survived all
356 events intact: each MAP still cites its anchor fact, its original
licensing chain-fact node, and its proposal node with live type-1 DEP
edges. What changed under interference was the composed ANSWER (via
downstream revision creating new integrated facts), never the citation
structure. So the key question as phrased in the prereg ("does the
proposal-first ordering and the DEP-cited MAP structure survive
sustained interference") is answered: YES for the structure, with the
answer-value dynamics described in SEALED_EVAL.md. A reader who
conflates "structure survived" with "answers unchanged" would misread
the result; the verdict must keep them separate.

## Attack 3: is the CP-LH3 oracle mis-specified, and does LH-DEGRADED overclaim?

The oracle demanded the ORIGINAL chain values (22001+i) after the
battery deliberately contradicted and then corrected the underlying
chain facts. Three candidate "correct" behaviors exist: (a) retain the
original (the oracle's demand), (b) track the contradiction (what the
learner did), (c) track the resolved correction (arguably the ideal
continuing-learner behavior). The learner did (b), not (c): the composed
structures froze at the contradiction's value and never picked up the
resolved value.

The verdict LH-DEGRADED is the honest literal reading of the frozen bar
(the bar is not weakened retroactively), but it must not be read as
"the learner forgot things under load." The precise claim is narrower:
under targeted conflicting evidence on a composition's licensing facts,
the frozen revision operator revises downstream once (on contradiction)
and does not re-revise on correction; composed answers can therefore go
stale at the contradicted value. That is a real, deterministic,
instrument-independent limitation (it reproduces identically on the
unmodified control core), and it is more informative than a flat
12/12/12 would have been. The red team notes the oracle's demand (a)
was the least defensible of the three; the experiment's value is in
distinguishing (b) from (c), which the design did not anticipate but the
diagnostic established.

## Attack 4: could the degradation be a driver artifact?

Considered and rejected. The contradictory objects (22101+i) and
resolved objects (22111+i) are fresh ids with no prior use; the OBSERVE
protocol returned rv=0 in all four subset episodes; the fact-level
oracles (CONFLICT2/3_OK, CORRECT2/3_OK) confirm the revision protocol
behaved as designed at the fact level (original superseded, contradictory
superseded, resolved live). The downstream staleness is in the frozen
core's revision propagation, exercised identically by both binaries
(TREAT and CONTROL curves match rep for rep). No driver choice explains
it.

## Attack 5: the gate's refusal branch is still empirically unexercised

Carried over from CONTLEARN3: 0 MACHINERY_SKIPPED lines on all reps.
The structural enforcement (machinery refuses without a live proposal)
is in the instrument source but no run has exercised it. This lane did
not test it either. It remains a queued follow-up, not a claim.

## Attack 6: small-n and disclosed battery

LATE-NOVEL is n=2; the ordering-maintained claim at the longest horizon
rests on 2 ordered pairs (plus the 6 NOVEL pairs). The battery is
disclosed, not sealed adversarial; the subset conflicts were designed by
the lane worker, not an adversary. No generality claim is made; the claim
bound (machinery-enabled citation, no L3, fixed proposal template) is
unchanged from CONTLEARN3.

## Attack 7: does anything here contradict CONTLEARN3?

No. CONTLEARN3's battery had no subset conflicts on the chains'
licensing facts (its conflict/correction pair was on a side fact,
26001/541), so its 12/12 reuse result stands uncontradicted. The LH
result refines it: reuse survives unrelated interference at 3 volumes and
side-fact conflicts; it changes (deterministically, via live revision)
under direct conflicting evidence on the composition's own licensing
facts.

## Red-team bottom line

The experiment is BUILD-FAIL for the as-frozen sustained-retention claim
(LH-DEGRADED per the decision rule), but the failure is the informative
kind: it localizes to a precise, reproducible property of the frozen
revision operator (single downstream propagation on contradiction, none
on correction), not to capacity, ordering, citation integrity, or the
proposal-gate instrument. The recommended next hypothesis is a
correction-propagation design (does a second downstream revision fire
when the contradicted node is itself superseded?), tested against the
same frozen oracles, with no new modes, bridges, or handlers.
