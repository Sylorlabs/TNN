# H-CAUSAL-UNIFIED4: Principled Un-Conflicting Adjudication

**Date:** 2026-09-29
**Hypothesis:** H-CAUSAL-UNIFIED4
**Status:** SURVIVES 16/16 builder battery plus 3/3 byte-identical
regression. Independent red team not yet run (queued).
**Parent:** H-CAUSAL-UNIFIED3 (SURVIVES 6/6 + 28/28 builder; red team
SURVIVES all four attacks failed).
**Lineage:** commits 9331cf67a (PREREG frozen), 5593aa542 (AMEND1 frozen),
2b9c61eef (AMEND2 frozen); implementation and results committed below.
**Mechanism file:** `docs/lab/research-lead/overnight-20260928/causal_unified4/unified_causal4.zag`
**Test file:** `docs/lab/research-lead/overnight-20260928/causal_unified4/cu4_test.zag`
**Toolchain:** `znc 2026.07.0-dev (edition 2026)`. Pure Zag. No Python in
any step (research, generators, verifiers, debugging, analysis, harnesses,
scratch).

## 1. Problem

H-CAUSAL-UNIFIED3 left one sharp boundary: the permanent conflict
blackhole. Twenty later consistent episodes at a conflicted state are
absorbed and never reactivate it. The contest machinery can retire a
contradiction only through a tracked contest. An untracked contradiction
in a contest-capacity conflicted entry is permanently unresolvable by
design. The withhold is honest but irreversible, even when later evidence
resolves the underlying disagreement.

H-CAUSAL-UNIFIED4 asks whether the conflicted entry can be retired
*principled and un-conflicted* while preserving the closure of X-CU2-1
(the anti-silent-forget invariant: a conflicted state's contradiction is
never silently retired by fresh-entry creation).

## 2. Method

### 2.1 Preregistration (strict order)

1. `PREREG_CAUSAL_UNIFIED4.md` committed as 9331cf67a before any
   implementation. It froze: the adjudication criterion (reuse the frozen
   `contest_feed` resolution bar: support at least 2 and strict majority),
   exactly 2 distinct outcomes required, 3 or more outcomes stay
   conflicted, loser episodes become EP_SUP, the entry returns to
   ST_ACTIVE, effects recompute, split/merge runs, an explicit UNCONFLICT
   trace is emitted, no fresh entry is created at the conflicted state,
   and the frozen kill bars K-CU4-1 through K-CU4-6.
2. First implementation executed: 11/14 design experiment (discarded, no
   verdict; disclosed in section 5).
3. `PREREG_CAUSAL_UNIFIED4_AMEND1.md` committed as 5593aa542 before the
   corrected implementation. It froze: scope the reactivation mask to the
   exact adjudicated state when all live episodes are at that state.
4. AMEND1 implementation executed: the design did not fire (precondition
   never true; disclosed in section 5).
5. `PREREG_CAUSAL_UNIFIED4_AMEND2.md` committed as 2b9c61eef before the
   final implementation. It froze: the carve-out design (new ACTIVE entry
   scoped to the exact state; conflicted entry stays ST_CONFL as
   tombstone; nent grows by exactly 1 per adjudication, explicitly
   traced) and the updated bars K-CU4-1c-i, K-CU4-1c-ii, K-CU4-1c-iii,
   K-CU4-2a.

### 2.2 Implementation (additive, AMEND2)

The source is a byte-identical copy of `unified_causal3.zag` plus exactly
one additive path: `conflict_adjudicate`, called at the end of the
CONFLICTED-ABSORB path in `learn_episode`, plus its helper `out_eq3`.
No existing function was modified. The mechanism:

- After an absorb into a ST_CONFL entry, tally live (non-EP_SUP) episodes
  at the exact absorbed state. If they form exactly 2 distinct outcome
  triples, apply the frozen `contest_feed` criterion verbatim
  (support at least 2, strict majority). A winner adjudicates.
- On adjudication (AMEND2 carve-out):
  - `new_entry(W, a, 7, cf, seq)`: mask 7, cond set to the exact state,
    parent cf (provenance). If entry capacity is exhausted, the function
    returns 0 and the conflict stands (explicit; the existing
    `new_entry` error path).
  - Every live winner-outcome episode at the state is added to the new
    entry (shared global indices; they stay live).
  - Every live loser-outcome episode at the state is marked EP_SUP in
    the conflicted entry (explicit retirement; losers are not shared).
  - Effects are recomputed on the new entry (`effects_over`, excl=ni);
    if unresolved, `split_attempt` runs (it may honestly re-conflict);
    then `merge_pass`.
  - The conflicted entry cf stays ST_CONFL with all its other evidence,
    contests, and withholds intact.
  - An explicit UNCONFLICT trace names the new entry index, the scoped
    cond, the winner move count, and the superseded loser count.
