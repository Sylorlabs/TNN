# H-UNIFIED9 Red Team Result: DOWNGRADED (3/3 attacks succeed; regression holds)

**Date:** 2026-09-30
**Adversary:** H-UNIFIED9 Red Team (independent subagent)
**Target:** H-UNIFIED9 SURVIVES (26/26), prereg `ecaa78494`, result `09bd9b933`
**Adversary prereg:** `7464cf28c` (committed alone before any fixture, build, or run; one em dash caught and amended out)
**Verdict: DOWNGRADED.** No kill bar fires. All three downgrade attacks succeed as preregistered. X-U9-4 regression holds fully.

## 1. Method

Pure Zag throughout: no Python at any stage. Toolchain
`/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`.
Builds and runs in `/tmp/u9adv` only; no binaries committed.

The adversary harness `u9_adv.zag` = lines 1..1503 of the committed
`unified9_learn.zag` blob (commit `09bd9b933`, md5
`89d424426f6797ae2b8c3e60c2d576dc`), cmp-verified byte-identical, plus an
adversary-written `main()` containing only X-U9-1..X-U9-3 and a self-check.
Zero mechanism edits. Single `fn main()` at line 1522 of the harness.

Episode strings for parameterized attacks were built by `adv_ep(s0, eff)`,
which writes the 10 bytes of `"s0,0,0>0,eff"` (10<=s0<=99) into a fresh
`z_alloc` buffer and returns a length-10 slice. Self-check:
`streq(adv_ep(72,1),"72,0,0>0,1")==1` and `streq(adv_ep(60,7),"60,0,0>0,7")==1`,
PASS.

The adversary binary was run 3 times; all outputs byte-identical
(md5 `67871213f8b341fe143a6915ea94fc0e`). Exit code 0 every run.

X-U9-4 (regression) was executed at shell level: the committed
`unified9_learn.zag` compiled unmodified, run 3 times, outputs compared
byte-for-byte against each other and against the committed
`UNIFIED9_RAW_OUTPUT.txt`.

## 2. Frozen bars and verdict rule (from PREREG_U9_ADV.md, commit 7464cf28c)

- KILL if: K1 any DCOUNT increment; K2 any USTOREFULL trace; K3 ECOUNT delta !=
  UEVICT/UEVICT-FALLBACK line count (silent eviction or phantom trace); K4 X-U9-4
  fails (pristine rebuild differs from committed raw, or any refusal/silent
  eviction in committed evidence).
- Else DOWNGRADE if X-U9-1, X-U9-2, or X-U9-3a succeeds as defined.
- Else SURVIVES.

## 3. Raw results

Adversary binary, final run (3/3 byte-identical):

```
ADV-SELFCHECK adv_ep builds exact episode bytes PASS
X-U9-1 flooded junk displaces 16/16 honest rules, 160 queries, 0 drops PASS
X-U9-2 quarantined contradiction committed as fresh rule after eviction PASS
X-U9-3a query merit costs zero clock (CSEQ still 1 after 100 queries) PASS
X-U9-3a inversion: uses=100 G evicted ahead of 15 young uses=2 PASS
X-U9-3b edge: protected at check CSEQ=32, evicted at CSEQ=33 PASS
ADV-GLOBAL zero drops/refusals across all attacks PASS
=== ADV RESULT: 7/7 ===
```

### X-U9-1: merit flooding (DOWNGRADE, succeeds)

Fixture: 16 honest rules (s0=10..25, 8 fill calls returning 2 each), then 16
overfills with junk episodes s0=60..75 (`(60+j,0,0)>(0,7)`), each followed by 10
`cpredict` flood queries through the junk rule (160 queries total).

Observed: ECOUNT delta = 16, DCOUNT delta = 0, `caus_active_count` = 16,
`cpredict` on all honest s0=10..25 = 0 (16/16 honest rules evicted), `cpredict`
on all junk s0=60..75 = 1 (16/16 junk present). Victim sequence was slot
0,1,...,15 in order, exactly as hand-derived (each prior junk young with
uses=10 and protected; each remaining honest rule uses=0 and eligible).

Causal interpretation: merit is pure exercise-volume. Queries increment `uses`
without advancing CSEQ and without decay, so 160 silent queries manufacture
enough merit to displace 16 honestly-learned rules deterministically. The
mechanism cannot distinguish flooded from earned merit: there is no
authentication of experience. The builder headline "retention must be earned
(uses>=2)" holds only under honest experience; under adversarial experience
the policy is volume-ordered toward whoever queries most. The spec is
implemented exactly as written, so this narrows the claim, it does not break
the implementation.

### X-U9-2: quarantine resurrection (DOWNGRADE, succeeds)

Fixture trace (exact, from raw):

1. `handle_caus_learn(W,"5,0,0>0,1")` returns 1. R stored: slot 0, bseq=1.
2. `handle_caus_learn(W,"5,0,0>0,9")` returns 0. Exactly one
   `UCOHERE: QUARANTINE` trace; QCOUNT delta = 1. `cpredict(5,0,0)` = 1, s1 = 1
   (R intact).
