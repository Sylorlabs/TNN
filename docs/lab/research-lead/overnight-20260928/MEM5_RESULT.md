# MEM5_RESULT: H-MEM5 Builder Report

**Date:** 2026-09-29
**Verdict: H-MEM5 SURVIVES 4/4.**
**Frozen prereg:** `PREREG_MEM5.md` (commit `df6a56fd4`), strictly before
any implementation or execution (verified: prereg commit is an ancestor
of the implementation and result commits; no amendments).
**Target:** the H-MEM4 red-team downgrade (`MEM4_ADV_RESULT.md`):
X-M4-2a (grace-window harm) and X-M4-2b (fig-leaf merit).
**Raw evidence:** `MEM5_RAW_OUTPUT.txt` (md5
`2888f9331dae55f802055ec65e9101fb`, 3 runs byte-identical via cmp)
**Implementation:** `mem5_learn.zag` (delta vs `mem4_learn.zag`: R4
substantive merit threshold only; R1/R3 untouched).
**Pure Zag. No Python in fixtures, implementation, build, execution,
analysis, or editing.**

## Hypothesis

H-MEM5: protection is earned solely by demonstrated merit
(uses >= MERITK = 2) and never granted by age alone (no absolute
grace). This closes the X-M4-2a grace-window harm and the X-M4-2b
fig-leaf merit harm at the `elig()` level while preserving every
surviving H-MEM4 claim.

## Methodology

1. Read the red-team report (`MEM4_ADV_RESULT.md`), the H-MEM4 prereg
   (`PREREG_MEM4.md`), the adversary prereg (`PREREG_MEM4_ADV.md`), and
   the full `mem4_learn.zag` source.
2. Hand-derived the R4 `elig()` rewrite and all new fixture arithmetic
   (F-M5-1, F-M5-2, F-M5-3a, F-M5-3b, F-M5-3c) before freezing.
3. Validated in /tmp scratch (pure Zag, never committed): (a) an
   elig-change-only build of `mem4_learn.zag` was diffed against the
   frozen `MEM4_RAW_OUTPUT.txt` (md5
   `7921b0f4bc917d9ccb3627aa41d1ca97`); the only stdout differences
   were the fallback section and the K-M4-1b section, both intended
   supersessions; (b) the four new fixtures executed in scratch
   reproduced the frozen expectations on first run with no fixture
   tuning.
4. Froze `PREREG_MEM5.md` (commit `df6a56fd4`) before any
   implementation.
5. Implemented `mem5_learn.zag` by copying `mem4_learn.zag` and applying
   exactly the preregistered delta: header comment, `GRACE()` removed
   and `MERITK()=2` added, `elig()` rewritten, fallback fixture
   replaced (F-M5-3c), K-M4-1b section replaced (F-M5-3a) plus
   `setup_flip2` and the F-M5-3b section, new F-M5-1 and F-M5-2
   sections. No other source lines changed.
6. Built with `znc mem5_learn.zag -o /tmp/mem5_bin`; ran 3x;
   byte-identical via cmp; exit code 0 on all runs; 0 FAIL lines.

## Mechanism delta (R4)

```zag
fn MERITK()i32 { return 2; }
fn elig(W:[]u8, ST:[]u8, s:i32, use_prot:i32)i32 {
  if(st_used(W,s)==0){ return 0; }
  if(use_prot==1){
    if(st_seq(ST)<st_prot(W,s)){
      if(st_uses(W,s)>=MERITK()){ return 0; }
      return 1;
    }
  }
  return 1;
}
```

Within the age window, a slot is protected iff uses >= 2. A newcomer
with 0 or 1 queries is evictable from the moment it is stored. The
`GRACE()` constant is removed. Rationale for k=2 (authored,
disclosed): one query is not evidence of merit (probe, misroute,
noise); two queries are the smallest substantive signal; k=2 is the
minimal threshold satisfying the red team's stated requirement
(k > 1).

## Bar results

### K-M5-1 (grace-window harm closed; X-M4-2a): PASS

Frozen fixture F-M5-1 (slot7: proc7, uses=0, age=2; slots 0..6:
uses 10..70; 20-query window with proc7 absent). Observed:

```
harm-2a: wprot=LFU vprot=slot7 wun=LFU vun=slot7 cprot=0
  [full counterfactual] protected: LFU victim=slot7(proc7) | unprotected: LFU victim=slot7(proc7)
  [selected-policy] protected-victim=slot7 unprotected-victim=slot7
  CHURN-FULL:0 (winner stable at LFU; eviction unchanged)
K-M5-1 PASS: grace-window harm closed; protected LFU evicts the meritless newcomer at cost 0
```