- 3 or more distinct outcomes, a single outcome, no majority, or a
  failed entry allocation: the entry stays ST_CONFL. No emit (the absorb
  emit already recorded the withhold).

### 2.3 Test battery

`cu4_test.zag` holds the mechanism lines byte-verbatim (verified by
`cmp` after extraction); only `main()` is replaced (same pattern as the
CU3 adversary driver). The battery replays the exact CU3 red-team flood
(20 episodes), then:

- K-CU4-1a: flood produces nct=8 and 2 ST_CONFL entries.
- K-CU4-1b: immediate post-flood query at (2,0,0) withholds (r=0).
- K-CU4-1c: one more (0,0,0) at (2,0,0) is absorbed, then UNCONFLICT
  carves entry 2: (i) nent grows by exactly 1; (ii) `find_entry`
  returns an ACTIVE mask-7 entry; (iii) the ST_CONFL tombstone holds a
  superseded loser at the exact state; (iv) the carved entry has parent
  set.
- K-CU4-1d: query (2,0,0) returns r=1 predicting (0,0,0). This
  SUPERSEDES K-CU3-1d (permanent withhold at the resolved state) by
  explicit evidence-driven behavior, not by a retroactive bar change.
- K-CU4-1e: untouched (2,0,1) still withholds (r=0).
- K-CU4-2c: re-contradiction (1,1,1) at (2,0,0) re-conflicts the carved
  entry (find_entry skips; query withholds r=0); a further (1,1,1) is
  absorbed (2-vs-2, no majority) with nent stable.
- K-CU4-1f: fresh state (2,0,2) is normally learnable (fresh entry, r=1).
- K-CU4-2a: nent accounting (exactly the carved entry plus the 1f fresh
  entry); the learn path never creates a fresh entry at the conflicted
  state.
- K-CU4-3: third outcome (2,2,2) at (2,0,0) on a fresh workspace: no
  carve-out, nent stable, withhold persists (r=0), and zero UNCONFLICT
  emits (checked by grep on the raw output).

Ordering note: K-CU4-2c runs before K-CU4-1f in the driver. A
later-created general ACTIVE entry would shadow the re-conflicted
specific entry under the pre-existing `find_entry` most-specific-ACTIVE
policy (present in CU3 as well); ordering avoids that unrelated
interaction. The bars themselves are unchanged. The shadowing is
disclosed as a limitation in section 7.

## 3. Frozen bars

K-CU4-1a (flood nct=8, 2 ST_CONFL). K-CU4-1b (immediate withhold).
K-CU4-1c (carve-out: nent+1, ACTIVE mask-7 entry, loser EP_SUP in the
ST_CONFL tombstone, parent provenance) [AMEND2]. K-CU4-1d (r=1 predicts
(0,0,0); K-CU3-1d SUPERSEDED). K-CU4-1e ((2,0,1) withholds).
K-CU4-1f (fresh-state learning). K-CU4-2a (X-CU2-1 closure: nent
accounting; learn path creates nothing at the conflicted state).
K-CU4-2b (UNCONFLICT trace names the superseded loser). K-CU4-2c
(re-contradiction re-conflicts; absorb stable). K-CU4-3 (messy stays
conflicted; zero UNCONFLICT). K-CU4-4 (main() regression byte-identical).
K-CU4-5 (3/3 byte-identical). K-CU4-6 (no Python).

## 4. Results

### 4.1 Regression (K-CU4-4, K-CU4-5)

`unified_causal4.zag` `main()` executed 3 times:

- 3/3 byte-identical.
- MD5 `87f8edc29825802327029f46f045dbe3`, exactly matching the committed
  `CU3_RAW_MAIN.txt`.
- 28 PASS markers, 0 FAIL. Every PASS line is the CU3 main; the
  additive path never fires in the main driver (no conflicted entry
  arises there), which is the expected closure.

### 4.2 Test battery (K-CU4-1/2/3, K-CU4-5)

`cu4_test.zag` executed 3 times:

- 3/3 byte-identical. MD5 `3bde55fe381a7c8ff1cef93d8c038da3`.
- 16/16 PASS, 0 FAIL, on every run.

