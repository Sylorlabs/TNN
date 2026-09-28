# MINIMAL_ANOMALY — investigation report (2026-09-27)

## The question

Round-3 score table: `onebrain 23/44`, `minimal 23/44` — exact tie.
If "minimal" meant reduced machinery achieving the same score as the
full one-brain, the round-3 victory story ("the +2 net over single
rides the shared-state channel") would need re-examination.

## 1. What `minimal` actually is (exact definition)

Source: `docs/lab/onebrain3/impl/onebrain_v3.zag`, committed in
`51b7de35d`. Mode dispatch (`main`, end of file):

```
single   → run_full(mode,path,0,1,0,0)   // fork_en=0, shared=1
onebrain → run_full(mode,path,1,1,0,0)   // fork_en=1, shared=1
ablate   → run_full(mode,path,1,0,0,0)   // fork_en=1, shared=0
poison   → run_full(mode,path,1,1,1,0)
min      → run_minimal(path)             // → solve_one(...,1,1,0,0,0,mode="min")
```

The source comment above `run_minimal` states it verbatim:

```
// Minimal driver for the K3 scaffold-removal test: a bare loop with no
// trace and no fan_out call anywhere. Same machinery, same config as
// onebrain mode (fork_en=1, shared=1).
```

`run_minimal` and `run_full` are the same problem loop; the ONLY
differences between `min` and `onebrain` are:

| Aspect | onebrain | min |
|---|---|---|
| `solve_one` machinery | identical | identical |
| fork_en / shared / poison / neuter | 1 / 1 / 0 / 0 | 1 / 1 / 0 / 0 |
| trace flag | 1 | 0 |
| mode label | "onebrain" | "min" |

The `trace` flag is **print-only**: every `trace==1` branch in the
source is a `pr`/`prl`/`prn` call (verified by grep over all 20+
use sites: gen_readings, gen_facts, gen_actions, elim_phase,
fork_assess, audit_invalidate, audit_cleanup, duel_delib,
branch_snapshot, reint_delib). It has zero behavioral effect.

**Therefore: `min` is NOT a reduced-machinery arm. It is the full
one-brain machinery with the shared-state channel ON (shared=1),
driven by a bare loop instead of the full driver.** "Minimal" =
minimal *driver*, not minimal machinery.

Corroborating facts:
- No `fan_out` function exists anywhere in v2 or v3 (grep: zero
  hits). The driver never contained fork/fan_out/subpass logic —
  v2's comment: "The driver contains NO fork/fan_out/subpass logic:
  it only parses the mode, loads problems, and calls the machinery
  (ob_deliberate) per problem."
- The fork decision is made internally: `fork_assess` sets the FORK
  flag at ledger offset 13816; sub-deliberations run inside
  `ob_deliberate`, never in the driver.

## 2. The tie, item-level

From committed traces (`docs/lab/onebrain3/traces/v6_min_r1.txt`,
`v6_onebrain_r1.txt`):

- Winner hids: **identical on all 44 items** (diff of per-problem
  winners: empty). min's 23 is the SAME 23 items as one-brain's —
  not a different 23.
- FORK flags: **identical per problem** — 40/44 `fork=1` in both
  modes (matches the 40/44 fork-firable design target in
  BUILD_NOTES3.md). The machinery fans out on its own in min mode.
- Independent red team (commit `6b23696fc`, REDTEAM3.md):
  "**min == onebrain: 0 deltas — CONFIRMED**; min traces show
  `fork=1` (the machinery's own ledger fork flag), so K3'' is NOT
  VOIDED."

## 3. Does the round-3 attribution survive?

The K1'' attribution was conjunctive: `onebrain 23 > single 20`
AND `ablate 21 < onebrain 23` → the +2 net rides the shared channel.

The tie does NOT threaten this, because the channel ablation is
`ablate` (shared=0), not `min` (shared=1). Item-level anatomy:

- `ablate` vs `onebrain`: 6 winner-deltas (q01, q02, q04, q06, q21,
  q31). Ablate loses the 4 Cat-A duel wins (q01/q02/q04/q06 — the
  red team: "these genuinely need the shared ledger for the duel
  kill to propagate") and un-breaks q21, q31. Net: 23 → 21 (−2).
- Gross channel contribution: **+4 / −2, net +2.** The "gain rides
  the channel" claim is accurate at the net level; the gross
  picture is +4 duel wins against 2 channel-caused breaks.
- `min` ≡ `onebrain` is consistent with all of this: it is the
  same machine, so it keeps the same +4/−2.

Discriminating probes considered (no new runs needed — the
committed battery already contains them):
- "Ablate the channel from within minimal": that IS `ablate`
  (fork_en=1, shared=0) — already run: 21/44, 6 deltas.
- "Add the channel to single": incoherent by construction —
  `single` has fork_en=0, so there are no branches for a channel
  to connect.
- "Strip the fork from onebrain": that's `nF` (fork→0 neuter) —
  22/44, 11 deltas, already in the table.

No re-run of the battery was performed (disk at 99%); the
committed traces plus source inspection are the discriminating
evidence, and they agree.

## 4. Verdict: (a) attribution CONFIRMED — with two honest caveats

**The round-3 win story holds.** `minimal` tying `onebrain` is
expected by construction (identical machinery, identical config;
the only difference is a print flag). The shared-channel
attribution rests on `ablate`, which genuinely removes the channel
and genuinely loses 2 net. No re-interpretation of the round-3
verdict is required. K3'' ("TNN's own decision") stands: the
machinery sets its own FORK flag and fans out with no driver
orchestration.

**Caveat 1 — the arm name is misleading.** A reader seeing the
score table alone will reasonably read "minimal" as "reduced
machinery" and conclude the full machinery is unnecessary. The
source comment and MEASUREMENT3.md document the true meaning
("bare driver, no scaffold"), but the table does not. **Recommend:
rename to `bare` (or `nodriver`) in round 4+ and restate the
config in every future score table.**

**Caveat 2 — the K3'' test is weaker than it looks.** Since the
driver never contained `fan_out` logic (no such function exists in
v2 or v3), "scaffold removal" removes something that never
existed. The 0-delta outcome is the expected-by-construction PASS,
not an independent empirical discovery. The substantive evidence
for "TNN's own decision" is narrower but real: the FORK flag is set
internally by `fork_assess` (ledger offset 13816) and fires
40/44 in min mode with no driver involvement. Future K3-style bars
should name the actual scaffold being removed, or the test should
be retired as vacuous.

## 5. Recommendation

No change to the round-3 verdicts. For round 4: rename the arm,
restate per-arm configs in the score table, and either strengthen
K3 (name a real scaffold) or drop it.