Every frozen value matches: wprot=LFU, vprot=slot7, wun=LFU,
vun=slot7, cprot=0, verdict 0. The X-M4-2a harm (protected LIFO
evicts proc6 at cost 2 while unprotected LFU evicts proc7 at cost 0)
does not occur. Under H-MEM4 the same fixture produced wprot=LIFO,
vprot=slot6, cost 2 (per `MEM4_ADV_RESULT.md`).

### K-M5-2 (fig-leaf merit closed; X-M4-2b): PASS

Frozen fixture F-M5-2 (slot7: proc7, uses=1, one stale query outside
the 20-query window, age=3, prot=112). Observed:

```
harm-2b: wprot=LFU vprot=slot7 wun=LFU vun=slot7 cprot=0
  [full counterfactual] protected: LFU victim=slot7(proc7) | unprotected: LFU victim=slot7(proc7)
  [selected-policy] protected-victim=slot7 unprotected-victim=slot7
  CHURN-FULL:0 (winner stable at LFU; eviction unchanged)
K-M5-2 PASS: fig-leaf harm closed; protected LFU evicts the uses=1 newcomer at cost 0
```

Every frozen value matches. The X-M4-2b harm does not occur behind
the single stale query of merit.

### K-M5-3 (preserved and superseded bars): PASS

(a) K-M4-1a (F1): PASS. At ev1 pre-pressure wprot=LFU, wun=LFU,
vprot=slot7, vun=slot7, cprot=0; pressure(ev=1) selects LFU, evicts
slot7(proc8, uses=0) at cost 0; has_proc(8)==0, has_proc(0)==1,
has_proc(9)==1. Unchanged from H-MEM4.

(b) K-M4-1b SUPERSEDED by F-M5-3a: PASS. On the frozen setup_flip
state: `flip state: wprot=LFU vprot=slot7 wun=LFU vun=slot7`,
churn_verdict=0, print "CHURN-FULL:0 (winner stable at LFU; eviction
unchanged)". The old expectation (wprot=FIFO, vprot=slot0, wun=LFU,
vun=slot7, verdict 1) relied on the grace protection that H-MEM5
removes; the frozen fixture now documents that the grace-window flip
no longer occurs.

(c) New F-M5-3b (setup_flip2, slot7 uses=2): PASS. `flip2 state:
wprot=FIFO vprot=slot0 wun=LRU vun=slot7`, churn_verdict=1, print
"CHURN-FULL:1 (winner flips FIFO->LRU; eviction
slot0(proc0)->slot7(proc7))". The :1 path is preserved under the new
rule, and the merit-positive slot's protection is load-bearing
(without it the protected winner would be LRU, not FIFO).

(d) Preserved bars: all PASS, behavior unchanged from the frozen
H-MEM4 output. K-M4-2 (meritless newcomer evicted at cost 0; queried
procedure survives); K-M4-3a (adversarial future explicitly detected
and excluded, selected LFU, victim proc5, return 2); K-M4-3b
(old dist_differs=1, new dist_differs2=0 on the single-query flip);
K-M3-1 ev1 (LRU, slot6(proc6)/slot6(proc6), CHURN-FULL:0) and ev2
(LFU, slot4(proc4)/slot6(proc9), CHURN-FULL:1); K-M2-3 (5 strict
selections); K-M2-5 (band {20,25,30} agrees and is strict at
A2/B2/C2); the flat fixture reports ties. Scratch differential
confirmed: on every builder stream, every slot within its protection
window at a selection event has uses >= 2 or an expired window, so no
eligible set changed.

(e) K-M3-4 fallback SUPERSEDED by F-M5-3c: PASS. Hand-built
all-merit-protected state (8 slots uses=2, seq=100 < prot=108, Q=20x
proc7): FALLBACK-ALL-PROTECTED emitted, fbf flag=1, fbsel=LFU
(unprotected tie-break), proc8 stored at slot0, no crash. The old
0-query fixture is no longer all-protected under the new rule
(uses=0 < MERITK makes every slot evictable), so it cannot
demonstrate the fallback path; the new fixture does.

### K-M5-4 (deterministic): PASS

Three consecutive runs of `/tmp/mem5_bin` produce byte-identical
stdout (cmp clean on all pairs); md5
`2888f9331dae55f802055ec65e9101fb`; exit code 0 on all runs; 0 FAIL
lines; final line "ALL BARS PASS".

## Causal interpretation

