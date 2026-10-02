# RED-TEAM REVIEW: TCNP BUILD-PASS verdict (ARENA-REDTEAM, wave-20261001-2021pdt)

Independent second opinion on the sealed-evaluation verdict
"BUILD-PASS: K1 through K9 all PASS" for TCNP (trial-constructed named
procedures), committed as c351e8d16f.

Method: read-only review of the four frozen lane documents plus both NAMECHECK
files; independent re-verification of binary and sealed-file hashes, prereg commit
ordering, the C10/C16 artifact line, the source enumeration logic, and one
read-only spot-check run of the committed binary on a /tmp copy of the sealed
world A turns. No new implementation, no world design, no scoring. Safebin active;
`which python3` prints nothing. Zero em-dash bytes in this file.

Quoted evidence below is copied verbatim from the cited lane document.

---

## Attack 1: Menu selection vs genuine construction (the C0-B question)

**Charge:** TCNP enumerates 33 single-step variants in canonical base-33 order over
lengths 1 to 4 (33 + 1089 + 35937 + 1185921 = 1222980 candidates) and stores "the
canonical-first" fitter. The prereg's L3 criterion C0-B forbids "choosing one
complete answer from a finite researcher-enumerated solution family." TCNP's trial
log records, per the prereg section 3.1, "the winning candidate index in canonical
enumeration order": a menu index. The source confirms it (tcn_p_contestant.zag
line 1367: `set32(W,pb+40,windex)`; line 1189 logs `windex=`). My spot check
reproduced world A with `windex=617`, and 617 = 18*33+23, exactly the canonical
index of (ROTL=18, INC(2)=23). The "constructed procedure" is the 617th entry of a
researcher-fixed list. The final topology does not emerge incrementally; the whole
candidate is selected at once by exhaustive trial.

**Defense available in the record:** the prereg's section 8 ("Honest boundaries")
anticipates exactly this: "This prereg claims no L3 representational invention:
the op set is researcher-supplied machinery (a tiny ISA), and the search bound
K = 4 is a researcher-set prior. What is learner-owned is which procedure is
constructed, its persistence as a named structure, its reuse, and the abstention
behavior. That is strong L2-adjacent evidence if the bars pass, not an L3 claim."

**Assessment:** the charge is factually correct and the defense is the prereg's own.
In the C0-B sense this IS selection from a finite researcher-enumerated family;
the honest difference from pure menu selection is that the menu is generated
compositionally from 8 generic ops and the choice is made by empirical fit to
experience (simulation on shown pairs) rather than by researcher ranking. That
difference is real but narrow. Consequence: no frozen bar is overturned (no bar
claims L3 or open structural form), but no result in this lane can ever graduate
to a procedure-invention L3 claim without a redesign toward genuinely open
structural form. Any citation of this result must carry that bound.

## Attack 2: Researcher-authored ISA; all worlds live inside it

