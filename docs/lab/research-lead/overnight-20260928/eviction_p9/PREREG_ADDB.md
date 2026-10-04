# PREREG ADDB -- SCALING-EVICT continuation: a control that never ran, a consequence key, and a sublinear probe

Frozen BEFORE any code in this addendum is written and BEFORE any run under it.
Base for this continuation: `lane/eviction` @ 3b9797fc5 (which recovered the
aborted attempt's REPORT.md, C542-C554). Steps 1 and 2 of the mission (20k Q1
root cause; namespace invariant battery) are DONE and are not re-opened here.

Frozen fixtures, kill bars and limits are as written below. Where a prediction
fails, it is reported as failed.

---

## 0. THE FINDING THAT MOTIVATES THIS ADDENDUM: THE LRU CONTROL NEVER RAN

C554 reported K4 INCONCLUSIVE because "the LRU-by-oldest-id control produced
numbers identical to the structural policy". Reading the code, that identity is
not a property of the policies. It is a **harness defect**, found before any new
experiment:

`e11_setup` decodes the policy as
```
if((mode&32)==32){pol=2;}     // bit5 -> LRU control
if((mode&8)==8){pol=1;}       // bit3 -> fast structural  (OVERWRITES bit5)
```
`k4_lru40k` was launched with `mode 45` = 32+8+5. Both bits are set, bit3 is
tested last, so `pol=1`. **The control ran the fast policy.** The two logs
`out/k4_lru40k.log` and `out/k4_fast40k.log` are identical because they are the
same run, twice.

**Consequence for the record: the C554 K4 verdict "INCONCLUSIVE as a policy
discriminator" is not supported. The control was never executed, so the test
never discriminated anything, and the reason was a bit-decode bug rather than
policy equivalence.** C554's *other* conclusions are unaffected and stand: the
answer facts were reclaimed, `downstream_ans=-2`, and the frozen key is in-degree.

**K9 (this addendum) -- fix the decode and run the control.** New bit 6 (64) =
LRU control; bit 3 (8) = fast structural; if both are set the run is a
PROCESS-FAIL, not a result. Preregistered prediction, from the mechanism and
before the run:

> The foundational MAP nodes are allocated FIRST and therefore hold the LOWEST
> ids in the arena. `evict_lru` picks the lowest-id eligible node and never looks
> at bid. Therefore the LRU control **will kill foundational MAP nodes first**,
> `E11FOUND total_survived` will be **0 of 6**, and `downstream_ans` will be
> wrong. Kill bar K9a: `total_survived < 6` under LRU. If LRU also scores 6/6
> the decode is still wrong and K9 stays FAIL.

**K9b -- the answer-fact question is separate and must be reported separately.**
Under LRU the answer facts also die. Under the fast policy they also died in
C554. A consequence term (K10) is therefore required regardless of K9.

---

## 1. K10 -- A CONSEQUENCE (DEPENDENCY) TERM, NOT AN AGE TERM

Charter 32 forbids optimising only LRU/LFU/frequency/age. Charter 168 requires
reclamation to act on meaningful structure and to keep foundational structure
whose consequences justify it.

**The measured defect (C553/C554), restated precisely.** `bid_ref(n)` is an
IN-DEGREE: `evcount(n,1)+evcount(n,2)+evcount(n,6)+evcount(n,7)-evcount(n,3)`.
Every MAP carries its own type-2 and type-6 self-edges, so every MAP sits at
bid 2. The MAP's **answer fact** is the head of the MAP's promoted graph; nothing
cites it, so it sits at bid **0**, strictly below every MAP. Min-bid therefore
ranks the load-bearing answer of old foundational structure as the cheapest
object in the arena. In-degree is a proxy for load-bearingness that is exactly
WRONG for the one object whose loss actually destroys an answer.

**The frozen signal that does not depend on age, frequency or bid: ownership.**
`own_get(c)` names the MAP that exclusively owns cell `c` (set by `own_add` from
`promote_graph`; `-1` = unowned, `-2` = shared/released). If cell `c` dies and
its owner is still live, the owner's graph is damaged and the owner can lose an
answer. That is a downstream-consequence statement. It is orthogonal to age, to
access frequency, and to bid.

