# H5R2 Synthesis: four gate verdicts for the debate

Lane H5R2-SYNTH, wave-20261001-2321pdt. Pure synthesis; no experiments,
no code. Toolchain guard: safebin PATH, `which python3` printed
nothing (NAMECHECK.md Step 0). Sources are the four H5R2 lanes'
committed EVAL files; read only, unchanged here.

## The four verdicts, in one table

| Lane | Verdict | Core result |
|---|---|---|
| H5R2-BASELINE | BASELINE-MATCHES | Recency (REVERT-TO-LATEST) matches H5R2 on all 5 bars (36/36, 12/12, 24/24, 8/8, 24/24); CB-2 violated; gate not shown necessary by 4 sealed worlds |
| H5R2-DECOY | DECOY-DISCRIMINATES | H5R2 8/8 D ok; recency anchors to the decoy 8/8; gate shown necessary vs recency |
| H5R2-SKEPTIC2 | SKEPTIC-SURVIVES | NEWEST-LIVE-ON-KEY matches H5R2 8/8 on chained decoys with byte-identical stdout; gate necessity unproven vs the stronger skeptic |
| H5R2-SKEPTIC3 | SEPARATED | On re-teach families H5R2 anchors to the older live fact 8/8 (SEP-OLD) while NEWEST wins 8/8 (SEP-NEW); pre-registered favored arm: NEWEST |

## The arc

The four lanes tell one coherent story, not four independent ones.

BASELINE-MATCHES opened with a negative: on the four sealed worlds
(C families for W0/W2R/B2R, W3 families), preferring the most
recently created facts reproduced the full H5R2 five-bar vector.
Recency explained the battery as well as the gate, because on those
worlds the newest fact happened to be the live one. The gate looked
indistinguishable from a cheap heuristic.

DECOY-DISCRIMINATES closed that gap against recency. On worlds where a
decoy OBSERVE on another key makes a dead fact the newest while the
correct live fact is older, H5R2 anchors every revert MAP to the live
fact (8/8) while REVERT-TO-LATEST anchors to the decoy on 8/8. The
gate is necessary against recency; the baseline-lane match was an
artifact of the battery, not of the gate.

SKEPTIC-SURVIVES then replaced the skeptic. The decoy lane
recommended a stronger adversary, and it arrived: NEWEST-LIVE-ON-KEY,
which rejects decoys (liveness) and, per chain-link key, takes the
newest live fact. On the chained decoy family (decoys at both chain
levels) it matched H5R2 8/8 with byte-identical full stdout on both
worlds. The gate beat recency, no-gate, and chance, but not the
per-key newest-live heuristic. Necessity was still unproven.

SEPARATED finally discriminated the two. The skeptic2 lane asked
whether two live facts could ever sit on one key (normally
contradiction supersedes, leaving one); the answer is yes via a
re-teach path that does not trigger supersession. On that separator
family, with two live tag-1 non-superseded facts on K (F_old with
c_old, F_new with c_new), the gate anchors the re-derived MAP to the
older live teaching (SEP-OLD 8/8) and the skeptic to the newest live
teaching (SEP-NEW 8/8). Under the standard belief-revision reading
(the second teach is an update without contradiction, and the
protocol's own contradiction behavior leaves the newest fact live),
NEWEST-LIVE-ON-KEY is the pre-registered favored arm. The gate's
oldest-first pick is a creation-order artifact of forward node-id
enumeration, not a provenance principle: both facts are live, so the
gate's own "a superseded fact licenses nothing" rule cannot
discriminate them. On a re-teach, the gate re-derives from stale
knowledge.

## What t2_prov_ok IS

A stale-provenance gate, defined precisely by the four lanes:

- A candidate-verification filter at the four t2_trial promote sites
  (chain, count, single-hop, sum paths). The H5R2 base enumerates
  candidates in forward node-id order and the gate licenses only
  candidates whose licensing facts are live tag-1 and non-superseded;
  the first verifying candidate in node-id order is promoted.
- It is a filter, not a repair. Against the killed H5R failure it does
  one thing: it refuses to anchor DEP edges of re-derived MAPs to
  superseded or dead facts, while the old code anchored to them. All
  observed behavioral bars (values, counts) are identical with or
  without it; every observed failure of every alternative arm is
  provenance-only (W2R-DEP-FAIL, D-DECOY-FAIL, CD-DEP-FAIL), and the
  lane evals report D-ANS / VAL bars intact on all arms.
- What it demonstrably buys over the weaker alternatives: it beats
  recency on decoy worlds (8/8 vs 0/8 D ok), beats no-gate on all
  revert provenance bars, and beats chance.

## What t2_prov_ok IS NOT

Not uniquely correct.

- NEWEST-LIVE-ON-KEY is a viable alternative promotion policy:
  identical to H5R2 on the four baseline worlds (via the recency lane,
  since recency equals H5R2 there), on the decoy family it agrees with
  H5R2 (the live fact is the newest live fact on its key), on the
  chained decoy family it is byte-identical to H5R2, and on the
  separator family it is strictly favored by pre-registered protocol
  (8/8 SEP-NEW under the update reading of re-teach).
- The gate's oldest-first behavior has no independent justification in
  the lanes' evidence. No lane shows a world where picking the older
  live fact over the newer live fact is the correct policy. Its
  oldest-first direction comes from forward node-id enumeration
  order, which is an implementation artifact, not a stated provenance
  principle.
- Honest costs on record for the alternatives (baseline lane): pure
  recency regresses the substrate's built-in battery to 45/46 (F2
  masked-query disambiguation breaks), while H5R2 holds 46/46. The
  newest-live-on-key skeptic was not scored against the built-in
  battery in these lanes; that is an open measurement.