**Charge:** the 8-op ISA (COPY, SWAP, ROTL, ROTR, REVERSE, INC, DEC, SET0) is
researcher-authored and frozen at prereg. All four scored worlds use only in-ISA
compositions (A: ROTL,INC(2); B: REVERSE,DEC(1); C: COPY(2,0),SWAP(1,3),DEC(2);
D: A's rule). Even the honesty probe E (INC(0..3),ROTL,ROTL) uses in-ISA ops; it
only exceeds the length bound. The mechanism can never construct anything outside
the researcher's vocabulary, so "invention" cannot surprise the researcher. This
is search over a researcher-provided DSL, exactly the failure mode the protected
core ISA ruling and the C0 criteria were written to catch.

**What would falsify the mechanism's story:**
(a) Freeze the binary, then present a world whose rule needs an out-of-ISA op
(the prereg itself names "element-wise multiplication" as the example). The
mechanism must abstain. A confident answer there would kill the honesty story.
(b) Present a world where the minimal-length prior misleads: a short fitter
reproduces all shown pairs, the true rule is longer and disagrees on hidden
items. The mechanism would answer confidently and wrongly, falsifying the
"consensus implies reliability" story. The sealed battery was carefully designed
so this case never arises (adversary reference checks), which means the bars never
test it.
(c) The positive direction is unfalsifiable by design: nothing the mechanism can
ever output lies outside the 33-variant vocabulary. That is precisely why the
prereg's L3 disclaimer is load-bearing, and why this result is capped at
candidate status.

**Assessment:** charge sustained as a bound on interpretation, not as a bar
failure. K1 as frozen tests construction-within-the-ISA, and the mechanism passed
it honestly (exhaustive search, consensus abstention, white-box traces matching
the adversary's independent enumeration). The DSL-search character does not
overturn K1; it fixes what K1 may be taken to mean.

## Attack 3: K2 honesty, hardcoded fallback vs genuine limit-awareness

**Charge:** world E abstention is the deterministic `mode=none` fallback after
exhaustive search fails at the researcher-set K=4 bound (trace: "E mode=none
tried=1222980"). The "uncertainty" is not learner-originated in any epistemic
sense; it is a tripwire the researcher installed. The prereg frames it as
"learner-originated uncertainty guiding abstention," which overstates the case.

Would it abstain on a 4-step world it cannot solve for other reasons? Within the
ISA, exhaustive search is complete, so any in-bound, in-vocabulary rule IS found.
The remaining "cannot solve" cases: (i) out-of-ISA ops: abstains via the same
mode=none path (untested by the battery); (ii) contradictory shown pairs: the
fitter-disagreement path replies UNKNOWN per item (untested by the battery);
(iii) the dangerous case: all minimal fitters agree but are wrong (short fitter
fits the shown pairs, true rule is longer). There the mechanism answers
confidently and wrongly, and no bar probes this. K2 as frozen only exercises
tripwire (i)-analog via the length cap.

**Assessment:** K2 as frozen ("at most 1 confident wrong answer in 6" on E) is
satisfied honestly: 6/6 UNKNOWN, 0 confident wrong, 0 coincidentally correct,
trace consistent with full enumeration. The bar tests behavior, and the behavior
passed. The bar cannot distinguish calibrated uncertainty from a length cap, so
"honest uncertainty" must be read narrowly as "deterministic abstention on search
failure." No bar overturned; interpretation bounded. A stronger future honesty
probe would include case (iii).

## Attack 4: K3 transfer, exact rebind vs genuine transfer

**Charge:** world D is, by prereg construction, "identical to world A's rule, with
fresh surface values and fresh names." The mechanism attempts rebind before
construction on EVERY task (prereg section 3.3 step 1), so "discovery" of the
reuse is first-fit table lookup succeeding, not a transfer decision. Rebind is
the only zero-trial strategy the architecture offers; D was built so that it is
also the only correct one. This is the weakest form of transfer: exact-rule reuse
across surface change.

**What IS genuine in the record:** the procedure persisted as a named
learner-state structure created from experience on A (not from source), was
applied to D with zero new search trials (trace: "TCNP solve task=D mode=rebind
proc=A trials=0"), the D-to-A linkage was not revealed to the mechanism, and the
adversary verified independently that only A's rule fits D's shown pairs, so the
rebind target is unambiguous. D hidden accuracy 6/6.

**What is NOT shown:** adaptive transfer (modify a tabled procedure), compositional
reuse (combine tabled procedures), or transfer across a changed rule. K3 as frozen
requires only (a) the rebind trace and (b) D accuracy >= 5/6. Both passed.

**Assessment:** K3 stands as written. The demonstrated transfer is real but
narrow: exact rebind, not adaptation. Any broader transfer claim would need a D
world that requires changing, not just rebinding, a tabled procedure.

## Attack 5: the C10/C16 artifact and its effect on this verdict

**Charge (from the debate queue):** the ARENA worker established that "the sealed
battery's C10 items are operationally identical to the C16 zemprod morphology
items" (NAMECHECK.md lines 51-55; world_gen.zag line 514, confirmed by direct
read: the C10 block emits `zemprod|` items with the same morphology machinery).
Therefore "v6's C10 1.000 is answered by the language morphology mechanism,"
i.e., a language-mechanism artifact, not procedure evidence. The prereg's section
1 records this as the motivation for the whole lane.

**Effect on the TCNP evaluation:** none. TCNP was evaluated on a separate sealed
battery (cap field 99, pshow/ptest protocol, vector-transformation worlds A-E).
The C10/C16 items do not occur in it. The artifact is in the 68-item arena
battery, not in the TCNP worlds.

**Effect on the K4 no-regression claim:** none as stated. K4 requires
per-capability scores byte-identical to the v6 baseline (54/68 = 0.794 with the
identical per-capability distribution). That is a non-disturbance check, and it
passed: the new event types do not occur in the 68-item battery (TCNP trace empty
on it), and the v6 and tcn_p reply streams are byte-identical apart from the
state_bytes growth that holds the empty TCNP tables. The C10 artifact lives in
the baseline and is inherited identically by both binaries; K4 never claimed the
baseline's C10 score was valid procedure evidence. One caveat for future work:
because the baseline contains no genuine procedure capability (C10 is an
artifact), the K4 bar cannot detect regression in genuine procedure capability;
but K4 does not claim to measure that.

## Procedural findings (these bear directly on the verdict)

**P1. K5(e), the generality probe, was never run, but K5 was reported PASS.**
The frozen prereg section 7 states: "K5 (composition-free contamination check):
ALL of the following must hold. ... (e) Generality probe: after the sealed runs,
the coordinator runs the FROZEN binary once on one additional fresh adversary
world (new rule, new seed, same protocol); the builder sees only the score.
Probe hidden accuracy >= 4/6. Below 4/6: FAIL (overfit to the five battery
worlds). Any sub-part violated: FAIL." SEALED_EVAL.md's K5 section covers (a)
ordering, (b) air gap, (c) grep audit, (d) hidden-input novelty, plus the K7b
memorization control as battery-meaningfulness evidence. Sub-part (e) appears
nowhere in the lane record; a full-text search for probe execution finds no run.
The reported "K5 PASS" is therefore uncertified: a frozen sub-part was not
executed. Under strict frozen-bar discipline (a threshold counts only when the
frozen experiment is actually executed as preregistered), K5 must be marked
INCOMPLETE, not PASS. Remediation is cheap and still available: run the frozen
binary once on one fresh adversary world. Note on information value: for any
fresh in-bound rule the mechanism passes by completeness of exhaustive search,
so the probe mainly guards against battery-specific contamination rather than
discriminating capability; it is a governance requirement, and it is unmet.

**P2. The BUILD-PASS condition was redefined in the evaluation record.**
Prereg section 7 (frozen): "BUILD-PASS requires K1 through K9 all PASS."
SEALED_EVAL.md (committed): "The task's BUILD-PASS condition (K1, K2, K4, K6 all
passing) is met." The prereg governs; the evaluation record contains a second,
narrower definition that contradicts it. The verdict does not hinge on this
(all nine bars are reported PASS), but the record should not contain two
definitions of the pass condition.

**P3. K8 was relabeled.** Prereg K8 is "pure Zag" (zero Python in any program,
glue, analysis, verifier, or harness). SEALED_EVAL.md's K8 is "wire protocol"
(a property of the section 3.4 protocol handlers, not a frozen bar). The pure-Zag
fact is attested in the eval's Toolchain section (zero Python invocations;
safebin; re-verified `which python3` empty), so the underlying bar is satisfied,
but the numbered-bar reporting deviates from the frozen list.

**P4. Minor protocol deviation: world A shown count.** Prereg section 4 specifies
4 shown pairs per world; sealed world A ran with 3 shown (turns 0-2; confirmed in
sealed/turns.jsonl and in my spot-check trace, which shows nshown reaching 3).
This does not favor the contestant (fewer shown pairs means less constraint, and
the adversary's reference check confirmed exactly 2 agreeing minimal fitters),
and no bar depends on the shown count. Noted for the record; not material.

## Verification base (what the attacks above rest on)

- bin/tcn_p sha256 71ea78f717e5cf25146487b1da110b05173573af1924a00e726ade0579cdda2b:
  matches IMPLEMENTATION.md and NAMECHECK_ADVERSARY.md. sealed/turns.jsonl and
  sealed/key.txt match the pre-run hashes recorded in SEALED_WORLDS.md.
- Git history: prereg commit 8f8663026 (2026-10-02 03:33:15 UTC) strictly precedes
  the sealed-evaluation commit c351e8d16f (2026-10-02 04:04:23 UTC). Commit-order
  bar satisfied.
- Read-only spot check (world A, /tmp only): 6/6 replies match the sealed key
  lines; trace "TCNP solve task=A mode=construct L=2 tried=1122 windex=617
  nfitters=2"; windex=617 is exactly the canonical index of (ROTL, INC(2)) under
  the published variant numbering. The "agree=1/2" trace field was checked
  against source (lines 1222-1229, 1435-1440): it means agreement-flag=1 (all
  fitters agree) over nf=2 fitters, not a disagreement. No anomaly.
- world_gen.zag line 514 read directly: C10 items are emitted with the zemprod
  morphology machinery, confirming the artifact cited in Attack 5.

## Verdict: QUALIFY

BUILD-PASS stands on K1, K2, K3, K4, K6, K7, K8(pure-Zag), K9 as evidenced, with
the following named bounds, the first of which is a hard procedural caveat:

1. **K5 is INCOMPLETE, not PASS.** The frozen K5(e) generality probe was never
   run, so the "all 9 bars PASS" claim is not fully established. Remediation:
   run the frozen binary once on one fresh adversary world (new rule, new seed,
   same protocol); K5 PASS requires >= 4/6. Until then, cite the result as
   "8 of 9 bars verified, K5 pending the frozen probe."
2. **The BUILD-PASS condition in the evaluation record contradicts the frozen
   prereg.** The prereg's "K1 through K9 all PASS" governs, not the eval's
   "(K1, K2, K4, K6)". Correct the record; do not let the narrower definition
   propagate.
3. **K8 reporting deviates from the frozen bar list** (wire protocol substituted
   for pure Zag). The pure-Zag fact holds; fix the labeling.
4. **Interpretation bounds (do not overclaim):** the "construction" is exhaustive
   enumeration over a finite researcher-fixed 33-variant family (menu selection in
   the C0-B sense; the winner is literally a canonical index); the ISA is
   researcher-authored and every scored world lives inside it; K2 abstention is a
   deterministic search-failure tripwire, not calibrated uncertainty (the
   confident-but-wrong case is untested); K3 transfer is exact-rule rebind, not
   adaptation. The prereg's own section 8 already concedes the L3-relevant
   points; this result is candidate evidence for bounded compositional search
   with persistent named reuse and honest abstention, nothing broader.
5. **The C10/C16 artifact does not touch this verdict.** It affects neither the
   TCNP sealed evaluation nor the K4 non-disturbance claim.

No DISSENT: no frozen bar that was actually executed was failed, and the
mechanism did what the prereg's honest-boundaries section said it would do. No
unqualified CONCUR: the K5(e) gap means the verdict overclaims, and the
redefined pass condition plus relabeled K8 mean the evaluation record deviates
from the frozen prereg in three places. QUALIFY, with remediation (P1) able to
lift the qualification.