**Frozen primary rule (PRIMARY, an eligibility refinement, not a new key):**
> A cell `c` whose owner `o = own_get(c)` satisfies `o >= 2`, `o < NN`,
> `ng(o,36)==1` (o is live) and `ng(o,0)==20` (o is a MAP), and whose owner is
> **cited at least once** by a live node (`bid(o) >= 3`; a MAP's baseline bid is
> exactly 2, so `bid(o) >= 3` is precisely "cited at least once"), is **not a
> reclamation victim**. It is dropped from the victim index and counted by a new
> counter.

The threshold is 3 and not something tuned to the fixture: 3 is the bid of a MAP
that has been cited once, derived from the fact that a MAP's self-edges
contribute exactly 2.

**Why an eligibility refinement and not a key term.** It is O(1) per cell
(`own_get` and `bid_get` are both hash-slot reads), it needs no fixpoint
propagation, and it leaves `bid_ref == bid_fast` untouched so the K1/C553 kill
bar on the bid counters still means something. The alternative (adding
`LB_W * bid(owner)` into the bucket key) is preregistered as the ABLATION, with
no prediction attached, and is only run if the primary passes.

**Preregistered predictions, K10:**
* K10a: `E11FACTS ansfact_live = 6 of 6` (all six foundational answer facts
  survive). **Kill bar.**
* K10b: `E11JF downstream_ans = 7000`, `ok=1`. **Kill bar.** (C554 measured
  `-2`.)
* K10c: `evict_FOUND` (counter 86, a tag-20 victim whose subject is in
  20000..60000, i.e. a JUNK MAP) becomes **nonzero** under the MAP-only
  victim set (K12), proving junk MAPs and not foundational MAPs are what dies.
* K10d: the number of evictions at fixed JF must not drop by more than 2x
  versus the unprotected run. If protection starves the arena and evictions
  collapse, protection is too broad and K10 FAILS.
* K10e: the charter-32 RECENT-JUNK-vs-OLD-FOUNDATIONAL comparison must now be a
  REAL comparison: junk retention is measured as before and reported as
  uninformative (junk MAPs are built broken), while the foundational answer is
  the loss measure. No single blended "forgetting score" is reported (C552).

**Explicitly NOT claimed:** that protected cells are the *only* meaningful
structure, or that ownership is the complete notion of consequence. It is one
O(1) consequence signal, and its adequacy is exactly what K10 measures.

---

## 2. K11 -- `sel_fast`'s PER-EVICTION O(NN) PROBE (the K2 cost model, FAILED at C554)

`sel_fast` finds the lowest-set-bit at/after the allocator cursor in the
current-bucket bitmap `E_BMC` by a **linear walk over all 262144 ids**, and
charges it unconditionally: `paddv(W,823,262144)`. At 9337 evictions that is
2.4e9 probes. This is why the K4 runs TIMEOUT at 600 s and why K2's amortized
O(1) cost model is reported FAILED.

**Frozen fix (structural, no change to the selected victim):** maintain a
one-level summary bitmap `E_BMS` (4096 bytes) in which bit `j` of summary byte
`i` is set iff bitmap byte `i` of `E_BMC` is nonzero, updated at the single
generic mutators `bms`/`bmx`/`bmz` when the target base is `E_BMC`, so no call
site can be missed. Lowest-set-bit-at/after `cur` is then found by at most 8
summary-bit probes inside the summary byte, at most 8 bitmap-bit probes inside
the located byte, and one wrap-around byte.

**Preregistered kill bars, K11:**
* K11a **EQUIVALENCE**: on the same world, the victim sequence of the new
  `sel_fast` is identical, element for element, to the linear `sel_fast`
  (retained as `sel_fast_ref` and run in the same process). Any divergence is a
  FAIL, not a tolerance.
* K11b probes charged per eviction (`823` / evictions) **< 100**.
* K11c `E11JF` identical to K10's run in every field except the probe counters
  and wall time. Any answer difference is a FAIL.
* K11d: because K11 changes only the probe path, `bid_ref == bid_fast` must
  still hold at all six foundational MAPs (the K1 kill bar).

---

## 3. K12 -- ATOMIC STRUCTURAL RECLAMATION, EXERCISED FOR THE FIRST TIME

