# Result: H-CAUSAL-UNIFIED SURVIVES (28/28)

**Date:** 2026-09-29
**Hypothesis:** H-CAUSAL-UNIFIED
**Prereg:** PREREG_CAUSAL_UNIFIED.md (committed c37887616, amended 6f73c0cbc;
  amendment before any implementation; commit-order satisfied)
**Implementation:** unified_causal.zag (new file, based on committed
  unified_learn.zag at e27edbaf3)
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
  (znc 2026.07.0-dev, edition 2026)
**Purity:** Pure Zag. No Python. Determinism via cmp/sha256sum (shell).

## Verdict: SURVIVES (28/28), bounded L2 integration

The full causal contest/split/merge machinery from causal_learn.zag now
operates inside the unified learner process. All frozen bars pass.

## What was built

unified_causal.zag (2478 lines) ports the H-CAUSAL machinery verbatim
except for workspace rebasing and capacity guards:

- **Rebase:** all 26 causal workspace offsets moved to FUBASE=3600
  (absolute); 4376 bytes for 128 episodes / 32 entries / 8 contests,
  ending at 7976, clear of the proc store, bridge store, simplified
  causal store, bridge WORK scratch, pair descriptors, and the H-INTENT
  IBASE region.
- **Guards:** new_entry 64->32, new_contest 16->8 (test uses 18 episodes,
  under 32 entries, 3 contests; guards never trigger).
- **Wrappers:** fu_init, fu_learn_ep, fu_predict, fu_hist_count,
  fu_contests_open replace load_obs/main for stream-driven use.
- **Router (additive):** "iiiia>iii" 2+ segment lines route to CAUS_LEARN;
  single 4-int tuples route to CAUS_QUERY; the literal "caus_hist"
  routes to new code 5 CAUS_HIST. Mixed 3>2/4>3 lines withhold.
- **Handlers:** handle_caus_learn and handle_caus_query dispatch per
  segment/tuple length (legacy 3>2 path unchanged); handle_caus_hist
  emits the hypothesis/contest listing and returns counts.

## Frozen bars

**K-CU1 (20/20 preserved):** All Part A tests (K-U1, K-U2a, K-U2b, K-U2c,
K-U3, K-U4a intent-adapted, K-U4a2, K-U4b, K-U5, K-A) and all Part B
H-INTENT battery tests (B-T1 through B-T3c) PASS unchanged.

**K-CU2 (14/14 causal probes):** The 17 H-CAUSAL episodes fed
incrementally as iiiia>iii stream items; all 14 frozen probes return the
exact expected outputs:
- C-A: (2,0,0,2)->(2,1,0); (1,1,0,2)->(1,1,0); (0,0,0,0)->(1,0,0)
- C-B: (2,0,0,2)->WITHHOLD; (2,0,1,2)->(2,0,1); (0,0,0,2)->(0,1,0)
- C-B2: (2,0,0,2)->(2,0,0); (0,0,0,2)->(0,1,0); (1,1,1,2)->(1,1,1)
- C-C1: (2,0,0,2)->(2,1,0); (2,0,1,2)->(2,0,1)
- C-C2: (2,0,0,2)->(2,1,0); (2,0,1,2)->(2,1,1); (0,0,0,2)->(0,1,0)

The trace shows the ported machinery firing inside the unified process:
SPLIT on s0 at seq 12, SUPERSEDE on split, CONTEST opened at seq 13,
RESOLVE with loser SUPERSEDED at seq 15, SPLIT on s2 at seq 15,
RESOLVE at seq 17, MERGE dissolving the lamp split.

**K-CU3 (queryable provenance):** After phase C2, `caus_hist` routes to
CAUS_HIST, emits the full hypothesis and contest listing (showing H2 and
H6 with status=SUPERSEDED and their temporal bounds), and returns
superseded=2. The "decorative provenance" downgrade is repaired:
superseded episodes are now queryable through the unified stream.

**K-CU4 (determinism):** Three full runs byte-identical via cmp.
sha256: 21bd89ea94a90c0e18a498849679a9285a80f8694e7184b6bcf825baa55d3190

**K-CU5 (U-A2 regression):** After C2 verifies Q(2,0,0,2)->(2,1,0),
feeding the interfering item "2,0,0,2>2,0,0":
- (a) a contest opens (emitted: CONTEST action 2 state (2 0 0) ...),
- (b) Q(2,0,0,2) WITHHOLDS while the contest is unresolved (no silent
  replacement of the verified answer),
- (c) the history query shows open_contests=1.
The simplified store's U-A2 failure mode (silent confident replacement)
does not occur on the full path; it becomes explicit contest plus
withhold with provenance.

## Classification

Bounded causal L2 integration, not L3. The machinery constructs
conditional structure (splits), revises beliefs (contests), and retires
structure (merge) from evidence, but the representation (episodes,
entries, contests) was supplied by the researcher. The port is faithful:
no dynamics were added, and the 14 probes reproduce the standalone
results exactly.

## Relationship to the U-A2 kill

The H-UNIFIED adversary (commit 383c05aeb) KILLED the general
composition claim via U-A2: the simplified causal store silently replaced
a verified answer on a format-colliding interfering item. This
integration does not resurrect that claim. It demonstrates that the FULL
causal machinery, when ported into the unified process, handles the same
interference pattern correctly (contest + withhold + provenance). The
legacy iii>ii path retains the U-A2 vulnerability; repairing it (router
ambiguity signal or coherence gating) remains separate work. The frozen
9/9 H-UNIFIED bars (now 20/20 with intent) still pass; lineage is
preserved.

## Artifacts

- unified_causal.zag (implementation)
- unified_causal/run_a.txt, run_b.txt, run_c.txt (three deterministic runs)
- PREREG_CAUSAL_UNIFIED.md (frozen prereg)

Binaries are NOT committed.