3. 15 junk fills (s0=10..24), each queried once to equalize uses=1 with R
   (see section 5, fixture correction 1).
4. `handle_caus_learn(W,"99,0,0>0,1")` returns 1; ECOUNT delta = 1; trace:
   `UEVICT: causal rule R0 IF s0==5 AND a==0 THEN s1:=1 (uses=1) evicted for
   incoming (99,0,0)->(0,1)`. `cpredict(5,0,0)` = 0 (R gone).
5. `handle_caus_learn(W,"5,0,0>0,9")` returns 1 (stored fresh); QCOUNT delta = 0
   (no new quarantine); trace:
   `UEVICT: causal rule R0 IF s0==99 AND a==0 THEN s1:=1 (uses=1) evicted for
   incoming (5,0,0)->(0,9)`; `cpredict(5,0,0)` = 1 with s1 = 9.

Causal interpretation: quarantine is a property of the (episode, current store)
pair, not of the episode. The store keeps no tombstone of quarantined episodes.
Evicting the blocking rule flips a quarantined contradiction to admissible, and
it is committed as verified knowledge with no record that this exact episode
was ever quarantined. The builder disclosed this cost in the base result; this
attack demonstrates it end-to-end through the public stream interface, with the
stronger consequence that attacker-influenced capacity pressure alone (no new
causal evidence) converts quarantined evidence into accepted knowledge.
"Contradictory episodes are quarantined, never committed" holds only while the
contradicting rule is retained.

### X-U9-3a: birth-age inversion (DOWNGRADE, succeeds)

Fixture: G stored (`10,0,0>0,1`, slot 0, bseq=1), then 100 `cpredict` queries.
Observed `get32(W,CSEQ())==1` afterwards: query merit costs zero clock, so the
youth window does not move under exercise. 15 junk stored (s0=20..34). 33 aging
overfills (s0=40..72), each newcomer queried once (uses=1). Hand-derived victim
dynamics confirmed in trace: overfills #1..#15 evict slots 1..15 in order;
#16,#17 (check CSEQ 31,32 < 33) evict slot 1 with G protected; #18..#33 (check
33..48) evict slot 1 with G eligible but surviving on uses=100. Then slots 1..15
flooded to uses=2 (young, protected). Final overfill `(99,0,0)>(0,1)`.

Observed trace:
`UEVICT: causal rule R0 IF s0==10 AND a==0 THEN s1:=1 (uses=100) evicted for
incoming (99,0,0)->(0,1) (H-UNIFIED9)`.
ECOUNT delta = 1; `cpredict(10,0,0)` = 0; `cpredict(99,0,0)` = 1;
`caus_active_count` = 16.

Causal interpretation: eviction order is protection-class-first, then
lowest-uses within the eligible class. It is NOT globally merit-ordered. The
protection predicate (young AND uses>=2) is a discontinuous birth-age gate: an
old rule with arbitrarily high merit (uses=100 here) is retired ahead of any
young rule with uses>=2, to admit a meritless newcomer. Retention depends on
birth age, not recency of use: G was exercised 100 times immediately before the
aging phase and it changed nothing, because queries do not refresh `bseq`.
"Every retirement is merit-ordered" is false as a global claim; narrowed to
merit-ordered within the eligible class.

### X-U9-3b: window edge precision (confirmation, no separate verdict)