C554 recorded `reclaimed=0` and stated that shared-subgraph protection "was
never exercised at scale and is NOT CLAIMED", because **no MAP was ever a
victim**: at mode 13 the minimum bid is 0 and ~9337 non-MAP cells sit at bid 0,
so they are all consumed before any MAP at bid >= 2 is reached.

**Frozen trigger.** `pset(W,122,1)` (mode bit 4 = 16) restricts the victim set
to tag-20 nodes ONLY. Junk MAPs sit at bid 2 and foundational MAPs at
bid 6224-6226, so the junk MAPs become the victims and `do_evict` ->
`reclaim_map` runs. This is the first configuration in which the structural
reclamation path executes at all.

**Preregistered kill bars, K12 (all must hold, else K12 FAILS):**
* K12a `reclaimed` (counter 830) **> 0** -- atomic structural reclamation ran.
* K12b `E11JF downstream_ans = 7000` after the junk MAPs' structures are
  reclaimed: reclaiming junk must not damage foundational structure. This is the
  shared-subgraph test -- each junk MAP cites a foundational MAP with a type-1
  edge, and `reclaim_one` must SKIP anything not exclusively owned
  (`own_get(c) != m`) and anything with a live referent count
  (`ing(1..3,6,7,12) > 0`).
* K12c `E11FOUND total_survived = 6 of 6` and `ansfact_live = 6 of 6`.
* K12d **version history survives**: `nontag_HISTORY` (counter for reclaimed
  history-class nodes) must be **0**. Charter requirement from the mission.
* K12e **cycles terminate**: the run must reach its dump. `reclaim_one` walks
  the ownership chain with the `E_VIS` bitmap and a bounded queue (65536); a
  cyclic ownership/edge shape must not hang. A TIMEOUT here is a FAIL.
* K12f **no corruption**: `idxmode_lost = 0`, `classid_ok = 1`, the namespace
  battery reports 0 violations, and the run ends with `E11END`.
* K12g **reclamation cost** is reported: counter 830 (cells reclaimed),
  825/826 (kill and edge-delete events), 827/828 (skips: still-referenced,
  shared), and wall seconds.
* K12h **reconstruction cost, predictive usefulness, composition usefulness,
  uniqueness of evidence, revision relevance** are reported after reclamation
  (`E11MEAS`) and compared to the pre-reclamation values, so the cost of what was
  reclaimed is visible rather than asserted.

---

## 4. RUNS, LIMITS AND DISCIPLINE

All runs through `tnnwatch.sh` with the limit fixed HERE, not after seeing a
miss. `setsid` does not exist on this host, so every launch is detached via
`wrun.sh` (nohup+disown) and never left in the foreground.

| run | command | limit |
|---|---|---|
| `j_selref` | `./e11p ./e11_prof_v2 2000 13 4 2000` (K11a equivalence + K9/K10 at small scale) | 300 s |
| `j_k9lru` | policy=Lru via bit6, `2000 junk` | 300 s |
| `j_k10` | policy=fast + consequence term, `2000 junk` | 300 s |
| `j_k12` | policy=fast + consequence term + MAP-only victims (bit4), `2000 junk` | 300 s |
| `j_k12lru`| as `j_k12` but policy=Lru (the control that must lose) | 300 s |
| `j_reg_*` | canonical regressions D=1000/5000/10000/20000, mode 13 | 200/250/300/400 s |

The K4 world is first run at **JF=2000**, not 40000. Rationale: 40000 junk
TIMEOUTs at 600 s and two prior runs of this lane died there. 2000 completes in
seconds and answers the same questions; scale is a separate, later step and a
timeout at 40000 will be recorded as a timeout, not re-run longer.

**Determinism:** 3/3 byte-identical stdout per configuration via `zbuild.sh
--rep 3` or an equivalent 3-run sha comparison. Non-determinism is a FAIL.

**Correctness beats speed.** If the fast policy and the frozen scan disagree on
any answer, the frozen scan wins and the run is reported as a correctness
regression regardless of speed.

**Process-fail conditions** (recorded as FAIL, not as results): a policy-select
decode that resolves to two policies at once; `idxmode_lost != 0`; namespace
violations != 0; missing `E11END`; zero-byte output.
