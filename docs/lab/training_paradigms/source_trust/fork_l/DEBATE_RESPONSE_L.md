# Fork L — Response to DEBATE_SOURCETRUST.md §9 must-address items

Frozen debate record: `DEBATE_SOURCETRUST.md` (committed e2dec8bc, 2026-09-23).
This document answers the six Fork-L items in §9, the §8 placement question,
the Q5 candidate-law tension, and the Q4 identity assumption. It adds no new
mechanism; the build spec (`BUILD_SPEC_L.md`) and `fork_l.zag` are unchanged.
Where this document is stricter than the build spec, the stricter reading wins
for honesty; where it conflicts, the frozen spec governs the build.

## L-1. Classified constant inventory (anti-knob criterion, §7 Q2)

A parameter is a knob iff it embodies a human's theory of how trust should work
in a place TNN cannot revise. Inventory of every constant in the update path:

**Substrate-general (not knobs):**
- `L_A = 1`, `L_B = 1` — symmetric Laplace pseudocounts. Arithmetic of memory
  (smoothing), not a theory of trust. Symmetric by construction: no designer
  ranking of good vs. bad prior weight.
- Fixed-point scale `1000` — integer scaling, no semantic content.
- Ring capacities (1024 outcomes/source, 64 key slots/source, 16384-claim ring,
  2048-entry world table, 64 sources) — bounded-memory management. Declared
  caveat: at scales where rings wrap, truncation behaves like implicit recency
  weighting. That is a capacity effect, not a tuned decay, but it is real and
  the battery should probe it.
- Episode boundaries — one `decide` call / one `st_world` call is one episode.
  Interface granularity, not trust theory.
- OOB input (src_id outside 0..63) → WITHHOLD. Fail-safe input validation,
  identical for every source, not a per-source rule.

**Structural, defended as not-a-knob (the load-bearing claim):**
- Regime truncation on PEND/MAL. This encodes "a refutation changes the theory
  of the source," which is uncomfortably close to a human trust theory — so
  here is the precise defense: the reset contains **no magnitude parameter**.
  The trust drop after the first caught lie (1000→333, or 900→333, or
  998→333 — always 333) is a pure consequence of applying the Laplace formula
  to the new regime, not a chosen betrayal penalty. There is no constant that
  says "how much betrayal should hurt." The debate's Q2 demands exactly this:
  "how much betrayal should hurt may not appear as a constant." It does not.
  The discontinuity is in the *structure* (which outcomes count), never in a
  tuned number. If the debate crew judges that the reset *event itself* is a
  trust theory, then Fork L concedes one structural knob and argues it is the
  minimum needed for the sleeper tripwire (L-4) — it is the tripwire, not a dial.

**Designer-authored grounding (declared, one level below dynamics):**
- The outcome taxonomy (OK / PEND / MAL / deleted) and its transitions
  (world-agreement→OK, world-disagreement→PEND, correction→expunge,
  defiance→MAL, vindication→OK). A human chose these evidence types. Defense:
  they are a theory of *evidence*, not of trust dynamics — they name what the
  world can tell us, with no rates, magnitudes, or recovery constants. The
  bootstrap (L-3) shows they are the trust-independent ground. A fuller
  endgame would put even this taxonomy under TNN's deliberate self-change
  (RC1 pattern); the frozen fork cannot.