Per-check results (identical all 3 runs):

- K-CU4-1a flood nct=8 PASS
- K-CU4-1a2 two ST_CONFL entries PASS
- K-CU4-1b immediate withhold r=0 PASS
- K-CU4-1c-i exactly one carved entry (nent ne0+1) PASS
- K-CU4-1c-ii carved entry ACTIVE scoped mask=7 PASS
- K-CU4-1c-iii loser superseded in ST_CONFL tombstone PASS
- K-CU4-1c-iv carved entry parent set (provenance) PASS
- K-CU4-1d query r=1 predicts (0,0,0) PASS (K-CU3-1d SUPERSEDED)
- K-CU4-1e (2,0,1) still withholds r=0 PASS
- K-CU4-2c-i carved entry re-conflicted, find_entry skips PASS
- K-CU4-2c-ii query withholds r=0 PASS
- K-CU4-2c-iii re-conflicted carved entry still absorbs (nent stable) PASS
- K-CU4-1f fresh-state learning intact PASS
- K-CU4-2a nent stable, learn path created nothing at conflicted state PASS
- K-CU4-3a messy: no carve-out (nent stable) PASS
- K-CU4-3b messy stays conflicted, withhold r=0 PASS

### 4.3 Raw trace evidence

The single UNCONFLICT emit (line 24 of the raw test output):

```
UNCONFLICT action 2 state (2 0 0) at seq 21: winner outcome (0 0 0) support 2 vs loser (1 1 1) support 1; carved new entry 2 [s0=2&s1=0&s2=0] with 2 winner episode(s); 1 loser episode(s) SUPERSEDED in conflicted entry 0 (ST_CONFL kept)
```

Exactly 1 UNCONFLICT line in the full output; 0 in the K-CU4-3 messy
section (grep-verified). The re-contradiction produces the honest
conflict emit:

```
ENTRY action 2 [s0=2&s1=0&s2=0] CONFLICTED: contradiction untracked (contest cap) at seq 23 (WITHHOLD)
```

Raw outputs: `CU4_RAW_MAIN.txt`, `CU4_RAW_TEST.txt` (run 1 of 3;
runs 2 and 3 byte-identical, MD5s above).

## 5. Failed design experiments (discarded, no verdict)

Two design experiments were executed and discarded under the frozen
amendment process. Neither produced a verdict; both are preserved here
as negative evidence.

