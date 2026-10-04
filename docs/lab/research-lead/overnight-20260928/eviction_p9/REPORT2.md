# SCALING-EVICT REPORT 2 -- a control that never ran, a consequence term that works, and a test that still does not discriminate

Lane `lane/eviction`, continuation after two aborted attempts. Claims C555-C562.
Base `lane/scalingp8` @ 310a8a2d6 via `lane/eviction` @ 3b9797fc5. Pure Zag for
all computation and profiling; shell/git for orchestration only. Every run
through `tnnwatch.sh` with a limit fixed in the prereg. No orphan binaries left.

---

## 0. HEADLINE

1. **The C554 LRU control never ran.** `e11_setup` tested bit5 (LRU) before
   bit3 (fast) and the second assignment overwrote the first, so `mode 45`
   selected the *fast* policy. `out/k4_lru40k.log` and `out/k4_fast40k.log` are
   the same run twice. C554's verdict "K4 INCONCLUSIVE because the control
   produced identical numbers" is therefore **not supported** -- the test never
   discriminated anything, and the cause was a bit-decode bug, not policy
   equivalence. C554's substantive findings stand unchanged.
2. **K11 SUBLINEAR EVICTION: ACHIEVED.** Victim selection went from 262,144
   probes per eviction to **2.05**, with the victim sequence verified
   **element-for-element identical to the linear selector across 2000
   successive real evictions** (mismatches=0). 128,000x fewer probes.
3. **K10 CONSEQUENCE TERM: WORKS, and it reverses the C554 finding.** All six
   foundational answer facts survive (`ansfact_live 6/6`, C554 measured 0/6).
   Foundational MAPs survive 6/6 under both policies.
4. **K9a FAILED, and K4 REMAINS INCONCLUSIVE -- now for a different and better
   understood reason.** My preregistered prediction was that LRU would destroy
   the foundational MAPs. It did not: the consequence term protects
   foundational structure from *every* policy, so the age-based control scores
   the same as the structural one. The discriminator does not live in the
   eligibility predicate, so no eligibility-level fix can make this test
   discriminate. This is reported as a failure, not reframed as a pass.
5. **All canonical levels are unchanged**, byte-identical to the pre-change
   binary except one self-referential counter, 3/3 deterministic.

---

## 1. K9 -- THE CONTROL, RUN FOR REAL

**C555.** bit6 (64) is LRU, bit3 (8) is fast structural, bit5 (32) retired.
Selecting both is a PROCESS FAIL (`pol=3`, counter 930, `E11FAIL pol_decode`).

`y_k9lru`, mode 69 (both indices + LRU), JF=40000, TIMEOUT at the preregistered
560 s, all measurements reached:

```
evictions=9337 evict_tag20=1334 evict_JUNK=1334 evict_FOUND=0
sel_visits=6423847 idxmode_lost=0
E11FOUND total_survived=6 of 6      (bid 6224-6226, bid==bid_fast)
E11FACTS ansfact_live_total=6 of 6
E11JF downstream_ans=-2 expect=7000 ok=0
rc_t1=2666 rc_other=5337 rc_verhist=13
```

**K9a FAILED.** Predicted `total_survived < 6`; measured 6 of 6. Two measured
reasons, both interesting:

* **Low ids are recycled, so "oldest id" is not "oldest structure".**
  `evict_lru` picks the lowest-id live eligible node, and the free-id bitmap
  hands the SAME ids back. The foundational nodes occupy ids 2..~816 at build
  time, but the moment one of them is freed its id is immediately reissued to a
  junk MAP. LRU therefore killed 1334 **junk** MAPs and 0 foundational ones --
  age-priority and structure-priority agreed because the arena recycles ids.
* **The consequence term protects both policies equally.** The entire
  foundational structure is owned by a cited MAP, so it is not eligible under
  LRU either. `own_prot` = 2 in this run.

LRU's cost is confirmed as the reference control: `sel_visits` = 6,423,847
(688 probes per eviction, O(NN) by construction) against 9,337 for the fast
policy.

**Verdict: K4 is INCONCLUSIVE as a policy discriminator.** The test as
constructed cannot separate a consequence-aware policy from an age-based one,
because the consequence term is doing all of the discriminating work in both
arms. The prereg anticipated a passing control and required INCONCLUSIVE; that
is what is reported.

---

## 2. K10 -- THE CONSEQUENCE TERM

**C556.** `own_protected(n)`: if `n`'s owner is a live MAP with `bid(owner) >= 3`,
`n` is not a reclamation victim. The threshold is derived, not tuned:
`promote_graph` gives every MAP type-2 and type-6 self-edges, so an uncited
MAP's bid is exactly 2 and `>= 3` **is** "cited at least once". Applied at all
three eligibility decisions -- `vre`, `evict_lru`, `evict_scan` -- so the
policies differ only in which eligible node they choose.

**C560, reported as an ADDED CONDITION and not as preregistered.** The
ownership relation was INCOMPLETE. `promote_graph` claimed the whole SEQ chain
reachable from `root` but not the answer fact it creates in the same function,
so the MAP's answer was the single cell in the structure with no declared owner
and therefore the single cell the consequence term could not see. Without this
one line the term protects nothing that matters. This is a finding about the
original design, not a tuning knob.