**Decision-policy knobs (honestly labeled as knobs — they live in admission,
not in trust learning):**
- `L_TH = 900` — the admission cutoff. This IS a knob by the debate's
  criterion: it encodes a human judgment ("how much evidence before acting
  without corroboration") where TNN cannot revise it. Defense is positional,
  not substantive: the frozen `decide → 0/1/2` interface *requires* a decision
  rule, and a decision rule requires a cutoff (Sol-A's "action requires a
  decision statistic"). The trust *value* is knob-free; the *verdict mapping*
  is not. In the endgame this cutoff moves under TNN's control or dissolves
  into scrutiny budgeting (see "Merge notes").
- Support quorum `2` (two established independent asserters admit a tainted
  claim) — decision-policy constant, knob-adjacent. It encodes "one
  independent confirmation is not enough." Minimal non-trivial corroboration;
  declared, not derived.
- Contradiction → WITHHOLD (never REJECT without world evidence) — decision
  policy, defended under the trust-vs-truth law (below).

## L-2. Behavioral initial policy (the "no initial value" claim)

Declared: an unseen source is admitted **0% of the time on reputation alone**.
Fresh trust is 500 < 900, so a novel claim from a source with no record
WITHHOLDs. Admission for newcomers happens only via trust-independent paths:
world-agreement (INSTALL) or two established independent asserters (INSTALL).
X=0%, Y={world-confirmed claims, independently-corroborated claims}.
Defense: this is the non-circular bootstrap — a source with no evidence about
it cannot admit on its own reputation because it has none. Under Sybil it is
the pessimistic-but-not-paralyzing setting: newcomers can contribute (their
claims are judged on corroboration, not identity) but cannot self-admit.
Per Sol-A's accepted challenge, this *is* the initial trust policy, stated
behaviorally rather than as a stored number.

## L-3. The bootstrap, solved explicitly

The trust-independent verdicts that train the dynamics are exactly the world
episodes, and only the world episodes:
- world-agreement → OK outcome (trust-independent: uses no trust value).
- world-disagreement → PEND outcome (trust-independent).
- correction (source restates the world value) → expunge; defiance (source
  restates the refuted claim) → MAL; vindication (world re-confirms a refuted
  claim) → OK.
Corroboration-based admissions deliberately do NOT mint trust outcomes —
admitting "two established sources said it" as evidence *for* a third source
would train trust on trust (the circularity the debate's AGAINST-L case
names). The one asymmetry: world episodes mint outcomes for every source with
a claim on that key, including sources whose claims were WITHHELD — withheld
does not mean wrong, and the world is allowed to prove it.

## L-4. The sleeper tripwire (discontinuity, not gradient)

Mechanism: the outcome ring scan recomputes the regime from scratch on every
query and stops at the most recent MAL/PEND. A world-disagreement appends one
PEND; every outcome before it leaves the trust computation *immediately and
completely*. Arithmetic proof of discontinuity: a source with 500 straight OKs
has trust 1000·501/502 = 998; after one caught lie the regime is [PEND] and
trust is 1000·1/3 = 333. The drop 998→333 does not depend on history length —
there is no gradient to be smooth about. The source's *theory* changes in one
event (PEND = "currently refuted, presumed resolvable"), which is the
structural tripwire the debate demands. What it is not (honest limit): the
fork does not distinguish the three sleeper kinds (one-off error / changed
circumstance / revealed long con) at trip time — one-off error vs. long con
is disambiguated only by what happens next (correction expunges; defiance
escalates to MAL; silence leaves the PEND standing). The *retroactive* half
of the sleeper requirement is not built (see Placement).

## L-5. Table vs. learned function; Sybil

Fork L is a **per-source table**, stated explicitly in the build spec. It
therefore claims **zero Sybil resistance** and accepts K's Sybil analysis in
full: under costless identities the attacker mints infinite fresh 500-trust
identities; the fork's only defenses are (a) 500 < 900, so sockpuppets cannot
self-admit, and (b) corroboration requires two *established* asserters. Known
hole, declared: an attacker can farm a sockpuppet to 900 by telling the world
8 confirmable truths, then spend it on one lie — the per-identity sleeper,
which the tripwire catches exactly once per identity, at the cost of one
admitted lie. L-as-learned-function-over-behavioral-features (the debate's
only Sybil-resistant variant) is not built; building it would be a different
fork. **Identity assumption (Q4):** `src_id` is a stable, opaque, costless
identifier; distinct ids are treated as independent sources; there is no
burst/coordination detection and no identity cost. A battery Sybil leg run
under these assumptions tests *identity*, not trust — all forks fail it
identically, and it must be labeled as such per §9.

## L-6. What distinguishes L from S-with-a-cache

The record behind the scalar does real work in the hard cases (regime
structure, PEND vs. MAL, correction/defiance/vindication transitions) — so
the "scalar is theater" charge has teeth, and here is the answer: Fork L is
honestly closer to **K-with-learned-dynamics** than to S. What distinguishes
it from S-with-a-cache: (a) the admission path never walks the record — it
reads the O(1) scalar; the record serves audit and the trust recomputation,
not per-decision deliberation; (b) the record is a fixed-schema per-source
tally, not a provenance graph — there are no cross-source edges, no
corroboration links, no burst patterns, no backward walk. S preserves *shape*
(which claim supported which, who copied whom); L preserves only per-source
outcome sequences. What distinguishes it from K: no hand-set value, no
trust-theory magnitudes anywhere in the update path (no learning rate, no
betrayal penalty, no recovery constant, no decay), and the dynamics are
structured so TNN could revise them (the only frozen trust value permitted is
an audited human force-pin, per standing law).

## Placement (§8): where the record lives; the retroactive gap

In this fork: the track record lives in `ForkHist` (substrate-adjacent
memory, passed to the admission entry); `decide` is called at the PAM
admission gate; `st_world` is the world's write path. Which organ revises the
update dynamics? Currently none — the fork is frozen code. In the endgame,
the source-trust organ owns both the record and the dynamics, and TNN's
deliberate self-change (RC1 pattern: 100% of reasoning machinery, 0% of
constitution) is the revision mechanism. **The retroactive gap, stated
plainly:** when the sleeper betrays at episode 501, Fork L clamps future
admissions (trust 998→333) but does NOT re-examine the 500 previously
installed claims. Retroactive re-valuation is unsupported by the
representation — there is no claim→source backward index in the admission
path (the claim ring exists but is append-only and not walked). This is the
fork's largest concession to S, and the merge fixes it (below).

## Q5 candidate law: "trust allocates verification effort, never verdicts"

Tension, honestly stated: **Fork L as built violates the candidate law as
stated.** `trust ≥ 900 → INSTALL` lets source trust determine a verdict on a
claim. Three mitigations are real but partial: (1) low trust never REJECTs —
rejection requires world evidence, so distrust cannot veto; (2) high trust
never INSTALLs a world-contradicted claim; (3) WITHHOLD is the middle verdict
and functions as "needs scrutiny." But the core stands: within the frozen
0/1/2 interface there is no scrutiny output, so the fork *cannot* implement
the law — the interface forces compression of scrutiny advice into the
verdict. The compliant behavior the law wants (distrusted-source truth with
corroboration installs on the corroboration) IS implemented: tainted claims
with two established asserters INSTALL and the asserters' trust is untouched.
Full compliance requires an interface change: a scrutiny/effort output
alongside the verdict. Noted as merge change 1.

## Merge notes: where L+S-with-K-as-cache changes this design

1. **Scrutiny output.** `decide` gains a verification-effort signal; the
   scalar becomes advice to the PAM gate ("how much scrutiny for this claim
   from this source"), and INSTALL is decided by evidence. `L_TH` dissolves
   into budgeted scrutiny — the one labeled knob leaves the design.
2. **Provenance links + retroactive walk.** The per-source tally gains S's
   claim-level edges (which claims corroborated which, cross-source links);
   the PEND tripwire fires the backward re-examination the debate requires.
   The regime-reset stays as the fast clamp; the walk is the slow
   understanding.
3. **K as explicitly-labeled cache.** The `1000·(ok+1)/(tot+2)` formula
   becomes the memoized readout over the organ's record, invalidated on
   regime change — cache, never truth. This answers L-6 permanently.
4. **Malice-vs-error representation.** The outcome taxonomy gains intent
   verdicts from the FL2/lie-detection line (PEND/MAL already separate
   presumed-refuted from defiant; "honest-but-wrong" needs an explicit
   intent judgment the fork does not make). No single scalar carries it.
5. **Learned-function extension (optional, honestly labeled as a new fork).**
   Trust as a function over behavioral features (burst, copy-patterns,
   stake behavior) is the only path to Sybil resistance; the table cannot
   get there.

## What a merge would NOT change

The world-anchored bootstrap (only trust-independent training signal); the
no-circularity rule (corroboration never mints trust outcomes); source-
symmetric initialization with a declared 0% reputation-only admission
policy; the magnitude-free tripwire (no betrayal-penalty constant, ever);
deterministic byte-identical reruns with zero RNG in the decision path.