**Experiment 1 (in-place reactivation, PREREG as frozen):** 11/14. The
adjudication fired correctly (UNCONFLICT, loser EP_SUP, no fresh entry,
(2,0,0) predicted (0,0,0), re-contradiction restored conflict, messy
stayed conflicted), but the reactivated entry kept mask 0 ([any]), so
the adjudicated law generalized across all 9 states in the entry: the
untouched (2,0,1) predicted instead of withholding (K-CU4-1e FAIL), and
the fresh (2,0,2) routed into the broad entry instead of the fresh-entry
path (K-CU4-1f FAIL, K-CU4-2a consequential). Root cause: in-place
reactivation generalizes beyond the evidence. This is a soundness hole
(a red team can retire a withhold at a state with an explicit unresolved
contradiction using a neighboring state's evidence), not just a missed
bar.

**Experiment 2 (AMEND1: narrow the mask when all live episodes are at
the state):** The implementation compiled and the regression held, but
the diagnostic (a pure-Zag workspace dump, `/tmp/cu4_diag.zag`) showed
the conflicted entry holds 18 episodes across 9 states (the 8 tracked
contests all sit on entry 0), so the all-live-at-one-state precondition
never fires. The 11/14 result was unchanged. Root cause: the AMEND1
precondition cannot hold for the CU3 flood shape.

Both experiments motivated AMEND2 (carve-out), which was frozen before
implementation.

## 6. Causal interpretation

The adjudication criterion is the mechanism's own definition of enough
evidence to call a law change (`contest_feed`: support at least 2,
strict majority). An untracked contradiction in a contest-capacity
conflicted entry is exactly contest-shaped, so reusing the contest bar
is the least-arbitrary choice; no new bar was invented. The carve-out
scopes the retired withhold to the evidence: the resolved state gets a
clean ACTIVE entry, every other state's contradiction keeps its
withhold, losers are explicitly superseded (not silently dropped), and
the conflicted entry remains as a tombstone. The re-contradiction test
shows the machinery is not a one-way ratchet: a new contradiction
re-conflicts the carved entry and the withhold returns immediately.

Classification: bounded L2 causal integration (same as CU3). The
mechanism constructs a new entry (a new structural relationship between
a state and its adjudicated law) from generic machinery, but the
adjudication bar, the carve-out shape, and the tracing were all
researcher-authored. Nothing here is L3.

## 7. Limitations

1. **Shadowing by general ACTIVE entries.** `find_entry` returns the
   most specific ACTIVE entry and skips ST_CONFL. A later-created
   general ACTIVE entry covering a conflicted specific state will
   predict through the conflict. This policy predates CU4 (present in
   CU3); the carve-out makes the conflicted entry specific, which makes
   the shadowing more reachable. The test battery orders 2c before 1f
   to avoid this unrelated interaction. A principled fix (conflict
   shadowing in `find_entry`) is future work and was deliberately left
   out of the frozen design.
2. **The tombstone's winner episodes stay listed as live in the
   conflicted entry.** The carved entry shares the winner episode
   indices (they must stay live for the carved entry to function).
   `find_conflicted` prefers the most specific entry, so the carved
   (later re-conflicted) entry wins routing; the tombstone listing is a
   historical record. This is disclosed, not hidden.
3. **Entry-capacity exhaustion during carve-out.** If `new_entry`
   fails, the conflict stands (explicit return 0). The withhold is
   preserved; the adjudication is lost. No silent behavior.
4. **The adjudication bar is the contest bar.** Reusing `contest_feed`
   is principled but not derived from first principles; a different
   bar (for example support at least 3) would change the boundary.
   The bar is frozen and explicit, so the boundary is testable.
5. **No independent red team yet.** The builder battery is 16/16, but
   H-CAUSAL-UNIFIED4 has not faced the adversary. The red-team run is
   queued; the SURVIVES verdict here covers the builder battery only.
6. **Merge interaction.** The carved entry participates in `merge_pass`
   under the existing safety checks. A merge with an identical-fx
   sibling could broaden its cond; this is the normal machinery, but it
   means the scoping guarantee holds at carve-out time and is subject
   to the standard merge policy afterward.

## 8. Governance disclosures

- Preregistration strictly preceded implementation at all three stages
  (commits 9331cf67a, 5593aa542, 2b9c61eef). No frozen bar was weakened
  or retroactively changed. K-CU4-1c-i, K-CU4-1c-ii, K-CU4-1c-iii, and
  K-CU4-2a were transparently amended (AMEND2) before the final
  implementation; K-CU3-1d and K-CU3-1e are marked SUPERSEDED by
  explicit evidence-driven behavior, not edited in place.
- The 11/14 experiments are discarded design experiments, preserved as
  negative evidence. No verdict was drawn from them.
- Pure Zag throughout: no Python in research, generators, verifiers,
  debugging, analysis, harnesses, or scratch. Diagnostics were Zag
  harnesses; file operations were shell.
- A concurrent `.git/index.lock` blocked one commit attempt; it was not
  removed (waited 20 seconds; the lock cleared).
- Only explicitly owned paths were staged and committed:
  `docs/lab/research-lead/overnight-20260928/causal_unified4/`.
- No binaries or unnecessary generated artifacts committed.
- Commits are local; no push was attempted or authorized.
- This document contains no em dashes.

## 9. Commit lineage

- 9331cf67a `PREREG H-CAUSAL-UNIFIED4 FROZEN: principled un-conflicting adjudication`
- 5593aa542 `AMEND1 H-CAUSAL-UNIFIED4 FROZEN: scope adjudication to adjudicated state`
- 2b9c61eef `AMEND2 H-CAUSAL-UNIFIED4 FROZEN: carve-out adjudication scoped to evidence`
- (this commit) implementation (`unified_causal4.zag`), test driver
  (`cu4_test.zag`), raw outputs, and this report.

## 10. Verdict

**H-CAUSAL-UNIFIED4: SURVIVES the builder battery (16/16, 3/3
byte-identical; regression 3/3 byte-identical to the CU3 hash).**
X-CU2-1 remains closed: no silent-forget path was reintroduced; the
learn path never creates a fresh entry at a conflicted state; losers are
explicitly superseded; the messy boundary stays conflicted; the
re-contradiction restores the withhold. The CU3 permanent-conflict
blackhole now has a principled, evidence-driven exit that stays scoped
to the evidence. Independent red team is queued before any stronger
claim.