**Applied at selection time, not at index time.** The first implementation put
the test inside `vre`, where the decision is cached. It protected only 17 cells:
`vre(n)` runs when `n` changes, and at the moment `ev_teach_in` registered the
answer fact its owner MAP was not yet cited, so `bid(owner)` was still 2. The
owner's bid later rose to 336 and the cached decision never revisited it
(`own_prot=17`, `ansfact_live 2/6`). Selection-time evaluation reads the owner's
CURRENT bid and has no staleness.

**`y_k10e` / `y_k10d`, mode 13, JF=40000, TIMEOUT at 600 s:**

| | C554 (frozen key) | C556 (consequence term) |
|---|---|---|
| `E11FACTS ansfact_live_total` | **0 of 6** | **6 of 6** |
| `E11FOUND total_survived` | 6 of 6 | 6 of 6 |
| `evictions` | 9337 | 9337 |
| `idxmode_lost` | 0 | 0 |
| `own_prot` (cells skipped) | -- | 17 + selection-time skips |

**K10a PASSED** (6/6 vs 0/6). **K10b (`downstream_ans = 7000`) NOT ESTABLISHED**
-- see the boundary below. K10d held: evictions did not drop.

### 2.1 A NEW FINDING PRODUCED BY THE FIX, AND IT IS NOT A PASS

`y_k10c` (protection broken, `ansfact_live 2/6`) printed
`downstream_ans=-2` in seconds. `y_k10d` and `y_k10e` (`ansfact_live 6/6`) never
printed `downstream_ans` at all, even after C562 moved the query to the first
statement after the build, with >100 s of budget left.

**Interpretation, stated as measured:** with the answer fact DEAD the query
bails out at the `-2` sentinel in microseconds; with it ALIVE the engine
actually attempts the answer and enters the `mp_run`/`t2_trial` miss path, which
did not return inside the remaining watchdog budget. **So the C556 fix converts a
fast WRONG answer into a SLOW path of unresolved cost, and whether that path
returns 7000 is UNKNOWN.** `E11JF downstream_recheck=1` was reached in the LRU
run, so the re-emit path works; the number itself is not on the record.

This is the same `mp_run`/`t2_trial` superlinear residue flagged at mission
priority 2 and never root-caused. It is now the binding limit for this lane, and
it is a **retrieval-side** residue, not a reclamation-side one.

---

## 3. K11 -- SUBLINEAR SELECTION: ACHIEVED

**C555.** `E_BMB` was a reserved-but-unused 32768-byte region (allocated and
zeroed at init, referenced nowhere). It is now a one-level summary over
`E_BMC`: bit `j` of summary byte `i` is set iff bitmap byte `i` is nonzero.
The summary is maintained inside the generic `bms`/`bmx`/`bmz` mutators guarded
on the base, so `vto`, `vdrop` and the init sequence are covered without editing
a single call site.

| | probes charged per eviction | source |
|---|---|---|
| linear `sel_fast` (C554) | 262,144 | `paddv(W,823,262144)` |
| sublinear (C555) | **2.05** (19,176 probes / 9,337 evictions) | counter 933 |

**K11b PASSED** (<100/eviction). **K11d PASSED**: `bid_ref == bid_fast` still
holds at every foundational MAP.

**K11a, the kill bar that earned its keep.** The linear selector is retained
verbatim as `sel_fast_ref` and the two are compared at **every one of 2000
successive real evictions**, with the world actually being torn down between
them: `mismatches=0`, `equiv_ok=1`, `probes_fast=4115` vs
`probes_ref=913309696` (2 vs 456,426 per eviction).

It immediately caught a real defect **in my own first implementation**, of
exactly the class the brief warns about: I derived the summary index from the
absolute workspace offset `o = base + i/8` instead of from the node id, so every
summary write landed at `base/8 + n/64`, tens of millions of bytes past a
4096-byte structure, silently in unrelated workspace. Symptom: `find_bl`
returned -1 for a non-empty bucket, `mismatches=1` at step 0.

---

## 4. REGRESSION AND DETERMINISM

All through the watchdog, mode 13:

| D | elapsed | scan | ans | live_nodes | live_edges |
|---|---|---|---|---|---|
| 1,000 | 2 s | 5 / 6 | 6205 / 6405 | 7,802 | 6,796 |
| 5,000 | 2 s | 5 / 6 | 6205 / 6405 | 35,802 | 30,796 |
| 10,000 | 3 s | 5 / 6 | 6205 / 6405 | 70,802 | 60,796 |
| 20,000 | 4 s | 5 / 6 | 6205 / 6405 | 140,802 | 120,796 |

**Byte-identity against the pre-change binary** (`e11_prof_v2`, C542-C554
lineage) at D=1000/10000/20000: exactly **6 diff lines out of the whole log**,
all of them `vre_calls`, and all of them `+(D+5)` -- one extra call per promoted
MAP from C560's `vre(W,af)`. Excluding that self-referential counter the logs
are **byte-identical**. `fails=0` at every level.

