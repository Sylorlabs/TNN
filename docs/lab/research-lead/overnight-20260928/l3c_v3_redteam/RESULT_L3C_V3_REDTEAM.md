# RESULT: L3C v3 Independent Red Team (L3C-V3-REDTEAM-SURVIVES)

Date: 2026-09-30. Target: L3C-V3-PASS (commit 3bfa0947c). Sealed plan:
ATTACK_PLAN.md (committed alone as f63d36e3a, strictly before any attack
code). Method: the attack harness reuses the committed mechanism
(l3c_v3.zag lines 1-1115) byte-verbatim, cmp-verified identical, with only
the main() test worlds replaced by adversarial ones.

## Verdict

L3C-V3-REDTEAM-SURVIVES. All four attacks executed against the committed
mechanism. Three attacks confirm the claim (A, C, D). Attack B's frozen
prediction missed because of a flaw in the attack design, not the
mechanism: the direct path fired incrementally and produced a correct
structure. A clearly-labeled supplementary probe (B2, post-hoc, outside
the frozen predictions) then confirmed the minimality criterion genuinely
discriminates on the cover path. The claim stands; the red team did not
break it.

## Attack A: three-element disjunction (sig 801) -- SURVIVES

World: out=0 iff f1==1 OR f1==5 OR f2==9. Observed: HONEST_FAIL x4,
BUILT_COVER sig=801 ncover=3, truth_eval 6/6, all structure checks pass
(DISP, 3 labeled edges with atoms (1,0,1),(1,0,5),(2,0,9) all targeting
TERM(0), 1 default edge targeting TERM(2), rep natoms=3). Matches the
frozen predictions exactly. Cover-set composition generalizes beyond the
two-element F2 case with no new machinery.

## Attack B: minimality on a genuine cover path (sig 802) -- PREDICTION
MISSED, MECHANISM CORRECT

Frozen prediction: HONEST_FAIL x6 then BUILT_COVER ncover=2 at clash_n=8.
Observed: BUILT sig=802 natoms=1 at clash_n=2, then REFINE sig=802 edge=4
natoms=1 a0=(2,0,9); built_delta=2, unresolved_delta=0, truth_eval 4/4.

Cause (attack-design flaw, disclosed): the frozen analysis forgot that
disc2 runs incrementally at every clash. At clash_n=2 only rows R1,R2 had
been seen, and (f1==1) covers both with zero target matches, so the
direct path fired immediately; later refinement added (f2==9). The
mechanism built a correct two-level chain expressing (f1==1) OR (f2==9)
with 4/4 truth eval. The prediction was wrong; the mechanism was right.
This mirrors the builder's own P4 miss in reverse. The bar was not moved:
recorded as an attack-design miss.

## Supplementary probe B2: minimality confirmed on the cover path
(sig 804) -- CONFIRMED (post-hoc, outside frozen predictions)

To actually force the cover path, rows were reordered
R1,R3,R2,R4,R1,R3,R2,R4 so no single atom ever covers all rows seen so
far. Observed: HONEST_FAIL x2 (clash_n=2,3), BUILT_COVER sig=804
ncover=2 at clash_n=4, truth_eval 4/4, all structure checks pass (DISP, 2
labeled edges (1,0,1),(2,0,9) to TERM(0), default to TERM(2), rep
natoms=2).

Note: the cover fired at clash_n=4, not clash_n=8 as a naive analysis
would expect, because EVID_MIN counts rows and one atom already covers
two distinct rows. The unique minimal cover {(f1==1),(f2==9)} beat the
larger corroborated covers ({A,G,H}, {B,E,F}, {E,F,G,H}). Minimality
genuinely discriminates among multi-atom covers on the cover path. The
builder's open item from the P4 miss is now closed by this probe.

## Attack C: hidden OR-case source audit -- SURVIVES

(1) Full diff of v3 against committed v2 source (20705ab5a): the only
additions are scratch-buffer definitions, bit utilities
(popcnt/bitset/bitor), candidate/mask helpers, disc_cover (generic
subset-enumeration set cover over the existing atom vocabulary),
build_cover (one DISP node, one labeled edge per cover atom, existing ops
only), emit_cover_amb, the two control-flow fallback branches, and test
helpers plus the new main. No branch anywhere is conditioned on cover
size, atom count, or disjunction-shaped structure. The "first" cover
recorded is first-in-subset-enumeration-order among equal-size minimal
covers: deterministic, not disjunction-specific.
(2) Independent re-verification of the interpreter-diff claim: featv,
pred_match, select_edge, interp, trace_last_edge, path_uses extracted
from both sources with shell tools and diffed: all six byte-identical.
No hidden OR case exists in builder logic or interpreter.

## Attack D: ambiguity generalization to k=3 (sig 803) -- SURVIVES

World with exactly 3 distinct minimal covers. Observed: HONEST_FAIL x4,
AMBIGUOUS_COVER sig=803 k=3, built_delta=0, ambig_delta=1, rule(803)
still TERM(2) with ambig field = 3. Matches the frozen predictions
exactly. Ambiguity counting generalizes beyond the tested k=2; no
withhold-by-fiat, no silent choice.

## Determinism and purity

rt1/rt2/rt3 byte-identical (sha256
da9bbac49cf6762231d16e61f4d6d2b6fe12d9948c63125ea769aaf632177ddf);
B2 runs byte-identical 2/2. Zero Python anywhere. Dash-clean per
check_no_dash.sh. Contaminated paper untouched (0 diff lines).

## Kill bars

K1: PASS. Sealed plan f63d36e3a strictly precedes all attack code
(sequential commits on the same branch; merge-base verified below).
K2: PASS with one disclosed attack-design miss (B). The harness mechanism
region is cmp-verified byte-identical to committed l3c_v3.zag lines
1-1115; all four attacks plus the supplementary probe executed against
it; every result recorded honestly against the frozen predictions, with
the B miss and the post-hoc B2 status explicitly labeled.
K3: PASS. Pure Zag + shell; dash-clean; contaminated paper untouched.

## Architecture note (ONE-SYSTEM RULE)

No new mechanism was needed to survive this red team. The attacks
confirm the v3 machinery is the general operation it claims to be:
3-element disjunctions compose, minimality discriminates, ambiguity
counts honestly, and no disjunction-specific case hides in the builder.
Ceiling remains bounded L2, as claimed.