Both downgrade attacks are closed at the mechanism level, not by
fixture exclusion. The X-M4-2a harm required absolute protection of
a uses=0 newcomer; the X-M4-2b harm required protection on uses=1.
H-MEM5 removes both preconditions: `elig()` no longer has any
age-only protection branch, and the merit gate is uses >= 2. On both
frozen attack fixtures the protected outcome now coincides exactly
with the unprotected outcome (same winner LFU, same victim slot7,
same cost 0), so there is no protection-induced harm to report and
the CHURN-FULL:0 verdict is outcome-honest.

The closure is narrow and honest: it covers uses in {0,1}. A
newcomer with uses >= 2 is still protected (F-M5-3b proves the
protection is real and load-bearing), including the disclosed
stale-merit residual (uses >= 2 from ancient queries with no recent
queries remains protected; no recency weighting). That residual is a
new hypothesis (H-MEM6), not a defect in this one's bars.

Regression analysis: the elig-change-only scratch diff against the
frozen H-MEM4 output shows the new rule changes nothing on any
builder stream (A2/B2/C2, F1, F3/F4, flat). The only behavioral
changes are the two intended supersessions (fallback fixture,
K-M4-1b flip). This is strong evidence the threshold raise from
uses>0 to uses>=2 plus grace removal is surgical: it touches exactly
the harm class and nothing else.

## Classification

Bounded L2 experience-driven policy selection with substantive-merit
newcomer protection (no age-based grace), outcome-level churn
verdicts, and explicit adversarial-future detection, on
researcher-designed skewed-popularity streams. Explicitly not L3,
not policy-form invention (the menu is still authored), not
representational invention.

## Remaining limits (carried forward and new)

1. The candidate menu, window band, and constants (PROB=10,
   MERITK=2, L1MIN=6, strict-majority target threshold) are authored.
2. MERITK=2 is the minimal substantive threshold; stale merit
   (uses >= 2 from ancient queries) remains protected. No recency
   weighting (H-MEM6 material).
3. A newcomer is evictable until it demonstrates merit (2 queries); a
   procedure that would earn its queries just after a pressure event
   can churn first. Protection is earned, not granted.
4. Futures are researcher-frozen; adversarial futures are detected
   and excluded, not defeated.
5. Strictness is a (mechanism, skewed-regime) property; flat
   workloads degenerate to ties, reported honestly.
6. The adversarial-target screen is strict-majority; sub-majority
   targeting is missed (disclosed boundary, confirmed by X-M4-3).
7. Not integrated into the unified learner.

## Governance disclosures

- Prereg commit `df6a56fd4` strictly precedes the implementation and
  result commits; no amendments were made.
- Fixture arithmetic was hand-derived first, then validated in /tmp
  scratch (pure Zag, never committed) before the freeze; the four new
  fixtures reproduced the frozen expectations on first execution
  with no tuning.
- The implementation was produced by copying `mem4_learn.zag` and
  applying exactly the preregistered delta; no other source lines
  were changed (verified by review of the edit list).
- No Python was used at any stage: not in fixtures, implementation,
  build, execution, analysis, or file editing (edits were made with
  the file-editing tool; builds with `znc`; runs, diffs, and checks
  with shell builtins and coreutils only).
- Determinism: 3/3 byte-identical runs (cmp); exit code 0 on all
  runs.
- Supersessions are explicit and do not retroactively alter frozen
  verdicts: H-MEM4's 5/5 SURVIVES and its DOWNGRADED red-team verdict
  stand as executed; K-M4-1b and the K-M3-4 fixture expectations are
  superseded for H-MEM5 only, with the old fixtures retained in
  source (`setup_flip` unchanged) and their new outcomes documented.
- The red-team downgrade is addressed, not erased: X-M4-2a and X-M4-2b
  are closed on their exact frozen fixtures, and the closure is
  demonstrated inside the builder's own binary.

## Commit lineage

- `df6a56fd4` Prereg: H-MEM5 FROZEN (this prereg, alone).
- Implementation + `MEM5_RAW_OUTPUT.txt` + this report: committed
  next (see log).
- Baseline: `9b98d1fa9` (H-MEM4 SURVIVES 5/5);
  `afde4144c` (H-MEM4 red-team DOWNGRADED).

## Verdict

**H-MEM5 SURVIVES 4/4.** The H-MEM4 red-team downgrade is addressed:
the grace-window harm and the fig-leaf merit harm are closed at the
mechanism level on their exact frozen fixtures, with all surviving
H-MEM4 claims preserved and the two necessary supersessions made
explicit.