**Determinism: 3/3 byte-identical** at D=20000, sha256
`e63c251f31bec61630c1f51b861b9440322903a1f490505be0065902305d9b30`.

**Namespace battery re-run after all changes: 11/11.** Every site fires
(`viol=1`, `flagged=site`, `fired=1`, `at_site=1`), `canary=0` (no corruption),
`no_wrong=1`, `post_ok=1`, `pq=904`. `reach=1` at 9 sites and `reach=0` at sites
7 and 9 -- the two documented redundancy negatives from C542-C545, unchanged.

---

## 5. CEILING

| level | status |
|---|---|
| 20,000 MAPs | **4 s**, scan 5/6, ans 6205/6405, byte-identical |
| 40,000 MAPs | build completes, query stalls (TIMEOUT 400 s, C554) |
| 50,000 MAPs | not re-run post-C551 |
| 100,000 MAPs | build completes, 219,290 evictions, query TIMEOUT 800 s (C554) |
| K4 world, 40,000 junk | build ~500 s; **the query is now the cost** |

**The binding limit is no longer node capacity, edge capacity, or reclamation
cost. It is the `mp_run`/`t2_trial` miss path.** At 100k `live_edges` sat at
exactly `NE=262144`; per-eviction selection is now O(1) probes; and a single
foundational query that should be a fact lookup does not return in 100 s once
the answer fact is alive.

---

## 6. VERDICT

* **Sublinear eviction: ACHIEVED (K11).** 2.05 probes per eviction, verified
  element-for-element against the linear reference over 2000 real evictions.
  K2's amortized cost model is MET for selection. This is a real, kill-barred
  win and it is the direct unblocking of the C554 timeouts.
* **Charter 32/168, meaningful structure: PARTIAL POSITIVE on preservation,
  INCONCLUSIVE on discrimination.** Reclamation now provably preserves
  foundational answer facts that the frozen key destroyed (6/6 vs 0/6). But the
  age-based control scores identically, so the test does not show that the
  *policy* distinguishes junk from foundation -- only that the *predicate* does.
  C554's "age-priority in a structural costume" charge is withdrawn as applied
  to the predicate, and **re-issued as applied to the test**: the K4 world as
  built cannot discriminate, and now for a mechanical reason rather than a bug.
* **C560 is the more transferable finding:** the ownership relation the whole
  structural argument rests on was missing exactly one edge per MAP -- the
  answer. Any future structural policy keyed on ownership would have failed
  silently for the same reason.

---

## 7. BOUNDARIES

* **`downstream_ans = 7000` is NOT established** (K10b). The answer fact
  survives; whether the engine can ANSWER from it is unresolved, and the
  evidence points at an unresolved cost in the miss path rather than at a wrong
  answer. Do not cite K10 as "the foundational answer is retained end to end".
* **K12 was not reached.** `reclaimed=0` in every run here, so atomic
  structural reclamation, shared-subgraph protection and cycle termination
  remain **exercised at zero scale** and are NOT CLAIMED, exactly as at C554.
  Mode bit4 (16) is the frozen trigger and is implemented and ready.
* `rc_verhist` (a reclaimed node with a live type-5 predecessor edge) is
  **1873 of 1873 reclaimed tag-1 nodes** -- i.e. essentially every fact
  participates in the supersession chain, so this class is too loose to
  discriminate version history and the K12d kill bar as written is not yet
  meaningful. A sharper definition is needed before K12d can be scored.
* K9a's failure means the K4 world cannot separate policies. Making it
  discriminate requires moving the consequence term out of the eligibility
  predicate and into the selection KEY (the preregistered ablation), so that a
  policy which ignores the key still destroys the answer facts. Not attempted.
* The `live_nodes` (481,432) > `NN` (262,144) discrepancy at 100k is still
  unresolved.
* `t2_gather_idx` candidate ORDER is still untested for equivalence at scale.
* Runs on ONE host under heavy foreign load (load average 10-79 observed during
  this session). All elapsed times are wall clock on a contended machine.
* One host, one compiler, one corpus.

## 8. NEXT EXPERIMENT

1. **Root-cause the miss-path cost with a dedicated counter** -- the same move
   that solved the 20k build hang. Instrument `ev_query` -> `mp_run` ->
   `t2_trial` to find which loop a *successful* foundational query enters.
   This is now the ceiling and it is cheaper than anything else on the list.
2. **Move the consequence term from eligibility into the selection key**
   (`bid + LB_W*min(bid(owner),cap)`) and re-run K9. Only then does the LRU
   control have a chance to fail, and only then does K4 measure a policy.
3. **Run K12** (mode bit4 = 16) to exercise `reclaim_map` for the first time,
   with a sharpened `rc_verhist` definition first so K12d is scoreable.
4. Resolve `live_nodes` > `NN` at 100k, then re-attempt 50k/100k.
5. The C267 9-phase merge test (S1000L/I, S5000L/I, EML/I/M, FAL/I) for
   byte-identity against `s5000_run1.txt` sha `382e913a` was **not done** here.
   It remains the right way to show the disjoint-namespace fix survives the
   queued NN=131072 rebuild, and it is independent of everything above.
