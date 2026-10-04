# PREREG ERRATA -- FREEZE-ARENA-1 (FA1)

Claim block **C560-C562**. Committed ALONE, after PREREG.md (22a015c1e) and
**before any FA1 implementation line is written**. No prediction (P1-P11) and no
kill bar (K1-K12) is weakened or removed. Each entry below fixes a defect
that makes the preregistered text either unsatisfiable or self-contradictory,
and each names the authority it defers to.

---

## E1. LK7's midpoint memory clause is unsatisfiable as written; the suffix form replaces it

PREREG §6 LK7 and kill bar **K12** require, at the midpoint of each stage
(after `floor(n_s/2)` episodes of that stage), that **learner-memory purity
still be 0**, i.e. that **no cell of `L` or `LT` holds a relation id belonging
to stage `s`**.

That is false by construction for any stage whose first `floor(n_s/2)` facts
already mention the relation. Stage A is the proof: facts 0..25 are
`(10..17,101,20)`, `(10..17,102,30)` and `(10..14,103,40)`; after those 26
episodes the learner's RET/VFY/CNT coverage arrays and its functional-arity
store legitimately hold `101`, `102`, `103`, and `104`. K12 as written is
therefore unattainable at stages A, B, C, D, E, G and H, and honouring it would
void the whole run for a bookkeeping reason.

**Replaced, same intent, strictly checkable.** The property LK7 actually
exists to test is *no knowledge of facts that have not yet been delivered*.
The implemented midpoint memory test is:

> for every relation id `r` of stage `s` whose **first occurrence inside stage
> `s`** is at fact index `>= floor(n_s/2)`, count the cells of `L` and `LT`
> holding `r`. Frozen expectation **0**.

A relation whose first occurrence is inside the delivered prefix may and will
be in memory; a relation whose first occurrence is inside the undelivered
suffix must be absent, or something leaked. Stage A midpoint (m=26) then tests
`105`, `106`, `107` (first indices 29, 37, 42); stage F midpoint (m=8) tests
`305` (first index 8). The **arena** clause of LK7 is unchanged and exact:
`floor(n_s/2)` triples present at the midpoint, in FROZEN.

K12 is therefore read as: midpoint arena count `== floor(n_s/2)` exactly at all
8 midpoints, **and** midpoint suffix-memory count `== 0` at all 8.

## E2. `FRESH0`'s arena: PREREG §7 and PREREG §11 disagree under the freeze

PREREG §7 defines `FRESH0` as "learner cloned from the zero state, zero
episodes, **arena as the arm's arena is at that moment**". Under the FROZEN arm
that hands the zero-experience learner an arena that the *lifetime* learner's
episodes wrote -- i.e. it re-introduces through the baseline the very leak the
freeze removes. PREREG §11, which the prereg itself declares authoritative
("The scientific question is answered by one comparison, fixed here"), defines
the same row as "FROZEN-FRESH0 (**identical arena-construction rule, zero
episodes**)". Same rule with zero episodes means an empty arena.

**Both rows are measured in both arms; §11's is primary.**

| row | learner | arena | role |
|---|---|---|---|
| `FRESH0` | zero state | its own arena, built by the arm's construction rule, **zero episodes** | the §11 adjudication comparison |
| `FRESH_ARENA` | zero state | the arm's arena at that moment, handed over | reproduces C500-R1's published `FRESH0` row exactly, so the LIVE arm stays numerically comparable to `09a09548...` |

In the LIVE arm `FRESH0` and `FRESH_ARENA` differ only in that `FRESH0`'s
arena is empty; in the FROZEN arm `FRESH_ARENA` is explicitly reported as
**leak-contaminated for a zero-experience learner** and is not used for the
verdict. This adds a measurement; it moves no bar.

## E3. Stage F's episode stream is split around its goal, and the TTC target at F is stated

PREREG §3 fixes the two `w_stageF_ext` facts as the last two episodes of stage F
"AFTER F's goal has been answered and after the snapshot clone". Consequences
that the prereg left implicit, now pinned before implementation:

* MAIN: stage F delivers **14** episodes, `GF` is queried and scored against
  `lt_decl(4)`, then the **2** extension episodes are delivered, then the
  snapshot for the F-arm baselines is taken.
* LIVE arm: `frz_fill` at F's entry copies the **14** `w_stageF` facts only.
  The two extension facts reach the LIVE arena through their own episodes
  (`frz_add` is append-if-absent and is called on every episode in **both**
  arms), which is what keeps the arms' arenas element-wise equal (K8) while
  preserving the post-query extension that `ABL-SNAPSTALE` depends on.
* TTC at stage `s=5` is reported in two parts, both measured:
  `TTC-F-pre` = episodes to criterion for `GF`/`lt_decl(4)` over the 14
  `w_stageF` episodes (query after each of episodes 0..13), and
  `TTC-F-post` = the two further queries for `GF`/`lt_decl(9)` after the two
  extension episodes. LK6 requires `TTC-F-pre > 0`.

No bar changes: P2's "FROZEN TTC > 0 at A,B,C,D,F,G" is read on `TTC-F-pre`.

## E4. Facts about the implementation that the prereg already fixes

Recorded so that the report cannot be read as having chosen them later:

* the only arena writer is `frz_add(A,subj,rel,obj)` (append-if-absent); its
  only call site is inside `frz_episode`, immediately before the frozen
  observation step that consumes the same fact. `frz_fill` is the LIVE-only
  stage-entry prefill and appends from the **same** scratch arena the episodes
  read from, so arm content is identical by construction, not by assertion.
* scratch arena `AS` is built per stage by calling the unmodified
  `w_stageX(AS)`; the episodes of stage `s` read triple `k` of `AS`.
* `L` (16384 B) + `LT` (8192 B) are allocated once per arm and threaded
  unchanged; `frz_episode` and `lt_query` are the only two entry points into
  the learner.