## The precise open question

Is there a gate strictly stronger than both: the provenance filter
(live, non-superseded licensing facts) combined with newest-live
tie-breaking among all verifying candidates, i.e. newest-live among
all live licensing facts rather than oldest-first or per-key newest?

This is a concrete, buildable, testable next hypothesis. The
separator family discriminates exactly the tie-breaking axis
(creation-order-first vs newest-live) while holding the provenance
filter fixed. A newest-live-among-all-live gate would need to show:
SEP-NEW 8/8 on the re-teach family, D ok 8/8 on the decoy family, CD
ok 8/8 on the chained family, the full baseline five-bar vector, and
46/46 on the built-in battery. None of the four lanes built it; the
debate should decide whether it is the next build or whether a
stronger discriminator exists first.

## The debate question

Does SEPARATED undermine H5R2's BUILD-PASS, or does BUILD-PASS stand
within its scope?

The evidence for scope-standing: BUILD-PASS was awarded against the
frozen KB-W2R/KB-W3 families (KB-W0 36/36, KB-W2R 12/12, KB-B2R
24/24, KB-W3 8/8, KB-B3 24/24, KB-D1 3/3 x4), and REPRO-PASS confirmed
it. On every frozen family, the gate's promoted candidate coincides
with NEWEST-LIVE-ON-KEY's (the baseline lane, the decoy lane, and
the chained lane all show agreement). The re-teach separator family
was constructed by a later lane precisely to break that coincidence;
it lies outside the frozen battery's event sequences (the battery
never leaves two live facts on one key). Under frozen-bar discipline,
a verdict names the exact bars that governed it; SEPARATED does not
retroactively move the H5R2 bars.

The evidence against scope-standing: the H5R2 claim, as the debate
group reads it, is that t2_prov_ok is the correct provenance policy,
and SEPARATED shows the gate's tie-breaking direction is an artifact
that fails the protocol's own revision semantics on a constructible
event sequence. If the claim's scope is "stale provenance is fixed",
the re-teach world is a genuine counterexample inside that scope:
the gate re-derives from stale knowledge there.

The debate must decide which scope the BUILD-PASS claim owns. The
synthesis does not decide it; it bounds it: whatever the ruling,
the next gate (if any) must pass the union of the frozen families and
the separator family, or the scope must be explicitly and publicly
narrowed with the re-teach gap named as a known open gap.

## Caveats and honesty notes

- A process incident in SKEPTIC2: its implementation commit swept
  unrelated staged deletions and landed on tnn-native-lab instead of
  the lane branch; two lanes restored files in follow-up commits and
  a lane audit is verifying the rest. The lane reports its own sealed
  evaluation unaffected (all sources hash-verified before assembly)
  and its lane files intact. Noted here so the debate knows; it does
  not touch the separator verdict, which is on clean ordering.
- Determinism: every lane reports 3/3 byte-identical full-stdout runs
  per arm per world, with recorded SHA-256 hashes in each EVAL file.
- Every arm failure observed across the four lanes is provenance-only;
  value bars (D-ANS, VAL) are 8/8 on all arms in every lane. The gate
  dispute is entirely about which fact a MAP's DEP edges anchor to,
  never about answers.