Fixture: G with uses=4 (4 corroborations), 15 junk, 17 aging overfills with
newcomers at uses=3 (3 queries each). After 17 overfills (clock=33):
`cpredict(10,0,0)` = 1 (G alive: protected at check CSEQ=32 < 1+32),
`cpredict(55,0,0)` = 0 (newcomer N(55) was the #17 victim, slot 1).
Overfill #18 (check CSEQ=33, not < 33): G eligible with uses=4, all others
young+uses=3 protected, victim = G. `cpredict(10,0,0)` = 0, `cpredict(57,0,0)` = 1,
ECOUNT delta = 1. PASS.

Causal interpretation: the youth window is exactly [bseq, bseq+32):
protection flips discontinuously at CSEQ == bseq+32. One clock tick converts a
protected rule into the eviction victim with no change in its merit or
recency. This is the same birth-age mechanism as X-U9-3a, measured precisely.

### X-U9-4: regression (defense holds)

- Pristine rebuild of committed `unified9_learn.zag` (git HEAD blob), 3 runs:
  byte-identical to each other and to committed `UNIFIED9_RAW_OUTPUT.txt`
  (md5 `7b690bc7b26940e4848e60920fcfc4e0` all four). Exit 0.
- Committed raw: `USTOREFULL` = 0, `DROPPED` = 0. No refusal ever occurred.
- Committed raw: 4 UEVICT/UEVICT-FALLBACK lines; sum of `N evicted
  (H-UNIFIED9)` = 4. Every eviction loud; none silent.
- Committed raw: 26 PASS lines, 0 FAIL lines. 26/26 reproduced.
- Adversary harness mechanism region (lines 1..1503) cmp-identical to committed
  blob both before and after fixture corrections.

## 4. Kill-bar audit (all clear, no KILL)

- K1 (drops): DCOUNT delta = 0 in every attack and in the committed evidence.
- K2 (refusal): zero USTOREFULL traces in adversary runs (70 evictions) and in
  committed evidence.
- K3 (silent eviction): 70 UEVICT/UEVICT-FALLBACK lines for 70 expected
  evictions in adversary runs (16+2+34+18); 4 lines for 4 counted evictions in
  committed evidence. No phantom traces, none silent.
- K4 (regression): holds as above.

## 5. Prereg deviations (fixture corrections, transparently recorded)

The prereg (7464cf28c) is frozen and was not amended. Two fixture bugs were
found and corrected after run 1; the attack intents, kill/downgrade criteria,
and verdict rule are unchanged.

1. X-U9-2: my `qkeep` probe query (verifying R survived quarantine) raised R to
   uses=1, breaking the designed all-uses=0 tie; the overfill then evicted slot
   1 instead of R. Worse, my first correction placed the equalization queries
   before the fills, where they hit nothing (run 2, identical failure).
   Final correction: one `cpredict` per junk slot AFTER the fills, restoring a
   16-way uses=1 tie so the lowest-index tie-break takes slot 0 = R. The
   mechanism behaved per spec in all runs; the bug was entirely in my fixture.
2. X-U9-3b: my hand-derivation missed that with all slots protected, eviction
   goes to FALLBACK, and fallback picks lowest uses: G (uses=2) died at
   overfill #16 to a uses=3 newcomer instead of surviving to the window edge.
   Correction: G corroborated x4 (uses=4 > newcomers' 3), so the fallback takes
   slot 1 and G survives to flip exactly at check CSEQ=33. Again the mechanism
   followed its spec; my fixture mis-modeled the fallback.

Both corrections were re-verified against the spec before re-running, and the
final binary's mechanism region was re-cmp-verified identical to the committed
blob.

## 6. Boundaries confirmed (what the red team could NOT break)

- The learner never refuses: 0 drops, 0 USTOREFULL across 70 adversary
  evictions and the full 26-check committed battery.
- Every eviction is loud and named: 70/70 adversary, 4/4 committed.
- Victim order implemented exactly as specified, including the all-protected
  fallback and lowest-index tie-breaks (both observed in traces).
- The coherence gate quarantines contradictions presented against a live rule
  (X-U9-2 step 2: return 0, exactly one QUARANTINE trace, rule untouched).
- The full 26/26 battery reproduces byte-identically from the committed source.

## 7. Classification and lineage

- Classification: bounded L2, unchanged. Nothing in these attacks bears on L3.
- H-UNIFIED9 inherits the H-MEM5 stale-merit concern by its own disclosure;
  X-U9-3 independently demonstrates the birth-age variant inside the unified
  store (protection measures age since birth, not recency of use).
- Commit lineage: target prereg `ecaa78494`, target result `09bd9b933`;
  adversary prereg `7464cf28c` (this red team). Adversary source
  `u9_adversary/u9_adv.zag`, raw `u9_adversary/U9_ADV_RAW.txt` (md5
  `67871213f8b341fe143a6915ea94fc0e`, 3/3 deterministic), this report
  `u9_adversary/U9_ADV_RESULT.md`.
- Pure Zag: no Python at any stage (fixtures, builds, runs, greps, hashes,
  diffs, commits). Shell only for orchestration.
- Governance: prereg committed alone before any attack code (one em dash
  caught by byte-grep and amended out before any build). Only owned paths under
  `docs/lab/research-lead/overnight-20260928/u9_adversary/` staged. No broad
  git add. Concurrent workers untouched.

## 8. Verdict

**DOWNGRADED.** X-U9-1, X-U9-2, and X-U9-3a all succeed as preregistered; no
kill bar fires; X-U9-4 regression holds. The narrowed surviving claims:

- C1 (never refuses), C2 (every eviction loud), C3 (victim order as specified):
  hold exactly as specified.
- C4 ("retention must be earned"): narrowed to honest environments; merit is
  unauthenticated exercise-volume, manufacturable by query flooding at zero
  clock cost.
- C5 (quarantine): narrowed to the lifetime of the blocking rule; a
  quarantined contradiction is committed as fresh knowledge once its
  contradicting rule is evicted, with no tombstone.
- Merit-ordering: false as a global claim; eviction is protection-class-first
  (birth-age gate, window exactly [bseq, bseq+32)), then lowest-uses within the
  eligible class.

Recommended follow-ups: authenticate experience (weight merit by source or
recency, or make queries advance the clock); tombstone quarantined episodes
across eviction; replace the birth-age gate with a recency-based protection if
"earned retention" is the intended semantic. These are design decisions for the
builder lane, not part of this verdict.
